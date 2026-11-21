# -*- coding: utf-8 -*-
"""Iki orijinal Cursor surum klasoru arasindaki gercek yeni UI metin farkini cikarir.

Kullanim:
    python -X utf8 diff_versions.py
    python -X utf8 diff_versions.py --old orijinal-3.31.11 --new orijinal-3.31.15
"""
import argparse
import glob
import io
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

JS_TARGETS = [
    'workbench.glass.main.js',
    'workbench.desktop.main.js',
    'main.js',
    'workbench.anysphere-ui-automations.js',
]

PROPS = (
    'label', 'title', 'placeholder', 'tooltip', 'heading', 'header', 'subtitle',
    'emptyMessage', 'buttonLabel', 'primaryButtonLabel', 'secondaryButtonLabel',
    'confirmLabel', 'cancelLabel', 'okLabel', 'message', 'detail', 'children',
    'text', 'ariaLabel', 'description',
)

PROP_RE = re.compile(
    r'(?:(?:"aria-label")|\b(?:' + '|'.join(PROPS) +
    r')):(["\'`])((?:\\u[0-9a-fA-F]{4}|\\x[0-9a-fA-F]{2}|\\["\'\\]|[^"\'`\\\n\r$]){2,200})\1'
)

ASSIGN_RE = re.compile(
    r'(?<![=!<>])([=,?:])(["\'`])((?:\\u[0-9a-fA-F]{4}|\\x[0-9a-fA-F]{2}|\\["\'\\]|[^"\'`\\\n\r$]){4,220})\2'
)

ASSIGN_SKIP_BEFORE_RE = re.compile(
    r'(?:throw\s+new\s+[A-Za-z0-9_$]*Error\s*\(|new\s+[A-Za-z0-9_$]*Error\s*\(|\bcase\s+|===|!==|\.get\s*\(|\.has\s*\(|\.set\s*\()\s*$'
)
ASSIGN_SKIP_AFTER_RE = re.compile(r'^\s*(?:===|!==)')

TR_CHARS_RE = re.compile(r'[çğıöşüÇĞİÖŞÜ]')
BAD_CODE_RE = re.compile(
    r'[{}$<>=]|https?:|www\.|^[a-z0-9_.:/@#-]+$|^\d+$|^[A-Z0-9_ /:-]+$'
    r'|\.(?:tsx?|jsx?|mjs|cjs|json|css|scss|html|md|py|exe|dll|svg|png)\b'
)
EN_UI_HINT_RE = re.compile(
    r'\b(?:[A-Za-z]+(?:ing|ed|tion|ment|ally|able|ness|s)|the|to|of|and|for|or|a|an|is|are|be|'
    r'will|can|not|no|yes|all|new|this|that|your|you|with|from|when|how|what|where|use|used|'
    r'show|hide|open|close|set|get|run|add|remove|more|less|on|off|in|out|up|down|by|as|at|it|'
    r'if|do|does|has|have|was|were|only|also|may|please|try|again|now|here|there|other|each|'
    r'any|some|most|least|first|last|next|back|failed|success|error|warning|loading|done|'
    r'ready|active|enable|enables|disable|connect|disconnect|sign|allow|cancel|save|delete|'
    r'update|restart|install|authenticate|settings|tools|custom|model|search|filter|retry|skip|'
    r'confirm|continue|create|edit|view|click|select|switch|waiting|pending|check|manage|reset|'
    r'clear|apply|accept|reject|approve|deny|third-party|integrations)\b',
    re.I,
)


def _semver_key(name):
    ver = name.replace('orijinal-', '', 1)
    parts = []
    for p in re.split(r'[.-]', ver):
        if p.isdigit():
            parts.append((0, int(p)))
        else:
            parts.append((1, p))
    return tuple(parts)


def _decode_uesc(s):
    s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), s)
    return s.replace('\\"', '"').replace("\\'", "'").replace('\\`', '`')


