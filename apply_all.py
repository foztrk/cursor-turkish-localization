# -*- coding: utf-8 -*-
"""
Cursor Turkce yamasini SIFIRDAN uygular. TEK ADIM: TURKCELESTIR.bat dosyasina cift tikla.

Bu script otomatik olarak:
  1) Cursor'in mevcut surumunu tespit eder, orijinal dosyalari yedekler
  2) NLS ceviri bellegini (nls-tm.json) ve bundle prop haritalarini (tr2/m*.json) uygular
  3) Baglamli ozel yamalari (patch_*.py) calistirir
  4) Sozdizimini dogrular, checksum'i gunceller
  5) UAC ile Program Files'a kurar
  6) Yama sonrasi HALA Ingilizce gorunen metinleri tarar; bunlardan
     bilinen-ingilizce.json icinde olanlari (bilerek cevrilmeyen dev/jargon
     metinler) eler, geriye kalani YENI-EKLENENLER.txt'ye yazar. Bu dosyadaki
     her satir ya guncellemeyle gelen GERCEKTEN YENI bir metindir ya da
     henuz taranmamis eski bir metindir - Claude'a gosterip cevirtebilirsin.

Guncelleme sonrasi tek yapman gereken: Cursor'i kapat, TURKCELESTIR.bat'a cift tikla,
UAC'i onayla. YENI-EKLENENLER.txt doluysa bu dosyayi Codex'e goster; Codex
gercekten yeni olanlari cevirip, kasitli olarak birakmak istediklerini
bilinen-ingilizce.json'a ekleyerek raporu kalici olarak temizler.
"""
import io, json, glob, hashlib, base64, subprocess, shutil, os, sys, re

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)
subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Process Cursor -ErrorAction SilentlyContinue | Stop-Process -Force'], capture_output=True)
APP = r'C:\Program Files\cursor\resources\app'
FILES = {
    'nls.messages.json': APP + r'\out\nls.messages.json',
    'workbench.desktop.main.js': APP + r'\out\vs\workbench\workbench.desktop.main.js',
    'workbench.glass.main.js': APP + r'\out\vs\workbench\workbench.glass.main.js',
    'cursor-agent-exec-main.js': APP + r'\extensions\cursor-agent-exec\dist\main.js',
    'cursor-agent-host-main.js': APP + r'\extensions\cursor-agent-host\dist\main.js',
    'cursor-local-agent-runtime-main.js': APP + r'\extensions\cursor-local-agent-runtime\dist\main.js',
    'main.js': APP + r'\out\main.js',
    'product.json': APP + r'\product.json',
}

# Turkce dil paketi etkinken Electron, ana NLS dosyasi yerine kullanici
# profilindeki derlenmis dil onbellegini okur. Bu dosya yamalanmazsa Program
# Files altindaki NLS dogru olsa bile File/Edit/View gibi ana menuler Ingilizce
# kalir. Kurulu commit'e ait etkin onbellegi dagitim listesine dahil et.
_product_boot = json.load(io.open(FILES['product.json'], encoding='utf-8'))
_commit = _product_boot.get('commit')
CACHE_NLS_TARGET = None
CACHE_NLS_ROOT_TARGET = None
if _commit:
    _clp_base = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Cursor', 'clp')
    _tr_parents = glob.glob(os.path.join(_clp_base, '*.tr'))
    if _tr_parents:
        _commit_dir = os.path.join(_tr_parents[0], _commit)
        os.makedirs(_commit_dir, exist_ok=True)
        CACHE_NLS_TARGET = os.path.join(_commit_dir, 'nls.messages.json')
        FILES['nls.cache.messages.json'] = CACHE_NLS_TARGET
        CACHE_NLS_ROOT_TARGET = os.path.join(_tr_parents[0], 'nls.messages.json')
        FILES['nls.cache.root.messages.json'] = CACHE_NLS_ROOT_TARGET
        if not os.path.exists(CACHE_NLS_TARGET) and os.path.exists(FILES['nls.messages.json']):
            shutil.copy2(FILES['nls.messages.json'], CACHE_NLS_TARGET)
        if not os.path.exists(CACHE_NLS_ROOT_TARGET) and os.path.exists(FILES['nls.messages.json']):
            shutil.copy2(FILES['nls.messages.json'], CACHE_NLS_ROOT_TARGET)
