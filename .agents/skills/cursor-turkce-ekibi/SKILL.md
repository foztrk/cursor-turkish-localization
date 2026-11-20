---
name: cursor-turkce-ekibi
description: >-
  Cursor güncellemelerinden sonra Türkçe yamayı uygulayan, Ortak Sözlük Köprüsü
  (NLS + Bundle + Molten) ile senkronize eden, deterministik doğrulama
  kapısından (verify_patch.py) geçiren ve bağımsız denetçi alt ajanla
  (research) kontrol eden 3 aşamalı iş akışı. Kullanıcı "güncelleme geldi",
  "cursor güncellendi" veya ekran görüntüsü ile kalan İngilizce metin
  bildirdiğinde bu skill'i oku ve uygula.
---

# Cursor Türkçe Yama & Bağımsız Denetim İş Akışı

Çalışma dizini: `C:\Users\Work-D\cursor-turkish-localization`
Her Cursor güncellemesinde veya görsel geri bildirimde aşağıdaki **3 aşamalı protokolü** sırasıyla çalıştır. Aşama 2 ve Aşama 3 `PASS` vermeden GitHub push veya Obsidian güncellemesi yapma.

## Aşama 1 — Yamalayıcı (`patcher`)
1. Kurulu sürümü ve commit'i tespit et (`C:\Program Files\cursor\resources\app\package.json` ve `product.json`).
2. Yeni metin veya görsel geri bildirim varsa:
   - **NLS (`O(index, null)`)** anahtarlarını `C:\Program Files\cursor\resources\app\out\nls.keys.json` üzerinden bulup `patch_glass_nls.py` (`GLASS_NLS_MAP`) veya `nls-tm.json` içine ekle.
   - **Bundle (`workbench.glass.main.js` / `workbench.desktop.main.js`)** prop ve minified değişken atamalarını `patch_fixes.py` içine ekle (`===` kod mantığı anahtarlarına dokunma; regex'lerde `[^\]\[]+?` kullanarak sınır taşmasını önle).
   - **Molten (`molten/dist/renderer/assets/*.js`)** backtick sabitlerini `patch_molten.py` içine ekle (`patch_molten.py` içindeki `_load_unified_en_tr_dict()` tüm sözlüklerdeki görünür UI prop'larını Molten'e otomatik miras alır).
   - **Tray (`out/main.js`)** veya **Eklenti (`~/.cursor/extensions/`)** metinlerini `patch_main_process.py` / `patch_extensions.py` içine ekle.
3. `python -X utf8 -m py_compile apply_all.py patch_fixes.py patch_molten.py patch_glass_nls.py verify_patch.py` ile sözdizimini doğrula.
4. `python -X utf8 apply_all.py --force` komutunu çalıştır (`apply_all.py` sonunda `verify_patch.py` otomatik koşar).

## Aşama 2 — Deterministik Doğrulama Kapısı (`verify_patch.py`)
1. `python -X utf8 verify_patch.py` komutunun çıktısını kontrol et (`0` token, `~2` saniye).
2. Bu kapı şu 4 katmanı otomatik doğrular:
   - `deploy_result.txt == OK_VERIFIED` ve canlı `Program Files` SHA-256 eşleşmesi.
   - `nls.messages.json` ve `%APPDATA%\Cursor\clp\*.tr\<commit>\nls.messages.json` üzerinde `GLASS_NLS_MAP` (`Ortamlar`, `Makineler`, `Bulut`, `Havuzlar`, `Depolar`, `Çevrimdışı` vb.) eşitliği ve tüm `14.600+` NLS mesajında `{0}` yer tutucu uyuşmazlığı `== 0` kontrolü.
   - Canlı `workbench.glass.main.js` üzerinde greedy-regex regresyonu (`children:["%",v,y]` = `0`) ve zorunlu Türkçe kalıplar.
   - Canlı `molten/dist/renderer/assets/*.js` ve `out/main.js` doğrulaması.
3. `verify_patch.py` hata (`exit code 1`) verirse Aşama 1'e dönüp hatayı düzelt.

## Aşama 3 — Bağımsız Denetçi Alt Ajan (`invoke_subagent` -> `research`)
1. `verify_patch.py` `PASS` verdikten sonra `invoke_subagent(TypeName="research", Role="Bağımsız Yama Denetçisi", ...)` başlat.
2. Denetçi alt ajanın görevi:
   - `YENI-EKLENENLER.txt` ve `YENI-HOVER-ETIKETLER.txt` dosyalarını okumak,
   - Son yapılan `git diff` değişikliklerinde yanlışlıkla çevrilmiş bir kod mantığı anahtarı (`=== "..."`, route, ID), bozuk yer tutucu (`{0}`, `${x}`) veya kaçan bariz UI metni olup olmadığını bağımsız gözle denetlemek.
3. Denetçi `PASS` verdikten sonra:
   - `C:\Users\Work-D\Documents\Obsidian-Beyin\Cursor-Türkçe-Yama-İşlem-Günlüğü.md` ve `🧭 ŞU AN NEREDEYİZ.md` dosyalarını güncelle.
   - `git add`, `git commit` ve `git push origin main` ile GitHub'a gönder.
