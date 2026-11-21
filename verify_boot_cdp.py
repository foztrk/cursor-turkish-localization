# -*- coding: utf-8 -*-
"""Cursor'i CDP (--remote-debugging-port) ile acip pencere yuklenmesini,
JS hatalarini ve canli DOM toplayicisinin aktifligini dogrular.

Basarisiz olursa exit(1) doner (apply_all.py otomatik rollback tetikler).
"""
import argparse
import base64
import json
import os
import socket
import struct
import subprocess
import sys
import time
import urllib.request


def _find_cursor_exe():
    candidates = [
        r'C:\Program Files\cursor\Cursor.exe',
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'cursor', 'Cursor.exe'),
    ]
    for p in candidates:
        if p and os.path.exists(p):
            return p
    return None


def _kill_cursor():
    subprocess.run(
        ['taskkill', '/F', '/IM', 'Cursor.exe'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


class _SimpleCDP:
    def __init__(self, ws_url, timeout=5.0):
        host_port, path = ws_url[5:].split('/', 1)
        host, port = host_port.split(':')
        self.sock = socket.create_connection((host, int(port)), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f'GET /{path} HTTP/1.1\r\n'
            f'Host: {host_port}\r\n'
            f'Upgrade: websocket\r\n'
            f'Connection: Upgrade\r\n'
            f'Sec-WebSocket-Key: {key}\r\n'
            f'Sec-WebSocket-Version: 13\r\n\r\n'
        )
        self.sock.sendall(req.encode())
        buf = b''
        while b'\r\n\r\n' not in buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise RuntimeError('CDP WebSocket el sikismasi kapandi')
            buf += chunk
        self._msg_id = 0

    def send(self, method, params=None):
        self._msg_id += 1
        payload = json.dumps({'id': self._msg_id, 'method': method, 'params': params or {}}).encode()
        mask = os.urandom(4)
        hdr = bytearray([0x81])
        L = len(payload)
        if L < 126:
            hdr.append(0x80 | L)
        elif L < 65536:
            hdr.extend([0x80 | 126, L >> 8, L & 0xff])
        else:
            hdr.extend([0x80 | 127] + list(struct.pack('>Q', L)))
        hdr.extend(mask)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes(hdr) + masked)
        return self._msg_id

    def _recv_exact(self, n):
        buf = bytearray()
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise EOFError('WebSocket kapandi')
            buf.extend(chunk)
        return bytes(buf)

    def recv_frame(self):
        b1, b2 = self._recv_exact(2)
        opcode = b1 & 0x0f
        L = b2 & 0x7f
        if L == 126:
            L = struct.unpack('>H', self._recv_exact(2))[0]
        elif L == 127:
            L = struct.unpack('>Q', self._recv_exact(8))[0]
        payload = self._recv_exact(L)
        if opcode == 0x8:
            raise EOFError('WebSocket kapatma cercevesi')
        if opcode == 0x9:
            # ping -> pong
            return None
        return payload.decode('utf-8', 'replace')

    def drain(self, wait_sec=0.8):
        self.sock.settimeout(wait_sec)
        msgs = []
        deadline = time.time() + wait_sec
        while time.time() < deadline:
            try:
                raw = self.recv_frame()
                if raw:
                    msgs.append(json.loads(raw))
            except socket.timeout:
                break
            except Exception:
                break
        return msgs

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass


FATAL_TEXTS = ('[uncaught exception]', 'missing ref', 'SyntaxError', 'ReferenceError')


def verify_boot(port=9233, timeout=20, keep_open=False):
    exe = _find_cursor_exe()
    if not exe:
        print('BOOT_CDP: FAIL | Cursor.exe bulunamadi')
        return 1

    _kill_cursor()
    time.sleep(0.5)

    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    subprocess.Popen(
        [exe, f'--remote-debugging-port={port}'],
        creationflags=flags,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    start = time.time()
    target = None
    while time.time() - start < min(timeout, 12):
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/json', timeout=1.5) as r:
                targets = json.loads(r.read().decode())
            for t in targets:
                if t.get('type') == 'page' and 'workbench.html' in (t.get('url') or '') and t.get('webSocketDebuggerUrl'):
                    target = t
                    break
            if target:
                break
        except Exception:
            pass
        time.sleep(0.5)

    if not target:
        print(f'BOOT_CDP: FAIL | workbench.html CDP hedefi {timeout}sn icinde acilmadi')
        if not keep_open:
            _kill_cursor()
        return 1

    cdp = None
    exceptions = []
    fatal_console = []
    last_state = None
    eval_expr = (
        'JSON.stringify({'
        'title: document.title,'
        'bodyLen: document.body ? document.body.innerHTML.length : 0,'
        'workbenchLoaded: !!document.querySelector(".monaco-workbench"),'
        'collectorActive: !!globalThis.__cursorTrCollectorActive,'
        'missingCount: globalThis.__cursorTrMissing ? globalThis.__cursorTrMissing.size : -1'
        '})'
    )

    try:
        cdp = _SimpleCDP(target['webSocketDebuggerUrl'], timeout=5.0)
        cdp.send('Runtime.enable')
        cdp.send('Log.enable')

        while time.time() - start < timeout:
            eval_id = cdp.send('Runtime.evaluate', {'expression': eval_expr})
            msgs = cdp.drain(wait_sec=1.0)
            for msg in msgs:
                method = msg.get('method')
                if method == 'Runtime.exceptionThrown':
                    details = msg.get('params', {}).get('exceptionDetails', {})
                    exc_obj = details.get('exception', {})
                    desc = exc_obj.get('description') or details.get('text') or 'exception'
                    exceptions.append(desc.splitlines()[0][:240])
                elif method == 'Runtime.consoleAPICalled':
                    params = msg.get('params', {})
                    if params.get('type') == 'error':
                        txt = ' '.join(str(a.get('value', '')) for a in params.get('args', []))
                        if any(ft in txt for ft in FATAL_TEXTS):
                            fatal_console.append(txt[:240])
                elif msg.get('id') == eval_id:
                    val = msg.get('result', {}).get('result', {}).get('value')
                    if isinstance(val, str):
                        try:
                            last_state = json.loads(val)
                        except Exception:
                            pass

            if exceptions or fatal_console:
                break
            if (last_state
                    and last_state.get('workbenchLoaded')
                    and last_state.get('bodyLen', 0) >= 5000
                    and last_state.get('collectorActive')):
                break
            time.sleep(0.6)
    except Exception as exc:
        print(f'BOOT_CDP: FAIL | CDP baglanti hatasi: {exc}')
        if not keep_open:
            _kill_cursor()
        return 1
    finally:
        if cdp:
            cdp.close()

    if not keep_open:
        _kill_cursor()

    total_errs = len(exceptions) + len(fatal_console)
    if total_errs > 0:
        sample = (exceptions + fatal_console)[0]
        print(f'BOOT_CDP: FAIL | JS hatasi ({total_errs}): {sample}')
        return 1

    if not last_state or not last_state.get('workbenchLoaded') or last_state.get('bodyLen', 0) < 5000:
        print(f'BOOT_CDP: FAIL | workbench yuklenmedi: state={last_state}')
        return 1

    if not last_state.get('collectorActive'):
        print(f'BOOT_CDP: FAIL | canli DOM toplayici aktif degil: state={last_state}')
        return 1

    print(
        f"BOOT_CDP: PASS | title={last_state.get('title')!r} | "
        f"bodyLen={last_state.get('bodyLen')} | collectorActive=True | "
        f"missing={last_state.get('missingCount')} | exceptions=0"
    )
    return 0


def main():
    parser = argparse.ArgumentParser(description='CDP ile Cursor acilisini dogrular.')
    parser.add_argument('--port', type=int, default=9233)
    parser.add_argument('--timeout', type=int, default=20)
    parser.add_argument('--keep-open', action='store_true')
    args = parser.parse_args()
    sys.exit(verify_boot(port=args.port, timeout=args.timeout, keep_open=args.keep_open))


if __name__ == '__main__':
    main()
