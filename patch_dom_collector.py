# -*- coding: utf-8 -*-
"""Bundle dosyalarinin (workbench.desktop.main.js & workbench.glass.main.js)
sonuna tek sozluklu canli DOM ceviricisi + pasif Ingilizce metin toplayici
ekler. React/UI render sonrasinda kod mantigina dokunmadan cevirir ve sozlukte
olmayan Ingilizce etiketleri Electron IPC uzerinden eksik-ekran-metinleri.json
dosyasina toplar.
"""
import io
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
LIVE_COLLECTOR_MARKER = '/* CURSOR_TR_LIVE_COLLECTOR_V1 */'
TARGETS = ['workbench.desktop.main.js', 'workbench.glass.main.js']

PRIORITY_TPL_TOKENS = (
    'authenticated', 'Update to', 'Last used', 'Allow ', 'Connect', 'Disconnect',
    'restart', 'Restart', 'Install', 'Download', 'Sign in', 'Log in', 'Search ',
    'Review ', 'Manage ', 'Waiting ', 'Running ', 'Failed ', 'Delete ', 'Remove ',
    'Create ', 'Open ', 'Agent', 'Remote ', 'Automations',
)


def _add_exact_variants(exact, k, v):
    if (isinstance(k, str) and isinstance(v, str) and k != v
            and 2 <= len(k) <= 220 and '\n' not in k and '\r' not in k):
        if re.search(r'[çğıöşüÇĞİÖŞÜ]', k) or k in ('Depolarda ara…', 'Depolarda ara...'):
            return
        exact[k] = v
        if '...' in k:
            exact.setdefault(k.replace('...', '…'), v.replace('...', '…'))
        if '…' in k:
            exact.setdefault(k.replace('…', '...'), v.replace('…', '...'))
        if '’' in k:
            exact.setdefault(k.replace('’', "'"), v)


def _build_exact_map():
    exact = {}
    try:
        import sys as _sys
        if BASE not in _sys.path:
            _sys.path.insert(0, BASE)
        import patch_molten as _pm
        unified = _pm._load_unified_en_tr_dict()
        for k, v in unified.items():
            if '\\u' in k or '\\x' in k:
                continue
            _add_exact_variants(exact, k, v)
    except Exception:
        pass
    p = os.path.join(BASE, 'cursor-ui-tm.json')
    if os.path.exists(p):
        data = json.load(io.open(p, encoding='utf-8'))
        for k, v in data.items():
            _add_exact_variants(exact, k, v)
    return exact


def _build_tpl_rules(max_rules=1500):
    p = os.path.join(BASE, 'tpl-tm.json')
    if not os.path.exists(p):
        return []
    raw = json.load(io.open(p, encoding='utf-8'))
    candidates = []
    for k, v in raw.items():
        if not (isinstance(k, str) and isinstance(v, str) and k != v):
            continue
        if k.count('{0}') != 1 or v.count('{0}') != 1:
            continue
        if re.search(r'\{[1-9]\d*\}', k) or re.search(r'\{[1-9]\d*\}', v):
            continue
        if '\n' in k or '\r' in k or len(k) > 180:
            continue
        pre, suf = k.split('{0}', 1)
        static_part = (pre + suf).strip()
        if len(static_part) < 6 or not re.search(r'[A-Za-z]{3}', static_part):
            continue
        if any(bad in pre or bad in suf for bad in ('/', '\\', '://', '===', '{', '}', ';', '()')):
            continue
        if len(pre) < 4 and len(suf) < 4:
            continue
        prio = 1 if any(tok in k for tok in PRIORITY_TPL_TOKENS) else 0
        candidates.append((prio, len(static_part), pre, suf, v))

    # Spesifik/oncelikli kaliplar bucket icinde once denenir
    candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [[pre, suf, v] for _, _, pre, suf, v in candidates[:max_rules]]


