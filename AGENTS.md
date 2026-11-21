# AGENTS.md — Cursor Türkçe Yerelleştirme (Codex & AI Ajan Talimatnamesi)

Bu depo (`C:\Users\Work-D\cursor-turkish-localization`), Cursor güncellemelerinden sonra **ekran görüntüsü beklemeye gerek kalmadan** tüm gömülü dosyaları (`workbench.glass.main.js`, `workbench.desktop.main.js`, `nls.messages.json`, `out/main.js` ve `304` `molten/dist/renderer/assets/*.js`) tarayıp Türkçeleştiren ve `verify_patch.py` doğrulama kapısından geçiren sistemdir.

Kullanıcı **"talimatnameyi uygula"** veya **"güncelleme geldi"** dediğinde `.agents/skills/cursor-turkce-ekibi/SKILL.md` ve `C:\Users\Work-D\Documents\Obsidian-Beyin\Cursor-Türkçe-Yama-İşlem-Günlüğü.md` içindeki **3 aşamalı protokolü** eksiksiz uygula:

1. **Aşama 1 — `EN_WORD`-Bağımsız Tam Gömülü Dosya Taraması, Template Literal & Prop-Bağımsız Ortak Sözlük:**
   - `python -X utf8 apply_all.py --force` çalıştır (`patch_glass_nls.py`, `patch_tool_labels.py`, `patch_molten.py` ortak sözlük motoru `\u2019`/`\u2026`/`\u2014`/`\u00B7` Unicode kaçış varyantları dahil `8.490+` sabit çeviriyi ve `tpl-tm.json` içindeki `1.355+` `${...}` şablonunu hem tüm `*Label/*Title/*Description` prop'ları hem `=`/`?`/`:` değişken atamaları hem de template literaller üzerinde değişken adından bağımsız uygular).
   - `YENI-EKLENENLER.txt` ve `YENI-HOVER-ETIKETLER.txt` içinde kalan yeni UI/durum/computed prop/değişken ataması/şablon (`${...}`) metinlerini `cursor-ui-tm.json`, `tpl-tm.json`, `nls-tm.json`, `patch_fixes.py`, `patch_molten.py`, `patch_glass_nls.py` veya `patch_tool_labels.py` içine ekle (`.label === "..."` kod mantığı karşılaştırmaları olan `PROTECTED_PROP_LOGIC_PAIRS` çiftlerini koru).
2. **Aşama 2 — Zorunlu Deterministik Doğrulama Kapısı (`verify_patch.py`):**
   - `python -X utf8 verify_patch.py` çıktısı `0` hata (`PASS`) vermelidir (`14.600+` NLS `{0}` yer tutucu kontrolü, SHA-256 eşleşmesi, CLP önbellek eşleşmesi, `glass` ve `molten` regresyon kontrolleri).
3. **Aşama 3 — Bağımsız Denetim & Senkronizasyon:**
   - `git diff` ve kalan adayları bağımsız denetle; `Cursor-Türkçe-Yama-İşlem-Günlüğü.md` ve `🧭 ŞU AN NEREDEYİZ.md` dosyalarını güncelle; `origin/main`'e commit & push yap.
