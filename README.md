# 🇹🇷 Cursor Desktop Türkçe Dil Paketi ve Yerelleştirme Altyapısı
### (Community Turkish Localization & Engineering Infrastructure for Cursor Desktop)

<div align="center">

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tested On Cursor](https://img.shields.io/badge/Cursor%20Version-v3.24.18-purple.svg)](https://cursor.com)
[![Rules Translated](https://img.shields.io/badge/Translated%20Rules%20%26%20Props-4%2C620%2B-brightgreen.svg)](nls-tm.json)
[![Integrity Verified](https://img.shields.io/badge/IntegrityService-100%25%20Verified-blue.svg)](#-mimar%C3%AE-ve-b%C3%BCt%C3%BCnl%C3%BCk-integrityservice)
[![GitHub Stars](https://img.shields.io/github/stars/foztrk/cursor-turkish-localization?style=social)](https://github.com/foztrk/cursor-turkish-localization)
[![Maintenance Commitment](https://img.shields.io/badge/Maintenance-Day--0%20SLA-orange.svg)](#-open-letter--proposal-to-the-cursor--anysphere-team)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Cross--Platform-lightgrey.svg)](#-kurulum-installation)

[📥 **Tek Tıkla İndir (Releases)**](https://github.com/foztrk/cursor-turkish-localization/releases/latest) • 
[⭐ **Yıldız Ver (Star)**](https://github.com/foztrk/cursor-turkish-localization) • 
[💬 **Geri Bildirim / Hata Bildir**](https://github.com/foztrk/cursor-turkish-localization/issues) • 
[🏛️ **Proposal for Anysphere**](#-open-letter--proposal-to-the-cursor--anysphere-team)

</div>

---

> [!TIP]
> 🌟 **Bu projeyi faydalı bulduysanız ve Cursor'ı Türkçe kullanmaktan memnunsanız, sağ üst köşeden projeye bir Yıldız (Star ⭐) vererek destek olabilirsiniz!**  
> Yıldızlarınız projenin görünürlüğünü artırır ve Anysphere (Cursor) ekibinin Türkçe dil desteğini doğrudan çekirdeğe (native) eklemesini hızlandırır.

Dünyanın lider yapay zekâ destekli kod editörü olan **Cursor Desktop** için geliştirilmiş **en kapsamlı, modern ve mühendislik tabanlı Türkçe yerelleştirme projesidir**.

Yalnızca statik metinleri değil; Cursor'ın tescilli **Glass UI (React)** bileşenlerini, AST prop katmanlarını, yerel Windows menü çubuğunu, canlı DOM mutasyonlarını, Electron Ana Sürecini (`out/main.js` Sistem Tepsisi) ve **IntegrityService SHA-256 bütünlük kontrolünü** kapsayan tam teşekküllü bir yerelleştirme altyapısı sunar.

---

## 📢 Open Letter & Proposal to the Cursor / Anysphere Team

> **Dear Michael Truell, Sualeh Asif, Aman Sanger, Arvid Lunnemark, and the Anysphere Team ([@getcursor](https://github.com/getcursor)),**

First and foremost, congratulations on building **Cursor**! It is indisputably the gold standard of agentic coding environments and has completely transformed how our team and developer community write software every day.

### Why We Built This Project
Turkey has one of the fastest-growing software developer ecosystems in Europe and the Middle East, with **over 500,000 professional developers, researchers, and computer science students**. 

However, because Cursor combines standard VS Code core with proprietary, cutting-edge AI surfaces (**Glass UI**, **Composer**, **Agent Runtime**), standard VS Code language packs leave 60%+ of Cursor's AI interface untranslated or broken.

To solve this, we engineered this **end-to-end localization infrastructure**:
* **4,620+ verified rules & AST mappings** covering both VS Code core NLS and proprietary Glass UI.
* Complete resolution of the **CLP Cache** hierarchy and **IntegrityService SHA-256 Base64** hash verification (Zero *"Installation is corrupt"* errors).
* Clean separation of code terminology (e.g. `Composer`, `Diff`, `Git`, `Commit` remain natural to developers, while UI actions, menus, and onboarding are natively localized).

### Our Proposal to Anysphere / Cursor
1. **Official / Native Turkish Language Integration:**  
   We are ready to contribute our dictionary (`nls-tm.json`, `tr2/`, and UI maps) under MIT directly to the Cursor codebase or as an official language extension for Cursor.
2. **Day-0 Maintenance SLA Commitment:**  
   As active Cursor power users and contributors, **we commit to maintaining 100% Turkish compatibility for every new release of Cursor within hours of release (Day-0 SLA)**. Whenever your team pushes an update, we diff newly added keys, inspect bundles, and deploy validated translations.
3. **Contract / Dedicated Localization & Community Role:**  
   We are eager to collaborate with Anysphere either as a **Localization & Developer Experience Engineer**, **Contractor**, or **Turkish Community Lead**. We can ensure Turkish developers receive native support, seamless onboarding, and continuous documentation for Cursor.

📩 **Let's Connect:**
- **Core Team Inquiry Form:** [Open an Official Inquiry](https://github.com/foztrk/cursor-turkish-localization/issues/new?template=official_inquiry.md)
- **Direct Email:** `abdurrahmanavci@gmail.com`
- **GitHub:** [@foztrk](https://github.com/foztrk)

---

## 🌟 Neler İçerir? (Özellikler)

1. **Model Araç ve Durum Çıktıları (Agent Transcripts & Tool Calls):**
   - Modelin canlı yazışma esnasında ekrana bastığı 68 araç eylemi (`Çalıştırılıyor`/`Çalıştırıldı`, `Okunuyor`/`Okundu`, `Düzenleniyor`/`Düzenlendi`, `Siliniyor`/`Silindi`, `Dosyalar Aranıyor`/`Dosyalar Arandı`, `Plan Hazırlanıyor`, vb.).
   - Modelin düşünme ve planlama durumları (`Düşünülüyor`/`Düşündü`, `Sonraki Adımlar Planlanıyor`, `Toparlanıyor`, `Üretiliyor`, `Bekleme Atlandı`).
   - Tüm menü, buton ve kısa eylem etiketlerinde **Başlık Düzeni (Title Case)** standardı.
2. **Windows Sistem Tepsisi & Dış Bağlantılar (Tray Menu & Main Process):**
   - Sağ alt bildirim alanındaki Cursor tepsi simgesi sağ tık menüsü (`Tüm Bildirimleri Temizle`, `Cursor'ı Aç`, `Ayarlar`, `Çıkış`, `Son Kullanılan Ajan Yok`, `Yeni Ajan`).
   - Harici bağlantı açma onay diyaloğu (`Harici Bağlantıyı Aç`, `İptal` / `Aç`).
3. **Sesli Dikte & Mikrofon Koruması (Voice Input & Dictation):**
   - React `<kbd>` kısayol bileşenleri korunarak tam Türkçe sesli dikte ipuçları (`Dikte etmek için tıklayın veya [Ctrl] [M] tuşuna basılı tutun`, `Sesli Giriş (${kısayol})`, `Sesli Girişi Başlat`).
4. **Yerel Menü Çubuğu (Native Menu Bar & NLS Cache):**
   - Üst menü çubuğundaki tüm ana başlıklar (`Dosya`, `Düzen`, `Seçim`, `Görünüm`, `Görünümü Aç...`, `Git`, `Çalıştır`, `Terminal`, `Yardım`).
   - Electron NLS ve CLP önbelleği (`Roaming\Cursor\clp\*.tr`) ile tam senkronizasyon.
5. **Durum Çubuğu, Ortam & Bağlam (Status Bar, Environment & Context):**
   - `Depo Oluştur` butonu ve çok adımlı depo oluşturma çekmecesi.
   - Çalışma ortamı göstergesi (`☁ Bulut v` / `Bu Bilgisayar` / `Yerel`).
   - Bağlam ve token kullanım balonu (`% bağlam kullanıldı`, `X / Y belirteç`).
6. **Yardım & Geliştirici Menüsü (Help & DevTools):**
   - `Sorun Bildir`, `Geri Bildirim Gönder...`, `Geliştirici Araçlarını Aç/Kapat`, `İşlem Gezginini Aç` vb.
7. **Boş Editör & Filigran (Watermark & Quick Actions):**
   - `Dosyaya Git`, `Terminali Göster`, `Tarayıcıyı Aç`, `Sohbeti Büyüt`, `Depo Ekle`.
8. **Dal Seçici & Git Eylemleri (Branch Picker & SCM):**
   - `+ Dal Oluştur`, `${dal} Dalını Oluştur`, `Daha Fazla Yükle...`, `Dalı Güncelle`, `Dal Oluştur ve İşle`.
9. **Fark ve Değişiklik Kartı (Diff & Review Cards):**
   - `${count} Dosya Değişti` (`X Files Changed`), `1 Dosya Değişti`, diff istatistikleri ve satır özetleri.
10. **Canlı Güncelleme Bildirimleri (Live Update Notifications):**
    - `Yeni güncelleme mevcut`, `Sürüme güncelle: v`, `Yenilikler:`, `Daha Sonra`, `Şimdi Yükle`.
11. **Glass UI, Composer & Agent Runtime:**
    - Composer çoklu dosya arayüzü, Steer & Agent davranış başlıkları, model seçicileri ve durum çubuğu metrikleri.
12. **Bütünlük ve Güvenlik (IntegrityService):**
    - `product.json` Base64 SHA-256 sağlama toplamları otomatik hesaplanır; Cursor asla bozukluk uyarısı vermez.

---

## 🚀 Kurulum (Installation)

### Yöntem 1: Tek Tıkla Kurulum Paketi (.zip - Önerilen)
1. **[Releases](https://github.com/foztrk/cursor-turkish-localization/releases/latest)** sayfasından en son paketi (`Cursor_Turkce_Yama_v3.24.18.zip`) indirin.
2. ZIP arşivini bir klasöre çıkartın.
3. Cursor'ı tamamen kapatın.
4. `TURKCELESTIR.bat` dosyasına çift tıklayın ve Yönetici iznini (UAC) onaylayın.
5. Birkaç saniye içinde kurulum tamamlanır ve Cursor Türkçe olarak kullanıma hazır hale gelir!

### Yöntem 2: Git ile Kurulum
```bash
git clone https://github.com/foztrk/cursor-turkish-localization.git
cd cursor-turkish-localization
TURKCELESTIR.bat
```

### Yöntem 3: Python ile Kurulum (Geliştiriciler İçin)
```bash
python single_click_patcher.py
```

### Doğrulama (Verification)
Kurulumun bütünlüğünü test etmek için:
```bash
python verify_all.py
```
> Çıktı: `SONUÇ: %100 DOĞRULANDI — Cursor Türkçe Yaması Kusursuz Aktif!`

### Orijinale Dönüş (Rollback)
Dilediğiniz an Cursor'ı fabrika ayarlarına döndürmek için:
* `ORIJINALE_DON.bat` dosyasını çalıştırmanız yeterlidir.

---

## 🛡️ Mimarî ve Bütünlük (IntegrityService)

Cursor, VS Code tabanı üzerine kurulu olmasına rağmen Electron'un derinliklerinde çalışan özel güvenlik ve arayüz katmanlarına sahiptir:
* **CLP (Compiled Language Pack) Önbelleği:** Electron, dil paketi açıkken Program Files altındaki dosyaları değil, `%APPDATA%\Cursor\clp\<hash>.tr\<commit>\nls.messages.json` dosyasını okur. Yama motorumuz bu önbelleği otomatik olarak derler ve senkronize eder.
* **IntegrityService:** `product.json` içerisindeki dosyaların Base64 SHA-256 özetleri taranır. Yama motorumuz yamalı dosyaların yeni özetlerini birebir `product.json`'a işleyerek bütünlük uyarısını tamamen ortadan kaldırır.
* **Model Araç ve Durum Çıktıları:** `tool-action-labels.js` eylem sözlüğü üzerinden modelin tüm araç çıktıları (`Running`/`Çalıştırılıyor`, vb.) kodun mantıksal karşılaştırmaları bozulmadan güvenle çevrilir.
* **React / Glass AST Katmanı:** Glass UI doğrudan HTML üretmez; JSX/React bileşen ağacı üzerinden render edilir. Bu nedenle statik string yerine AST prop eşlemesi (`tr2/m*.json`) ve MutationObserver TreeWalker kullanılır.

Detaylı teknik mimari şeması ve çözüm analizleri için **[ARCHITECTURE_TR.md](ARCHITECTURE_TR.md)** dosyasını inceleyebilirsiniz.

---

## 📂 Depo Yapısı (Repository Structure)

```
cursor-turkish-localization/
├── nls-tm.json                  # 1.302 çekirdek NLS çeviri belleği
├── cursor-ui-tm.json            # Glass UI ve arayüz çeviri belleği
├── bilinen-ingilizce.json       # Kasıtlı olarak İngilizce bırakılan dev/jargon allowlist
├── tr2/                         # Bileşen ve AST prop haritaları (m01.json - m22.json)
├── apply_all.py                 # Ana orkestrasyon ve otomatik yama motoru
├── single_click_patcher.py      # Bağımsız tek tık çalıştırıcı (UAC + Process + Deploy)
├── verify_all.py                # Checksum, CLP ve dosya bütünlük test motoru
├── patch_tool_labels.py         # Model araç eylemleri (68 araç) ve düşünme etiketleri
├── patch_main_process.py        # out/main.js Sistem Tepsisi (Tray) ve dış bağlantı diyalogları
├── patch_fixes.py               # Sesli dikte, mikrofon ipuçları, sekme menüleri ve NLS fallback
├── patch_menu_gaps.py           # Menü çubuğu, dal seçici, diff kartı ve güncelleme yamaları
├── fix_all_corrupt_and_gaps.py  # IntegrityService checksum onarımı ve boşluk giderici
├── patch_help_menu_labels.py    # Yardım menüsü ve geliştirici araçları etiketleri
├── patch_steer_and_behavior.py  # Ajan yönlendirme ve davranış modelleri
├── patch_hook_tip.py            # Composer ve kanca ipuçları
├── patch_remaining_ui.py        # Kalan dinamik arayüz öğeleri
├── fix_all_checksums.py         # product.json SHA-256 Base64 otomatik güncelleyici
├── TURKCELESTIR.bat             # Son kullanıcılar için tek tık kurulum betiği
├── ORIJINALE_DON.bat            # Tek tık orijinal fabrika ayarlarına dönüş
├── ARCHITECTURE_TR.md           # Mimarî bilgi grafiği ve hata analiz kılavuzu
├── CONTRIBUTING.md              # Katkıda bulunma rehberi
├── SECURITY.md                  # Güvenlik politikası
├── LICENSE                      # MIT Lisansı
└── README.md                    # Dokümantasyon
```

---

## 🤝 Katkıda Bulunma & İletişim

* **Sorun veya Hata Bildir:** [Issues](https://github.com/foztrk/cursor-turkish-localization/issues)
* **Topluluk Tartışmaları:** [Discussions](https://github.com/foztrk/cursor-turkish-localization/discussions)
* **Pull Request:** [Pull Requests](https://github.com/foztrk/cursor-turkish-localization/pulls)

## 📄 Lisans (License)
Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.