def _build_known_en():
    out = set()
    p = os.path.join(BASE, 'bilinen-ingilizce.json')
    if os.path.exists(p):
        try:
            data = json.load(io.open(p, encoding='utf-8'))
            if isinstance(data, list):
                out.update(x.strip() for x in data if isinstance(x, str) and 2 <= len(x.strip()) <= 180)
            elif isinstance(data, dict):
                out.update(k.strip() for k in data.keys() if isinstance(k, str) and 2 <= len(k.strip()) <= 180)
        except Exception:
            pass
    return sorted(out)


def _build_known_tr(exact_map):
    tr_set = set(exact_map.values())
    tr_set.update({
        'Tema', 'Renkler', 'Hareket', 'Sistem', 'Otomatik', 'Yeni', 'Plan', 'Beceriler',
        'Model Listesini Yenile', 'Model Listesi Yenileniyor', 'Kaydedildi',
    })
    p_nls = os.path.join(BASE, 'nls-tm.json')
    if os.path.exists(p_nls):
        try:
            for v in json.load(io.open(p_nls, encoding='utf-8')).values():
                if isinstance(v, str) and 2 <= len(v.strip()) <= 180:
                    tr_set.add(v.strip())
        except Exception:
            pass
    try:
        from patch_remaining_ui import MAP as REM_MAP
        for v in REM_MAP.values():
            if isinstance(v, str) and 2 <= len(v.strip()) <= 180:
                tr_set.add(v.strip())
    except Exception:
        pass
    try:
        from patch_glass_nls import GLASS_NLS_MAP
        for v in GLASS_NLS_MAP.values():
            if isinstance(v, str) and 2 <= len(v.strip()) <= 180:
                tr_set.add(v.strip())
    except Exception:
        pass
    import glob as _glob
    for tf in _glob.glob(os.path.join(BASE, 'tr2', '*.json')):
        try:
            for v in json.load(io.open(tf, encoding='utf-8')).values():
                if isinstance(v, str) and 2 <= len(v.strip()) <= 180:
                    tr_set.add(v.strip())
        except Exception:
            pass
    return sorted(tr_set)


