# -*- coding: utf-8 -*-
"""
patch_molten.py: Cursor'in modern Vite tabanli Molten arayuz varliklarini (renderer/assets)
Turkcelestirir.
- Hakkinda Modali: "Copy version info" -> "Sürüm Bilgisini Kopyala", "Version " -> "Sürüm "
- Ses Ayarlari: "Voice" -> "Ses", hiz, dil ve mikrofon aciklamalari
- Mikrofon Menusu: "System Default" -> "Sistem Varsayılanı"
- Dil Menusu: "Auto-detect" -> "Otomatik Algıla"
"""
import io
import os
import sys
import re
import glob
import json

DEFAULT_MOLTEN_APP = r"C:\Program Files\cursor\resources\app"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MOLTEN_REPLACEMENTS = [
    ("`Copy version info`", "`Sürüm Bilgisini Kopyala`"),
    ("Copy version info", "Sürüm Bilgisini Kopyala"),
    ("[`Version `,", "[`Sürüm `,"),
    ("label:`System Default`", "label:`Sistem Varsayılanı`"),
    ("id:`voice`,label:`Voice`", "id:`voice`,label:`Ses`"),
    ("label:`Speed`,description:`How quickly the voice speaks in voice chats.`",
     "label:`Hız`,description:`Sesin sesli sohbetlerde konuşma hızı.`"),
    ("label:`Language`,description:`Language used in voice chats.`",
     "label:`Dil`,description:`Sesli sohbetlerde kullanılan dil.`"),
    ("label:`Microphone`,description:`Microphone used in voice chats.`",
     "label:`Mikrofon`,description:`Sesli sohbetlerde kullanılan mikrofon.`"),
    ("auto:`Auto-detect`", "auto:`Otomatik Algıla`"),
    ("en:`English`", "en:`İngilizce`"),
    ("tr:`Turkish`", "tr:`Türkçe`"),
    ("?`This PC`:`This Computer`", "?`Bu Bilgisayar`:`Bu Bilgisayar`"),
    ("?`This PC`:e.includes(`Mac`)?`This Mac`:`This Computer`", "?`Bu Bilgisayar`:e.includes(`Mac`)?`Bu Mac`:`Bu Bilgisayar`"),
    ("??`Select Environment`", "??`Ortam Seç`"),
    ("`No Repo`", "`Depo Yok`"),
    ("=`No Repository`", "=`Depo Yok`"),
    ("=`Start from scratch`", "=`Sıfırdan başla`"),
    ("children:`No recent agents`", "children:`Son Kullanılan Ajan Yok`"),
    ("children:`No recent agents yet.`", "children:`Henüz son kullanılan ajan yok.`"),
    ("Search This PC...", "Bu Bilgisayarda Ara..."),
    ("Search skills, context, chats", "Becerilerde, bağlamda, sohbetlerde ara"),
    ("Search custom modes", "Özel modlarda ara"),
]


MOLTEN_REGEX_REPS = [
    # Mikrofon aygıt etiketleri: "Default - ..." -> "Varsayılan - ...", "Communications - ..." -> "İletişim - ..."
    (re.compile(r'label:([a-zA-Z0-9_$]+)\.label\|\|`Microphone \$\{([a-zA-Z0-9_$]+)\+1\}`'),
     r'label:(\1.label?\1.label.replace(/^Default - /,"Varsayılan - ").replace(/^Communications - /,"İletişim - "):`Mikrofon ${\2+1}`)'),
]


def _load_backtick_prop_maps():
    bt_maps = []
    tr2_pattern = os.path.join(BASE_DIR, "tr2", "m*.json")
    for f in sorted(glob.glob(tr2_pattern)):
        try:
            data = json.load(io.open(f, encoding="utf-8"))
            for k, v in data.items():
                prop, old = k.split("\t", 1)
                if any(c in old or c in v for c in ["`", "$", "\\", "\n", "\r"]):
                    continue
                p_str = '"aria-label"' if prop == "aria-label" else prop
                bt_maps.append((f"{p_str}:`{old}`", f"{p_str}:`{v}`"))
        except Exception:
            pass
    return bt_maps


def patch_molten_dir(molten_dir):
    if not os.path.exists(molten_dir):
        return 0, 0
    bt_maps = _load_backtick_prop_maps()
    total_files = 0
    total_mods = 0
    for fname in sorted(os.listdir(molten_dir)):
        if not fname.endswith(".js"):
            continue
        p = os.path.join(molten_dir, fname)
        try:
            with io.open(p, "r", encoding="utf-8") as f:
                content = f.read()
            mods = 0
            for pat, rep in MOLTEN_REGEX_REPS:
                content, c = pat.subn(rep, content)
                mods += c
            for old_s, new_s in MOLTEN_REPLACEMENTS:
                c = content.count(old_s)
                if c:
                    content = content.replace(old_s, new_s)
                    mods += c
            for old_s, new_s in bt_maps:
                c = content.count(old_s)
                if c:
                    content = content.replace(old_s, new_s)
                    mods += c
            if mods > 0:
                with io.open(p, "w", encoding="utf-8", newline="") as f:
                    f.write(content)
                total_files += 1
                total_mods += mods
                print(f"[molten/{fname}] {mods} metin Turkcelestirildi.")
        except Exception as e:
            print(f"[molten/{fname}] Hata: {e}")
    return total_files, total_mods


def main():
    target_base = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MOLTEN_APP
    molten_assets = os.path.join(target_base, "molten", "dist", "renderer", "assets")
    if not os.path.isdir(molten_assets):
        print(f"Molten varlik dizini bulunamadi: {molten_assets}")
        return
    files, mods = patch_molten_dir(molten_assets)
    print(f"Molten yamalama tamamlandi: {files} dosyada {mods} degisim uygulandi.")


if __name__ == "__main__":
    main()