def _is_clean_ui_text(val, multiword_required=False):
    if not val or '\n' in val or '\r' in val or '\\' in val:
        return False
    s = val.strip()
    if len(s) < 2 or len(s) > 200:
        return False
    if TR_CHARS_RE.search(s) or BAD_CODE_RE.search(s):
        return False
    if not (s[0].isupper() or s[0] in ('—', '⏳', '✓')):
        return False
    if not re.search(r'[a-z]{2}', s):
        return False
    # Tek kelimelik veya kesik ek/parca korumalari
    words = s.split()
    if multiword_required and len(words) < 2 and not s.endswith(('…', '...')):
        return False
    if len(words) == 1 and re.search(r'[a-z][A-Z]|[0-9_./-]', s):
        return False
    # Sondaki tek acilmis alinti / kesik ifade ("Add \", "Remove content above \")
    if s.endswith(('\\', ' under', ' above')):
        return False
    if len(words) >= 2 and not EN_UI_HINT_RE.search(s):
        return False
    return True


def _load_known_sets():
    sys.path.insert(0, BASE)
    known_nls = set()
    known_ui = set()
    known_tpl = set()
    known_raw = set()

    for fn, target_set in [('nls-tm.json', known_nls), ('cursor-ui-tm.json', known_ui), ('tpl-tm.json', known_tpl)]:
        p = os.path.join(BASE, fn)
        if os.path.exists(p):
            try:
                data = json.load(io.open(p, encoding='utf-8'))
                if isinstance(data, dict):
                    target_set.update(data.keys())
            except Exception:
                pass

    p_en = os.path.join(BASE, 'bilinen-ingilizce.json')
    if os.path.exists(p_en):
        try:
            data = json.load(io.open(p_en, encoding='utf-8'))
            if isinstance(data, list):
                known_raw.update(x for x in data if isinstance(x, str))
            elif isinstance(data, dict):
                known_raw.update(data.keys())
        except Exception:
            pass

    try:
        import patch_molten
        unified = patch_molten._load_unified_en_tr_dict()
        known_ui.update(unified.keys())
        known_ui.update(_decode_uesc(k) for k in unified.keys())
    except Exception:
        pass

    # Normalizasyon varyantlari
    def _expand(s_set):
        extra = set()
        for k in s_set:
            dk = _decode_uesc(k)
            extra.add(dk)
            extra.add(dk.replace('…', '...'))
            extra.add(dk.replace('...', '…'))
            extra.add(dk.replace('’', "'"))
        return s_set | extra

    return _expand(known_nls), _expand(known_ui), _expand(known_tpl), _expand(known_raw)


def _extract_js_features(folder):
    sys.path.insert(0, BASE)
    import patch_molten

    props = set()
    assigns = set()
    tpls = set()

    for fn in JS_TARGETS:
        fp = os.path.join(folder, fn)
        if not os.path.exists(fp):
            continue
        text = io.open(fp, encoding='utf-8', errors='ignore').read()

        for m in PROP_RE.finditer(text):
            val = _decode_uesc(m.group(2))
            if _is_clean_ui_text(val, multiword_required=False):
                props.add(val)

        for m in ASSIGN_RE.finditer(text):
            before = text[max(0, m.start() - 48):m.start()]
            if ASSIGN_SKIP_BEFORE_RE.search(before):
                continue
            after = text[m.end():min(len(text), m.end() + 8)]
            if ASSIGN_SKIP_AFTER_RE.match(after):
                continue
            val = _decode_uesc(m.group(3))
            if _is_clean_ui_text(val, multiword_required=True):
                assigns.add(val)

        for m in patch_molten._TPL_LITERAL_RE.finditer(text):
            before = text[max(0, m.start() - 32):m.start()]
            if patch_molten._TPL_COMP_BEFORE_RE.search(before):
                continue
            raw = m.group(1)
            if '${' not in raw:
                continue
            norm, _ = patch_molten.normalize_template_literal(raw)
            if norm:
                static_part = re.sub(r'\{\d+\}', 'X', norm)
                if _is_clean_ui_text(static_part, multiword_required=False) and not BAD_CODE_RE.search(norm):
                    tpls.add(norm)

    return props, assigns, tpls


def _load_nls_set(folder):
    fp = os.path.join(folder, 'nls.messages.json')
    if not os.path.exists(fp):
        return set()
    try:
        arr = json.load(io.open(fp, encoding='utf-8'))
        return {x for x in arr if isinstance(x, str) and len(x.strip()) >= 2}
    except Exception:
        return set()