BUNDLE_FILES = ['workbench.desktop.main.js', 'workbench.glass.main.js']
RUNTIME_FILES = BUNDLE_FILES + ['cursor-agent-exec-main.js', 'cursor-agent-host-main.js', 'cursor-local-agent-runtime-main.js', 'main.js']
PATCH_SCRIPTS = ['patch_fixes.py', 'patch_glass2.py', 'patch_settings.py', 'patch_dropdowns.py',
                  'patch_extensions.py', 'patch_localized_calls.py', 'patch_values.py', 'patch_extra.py',
                  'patch_cursor_ui_tm.py', 'patch_settings_gaps.py', 'patch_statusbar_stats.py', 'patch_help_menu_labels.py',
                  'patch_remaining_ui.py',
                  'fix_all_corrupt_and_gaps.py', 'patch_steer_and_behavior.py', 'patch_hook_tip.py',
                  'patch_tool_labels.py', 'patch_main_process.py', 'patch_molten.py',
                  'patch_glass_nls.py']
report = []
OVERLAY_MARKERS = [
    'CURSOR_TR_UI_PATCH_V5', 'CURSOR_TR_UI_EXPANSION_V1',
    'CURSOR_TR_IDE_SURFACE_V1', 'CURSOR_TR_IDE_SURFACE_V2',
    'CURSOR_TR_SMALL_DIALOGS_V1', 'CURSOR_TR_SETTINGS_V1',
    'CURSOR_TR_SETTINGS_V2',
]


def log(msg):
    print(msg)
    report.append(msg)


# --- yardimci: bundle icindeki cevrilebilir metin adaylarini cikar -----------
PROPS = ['label', 'title', 'placeholder', 'tooltip', 'heading', 'header', 'subtitle',
         'emptyMessage', 'buttonLabel', 'primaryButtonLabel', 'secondaryButtonLabel',
         'confirmLabel', 'cancelLabel', 'okLabel', 'message', 'detail', 'children',
         'text', 'ariaLabel', 'description']
PROP_RE = re.compile(
    r'(?:(?:"aria-label")|' + '|'.join(PROPS) +
    r'):(?:"((?:\\.|[^"\\]){2,180})"|\'((?:\\.|[^\'\\]){2,180})\')'
)
RUNTIME_UI_RE = re.compile(r'\{id:"[a-z_]+",label:"([^"\\]{2,180})"\}')
LOCALIZED_CALL_RE = re.compile(r'De\((\d+),("(?:\\.|[^"\\])*")')
TR_CHARS = re.compile('[çğıöşüÇĞİÖŞÜ]')
BAD = re.compile(r'[{}$<>=\\]|https?:|^[a-z0-9_.:/-]+$|^\d+$|^[A-Z0-9_]+$')
EN_WORD = re.compile(
    r'\b(?:[A-Za-z]+(?:ing|ed|tion|ment|ally|able|ness)|the|to|of|and|for|or|a|an|is|are|be|'
    r'will|can|not|no|yes|all|new|this|that|your|you|with|from|when|how|what|where|use|used|'
    r'show|hide|open|close|set|get|run|add|remove|more|less|on|off|in|out|up|down|by|as|at|it|'
    r'if|do|does|has|have|was|were|only|also|may|please|try|again|now|here|there|other|each|'
    r'any|some|most|least|first|last|next|back|failed|success|error|warning|loading|done|'
    r'ready|active)\b', re.I)


def extract_candidates(text):
    """Bundle metninden İngilizce görünen (prop, deger) adaylarını çıkarır."""
    out = set()
    for m in PROP_RE.finditer(text):
        v = m.group(1) if m.group(1) is not None else m.group(2)
        if TR_CHARS.search(v) or BAD.search(v):
            continue
        if not re.search('[A-Za-z]{2}', v) or not EN_WORD.search(v):
            continue
        out.add(v)
    return out


# === 0) Guvenlik, surum tespiti + yedek =======================================
# Calisan Cursor dosyalari kopyalama sirasinda kilitleyebilir ve yarim kurulum
# birakabilir. Sessizce devam etmek yerine en basta dur.
_force_mode = '--force' in sys.argv
running = subprocess.run(
    ['tasklist', '/FI', 'IMAGENAME eq Cursor.exe', '/NH'],
    capture_output=True, text=True, errors='replace'
).stdout.lower()
if 'cursor.exe' in running and not _force_mode:
    log('HATA: Cursor halen calisiyor. Ana pencereyi ve Ajanlar Penceresini kapatip tekrar calistir.')
    io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
    sys.exit(2)
elif 'cursor.exe' in running and _force_mode:
    log('UYARI: Cursor.exe hala gorunuyor, --force ile devam ediliyor...')

