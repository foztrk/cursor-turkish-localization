# -*- coding: utf-8 -*-
"""Cursor'i normal baslatip native IPC (_boot_status.json) ve renderer.log
uzerinden pencere yuklenmesini, JS hatalarini ve canli DOM toplayicisinin
aktifligini dogrular. (Cursor 3.32.4+ ile --remote-debugging-port yerine
native vscode:cursorTrBootStatus IPC kanali kullanilir.)

Basarisiz olursa exit(1) doner (apply_all.py otomatik rollback tetikler).
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import time


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


def _boot_status_paths():
    base = os.path.dirname(os.path.abspath(__file__))
    return [
        os.path.join(base, '_boot_status.json'),
        os.path.join(os.environ.get('APPDATA', ''), 'Cursor', '_boot_status.json'),
    ]


def _clear_boot_status():
    for p in _boot_status_paths():
        if p and os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass


def _read_boot_status(min_ts_ms):
    for p in _boot_status_paths():
        if p and os.path.exists(p):
            try:
                data = json.load(open(p, encoding='utf-8'))
                if isinstance(data, dict) and data.get('ts', 0) >= min_ts_ms - 2000:
                    return data
            except Exception:
                pass
    return None


FATAL_TEXTS = ('[uncaught exception]', 'missing ref', 'SyntaxError', 'ReferenceError')


def _safe_mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


def _check_renderer_logs(start_epoch):
    log_root = os.path.join(os.environ.get('APPDATA', ''), 'Cursor', 'logs')
    if not os.path.isdir(log_root):
        return None
    dirs = sorted(glob.glob(os.path.join(log_root, '*')), key=_safe_mtime, reverse=True)
    for d in dirs[:2]:
        if _safe_mtime(d) < start_epoch - 5:
            continue
        for rl in glob.glob(os.path.join(d, 'window1*', 'renderer.log')):
            try:
                txt = open(rl, encoding='utf-8', errors='replace').read()
                for line in txt.splitlines():
                    if any(ft in line for ft in FATAL_TEXTS):
                        return line[:240]
            except OSError:
                pass
    return None


def verify_boot(port=9233, timeout=25, keep_open=False):
    del port  # 3.32.4+ debugger port kullanmaz, CLI geriye uyumluluk icin korunur
    exe = _find_cursor_exe()
    if not exe:
        print('BOOT_CDP: FAIL | Cursor.exe bulunamadi')
        return 1

    _kill_cursor()
    _clear_boot_status()
    time.sleep(0.5)

    start_epoch = time.time()
    min_ts_ms = int(start_epoch * 1000)

    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    proc = subprocess.Popen(
        [exe],
        creationflags=flags,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    last_state = None
    deadline = start_epoch + timeout
    early_err = None

    while time.time() < deadline:
        rc = proc.poll()
        if rc not in (None, 0):
            early_err = f'Cursor sureci beklenmedik kodla cikti: {rc}'
            break

        state = _read_boot_status(min_ts_ms)
        if state:
            last_state = state
            if state.get('errors'):
                break
            if (state.get('workbenchLoaded')
                    and state.get('bodyLen', 0) >= 5000
                    and state.get('collectorActive')):
                break

        log_err = _check_renderer_logs(start_epoch)
        if log_err:
            early_err = f'renderer.log hatasi: {log_err}'
            break

        time.sleep(0.5)

    if not early_err:
        log_err = _check_renderer_logs(start_epoch)
        if log_err:
            early_err = f'renderer.log hatasi: {log_err}'

    if not keep_open:
        _kill_cursor()
        _clear_boot_status()

    if early_err:
        print(f'BOOT_CDP: FAIL | {early_err}')
        return 1

    if not last_state:
        print(f'BOOT_CDP: FAIL | IPC acilis durumu {timeout}sn icinde alinamadi (_boot_status.json yok)')
        return 1

    errors = last_state.get('errors') or []
    if errors:
        print(f'BOOT_CDP: FAIL | JS hatasi ({len(errors)}): {errors[0]}')
        return 1

    if not last_state.get('workbenchLoaded') or last_state.get('bodyLen', 0) < 5000:
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
    parser = argparse.ArgumentParser(description='Native IPC ile Cursor acilisini dogrular.')
    parser.add_argument('--port', type=int, default=9233)
    parser.add_argument('--timeout', type=int, default=25)
    parser.add_argument('--keep-open', action='store_true')
    args = parser.parse_args()
    sys.exit(verify_boot(port=args.port, timeout=args.timeout, keep_open=args.keep_open))


if __name__ == '__main__':
    main()