def _resolve_dirs(old_arg, new_arg):
    if old_arg and new_arg:
        old_d = old_arg if os.path.isabs(old_arg) else os.path.join(BASE, old_arg)
        new_d = new_arg if os.path.isabs(new_arg) else os.path.join(BASE, new_arg)
        return old_d, new_d
    dirs = [d for d in glob.glob(os.path.join(BASE, 'orijinal-*')) if os.path.isdir(d)]
    dirs.sort(key=lambda d: _semver_key(os.path.basename(d)))
    if len(dirs) < 2:
        return None, (dirs[0] if dirs else None)
    return dirs[-2], dirs[-1]


def run_diff(old_dir=None, new_dir=None):
    old_d, new_d = _resolve_dirs(old_dir, new_dir)
    if not old_d or not new_d:
        print('Sürüm farkı: karşılaştırma için en az 2 orijinal-* klasörü gerekli; atlandı.')
        return None

    old_ver = os.path.basename(old_d).replace('orijinal-', '', 1)
    new_ver = os.path.basename(new_d).replace('orijinal-', '', 1)

    known_nls, known_ui, known_tpl, known_raw = _load_known_sets()

    old_nls = _load_nls_set(old_d)
    new_nls = _load_nls_set(new_d)
    diff_nls = sorted(
        x for x in (new_nls - old_nls)
        if x not in known_nls and x not in known_raw and not TR_CHARS_RE.search(x)
    )

    old_props, old_assigns, old_tpls = _extract_js_features(old_d)
    new_props, new_assigns, new_tpls = _extract_js_features(new_d)

    diff_props = sorted(
        x for x in (new_props - old_props)
        if x not in known_ui and x not in known_raw
    )
    prop_set = set(diff_props) | old_props
    diff_assigns = sorted(
        x for x in (new_assigns - old_assigns)
        if x not in known_ui and x not in known_raw and x not in prop_set
    )
    diff_tpls = sorted(
        x for x in (new_tpls - old_tpls)
        if x not in known_tpl and x not in known_raw
    )

    txt_name = f'SURUM-FARKI-{old_ver}-to-{new_ver}.txt'
    txt_path = os.path.join(BASE, txt_name)
    sections = [
        f'# Cursor Surum Farki: {old_ver} -> {new_ver}',
        f'# NLS={len(diff_nls)} | Prop={len(diff_props)} | Atama={len(diff_assigns)} | Sablon={len(diff_tpls)}',
        '',
        f'=== NLS ({len(diff_nls)}) ===',
        *diff_nls,
        '',
        f'=== BUNDLE PROPS ({len(diff_props)}) ===',
        *diff_props,
        '',
        f'=== BUNDLE ASSIGN/TERNARY ({len(diff_assigns)}) ===',
        *diff_assigns,
        '',
        f'=== TEMPLATES ({len(diff_tpls)}) ===',
        *diff_tpls,
        '',
    ]
    io.open(txt_path, 'w', encoding='utf-8').write('\n'.join(sections))

    payload = {
        'old_version': old_ver,
        'new_version': new_ver,
        'counts': {
            'nls': len(diff_nls),
            'bundle_props': len(diff_props),
            'bundle_assigns': len(diff_assigns),
            'templates': len(diff_tpls),
        },
        'items': {
            'nls': diff_nls,
            'bundle_props': diff_props,
            'bundle_assigns': diff_assigns,
            'templates': diff_tpls,
        },
    }
    json_path = os.path.join(BASE, 'surum-farki-son.json')
    io.open(json_path, 'w', encoding='utf-8').write(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')

    summary = (
        f'Sürüm farkı ({old_ver} -> {new_ver}): '
        f'NLS={len(diff_nls)}, Prop={len(diff_props)}, Atama={len(diff_assigns)}, Şablon={len(diff_tpls)} -> {txt_name}'
    )
    print(summary)
    return payload


def main():
    parser = argparse.ArgumentParser(description='Iki orijinal Cursor surum arasindaki yeni metinleri cikarir.')
    parser.add_argument('--old', help='Eski surum klasoru (or. orijinal-3.31.11)')
    parser.add_argument('--new', help='Yeni surum klasoru (or. orijinal-3.31.15)')
    args = parser.parse_args()
    run_diff(args.old, args.new)


if __name__ == '__main__':
    main()