# product.json kimi Cursor surumlerinde geride kalabiliyor. Kurulu uygulamanin
# gercek paket surumu resources/app/package.json icindedir.
package_json = os.path.join(APP, 'package.json')
if os.path.exists(package_json):
    ver = json.load(io.open(package_json, encoding='utf-8')).get('version', 'bilinmiyor')
else:
    ver = json.load(io.open(FILES['product.json'], encoding='utf-8')).get('version', 'bilinmiyor')
log('Cursor surumu: %s' % ver)
live_has_overlay = any(marker in io.open(FILES[BUNDLE_FILES[0]], encoding='utf-8').read()
                       for marker in OVERLAY_MARKERS)
snapdir = ('referans-yamali-' if live_has_overlay else 'orijinal-') + ver
if not os.path.isdir(snapdir):
    os.makedirs(snapdir)
    for name, src in FILES.items():
        shutil.copy2(src, os.path.join(snapdir, name))
    log('Bu surumun orijinal dosyalari yedeklendi: %s/' % snapdir)

# Ayni Cursor surumunde yama tekrar calistirildiginda canli (zaten yamali)
# dosyalari yeniden taban almak cevirileri katmanlandirir ve kaynak Ingilizce
# metinleri kaybettirir. Varsa bu surumun ilk temiz arsivinden her seferinde
# sifirdan uret. Eski surumlerden kalan referans-yamali arsivleri yalnizca temiz
# arsiv bulunmadiginda geriye donuk uyumluluk icin kullanilir.
clean_snapdir = 'orijinal-' + ver
base_snapdir = clean_snapdir if os.path.isdir(clean_snapdir) else snapdir
for name, src in FILES.items():
    archived_source = os.path.join(base_snapdir, name)
    shutil.copy2(archived_source if os.path.exists(archived_source) else src, name)
log('Yama tabani: %s/' % base_snapdir)

# Cursor guncellemesi bundle sonuna eklenen canli DOM ceviri katmanlarini siler.
# Son basarili ceviriden yedi imzali blogu geri ekle. Kismi imza durumu guvenli
# degildir; ayni blogu iki kez eklemek yerine kurulumu durdururuz.
archive_dir = 'ceviri-son-hali'
overlay_suffixes = {}
for fname in BUNDLE_FILES:
    current = io.open(fname, encoding='utf-8').read()
    present = [m for m in OVERLAY_MARKERS if m in current]
    if 0 < len(present) < len(OVERLAY_MARKERS):
        log('HATA: %s icinde dinamik yama imzalari eksik/kismi (%d/%d).' %
            (fname, len(present), len(OVERLAY_MARKERS)))
        io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
        sys.exit(3)
    if not present:
        archived = os.path.join(archive_dir, fname)
        if not os.path.exists(archived):
            log('HATA: Dinamik yama arsivi bulunamadi: %s' % archived)
            io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
            sys.exit(3)
        overlay_source = io.open(archived, encoding='utf-8').read()
        starts = [overlay_source.find('/* ' + m + ' */') for m in OVERLAY_MARKERS]
        if any(i < 0 for i in starts):
            log('HATA: Arsivde yedi dinamik yama imzasinin tamami yok: %s' % archived)
            io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
            sys.exit(3)
        overlay_suffixes[fname] = overlay_source[min(starts):]
        io.open(fname, 'w', encoding='utf-8', newline='').write(current.rstrip())
        log('%s: dinamik UI katmanlari arsivden alindi ve statik yamalardan korundu' % fname)
    else:
        starts = [current.find('/* ' + m + ' */') for m in OVERLAY_MARKERS]
        overlay_suffixes[fname] = current[min(starts):]
        current = current[:min(starts)].rstrip()
        io.open(fname, 'w', encoding='utf-8', newline='').write(current)
        log('%s: mevcut dinamik UI katmanlari statik yamalardan korundu' % fname)

# === 1) NLS: resmi dil paketi + ozel ceviri bellegi ==========================
# Cursor/VS Code guncellemeleri nls.messages.json dizisinin sirasini ve icerigini
# degistirebilir. Yalnizca Ingilizce metne gore esleme yapmak, yeni surumde ana
# menu gibi temel metinleri yeniden Ingilizce birakiyordu. Resmi Turkce dil
# paketini nls.keys.json icindeki (modul, anahtar) eslesmesiyle uygula; ardindan
# bizim ozel ceviri bellegimiz ayni Ingilizce kaynak metin uzerinden onu ezsin.
tm = json.load(io.open('nls-tm.json', encoding='utf-8'))
from patch_remaining_ui import NLS_REQUIRED
tm.update(NLS_REQUIRED)
msgs = json.load(io.open('nls.messages.json', encoding='utf-8'))
source_msgs = list(msgs)

