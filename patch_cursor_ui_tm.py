# -*- coding: utf-8 -*-
"""Cursor'a ozgu gorunur UI alanlarini guvenli, baglamli ceviri bellegiyle yamalar."""
import io
import json
import re

VISIBLE_PROPS = [
    'label', 'title', 'placeholder', 'tooltip', 'heading', 'header', 'subtitle',
    'emptyMessage', 'buttonLabel', 'primaryButtonLabel', 'secondaryButtonLabel',
    'confirmLabel', 'cancelLabel', 'okLabel', 'message', 'detail', 'children',
    'text', 'ariaLabel', 'aria-label', 'description',
]

VISIBLE_VALUE_RE = re.compile(
    r'(?P<prefix>(?P<prop>(?:"aria-label"|\b(?:' +
    '|'.join(re.escape(prop) for prop in VISIBLE_PROPS if prop != 'aria-label') +
    r'))):)(?P<value>"(?:\\.|[^"\\])*")'
)

try:
    from patch_molten import PROTECTED_PROP_LOGIC_PAIRS
except Exception:
    PROTECTED_PROP_LOGIC_PAIRS = {('text', 'Foreground')}


if __name__ == '__main__':
    translations = json.load(io.open('cursor-ui-tm.json', encoding='utf-8'))
    for fname in ['workbench.desktop.main.js', 'workbench.glass.main.js']:
        source = io.open(fname, encoding='utf-8').read()
        changes = [0]

        def translate_visible_value(match):
            try:
                english = json.loads(match.group('value'))
            except (TypeError, ValueError):
                return match.group(0)
            prop = match.group('prop')
            if (prop, english) in PROTECTED_PROP_LOGIC_PAIRS:
                return match.group(0)
            turkish = translations.get(english)
            if not isinstance(turkish, str) or turkish == english:
                return match.group(0)
            changes[0] += 1
            return match.group('prefix') + json.dumps(turkish, ensure_ascii=False)

        source = VISIBLE_VALUE_RE.sub(translate_visible_value, source)
        io.open(fname, 'w', encoding='utf-8', newline='').write(source)
        print('%s: %d gorunur Cursor UI metni cevrildi' % (fname, changes[0]))
