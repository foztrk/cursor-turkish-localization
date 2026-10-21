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

DEFAULT_MOLTEN_APP = r"C:\Program Files\cursor\resources\app"

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
    ("Search This PC...", "Bu bilgisayarda ara..."),
    ("Search skills, context, chats", "Becerilerde, bağlamda, sohbetlerde ara"),
    ("Search custom modes", "Özel modlarda ara"),
]


MOLTEN_REGEX_REPS = [
    # Mikrofon aygıt etiketleri: "Default - ..." -> "Varsayılan - ...", "Communications - ..." -> "İletişim - ..."
    (re.compile(r'label:([a-zA-Z0-9_$]+)\.label\|\|`Microphone \$\{([a-zA-Z0-9_$]+)\+1\}`'),
     r'label:(\1.label?\1.label.replace(/^Default - /,"Varsayılan - ").replace(/^Communications - /,"İletişim - "):`Mikrofon ${\2+1}`)'),
]


def patch_molten_dir(molten_dir):
    if not os.path.exists(molten_dir):
        return 0, 0
    total_files = 0
    total_mods = 0
    for fname in os.listdir(molten_dir):
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
