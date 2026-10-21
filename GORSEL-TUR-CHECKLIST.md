# Cursor TR — Görsel Checklist (güncel)

- **Tarih:** 2026-09-25 (Europe/Istanbul, UTC+3)
- **Cursor:** 3.22.7 / `37076c6c3f9e253c0fa2305197e45befd13a2260` (kutu + Work-PC, son stable)
- **Repo:** `a62fe3b` + Work-PC `ceviri-son-hali` (Work-PC yamalı dosyaları kutuya **bayt-bayt aynı** kuruldu) → `verify_all` **%100 DOĞRULANDI**
- **Ortam:** Linux box, `--locale=tr`, CLP `*.tr` önbelleği mevcut (NLS uyarısı yok)
- **Kapsam:** Agents, IDE menü, Cursor Settings, VS Code Settings, Explorer, Komut paleti
- **Not:** Yalnızca tespit. Marka/proper name ve üçüncü parti uzantı metinleri öncelikli değil.

## 2026-09-25 — Cursor 3.22.7 turu (Linux box, Work-PC yaması birebir)

- [x] Cursor 3.21.18 → 3.22.7 (apt stable), repo `331eb6d` → `a62fe3b`
- [x] Work-PC `ceviri-son-hali` kutuya kopyalandı; canlı `workbench.desktop.main.js` / `workbench.glass.main.js` / `nls.messages.json` Work-PC ile aynı SHA-256
- [x] `product.json` checksum'ları Linux için yeniden hesaplandı (6/6, "bozuk kurulum" uyarısı yok)
- [x] CLP/NLS önbelleği (`~/.config/Cursor/clp/*.tr` kök + `37076c6c…`) oluştu ve yamalandı
- [x] 8 overlay imzası canlıda mevcut (`CURSOR_TR_UI_PATCH_V5`, `IDE_SURFACE_V1/V2`, `MENU_GAPS_V1`, `SETTINGS_V1/V2`, `SMALL_DIALOGS_V1`, `UI_EXPANSION_V1`)

