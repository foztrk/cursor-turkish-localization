# -*- coding: utf-8 -*-
"""
Deterministik Yama Dogrulama Kapisi (0 token, ~2 sn).
Canli kurulum dosyalarini (Program Files + CLP Cache + Molten + Extensions)
4 katmanda denetler:
  1) deploy_result.txt == OK_VERIFIED ve SHA-256 eslesmesi
  2) Glass NLS (nls.messages.json & CLP onbellekleri) ve yer tutucu ({0}) butunlugu
  3) Bundle (glass & desktop) kritik ceviri, EN=0 ve greedy-regex regresyon denetimi
  4) Molten Vite varliklari ve out/main.js (Tray) canli dogrulamasi
"""
import glob
import hashlib
import io
import json
import os
import re
import sys

APP = r"C:\Program Files\cursor\resources\app"
BASE = os.path.dirname(os.path.abspath(__file__))


def fail(errors, msg):
    print(f"  [HATA] {msg}")
    errors.append(msg)


def ok(msg):
    print(f"  [OK] {msg}")


def main():
    os.chdir(BASE)
    errors = []
    print("=== 1. DAGITIM VE SHA-256 DOGRULAMASI ===")
    res_path = os.path.join(BASE, "deploy_result.txt")
    res = io.open(res_path, encoding="utf-8-sig").read().strip() if os.path.exists(res_path) else "YOK"
    if res != "OK_VERIFIED":
        fail(errors, f"deploy_result.txt OK_VERIFIED degil: {res}")
    else:
        ok("deploy_result.txt == OK_VERIFIED")

    live_files = {
        "nls.messages.json": os.path.join(APP, "out", "nls.messages.json"),
        "workbench.desktop.main.js": os.path.join(APP, "out", "vs", "workbench", "workbench.desktop.main.js"),
        "workbench.glass.main.js": os.path.join(APP, "out", "vs", "workbench", "workbench.glass.main.js"),
        "main.js": os.path.join(APP, "out", "main.js"),
    }
    for name, dst in live_files.items():
        src = os.path.join(BASE, name)
        if not os.path.exists(src) or not os.path.exists(dst):
            fail(errors, f"Dosya eksik: {name}")
            continue
        sh = hashlib.sha256(io.open(src, "rb").read()).hexdigest()
        dh = hashlib.sha256(io.open(dst, "rb").read()).hexdigest()
        if sh != dh:
            fail(errors, f"SHA-256 uyusmazligi: {name}")
        else:
            ok(f"SHA-256 eslesti: {name}")

    print("\n=== 2. GLASS NLS & CLP ONBELLEK DOGRULAMASI ===")
    from patch_glass_nls import GLASS_NLS_MAP
    keys_path = os.path.join(APP, "out", "nls.keys.json")
    keys_data = json.load(io.open(keys_path, encoding="utf-8"))
    flat_keys = [name for _, names in keys_data for name in names]
    msgs = json.load(io.open(live_files["nls.messages.json"], encoding="utf-8"))
    if len(flat_keys) != len(msgs):
        fail(errors, f"nls.keys.json ({len(flat_keys)}) != nls.messages.json ({len(msgs)})")
    else:
        must_keys = [
            ("glass.allowedMachines.environmentsMenu", "Ortamlar"),
            ("glass.allowedMachines.machinesMenu", "Makineler"),
            ("glass.allowedMachines.cloud", "Bulut"),
            ("glass.allowedMachines.poolsSection", "Havuzlar"),
            ("glass.allowedMachines.reposSection", "Depolar"),
            ("glass.allowedMachines.offline", "Çevrimdışı"),
            ("glass.allowedMachines.unknownMachine", "Bilinmeyen makine"),
            ("glass.agentMetadataTooltip.ongoingVoiceCall", "Devam Eden Sesli Görüşme"),
            ("glass.agentMetadataTooltip.local", "Yerel"),
            ("glass.agentMetadataTooltip.worktree", "Çalışma Ağacı"),
            ("glass.localDeployTray.confirmDeploy", "Klasörü Dağıt"),
            ("glass.deployPrototypeNudge.deploy", "Uygulamayı Dağıt"),
            ("inlineDiffs.undoChange", "Değişikliği geri al"),
            ("inlineDiffs.keepChange", "Değişikliği koru"),
        ]
        key_to_idx = {k: i for i, k in enumerate(flat_keys)}
        for k, expected_tr in must_keys:
            idx = key_to_idx.get(k)
            if idx is None:
                fail(errors, f"NLS anahtari bulunamadi: {k}")
            elif msgs[idx] != expected_tr:
                fail(errors, f"NLS[{idx}] ({k}) = {msgs[idx]!r}, beklenen = {expected_tr!r}")
            else:
                ok(f"NLS[{idx}] {k} -> {expected_tr!r}")

        # Tum 14.600+ NLS mesajinda orijinal ile {0}, {1} yer tutucu tutarlilik kontrolu
        pkg = json.load(io.open(os.path.join(APP, "package.json"), encoding="utf-8"))
        orig_nls_path = os.path.join(BASE, f"orijinal-{pkg.get('version', '')}", "nls.messages.json")
        if os.path.exists(orig_nls_path):
            orig_msgs = json.load(io.open(orig_nls_path, encoding="utf-8"))
            ph_re = re.compile(r"\{\d+\}")
            ph_mismatches = 0
            for i, (om, lm) in enumerate(zip(orig_msgs, msgs)):
                if isinstance(om, str) and isinstance(lm, str):
                    if sorted(ph_re.findall(om)) != sorted(ph_re.findall(lm)):
                        ph_mismatches += 1
            if ph_mismatches > 0:
                fail(errors, f"nls.messages.json icinde {ph_mismatches} yer tutucu ({{0}}) uyusmazligi var")
            else:
                ok(f"Tum {len(msgs)} NLS girdisinde yer tutucu ({{0}}) uyusmazligi: 0")

    # CLP onbellek esitligi
    prod = json.load(io.open(os.path.join(APP, "product.json"), encoding="utf-8"))
    commit = prod.get("commit", "")
    clp_files = glob.glob(os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Cursor", "clp", "*.tr", commit, "nls.messages.json"))
    for cf in clp_files:
        ch = hashlib.sha256(io.open(cf, "rb").read()).hexdigest()
        nh = hashlib.sha256(io.open(live_files["nls.messages.json"], "rb").read()).hexdigest()
        if ch != nh:
            fail(errors, f"CLP NLS onbellegi guncel degil: {cf}")
        else:
            ok(f"CLP NLS onbellegi guncel: {cf}")

    print("\n=== 3. CANLI BUNDLE & REGRESYON DOGRULAMASI ===")
    glass = io.open(live_files["workbench.glass.main.js"], encoding="utf-8").read()
    forbidden_glass = [
        'children:["%",v,y]',
        'title:"&&Settings"',
        'children:"Manage Origin Settings"',
        'label:"Worktree Cleanup"',
        '?"Installing":"Update"',
        'children:"Worker Model"',
        '===void 0?"Match":"Custom"',
        '"Auto-imports are temporarily disabled"',
        '"Add Custom Model"]',
        '="Control local agents from your phone"',
        ']:"More Actions"}',
        'done:"Message from"',
        'done:"Created"',
        'completed:"Created"',
        '?`Marked ${',
        '?"Messages from ":"Message from "',
        'children:"Copy Relative Path"',
        'children:"Diff View"',
        'children:"Line Numbers"',
        'children:"Discard Changes"',
        '="Disconnect from this computer"',
        '="Disconnect from all computers"',
        '="Don\\u2019t allow"',
        '?"Allow this device?":`Allow \\u201C${t}\\u201D?`',
        'Koordinatör çabası',
        'bu çabayla başlar',
        'is ready \\u2014 click to restart',
        'will apply on quit \\u2014 click to restart now',
    ]
    for fb in forbidden_glass:
        if fb in glass:
            fail(errors, f"Canli glass icinde Ingilizce/bozuk kalip kaldi: {fb}")
    required_glass = [
        'title:"&&Ayarlar"',
        'children:"Origin Ayarlarını Yönet"',
        'label:"Çalışma Ağacı Temizliği"',
        '?"Yükleniyor":"Güncelle"',
        'children:"Çalışan Modeli"',
        '===void 0?"Eşleştir":"Özel"',
        'Otomatik içe aktarmalar geçici olarak devre dışı',
        '"Özel Model Ekle"]',
        '="Telefonunuzdan yerel ajanları kontrol edin"',
        'children:"Göreli Yolu Kopyala"',
        'children:"Fark Görünümü"',
        'children:"Satır Numaraları"',
        'children:"Değişiklikleri Geri Al"',
        '="Bu bilgisayarla bağlantıyı kes"',
        '="Tüm bilgisayarlarla bağlantıyı kes"',
        '="İzin Verme"',
        '?"Bu cihaza izin verilsin mi?":',
        'izin verilsin mi?`',
        '`Son kullanım: ${',
        'Koordinatör Düşünme Düzeyi',
        'bu düşünme düzeyinde başlar',
        'sürümüne güncelleme hazır — yeniden başlatmak için tıklayın`',
        'sürümüne güncelleme çıkışta uygulanacak — şimdi yeniden başlatmak için tıklayın`',
        'Otomasyonlar Yüklenemedi',
        'Uzantıları yüklerken ve çalıştırırken uzantı imzalarını doğrulayın',
        'Dikte ederken isteminizi gönderen sözcükler',
    ]
    for rq in required_glass:
        if rq not in glass:
            fail(errors, f"Canli glass icinde beklenen Turkce kalip yok: {rq}")
    if not errors:
        ok("Canli workbench.glass.main.js tum regresyon ve ceviri kontrollerinden gecti")

    print("\n=== 4. MOLTEN VE MAIN.JS (TRAY) DOGRULAMASI ===")
    mainjs = io.open(live_files["main.js"], encoding="utf-8").read()
    if 'r.label==="Projects"?"Projeler"' not in mainjs or 'Tüm Bildirimleri Temizle' not in mainjs:
        fail(errors, "Canli out/main.js Tray yamasi eksik")
    else:
        ok("Canli out/main.js Tray yamasi dogrulandi")

    molten_dir = os.path.join(APP, "molten", "dist", "renderer", "assets")
    molten_files = glob.glob(os.path.join(molten_dir, "*.js"))
    molten_all = "\n".join(
        io.open(p, encoding="utf-8", errors="ignore").read()
        for p in molten_files
    )
    for rq in [
        '`Özel Model Ekle`',
        '`Telefonunuzdan yerel ajanları kontrol edin`',
        '`Eklentiler Ekle`',
        'done:`Mesaj Gönderen:`',
        '`İzin Verme`',
        '`Otomasyonlar Yüklenemedi`',
    ]:
        if rq not in molten_all:
            fail(errors, f"Canli Molten icinde beklenen Turkce kalip yok: {rq}")
        else:
            ok(f"Canli Molten dogrulandi: {rq}")

    mg_files = glob.glob(os.path.join(molten_dir, "messages.gen-*.js"))
    if not mg_files:
        fail(errors, "Canli Molten messages.gen-*.js bulunamadi")
    else:
        mg_txt = io.open(mg_files[0], encoding="utf-8", errors="ignore").read()
        for mrq in [
            "/* CURSOR_TR_LINGUI_V1 */",
            '"Worker Model","Çalışan Modeli"',
            '"Copy Relative Path","Göreli Yolu Kopyala"',
            '"Diff View","Fark Görünümü"',
            '"Line Numbers","Satır Numaraları"',
            '"Discard Changes","Değişiklikleri Geri Al"',
            '"Disconnect from this computer","Bu bilgisayarla bağlantıyı kes"',
            '"Disconnect from all computers","Tüm bilgisayarlarla bağlantıyı kes"',
            '"Add or search model","Model ekle veya ara"',
            '"More Actions","Diğer Eylemler"',
            "Son kullanım: ",
            "sürümüne güncelleme hazır",
        ]:
            if mrq not in mg_txt:
                fail(errors, f"Canli Molten Lingui katalogunda kalip yok: {mrq}")
            else:
                ok(f"Canli Molten Lingui dogrulandi: {mrq}")

    print("\n" + "=" * 60)
    if errors:
        print(f"DOGRULAMA BASARISIZ: {len(errors)} hata bulundu!")
        sys.exit(1)
    print("DOGRULAMA BASARILI: Tum deterministik kontroller PASS (0 hata).")
    print("=" * 60)


if __name__ == "__main__":
    main()