keys_path = os.path.join(APP, 'out', 'nls.keys.json')
langpack_pattern = os.path.join(os.path.expanduser('~'), '.cursor', 'extensions',
                                'ms-ceintl.vscode-language-pack-tr-*',
                                'translations', 'main.i18n.json')
langpacks = glob.glob(langpack_pattern)
official_hit = 0
official_skipped = 0
if os.path.exists(keys_path) and langpacks:
    langpack_path = max(langpacks, key=os.path.getmtime)
    keys_data = json.load(io.open(keys_path, encoding='utf-8'))
    official = json.load(io.open(langpack_path, encoding='utf-8')).get('contents', {})
    expected = sum(len(names) for _, names in keys_data)
    if expected != len(msgs):
        log('HATA: nls.keys.json ile nls.messages.json uzunluklari uyusmuyor (%d/%d).' %
            (expected, len(msgs)))
        io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
        sys.exit(3)
    index = 0
    placeholder_re = re.compile(r'\{\d+\}')
    for module, names in keys_data:
        module_translations = (
            official.get(module)
            or official.get(module.replace('.view.', '.'))
            or official.get(module.replace('electron-sandbox', 'electron-browser'))
            or official.get(module.replace('.view.', '.').replace('electron-sandbox', 'electron-browser'))
            or {}
        )
        for name in names:
            translated = module_translations.get(name)
            if isinstance(translated, str):
                source_placeholders = sorted(placeholder_re.findall(source_msgs[index]))
                translated_placeholders = sorted(placeholder_re.findall(translated))
                if source_placeholders == translated_placeholders:
                    msgs[index] = translated
                    official_hit += 1
                else:
                    official_skipped += 1
            index += 1
    log('Resmi Turkce dil paketi: %d metin uygulandi, %d yer tutucu uyusmazligi atlandi (%s)' %
        (official_hit, official_skipped, os.path.basename(os.path.dirname(os.path.dirname(langpack_path)))))
else:
    log('UYARI: Resmi Turkce dil paketi veya nls.keys.json bulunamadi; yalnizca ozel bellek uygulanacak.')

hit = 0
for i, source in enumerate(source_msgs):
    if isinstance(source, str) and source in tm:
        msgs[i] = tm[source]
        hit += 1
json.dump(msgs, io.open('nls.messages.json.new', 'w', encoding='utf-8'),
          ensure_ascii=False, separators=(',', ':'))
json.load(io.open('nls.messages.json.new', encoding='utf-8'))  # dogrulama
os.replace('nls.messages.json.new', 'nls.messages.json')
if CACHE_NLS_TARGET:
    shutil.copy2('nls.messages.json', 'nls.cache.messages.json')
    log('Etkin Cursor NLS onbellegi de yamaya dahil edildi: %s' % CACHE_NLS_TARGET)
if CACHE_NLS_ROOT_TARGET:
    shutil.copy2('nls.messages.json', 'nls.cache.root.messages.json')
    log('Kok Cursor NLS onbellegi de yamaya dahil edildi: %s' % CACHE_NLS_ROOT_TARGET)
if not CACHE_NLS_TARGET and not CACHE_NLS_ROOT_TARGET:
    log('UYARI: Etkin Cursor NLS onbellegi bulunamadi; Cursor bir kez acildiktan sonra yama tekrar calistirilmalidir.')
log('Ozel NLS bellegi: %d metin uygulandi (bellek: %d girdi)' % (hit, len(tm)))

# === 2) Bundle prop haritalari (tr2/m*.json) =================================
maps = {}
for f in sorted(glob.glob('tr2/m*.json')):
    for k, v in json.load(io.open(f, encoding='utf-8')).items():
        prop, old = k.split('\t', 1)
        key = ('"aria-label"' if prop == 'aria-label' else prop) + ':"' + old + '"'
        maps[key] = ('"aria-label"' if prop == 'aria-label' else prop) + ':"' + v + '"'

for fname in BUNDLE_FILES:
    s = io.open(fname, encoding='utf-8').read()
    n = miss = 0
    for a, b in maps.items():
        c = s.count(a)
        if c:
            s = s.replace(a, b)
            n += c
        else:
            miss += 1
    io.open(fname, 'w', encoding='utf-8', newline='').write(s)
    log('%s: prop haritasindan %d degisim (%d kalip bu surumde bulunamadi)' % (fname, n, miss))

