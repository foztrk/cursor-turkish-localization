# -*- coding: utf-8 -*-
"""
Otonom Derin Arayüz Tarayıcısı (Autonomous Deep UI Scanner).
Cursor kurulumundaki tüm paketleri tarayarak kullanıcıya dönük kalan tüm İngilizce metinleri tespit eder.
"""
import io
import json
import os
import re
from collections import defaultdict

APP_DIR = r'C:\Program Files\cursor\resources\app'
LOCAL_DIR = r'C:\Users\Work-D\cursor-turkish-localization'

TARGET_FILES = [
    os.path.join(APP_DIR, r'out\vs\workbench\workbench.glass.main.js'),
    os.path.join(APP_DIR, r'out\vs\workbench\workbench.desktop.main.js'),
    os.path.join(APP_DIR, r'out\main.js'),
]

# Add molten files
molten_dir = os.path.join(APP_DIR, r'extensions\cursor-molten\dist')
if os.path.exists(molten_dir):
    for root, _, fnames in os.walk(molten_dir):
        for fn in fnames:
            if fn.endswith('.js'):
                TARGET_FILES.append(os.path.join(root, fn))

PROPS = (
    "title", "tooltip", "ariaLabel", "aria-label", "label", "placeholder",
    "heading", "header", "subtitle", "emptyMessage", "buttonLabel",
    "primaryButtonLabel", "secondaryButtonLabel", "confirmLabel",
    "cancelLabel", "okLabel", "message", "detail", "description"
)

PROP_RE = re.compile(
    r'(?P<prop>(?:"aria-label"|' + "|".join(re.escape(p) for p in PROPS if p != "aria-label") +
    r')):(?P<quote>["\'])(?P<value>(?:\\.|(?!\2)[^\\]){2,180})\2'
)

NLS_RE = re.compile(r'N\(\s*["\'](?P<key>[a-zA-Z0-9_.-]+)["\']\s*,\s*["\'](?P<value>(?:\\.|[^"\\])+)["\']')

TURKISH = re.compile(r"[çğıöşüÇĞİÖŞÜ]")
TECHNICAL = re.compile(
    r"^(?:[a-z0-9_.:/@-]+|[A-Z0-9_]+|#[0-9a-fA-F]+|--[a-z-]+|\$[a-zA-Z0-9_]+|[A-Za-z0-9+/=]{20,})$"
)

# Non-UI words to exclude
EXCLUDE_WORDS = {
    "undefined", "boolean", "number", "string", "object", "function", "symbol", "bigint",
    "true", "false", "null", "none", "auto", "default", "inherit", "initial", "unset",
    "flex", "grid", "block", "inline", "inline-block", "table", "relative", "absolute", "fixed",
    "center", "left", "right", "top", "bottom", "middle", "baseline",
    "primary", "secondary", "tertiary", "ghost", "accent", "danger", "warning", "info", "success",
    "sm", "md", "lg", "xl", "xs", "solid", "dashed", "dotted",
    "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS",
    "utf-8", "ascii", "application/json", "text/plain",
    "vscode", "cursor", "electron", "node", "chrome",
    "commit", "branch", "repo", "worktree", "git"
}

def is_valid_ui_candidate(text):
    if not text or not isinstance(text, str):
        return False
    text = text.strip()
    if len(text) < 2 or len(text) > 150:
        return False
    if TURKISH.search(text):
        return False
    if TECHNICAL.match(text):
        return False
    if text.startswith('http://') or text.startswith('https://') or text.startswith('file://'):
        return False
    if text.startswith('cursor:') or text.startswith('vscode:') or text.startswith('command:'):
        return False
    if text.startswith('ui-') or text.startswith('glass-') or text.startswith('monaco-'):
        return False
    if re.search(r'[{};=\\<>~^|]', text):
        return False
    if text.lower() in EXCLUDE_WORDS:
        return False
    # Must contain letters and spaces, or be Title Case
    words = re.findall(r'[A-Za-z]+', text)
    if not words:
        return False
    # Must look like human text
    has_letters = bool(re.search(r'[A-Za-z]{2,}', text))
    if not has_letters:
        return False
    # If single word, must be capitalized and at least 3 chars, and common UI action/noun
    if len(words) == 1:
        w = words[0]
        if not w[0].isupper() or len(w) < 4:
            return False
        if w.lower() in EXCLUDE_WORDS:
            return False
    return True

# Load existing translations to skip already translated ones
with open(os.path.join(LOCAL_DIR, 'cursor-ui-tm.json'), 'r', encoding='utf-8') as f:
    existing_tm = json.load(f)

from patch_glass_nls import GLASS_NLS_MAP
from patch_remaining_ui import MAP, DIRECT_MAP

already_translated = set(existing_tm.keys()) | set(GLASS_NLS_MAP.keys()) | set(MAP.keys()) | set(DIRECT_MAP.keys())

nls_findings = {}
prop_findings = defaultdict(list)

for fpath in TARGET_FILES:
    if not os.path.exists(fpath):
        continue
    bn = os.path.basename(fpath)
    with io.open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. NLS scan
    for m in NLS_RE.finditer(content):
        key = m.group('key')
        val = m.group('value')
        if is_valid_ui_candidate(val) and key not in GLASS_NLS_MAP and val not in already_translated:
            nls_findings[key] = val
            
    # 2. Props scan
    for m in PROP_RE.finditer(content):
        prop = m.group('prop').strip('"')
        val = m.group('value')
        # unescape json string if needed
        try:
            val_clean = json.loads(f'"{val}"') if not val.startswith('"') else val
        except Exception:
            val_clean = val
        if is_valid_ui_candidate(val_clean) and val_clean not in already_translated:
            prop_findings[val_clean].append((bn, prop))

print(f"=== Otonom Tarama Tamamlandi ===")
print(f"Kalan Çevrilmemiş NLS Anahtarı: {len(nls_findings)}")
print(f"Kalan Çevrilmemiş Görünür UI Prop'u: {len(prop_findings)}")

# Save to scan report
out = {
    "nls": nls_findings,
    "props": {k: [list(x) for x in v] for k, v in sorted(prop_findings.items())}
}
with open(os.path.join(LOCAL_DIR, 'scratch_autonomous_scan.json'), 'w', encoding='utf-8') as fp:
    json.dump(out, fp, ensure_ascii=False, indent=2)

print("Sonuçlar scratch_autonomous_scan.json dosyasına yazıldı.")
