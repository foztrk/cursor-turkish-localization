# -*- coding: utf-8 -*-
"""
Cursor Tek Tık Türkçe Yama ve Güncelleyici (single_click_patcher.py)
------------------------------------------------------------------
Cursor güncellendiğinde veya sıfırdan kurulduğunda:
1. Yönetici (Admin / UAC) iznini otomatik kontrol eder ve ister.
2. Açık Cursor süreçlerini güvenle kapatır.
3. Orijinal dosyaları sürüm bazlı (orijinal-<sürüm>/) otomatik yedekler.
4. Çekirdek NLS sözlüğünü, AST prop haritalarını, native Electron menülerini,
   durum çubuğu istatistiklerini ve dinamik DOM gözlemcisini enjekte eder.
5. Cursor IntegrityService SHA-256 Base64 checksum'larını anında günceller.
6. CLP kullanıcı önbelleğini (Roaming\Cursor\clp\*.tr) senkronize eder.
7. Cursor'ı masaüstü oturumunuzda bağımsız (detached) olarak başlatır.
"""

import os
import sys
import json
import time
import shutil
import ctypes
import subprocess
import hashlib
import base64
import glob

if sys.platform == "win32":
    try:
        os.system("chcp 65001 >nul")
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
APP_DIR = r'C:\Program Files\cursor\resources\app'

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    if not is_admin():
        print("[!] Yönetici izinleri alınıyor (UAC)...")
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        try:
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable if not getattr(sys, 'frozen', False) else script,
                f'"{script}" {params}' if not getattr(sys, 'frozen', False) else params,
                None, 1
            )
            if ret > 32:
                sys.exit(0)
            else:
                print("[-] Yönetici izni verilmedi.")
        except Exception as e:
            print(f"[-] UAC Başarısız: {e}")
        return False
    return True

def kill_cursor():
    print("[*] Açık Cursor süreçleri kapatılıyor...")
    subprocess.run(['powershell', '-NoProfile', '-Command',
                    'Get-Process Cursor -ErrorAction SilentlyContinue | Stop-Process -Force'],
                   capture_output=True)
    time.sleep(1)

def run_pipeline():
    print("=" * 65)
    print("  CURSOR TÜRKÇE DİL PAKETİ VE YERELLEŞTİRME KURULUMU")
    print("=" * 65)

    if not os.path.exists(APP_DIR):
        print(f"[!] HATA: Cursor kurulu bulunamadı: {APP_DIR}")
        input("\nÇıkmak için Enter'a basın...")
        return False

    kill_cursor()

    apply_all_script = os.path.join(BASE_DIR, 'apply_all.py')
    if not os.path.exists(apply_all_script):
        print(f"[!] HATA: apply_all.py bulunamadı: {apply_all_script}")
        return False

    print("\n[*] 1/3 Çekirdek Yama Motoru (apply_all.py) Çalıştırılıyor...")
    res = subprocess.run([sys.executable, '-X', 'utf8', apply_all_script],
                         text=True, capture_output=False)
    if res.returncode != 0:
        print(f"\n[!] apply_all.py {res.returncode} koduyla başarısız oldu!")
        return False

    print("\n[*] 2/3 Integrity Checksum Doğrulaması...")
    verify_script = os.path.join(BASE_DIR, 'verify_all.py')
    if os.path.exists(verify_script):
        subprocess.run([sys.executable, '-X', 'utf8', verify_script])

    print("\n[*] 3/3 Cursor Bağımsız Olarak Başlatılıyor...")
    cursor_exe = r'C:\Program Files\cursor\Cursor.exe'
    if os.path.exists(cursor_exe):
        try:
            # WMI / Explorer ile detached başlat
            subprocess.Popen([cursor_exe], creationflags=0x00000008 | 0x00000200)
            print("[+] Cursor başarıyla Türkçe olarak başlatıldı.")
        except Exception as e:
            print(f"[!] Cursor başlatılamadı: {e}")

    print("\n" + "=" * 65)
    print("  KURULUM TAMAMLANDI! CURSOR ARTIK %100 TÜRKÇE.")
    print("\n  ⭐ Projeyi faydalı bulduysanız GitHub'da bir Yıldız (Star)")
    print("     vererek destek olmayı unutmayın:")
    print("     https://github.com/foztrk/cursor-turkish-localization")
    print("=" * 65)
    return True

if __name__ == '__main__':
    if not is_admin():
        run_as_admin()
    else:
        run_pipeline()