# === 3) Baglamli ozel yamalar ==================================================
for script in PATCH_SCRIPTS:
    if os.path.exists(script):
        r = subprocess.run([sys.executable, '-X', 'utf8', script], capture_output=True, encoding='utf-8', errors='replace')
        log('%s -> %s' % (script, (r.stdout or r.stderr).strip().replace('\n', ' | ')))
        if r.returncode != 0:
            log('HATA: %s basarisiz oldu (kod %d). Kurulum iptal.' % (script, r.returncode))
            io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
            sys.exit(4)

# Statik yamalar tamamlandiktan sonra korunan DOM katmanlarini degismeden geri
# ekle. Menu katmani en son kendi temiz sablonunu kurar.
for fname in BUNDLE_FILES:
    text = io.open(fname, encoding='utf-8').read().rstrip()
    text += '\n\n' + overlay_suffixes[fname].lstrip()
    io.open(fname, 'w', encoding='utf-8', newline='').write(text)
menu_script = 'patch_menu_gaps.py'
r = subprocess.run([sys.executable, '-X', 'utf8', menu_script], capture_output=True, encoding='utf-8', errors='replace')
log('%s -> %s' % (menu_script, (r.stdout or r.stderr).strip().replace('\n', ' | ')))
if r.returncode != 0:
    log('HATA: %s basarisiz oldu (kod %d). Kurulum iptal.' % (menu_script, r.returncode))
    io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
    sys.exit(4)

if CACHE_NLS_TARGET:
    shutil.copy2('nls.messages.json', 'nls.cache.messages.json')
if CACHE_NLS_ROOT_TARGET:
    shutil.copy2('nls.messages.json', 'nls.cache.root.messages.json')

# === 4) Sozdizimi dogrulamasi ==================================================
check_files = RUNTIME_FILES
for fname in check_files:
    if not os.path.exists(fname):
        continue
    shutil.copy(fname, '_chk.mjs')
    r = subprocess.run(['node', '--check', '_chk.mjs'], capture_output=True, text=True)
    if r.returncode != 0:
        log('HATA: %s sozdizimi bozuk! Kurulum iptal. %s' % (fname, r.stderr[:400]))
        os.remove('_chk.mjs')
        io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
        sys.exit(1)
os.remove('_chk.mjs')
log('Sozdizimi dogrulandi (tum dosyalar gecerli)')

# === 5) product.json TUM checksum'lari guncelle ===============================
# Sadece kendi patchledigimiz dosyayi degil, product.json'in referans verdigi
# HER dosyayi (preload.js, css, extensionHostProcess.js, workbench.js vb.)
# canli haliyle yeniden hesapliyoruz. Cursor'in gercek guncellemeleri bu
# dosyalari da degistirebiliyor; tek dosya guncellemek "kurulum bozuk"
# uyarisina yol aciyordu.
p = json.load(io.open('product.json', encoding='utf-8'))
cks = p.setdefault('checksums', {})
for rel in list(cks.keys()):
    live_path = os.path.join(APP, 'out', *rel.split('/'))
    if rel == 'vs/workbench/workbench.desktop.main.js':
        # bu dosyanin yamali/yerel kopyasini kullan (henuz Program Files'a kurulmadi)
        h = hashlib.sha256(io.open('workbench.desktop.main.js', 'rb').read()).digest()
    elif rel == 'vs/workbench/workbench.glass.main.js':
        # bu dosyanin yamali/yerel kopyasini kullan (henuz Program Files'a kurulmadi)
        h = hashlib.sha256(io.open('workbench.glass.main.js', 'rb').read()).digest()
    elif os.path.exists(live_path):
        h = hashlib.sha256(io.open(live_path, 'rb').read()).digest()
    else:
        continue
    cks[rel] = base64.b64encode(h).decode().rstrip('=')
io.open('product.json', 'w', encoding='utf-8').write(json.dumps(p, indent='\t', ensure_ascii=False) + '\n')
log('product.json: tum checksum girdileri (%d) guncellendi' % len(cks))

# === 6) Yama SONRASI kalan Ingilizceyi tara, bilinen listeyi ele ==============
known = set()
if os.path.exists('bilinen-ingilizce.json'):
    known = set(json.load(io.open('bilinen-ingilizce.json', encoding='utf-8')))