def build_collector_script():
    exact_map = _build_exact_map()
    tpl_rules = _build_tpl_rules()
    known_en = _build_known_en()
    known_tr = _build_known_tr(exact_map)

    exact_json = json.dumps(list(exact_map.items()), ensure_ascii=False, separators=(',', ':'))
    tpl_json = json.dumps(tpl_rules, ensure_ascii=False, separators=(',', ':'))
    known_en_json = json.dumps(known_en, ensure_ascii=False, separators=(',', ':'))
    known_tr_json = json.dumps(known_tr, ensure_ascii=False, separators=(',', ':'))

    return (
        f'{LIVE_COLLECTOR_MARKER}\n'
        ';(() => {\n'
        '  try {\n'
        '    if (globalThis.__cursorTrLiveCollectorLoaded) return;\n'
        '    globalThis.__cursorTrLiveCollectorLoaded = true;\n'
        '    globalThis.__cursorTrCollectorActive = true;\n'
        f'    const EXACT_MAP = new Map({exact_json});\n'
        f'    const TPL_RULES = {tpl_json};\n'
        '    const TPL_BY_PRE = new Map();\n'
        '    const TPL_BY_SUF = new Map();\n'
        '    for (const r of TPL_RULES) {\n'
        '      const pre = r[0], suf = r[1];\n'
        '      if (pre.length >= 4) {\n'
        '        const k = pre.slice(0, 4);\n'
        '        let arr = TPL_BY_PRE.get(k);\n'
        '        if (!arr) { arr = []; TPL_BY_PRE.set(k, arr); }\n'
        '        arr.push(r);\n'
        '      } else if (suf.length >= 4) {\n'
        '        const k = suf.slice(-4);\n'
        '        let arr = TPL_BY_SUF.get(k);\n'
        '        if (!arr) { arr = []; TPL_BY_SUF.set(k, arr); }\n'
        '        arr.push(r);\n'
        '      }\n'
        '    }\n'
        f'    const KNOWN_EN = new Set({known_en_json});\n'
        '    KNOWN_EN.add("Cursor"); KNOWN_EN.add("Cursor Agents");\n'
        '    KNOWN_EN.add("Ctrl"); KNOWN_EN.add("Shift"); KNOWN_EN.add("Alt"); KNOWN_EN.add("Tab"); KNOWN_EN.add("Esc");\n'
        f'    const KNOWN_TR = new Set({known_tr_json});\n'
        '    const ISSUE_KEY_RE = /^[A-Z]{2,6}-\\d+\\b/;\n'
        '    const SKIP_SELECTOR = [\n'
        '      "head", "title",\n'
        '      ".monaco-editor", ".view-lines", ".xterm", ".terminal-wrapper",\n'
        '      "textarea", "input", "[contenteditable=\'true\']",\n'
        '      "code", "pre", "svg", "style", "script", "iframe", "canvas",\n'
        '      ".explorer-folders-view", ".monaco-list-row .label-name",\n'
        '      ".output-view", ".repl",\n'
        '      ".composer-human-message", ".anysphere-markdown-container-root",\n'
        '      ".markdown-root", "[data-testid=\'markdown\']",\n'
         '      ".glass-empty-state-rotating-tips__text", "[data-component=\'glass-empty-state-rotating-tips\']"\n'
        '    ].join(",");\n'
        '    const INTERACTIVE_SEL = \'button,[role="button"],[role="menuitem"],[role="tab"],[role="option"],[role="tooltip"],h1,h2,h3,label\';\n'
        '    const TR_RE = /[çğıöşüÇĞİÖŞÜ]/;\n'
        '    const PATH_URL_RE = /(https?:\\/\\/|www\\.|@|\\.(?:tsx?|jsx?|mjs|cjs|json|css|scss|html|md|py|exe|dll|svg|png)\\b|[\\\\\\/]{1})/i;\n'
        '    const CODE_NUM_RE = /(?:^\\d|^(?:Ctrl|Alt|Shift|Cmd|Meta)\\+|^\\d+(?:ms|s|m|h|d|dk|sa|g|ay|KB|MB|GB)$|[a-z][A-Z]|_|--)/;\n'
        '    const ALL_CAPS_RE = /^[A-Z0-9 _.:\\/-]+$/;\n'
        '    const SINGLE_WORD_UI_RE = /^[A-Z][a-z]{3,24}$/;\n'
        '    const EN_UI_WORD_RE = /\\b(?:the|to|of|and|for|or|in|on|with|from|is|are|be|your|this|that|agent|agents|enable|enables|disable|connect|disconnect|sign|allow|cancel|save|open|close|copy|delete|remove|add|update|restart|install|authenticate|settings|tools|custom|model|search|filter|show|hide|run|stop|retry|skip|confirm|continue|create|edit|view|use|click|select|switch|load|loading|failed|error|ready|waiting|pending|again|more|all|new|no|not|can|will|must|should|only|when|if|please|try|check|manage|reset|clear|apply|accept|reject|approve|deny|third-party|integrations|changes|files|branch|commit|workspace|terminal|window|tab|panel|chat|plan|mode|auto|default)\\b/i;\n'
        '    const seenSet = new Set();\n'
        '    globalThis.__cursorTrMissing = seenSet;\n'
        '    const pendingQueue = [];\n'
        '    let sendTimer = null;\n'
        '\n'
        '    function isSkipped(node) {\n'
        '      const el = node && node.nodeType === 1 ? node : node && node.parentElement;\n'
        '      return Boolean(el && el.closest(SKIP_SELECTOR));\n'
        '    }\n'
        '\n'
        '    function matchTplBucket(key, arr) {\n'
        '      if (!arr) return null;\n'
        '      for (let i = 0; i < arr.length; i++) {\n'
        '        const r = arr[i];\n'
        '        const pre = r[0], suf = r[1], tr = r[2];\n'
        '        if (key.length > pre.length + suf.length && key.startsWith(pre) && key.endsWith(suf)) {\n'
        '          const slot = key.slice(pre.length, key.length - suf.length);\n'
        '          if (slot && !slot.includes("\\n") && slot.length <= 64) {\n'
        '            return tr.replace("{0}", slot);\n'
        '          }\n'
        '        }\n'
        '      }\n'
        '      return null;\n'
        '    }\n'
        '\n'
        '    function translateString(key) {\n'
        '      if (!key) return null;\n'
        '      const exact = EXACT_MAP.get(key);\n'
        '      if (exact) return exact;\n'
        '      if (key.length >= 6) {\n'
        '        const preHit = matchTplBucket(key, TPL_BY_PRE.get(key.slice(0, 4)));\n'
        '        if (preHit) return preHit;\n'
        '        const sufHit = matchTplBucket(key, TPL_BY_SUF.get(key.slice(-4)));\n'
        '        if (sufHit) return sufHit;\n'
        '      }\n'
        '      return null;\n'
        '    }\n'
        '\n'
        '    function flushMissing() {\n'
        '      sendTimer = null;\n'
        '      if (pendingQueue.length === 0) return;\n'
        '      const batch = pendingQueue.splice(0, pendingQueue.length);\n'
        '      try {\n'
        '        globalThis.vscode?.ipcRenderer?.send("vscode:cursorTrMissing", batch);\n'
        '      } catch {}\n'
        '    }\n'
        '\n'
        '    function maybeCollect(key, kind, el) {\n'
        '      if (!key || key.length < 2 || key.length > 180) return;\n'
        '      if (seenSet.size >= 1500 || seenSet.has(key)) return;\n'
        '      if (TR_RE.test(key) || KNOWN_EN.has(key) || KNOWN_TR.has(key)) return;\n'
        '      if (ISSUE_KEY_RE.test(key)) return;\n'
        '      if (PATH_URL_RE.test(key) || CODE_NUM_RE.test(key) || ALL_CAPS_RE.test(key)) return;\n'
        '      const hasSpace = key.includes(" ");\n'
        '      if (hasSpace) {\n'
        '        if (!EN_UI_WORD_RE.test(key)) return;\n'
        '      } else {\n'
        '        if (!SINGLE_WORD_UI_RE.test(key)) return;\n'
        '        if (!el || !el.closest(INTERACTIVE_SEL)) return;\n'
        '      }\n'
        '      seenSet.add(key);\n'
        '      pendingQueue.push({ text: key, kind, tag: el ? el.tagName.toLowerCase() : "" });\n'
        '      if (!sendTimer) sendTimer = setTimeout(flushMissing, 2000);\n'
        '    }\n'
        '\n'
         '    function lookupWithBrandSpacing(combined) {\n'
         '      const tr = translateString(combined);\n'
         '      if (tr) return tr;\n'
         '      if (combined.includes("Cursor")) {\n'
         '        const fixed = combined.replace(/([a-z.,;:])Cursor\\b/g, "$1 Cursor").replace(/\\bCursor([a-z])/g, "Cursor $1");\n'
         '        if (fixed !== combined) return translateString(fixed);\n'
         '      }\n'
         '      return null;\n'
         '    }\n'
         '\n'
         '    function translateTextRuns(el) {\n'
         '      if (!el || el.nodeType !== 1 || isSkipped(el)) return;\n'
         '      const nodes = el.childNodes;\n'
         '      let i = 0;\n'
         '      while (i < nodes.length) {\n'
         '        if (nodes[i].nodeType !== 3) { i++; continue; }\n'
         '        const run = [];\n'
         '        let j = i;\n'
         '        while (j < nodes.length && (nodes[j].nodeType === 3 || nodes[j].nodeType === 8)) {\n'
         '          if (nodes[j].nodeType === 3) run.push(nodes[j]);\n'
         '          j++;\n'
         '        }\n'
         '        i = j;\n'
         '        if (run.length < 2) continue;\n'
         '        const combined = run.map((n) => n.nodeValue || "").join("").replace(/\\s+/g, " ").trim();\n'
         '        if (!combined) continue;\n'
         '        const tr = lookupWithBrandSpacing(combined);\n'
         '        if (tr && tr !== combined) {\n'
         '          if (run[0].nodeValue !== tr) run[0].nodeValue = tr;\n'
         '          for (let k = 1; k < run.length; k++) {\n'
         '            if (run[k].nodeValue !== "") run[k].nodeValue = "";\n'
         '          }\n'
         '        } else {\n'
         '          maybeCollect(combined, "text", el);\n'
         '        }\n'
         '      }\n'
         '    }\n'
         '\n'
         '    function translateTextNode(node) {\n'
         '      if (!node || node.nodeType !== 3 || isSkipped(node)) return;\n'
         '      const ps = node.previousSibling, ns = node.nextSibling;\n'
         '      if ((ps && ps.nodeType === 3) || (ns && ns.nodeType === 3)) {\n'
         '        translateTextRuns(node.parentElement);\n'
         '        return;\n'
         '      }\n'
         '      const raw = node.nodeValue || "";\n'
         '      const key = raw.trim();\n'
         '      if (!key) return;\n'
         '      const tr = lookupWithBrandSpacing(key);\n'
         '      if (tr && tr !== key) {\n'
         '        const lead = raw.match(/^\\s*/)?.[0] || "";\n'
         '        const trail = raw.match(/\\s*$/)?.[0] || "";\n'
         '        const next = lead + tr + trail;\n'
         '        if (next !== raw) node.nodeValue = next;\n'
         '        return;\n'
         '      }\n'
         '      maybeCollect(key, "text", node.parentElement);\n'
         '    }\n'
        '\n'
        '    const ATTRS = ["aria-label", "title", "placeholder"];\n'
        '    function translateAttrs(el) {\n'
        '      if (!el || el.nodeType !== 1 || isSkipped(el)) return;\n'
        '      for (const attr of ATTRS) {\n'
        '        const raw = el.getAttribute(attr);\n'
        '        if (!raw) continue;\n'
        '        const key = raw.trim();\n'
        '        if (!key) continue;\n'
        '        const tr = translateString(key);\n'
        '        if (tr && tr !== key) {\n'
        '          if (tr !== raw) el.setAttribute(attr, tr);\n'
        '        } else {\n'
        '          maybeCollect(key, attr, el);\n'
        '        }\n'
        '      }\n'
        '    }\n'
        '\n'
         '    function translateTree(root) {\n'
         '      if (!root) return;\n'
         '      if (root.nodeType === 3) {\n'
         '        translateTextNode(root);\n'
         '        return;\n'
         '      }\n'
         '      if (root.nodeType !== 1 && root.nodeType !== 9) return;\n'
         '      if (root.nodeType === 1) {\n'
         '        translateAttrs(root);\n'
         '        translateTextRuns(root);\n'
         '      }\n'
         '      const walker = document.createTreeWalker(root, 5);\n'
         '      let cur;\n'
         '      while ((cur = walker.nextNode())) {\n'
         '        if (cur.nodeType === 3) translateTextNode(cur);\n'
         '        else {\n'
         '          translateAttrs(cur);\n'
         '          translateTextRuns(cur);\n'
         '        }\n'
         '      }\n'
         '    }\n'
        '\n'
        '    function startCollector() {\n'
        '      if (!document.documentElement || globalThis.__cursorTrCollectorStarted) return;\n'
        '      globalThis.__cursorTrCollectorStarted = true;\n'
        '      const bootErrors = [];\n'
        '      const reportBoot = () => {\n'
        '        try {\n'
        '          const wb = !!document.querySelector(".monaco-workbench");\n'
        '          const bl = document.body ? document.body.innerHTML.length : 0;\n'
        '          globalThis.vscode?.ipcRenderer?.send("vscode:cursorTrBootStatus", {\n'
        '            ok: wb && bl >= 5000 && bootErrors.length === 0,\n'
        '            title: document.title || "",\n'
        '            bodyLen: bl,\n'
        '            workbenchLoaded: wb,\n'
        '            collectorActive: true,\n'
        '            missingCount: seenSet.size,\n'
        '            errors: bootErrors.slice(0, 10),\n'
        '            ts: Date.now()\n'
        '          });\n'
        '        } catch {}\n'
        '      };\n'
        '      window.addEventListener("error", (ev) => {\n'
        '        const msg = String(ev?.message || ev?.error?.message || "window error");\n'
        '        if (/missing ref|SyntaxError|ReferenceError|TypeError|uncaught/i.test(msg)) {\n'
        '          bootErrors.push(msg.slice(0, 240));\n'
        '          reportBoot();\n'
        '        }\n'
        '      });\n'
        '      window.addEventListener("unhandledrejection", (ev) => {\n'
        '        const msg = String(ev?.reason?.message || ev?.reason || "unhandled rejection");\n'
        '        if (/missing ref|SyntaxError|ReferenceError|uncaught/i.test(msg)) {\n'
        '          bootErrors.push(msg.slice(0, 240));\n'
        '          reportBoot();\n'
        '        }\n'
        '      });\n'
        '      setTimeout(reportBoot, 1500);\n'
        '      setTimeout(reportBoot, 4000);\n'
        '      setTimeout(reportBoot, 8000);\n'
        '      const initScan = () => translateTree(document.documentElement);\n'
        '      if (typeof requestIdleCallback === "function") {\n'
        '        requestIdleCallback(initScan, { timeout: 600 });\n'
        '      } else {\n'
        '        setTimeout(initScan, 400);\n'
        '      }\n'
        '      const obs = new MutationObserver((mutations) => {\n'
        '        for (const m of mutations) {\n'
        '          if (m.type === "characterData") translateTextNode(m.target);\n'
        '          else if (m.type === "attributes") translateAttrs(m.target);\n'
        '          else for (const n of m.addedNodes) translateTree(n);\n'
        '        }\n'
        '      });\n'
        '      obs.observe(document.documentElement, {\n'
        '        subtree: true,\n'
        '        childList: true,\n'
        '        characterData: true,\n'
        '        attributes: true,\n'
        '        attributeFilter: ATTRS\n'
        '      });\n'
        '    }\n'
        '\n'
        '    if (document.readyState === "loading") {\n'
        '      document.addEventListener("DOMContentLoaded", startCollector, { once: true });\n'
        '    } else {\n'
        '      startCollector();\n'
        '    }\n'
        '  } catch {}\n'
        '})();\n'
    ), len(exact_map), len(tpl_rules), len(known_en)


def patch_bundles(files=None):
    files = files or TARGETS
    script, exact_n, tpl_n, known_n = build_collector_script()
    updated = 0
    for fn in files:
        p = os.path.join(BASE, fn) if not os.path.isabs(fn) else fn
        if not os.path.exists(p):
            continue
        content = io.open(p, encoding='utf-8').read()
        if LIVE_COLLECTOR_MARKER in content:
            content = content[:content.index(LIVE_COLLECTOR_MARKER)].rstrip()
        else:
            content = content.rstrip()
        content = content + '\n\n' + script
        io.open(p, 'w', encoding='utf-8', newline='').write(content)
        updated += 1
    print(f'patch_dom_collector.py -> {updated} bundle guncellendi (exact={exact_n}, tpl={tpl_n}, known_en={known_n})')
    return updated


if __name__ == '__main__':
    patch_bundles()
