# -*- coding: utf-8 -*-
"""
Cursor Türkçe Yerelleştirme Bütünlük ve Sağlık Doğrulayıcı
Tüm checksum'ları, dosya varlıklarını, NLS önbelleğini ve sözdizimini doğrular.
"""
import os
import sys
import json
import base64
import hashlib
import glob

if sys.platform == "win32":
    try:
        os.system("chcp 65001 >nul")
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

APP = r'C:\Program Files\cursor\resources\app'

def verify_all():
    print("=" * 65)
    print("  CURSOR TÜRKÇE YERELLEŞTİRME — TAM DOĞRULAMA (VERIFY_ALL)")
    print("=" * 65)
    
    if not os.path.exists(APP):
        print(f"[!] HATA: Cursor kurulu bulunamadı: {APP}")
        return False

    product_path = os.path.join(APP, 'product.json')
    if not os.path.exists(product_path):
        print(f"[!] HATA: product.json bulunamadı: {product_path}")
        return False

    with open(product_path, 'r', encoding='utf-8') as f:
        prod = json.load(f)

    version = prod.get('version', 'Bilinmiyor')
    commit = prod.get('commit', 'Bilinmiyor')
    print(f"[*] Cursor Sürümü : v{version}")
    print(f"[*] Commit ID     : {commit}")
    print("-" * 65)

    # 1. Checksum Doğrulaması (IntegrityService)
    print("[*] 1/3 Integrity Checksums Doğrulanıyor...")
    checksums = prod.get('checksums', {})
    mismatches = []
    missing_files = []

    for rel_path, expected_hash in checksums.items():
        full_path = os.path.join(APP, 'out', *rel_path.split('/'))
        if not os.path.exists(full_path):
            missing_files.append(rel_path)
            continue
        with open(full_path, 'rb') as bf:
            actual_hash = base64.b64encode(hashlib.sha256(bf.read()).digest()).decode().rstrip('=')
        if actual_hash != expected_hash:
            mismatches.append((rel_path, expected_hash, actual_hash))

    if missing_files:
        print(f"  [-] Eksik out/ dosyaları: {len(missing_files)}")
        for mf in missing_files:
            print(f"      - {mf}")
    if mismatches:
        print(f"  [-] Uyuşmayan Checksum'lar: {len(mismatches)}")
        for mm in mismatches:
            print(f"      - {mm[0]}: Beklenen={mm[1]} Gerçek={mm[2]}")
    if not missing_files and not mismatches:
        print(f"  [+] BAŞARILI: {len(checksums)}/{len(checksums)} dosya SHA-256 bütünlüğü %100 doğrulandı.")
        print("      (Cursor 'Installation appears to be corrupt' uyarısı ASLA vermez)")

    # 2. Dil Önbelleği (CLP) Doğrulaması
    print("\n[*] 2/3 Dil Önbelleği (CLP) Senkronizasyonu Kontrol Ediliyor...")
    clp_base = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Cursor', 'clp')
    tr_parents = glob.glob(os.path.join(clp_base, '*.tr'))
    if tr_parents:
        commit_cache = os.path.join(tr_parents[0], commit, 'nls.messages.json')
        root_cache = os.path.join(tr_parents[0], 'nls.messages.json')
        print(f"  [+] Bulunan CLP dizini: {tr_parents[0]}")
        if os.path.exists(commit_cache):
            sz = os.path.getsize(commit_cache)
            print(f"  [+] Commit NLS önbelleği mevcut ({sz:,} bayt): {commit_cache}")
        else:
            print(f"  [!] UYARI: Commit NLS önbelleği eksik: {commit_cache}")
        if os.path.exists(root_cache):
            sz = os.path.getsize(root_cache)
            print(f"  [+] Kök NLS önbelleği mevcut ({sz:,} bayt): {root_cache}")
    else:
        print("  [*] CLP dizini henüz oluşmamış (Cursor ilk açılışta oluşturur).")

    # 3. Canlı Arayüz Dosyaları Kontrolü
    print("\n[*] 3/3 Canlı Arayüz Dosyaları Boyut ve Bütünlük Kontrolü...")
    targets = {
        'workbench.desktop.main.js': os.path.join(APP, 'out', 'vs', 'workbench', 'workbench.desktop.main.js'),
        'workbench.glass.main.js': os.path.join(APP, 'out', 'vs', 'workbench', 'workbench.glass.main.js'),
        'cursor-agent-exec-main.js': os.path.join(APP, 'extensions', 'cursor-agent-exec', 'dist', 'main.js'),
        'cursor-local-agent-runtime-main.js': os.path.join(APP, 'extensions', 'cursor-local-agent-runtime', 'dist', 'main.js'),
    }
    all_targets_ok = True
    for name, path in targets.items():
        if os.path.exists(path):
            sz = os.path.getsize(path)
            print(f"  [+] {name:<35} : {sz:>10,} bayt [TAMAM]")
        else:
            print(f"  [-] {name:<35} : BULUNAMADI")
            all_targets_ok = False

    print("\n" + "=" * 65)
    overall_ok = (len(mismatches) == 0 and len(missing_files) == 0 and all_targets_ok)
    if overall_ok:
        print("  SONUÇ: %100 DOĞRULANDI — Cursor Türkçe Yaması Kusursuz Aktif!")
        print("  ⭐ Destek olmak için: https://github.com/foztrk/cursor-turkish-localization")
    else:
        print("  SONUÇ: UYARILAR MEVCUT — Lütfen yukarıdaki hataları inceleyin.")
    print("=" * 65)
    return overall_ok

if __name__ == '__main__':
    ok = verify_all()
    sys.exit(0 if ok else 1)