# Daha once yanlislikla "bilerek Ingilizce" listesine alinmis gercek UI
# metinleri, gelecekte baglamlari degisse bile taramadan saklanmasin.
from patch_remaining_ui import MAP as REQUIRED_UI_MAP
REQUIRED_MENU_UI = {
    'New Agents Window', 'Close Window', 'Exit', 'Zen Mode',
    'Secondary Side Bar', 'Render Whitespace'
}
known.difference_update(REQUIRED_UI_MAP.keys())
known.difference_update(REQUIRED_MENU_UI)
known.update({
    'Short tray status for this FSD run, e.g. "Checking CI logs".',
    'This example demonstrates the buttons prop with utility buttons like "more menu" and "Copy Request Info".',
})

new_bundle = {}
for fname in RUNTIME_FILES:
    patched = io.open(fname, encoding='utf-8').read()
    if fname in BUNDLE_FILES:
        cands = extract_candidates(patched) - known
    else:
        # Ajan runtime paketleri binlerce sistem istemi, SDK hata metni ve
        # polyfill adi tasir. Bunlar UI degildir. Yalnizca Baglam Kullanimi
        # panelinin id/label satirlarini tarayarak yeni UI etiketini yakala.
        cands = {m.group(1) for m in RUNTIME_UI_RE.finditer(patched)
                 if not TR_CHARS.search(m.group(1)) and EN_WORD.search(m.group(1))}
    if cands:
        new_bundle[fname] = cands

# De(index,"fallback") yerellestirme cagrilari normal prop taramasina girmez.
# patch_localized_calls, NLS'de Turkcesi olanlari kaynakta da cevirir. Geriye
# kalan yeni Ingilizce fallback'ler guncelleme raporunda ayrica gorunur.
intentional_de = set()
try:
    from patch_localized_calls import INTENTIONAL_ENGLISH as intentional_de
except Exception:
    pass
for fname in BUNDLE_FILES:
    patched = io.open(fname, encoding='utf-8').read()
    vals = set()
    for m in LOCALIZED_CALL_RE.finditer(patched):
        try:
            value = json.loads(m.group(2))
        except Exception:
            continue
        if (isinstance(value, str) and re.search('[A-Za-z]{2}', value)
                and not TR_CHARS.search(value) and EN_WORD.search(value)
                and value not in known and value not in intentional_de):
            vals.add(value)
    if vals:
        new_bundle.setdefault(fname, set()).update(vals)

new_nls = {s for s in msgs if isinstance(s, str) and EN_WORD.search(s)
           and not TR_CHARS.search(s) and s not in known}

total_new = sum(len(v) for v in new_bundle.values()) + len(new_nls)
log('Taranan kapsamda kalan aday: %d (etkin bilinen listede: %d)' % (total_new, len(known)))

with io.open('YENI-EKLENENLER.txt', 'w', encoding='utf-8') as f:
    f.write('Cursor surumu: %s\n' % ver)
    f.write('Bilinen/kasitli-Ingilizce listesindeki girdi sayisi: %d\n' % len(known))
    f.write('TARANAN KAPSAMDA listenin DISINDA kalan aday: %d\n\n' % total_new)
    f.write('Kapsam: NLS, gorunur prop metinleri, De(index,fallback) cagrilari ve\n')
    f.write('Ajan Baglam Kullanimi panelinin id/label satirlari.\n\n')
    f.write('Not: Buradaki her satir ya (a) guncellemeyle gelen yeni bir metin,\n')
    f.write('ya da (b) henuz kapsanmamis eski bir metindir. Codex bunlari inceleyip\n')
    f.write('gercekten cevrilmesi gerekenleri cevirir; kasitli Ingilizce birakilacaklari\n')
    f.write('(jargon, dev/debug metni vb.) bilinen-ingilizce.json listesine ekler.\n\n')
    if new_nls:
        f.write('=== nls.messages.json (%d) ===\n' % len(new_nls))
        f.write('\n'.join(sorted(new_nls)))
        f.write('\n\n')
    for fname, vals in new_bundle.items():
        f.write('=== %s (%d) ===\n' % (fname, len(vals)))
        f.write('\n'.join(sorted(vals)))
        f.write('\n\n')

# Hover/title/aria-label alanlarini ayrica tara. Bu katman Archive, Pin ve Copy
# gibi kisa etiketleri genel UI adaylarinin arasinda kaybetmeden raporlar.
hover_scan = subprocess.run(
    [sys.executable, '-X', 'utf8', 'scan_visible_props.py'],
    capture_output=True, encoding='utf-8', errors='replace'
)
log('scan_visible_props.py -> %s' %
    ((hover_scan.stdout or hover_scan.stderr).strip().replace('\n', ' | ')))