### A) Yalnızca Linux — sözlükte yok
- [ ] Agents konum seçici: `This Computer` (Windows'taki `This PC` zaten → "Bu Bilgisayar")
- [ ] Agents konum seçici arama: `Search This Computer...` / `Search This Computer…`
- [ ] Öneri: macOS karşılıklarını da ekle (`This Mac`, `Search This Mac…`)

### B) İki makinede de çevrilmemiş — sözlük girdisi yok
- [ ] Explorer: `Opening a folder will close all currently open editors. To keep them open, ... instead.` (şu an "bir klasör ekle" ile karışık)
- [ ] Agents filtre menüsü: `Repository`, `Filters`, `Source`

### C) Sözlükte var ama Linux'ta çalışma anında uygulanmıyor (bekleme/yeniden açma sonrası hâlâ İngilizce)
- [ ] Plan ve Kullanım: `Resets Oct 23, 2026`
- [ ] VS Code Settings başlıkları: `Files: Auto Save`, `Editor: Font Size`, `Editor: Font Family`, `Editor: Tab Size`
- [ ] VS Code Settings başlıkları: `Editor: Cursor Style`, `Editor: Multi Cursor Modifier`, karışık `Editor: Boşluk Karakterlerini Göster`
- [ ] Komut paleti: karışık `Aç Agent as Pane`, `Accept pending agent pane action`, karışık `Search: Focus on Ara View`
- [ ] Windows'ta bu metinlerin Türkçe görünüp görünmediği doğrulanacak

### D) Komut paleti — çift satırlar
- [ ] `Cursor: Güncellemeleri Denetle...` ile birlikte `Cursor: Check for Updates...` da görünüyor
- [ ] `Güncellemeyi Dene` ile birlikte `Attempt Update` da görünüyor
- Not: İngilizce satırlar büyük olasılıkla VS Code'un İngilizce takma adı (alias) araması; Yardım menüsü Türkçe (OK)

### E) Betik hatası — `patch_menu_gaps.py`
- [ ] ~2003-2007. satırlar: tekrar-ekleme kontrolü `'Agent skills help you customize Cursor for your workflows'` arıyor, ama eklenen satır `/^(?:Agent|Ajan) skills help you customize…/` regex'ini içeriyor → her `apply_all` çalıştırmasında satır yeniden ekleniyor (çalıştırma başına +253 bayt, `ceviri-son-hali` arşivine de taşınıyor)
- [ ] Düzeltme: kontrolü eklenen regex metnine göre yap

### F) 3.22.7 apply — atlanan hedefler (81 × `[ATLANDI]`, 77 × `[OK]`)
- [ ] Remote Machine / mobil denetim / QR kod metinleri
- [ ] Depo arama / `No repos` / `Create repo` akışı
- [ ] MCP ipucu (karışık "MCP Yapılandır MCPs in your Cursor…")
- [ ] Güncelleme bildirimi: `Install Now`, `Restart to Update`, `Attempt Update`
- [ ] `context used` (durum çubuğu / ipucu / özet)
- [ ] `Origin Notifications` etiket + açıklama
- [ ] Steer: `Steer / Send Now`, Desk `Steer from Phone`, `Steer without interrupting`, Observer Steer
- [ ] `patch_hook_tip.py`: 5 hedefin 5'i de bulunamadı
- Not: Bunların birçoğu bu testte arayüzde görünmedi; 3.22.7'de kaldırılmış/yeniden adlandırılmış olabilir

### G) NLS — dil paketi sürüm farkı
- [ ] Kutu Türkçe dil paketi 1.131, Work-PC 1.128; 8 NLS metni farklıydı (tünel mesajları / ayar açıklamaları). Şu an kutuya Work-PC NLS'si kurulu; sonraki `apply_all` kutu dil paketiyle yeniden üretir

## Öncelik A — Bu turda doğrulanan (Türkçe) — 2026-09-24

### Agents Window
- [x] Yer tutucu: "Soru sorun"
- [x] Öneri kartları / `/create-rule` metinleri Türkçe
- [x] Yan menü: Yeni Sohbet, Otomasyonlar, Özelleştir…

### Explorer / Kaynak denetimi
- [x] Git boş durum paragrafı ve düğmeler Türkçe (Klasör Aç, Depoyu Klonla…)
- [ ] Explorer uyarısı hâlâ karışık: "Opening a folder will close all currently open editors. To keep them open, bir klasör ekle instead." → 2026-09-25 **B** maddesine taşındı

### Cursor Settings
- [x] Yan çubuk Türkçe
- [x] Pro'ya Yükselt, Dahil Edilen Kullanım, Başlık Çubuğu, Durum Çubuğu
- [ ] "Resets Oct 23, 2026" hâlâ İngilizce (tarih cümlesi) → 2026-09-25 **C** maddesine taşındı (sözlükte var, çalışma anında uygulanmıyor)

### IDE menü / Composer / Terminal / Extensions arama
- [x] Üst menü: Dosya, Düzenle, Seçim, Görünüm, Git, Çalıştır, Terminal, Yardım
- [x] Panel sekmeleri: Sorunlar, Çıktı, Hata Ayıklama Konsolu, Terminal, Bağlantı Noktaları
- [x] Extensions: "Markette Uzantı Ara", "Yükle"

## Öncelik A — Hâlâ İngilizce / karışık (kullanıcıya dönük) — 2026-09-24

1. **Cursor Settings → Plan ve Kullanım:** `Resets Oct 23, 2026` → 2026-09-25 **C**
2. **VS Code Settings başlıkları** (kategoriler Türkçe, başlıklar İngilizce) → 2026-09-25 **C**:
   - `Files: Auto Save`
   - `Editor: Font Size`
   - `Editor: Font Family`
   - `Editor: Tab Size`
   - (önceki turdakilerle aynı aile: Cursor Style, Multi Cursor Modifier, Insert Spaces, Detect Indentation — bu turda tekrar doğrulanmadı ama aynı yüzey)
3. **Explorer boş durum:** `Opening a folder will close all currently open editors. To keep them open, bir klasör ekle instead.` → 2026-09-25 **B**

## Öncelik B — Bilinçli / kapsam dışı

- Marketplace üçüncü parti uzantı ad/açıklamaları (Remote - SSH, GitLens vb.)
- MCP / Git / URL / model adları
- Harici Docs sitesi
- Komut paleti NDJSON / deeplink (düşük öncelik; bu turda yeniden açılmadı)
- [x] ~~Overlay notu: canlı `workbench.glass.main.js` içinde yalnızca `CURSOR_TR_MENU_GAPS_V1` imzası var~~ — 2026-09-25: 3.22.7'de 8 overlay imzasının tamamı canlıda ve Work-PC arşivinde mevcut (çözüldü)

## Önceki denetime göre düzelenler

Agent placeholder ve kartlar, plan etiketleri, Title/Status Bar, Git boş paragraf, Terminal sekmeleri, Extensions arama/Yükle artık Türkçe.
2026-09-25: NLS/CLP önbelleği uyarısı giderildi; kutu ve Work-PC canlı yama dosyaları birebir aynı; Agents Window (yan menü, yer tutucu, öneri kartları) 3.22.7'de Türkçe — tek istisna `This Computer` (A).


## 2026-10-20 — Cursor 3.24.18 Turu ve Son Kazanımlar

- [x] **Cursor 3.24.18 (Commit: `be4c9e5350d77747b42cd467cbd3370a753d4640`):** Tam uyumluluk ve `[OK_VERIFIED]` canlı kurulum.
- [x] **Windows Sistem Tepsisi (Tray Menu - `patch_main_process.py`):**
  - `Clear All Notifications` ➔ `Tüm Bildirimleri Temizle`
  - `Open Cursor` ➔ `Cursor'ı Aç`
  - `Settings` ➔ `Ayarlar`
  - `Quit` ➔ `Çıkış`
  - `No recent agents` ➔ `Son Kullanılan Ajan Yok`
  - `Unread` ➔ `Okunmamış`
  - `Agent ${i+1}` ➔ `Ajan ${i+1}`
  - `${e} more unread` ➔ `${e} okunmamış daha`
  - `New Agent` (varsayılan) ➔ `Yeni Ajan`
- [x] **Model Araç ve Durum Çıktıları (`patch_tool_labels.py`):**
  - 68 araç çağrısının `{loading, completed, error}` sözlüğü `===` mantık kontrolleri bozulmadan Başlık Düzeni (Title Case) standardıyla Türkçeleştirildi (`Çalıştırılıyor`/`Çalıştırıldı`, `Okunuyor`/`Okundu`, `Düzenleniyor`/`Düzenlendi`, `Siliniyor`/`Silindi`, `Dosyalar Aranıyor`/`Dosyalar Arandı`, `Plan Hazırlanıyor`/`Plan Hazırlandı`, vb.).
  - Düşünme etiketleri: `Thinking`/`Düşünülüyor`, `Thought`/`Düşündü`, `Planning next moves`/`Sonraki Adımlar Planlanıyor`, `Wrapping up`/`Toparlanıyor`, `Wait skipped`/`Bekleme Atlandı`, `Generating`/`Üretiliyor`.
  - Yapılacaklar listesi durumları: `to-do list` ➔ `görev listesi`, `Updating` ➔ `Güncelleniyor`, `Cleared` ➔ `Temizlendi`, `Checked` ➔ `Kontrol Edildi`.
- [x] **Sesli Dikte ve Mikrofon Koruması (`patch_fixes.py`):**
  - `Click or hold [Ctrl] [M] to dictate` ➔ `Dikte etmek için tıklayın veya [Ctrl] [M] tuşuna basılı tutun` (React `<kbd>` JSX yapısı ve kısayol değişkeni bozulmadan).
  - `Voice Input (${shortcut})` ➔ `Sesli Giriş (${kısayol})`, `Sesli Girişi Başlat`.
- [x] **Başlık Düzeni (Title Case) Kuralı:**
  - Tüm menü, buton ve kısa eylem etiketleri (`Kuyruktan Çıkar`, `Kuyruğu Kapat`, `Dosya Ekle`, `Bu Makinede Çalıştır`, `Cursor Sunucularında Çalıştır`, `Sesli Sohbet Başlat`) AI çevirisi yapaylığından arındırılarak Title Case yapıldı.
- [x] **Electron Ana Süreç Entegrasyonu:**
  - `out/main.js` dosyası `apply_all.py` orkestrasyonuna eklendi; harici link onay diyalogları (`Harici Bağlantıyı Aç`, `İptal`/`Aç`) ana süreçte çözüldü.