if hover_scan.returncode != 0:
    log('HATA: hover/tooltip taramasi basarisiz oldu; kurulum iptal.')
    io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
    sys.exit(4)

# === 7) UAC ile islemsel kurulum + rollback ===================================
# Once canli dosyalarin tamami yedeklenir, sonra yamali dosyalar kopyalanir ve
# kaynak/hedef SHA256 degerleri karsilastirilir. Herhangi bir adim hata verirse
# tum hedefler onceki canli hallerine geri dondurulur.
deploy_ps1 = os.path.abspath('deploy_all.ps1')
rollback_dir = os.path.abspath('deploy-rollback')
if os.path.commonpath([BASE, rollback_dir]) != BASE:
    log('HATA: rollback klasoru calisma klasoru disina tasiyor.')
    sys.exit(5)

def ps_quote(value):
    return "'" + value.replace("'", "''") + "'"

with io.open(deploy_ps1, 'w', encoding='utf-8', newline='') as f:
    f.write("$ErrorActionPreference = 'Stop'\n")
    f.write('$resultFile = %s\n' % ps_quote(os.path.abspath('deploy_result.txt')))
    f.write('$rollbackDir = %s\n' % ps_quote(rollback_dir))
    f.write('$items = @(\n')
    deploy_items = list(FILES.items())
    for index, (name, dst) in enumerate(deploy_items):
        suffix = ',' if index < len(deploy_items) - 1 else ''
        f.write('  @{ Source = %s; Destination = %s; Backup = %s }%s\n' % (
            ps_quote(os.path.abspath(name)), ps_quote(dst),
            ps_quote(os.path.join(rollback_dir, name)), suffix))
    f.write(')\n')
    f.write(r'''
try {
  $cursorProcesses = @(Get-Process Cursor -ErrorAction SilentlyContinue)
  if ($cursorProcesses.Count -gt 0) {
    $cursorProcesses | Stop-Process -Force
    Start-Sleep -Seconds 1
  }
  if (Test-Path -LiteralPath $rollbackDir) {
    Remove-Item -LiteralPath $rollbackDir -Recurse -Force
  }
  New-Item -ItemType Directory -Path $rollbackDir -Force | Out-Null
  foreach ($item in $items) {
    Copy-Item -LiteralPath $item.Destination -Destination $item.Backup -Force
  }
  foreach ($item in $items) {
    Copy-Item -LiteralPath $item.Source -Destination $item.Destination -Force
  }
  try {
    $user = $env:USERNAME
    icacls 'C:\Program Files\cursor\resources\app' /grant "${user}:(OI)(CI)F" /Q | Out-Null
  } catch {}
  Set-Content -LiteralPath $resultFile -Value 'OK_VERIFIED' -Encoding ASCII
  exit 0
}
catch {
  $rollbackErrors = @()
  foreach ($item in $items) {
    if (Test-Path -LiteralPath $item.Backup) {
      try {
        Copy-Item -LiteralPath $item.Backup -Destination $item.Destination -Force
      }
      catch {
        $rollbackErrors += $item.Destination
      }
    }
  }
  if ($rollbackErrors.Count -eq 0) {
    Set-Content -LiteralPath $resultFile -Value ('FAIL_ROLLED_BACK: ' + $_.Exception.Message) -Encoding UTF8
  }
  else {
    Set-Content -LiteralPath $resultFile -Value ('FAIL_ROLLBACK_ERROR: ' + ($rollbackErrors -join ', ')) -Encoding UTF8
  }
  exit 1
}
''')
if os.path.exists('deploy_all.bat'):
    os.remove('deploy_all.bat')  # eski, rollback'siz dagitim betigi artik kullanilmaz
if os.path.exists('deploy_result.txt'):
    os.remove('deploy_result.txt')
launch = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', deploy_ps1]
subprocess.run(launch)
deploy_status = (io.open('deploy_result.txt', encoding='utf-8-sig').read().strip()
                 if os.path.exists('deploy_result.txt') else 'NO_RESULT')
ok = deploy_status == 'OK_VERIFIED'
if not ok:
    log('Standart izinle yazilamadi, UAC yonetici izni ile deneniyor...')
    if os.path.exists('deploy_result.txt'):
        os.remove('deploy_result.txt')
    elevated = [
        'powershell', '-NoProfile', '-Command',
        f'Start-Process -FilePath "powershell.exe" -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","{deploy_ps1}" -Verb RunAs -Wait'
    ]
    subprocess.run(elevated)
    deploy_status = (io.open('deploy_result.txt', encoding='utf-8-sig').read().strip()
                     if os.path.exists('deploy_result.txt') else 'NO_RESULT')
    ok = deploy_status == 'OK_VERIFIED'

# Yetkili betigin sonucuna ek olarak normal surecten ikinci kez birebir hash
# karsilastirmasi yap. Basarili raporu ancak iki dogrulama da gectiginde verilir.
post_mismatches = []
if ok:
    for name, dst in FILES.items():
        source_hash = hashlib.sha256(io.open(name, 'rb').read()).digest()
        target_hash = hashlib.sha256(io.open(dst, 'rb').read()).digest()
        if source_hash != target_hash:
            post_mismatches.append(name)
    if post_mismatches:
        ok = False
        deploy_status = 'POST_VERIFY_FAILED: ' + ', '.join(post_mismatches)
log('Kurulum: %s [%s]' % ('BASARILI' if ok else 'BASARISIZ', deploy_status))

if ok:
    os.makedirs('ceviri-son-hali', exist_ok=True)
    for name in FILES:
        shutil.copy2(name, os.path.join('ceviri-son-hali', name))
    log('ceviri-son-hali/ guncellendi')
    try:
        import patch_molten
        _m_files, _m_mods = patch_molten.patch_molten_dir(os.path.join(APP, "molten", "dist", "renderer", "assets"))
        log('Molten dagitim sonrasi yamalama: %d dosyada %d degisim uygulandi.' % (_m_files, _m_mods))
    except Exception as _em:
        log('Molten dagitim sonrasi yamalama uyarisi: %s' % _em)
    try:
        import sqlite3
        _db_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Cursor', 'User', 'globalStorage', 'state.vscdb')
        if os.path.exists(_db_path):
            _conn = sqlite3.connect(_db_path, timeout=5)
            _cur = _conn.cursor()
            _key = "src.vs.platform.reactivestorage.browser.reactiveStorageServiceImpl.persistentStorage.applicationUser"
            _cur.execute("SELECT value FROM ItemTable WHERE key = ?", (_key,))
            _row = _cur.fetchone()
            if _row:
                _data = json.loads(_row[0])
                _modes = _data.get("composerState", {}).get("modes4", [])
                _desc_map = {
                    "agent": "Planlayın, arayın, düzenlemeler yapın, komutlar çalıştırın",
                    "triage": "Yetkilendirilen alt ajanlarla uzun erimli görevleri koordine edin",
                    "plan": "Görevleri gerçekleştirmek için ayrıntılı planlar oluşturun",
                    "background": "Ajanları arka planda çalıştırın",
                    "chat": "Kod tabanınız hakkında Cursor'a sorular sorun",
                    "spec": "Uygulama adımları içeren yapılandırılmış planlar oluşturun",
                    "debug": "Çalışma zamanı izlerini kullanarak hataları sistematik olarak teşhis edin ve düzeltin",
                    "multitask": "Birden fazla görevi paralel olarak çalıştırın ve koordine edin",
                }
                _changed = False
                for _m in _modes:
                    _mid = _m.get("id")
                    if _mid in _desc_map and _m.get("description") != _desc_map[_mid]:
                        _m["description"] = _desc_map[_mid]
                        _changed = True
                if _changed:
                    _new_val = json.dumps(_data, ensure_ascii=False)
                    _cur.execute("UPDATE ItemTable SET value = ? WHERE key = ?", (_new_val, _key))
                    _conn.commit()
                    log("state.vscdb: modes4 Turkcelestirildi")
            _conn.close()
    except Exception as _e:
        log("state.vscdb guncelleme uyarisi: %s" % _e)
else:
    io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
    sys.exit(5)

io.open('apply_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
print('\n' + '=' * 60)
print('Kurulum BASARILI!')
print('Rapor          : apply_report.txt')
print('Yeni metinler  : YENI-EKLENENLER.txt (%d aday)' % total_new)
print('Hover denetimi : YENI-HOVER-ETIKETLER.txt')
print('=' * 60)
print('\n* Projeyi faydali bulduysaniz GitHub\'da bir Yildiz (Star) vererek destek olun:')
print('   https://github.com/foztrk/cursor-turkish-localization\n')
