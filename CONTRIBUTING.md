# Katkıda Bulunma Rehberi (Contributing Guidelines)

Cursor Türkçe Yerelleştirme projesine hoş geldiniz! Türkiye'deki yazılımcı topluluğu için Cursor'ı en yüksek mühendislik kalitesinde Türkçeleştirmeyi hedefliyoruz.

---

## 🛠️ Nasıl Katkı Sağlayabilirsiniz?

1. **Eksik veya Hatalı Çevirileri Bildirme:**
   - GitHub üzerinde bir [Hata Bildirimi (Bug Report)](https://github.com/foztrk/cursor-turkish-localization/issues/new?template=bug_report.md) açın.
2. **Yazılım Jargonu ve Terim İlkeleri:**
   - Yazılımcıların evrensel olarak kullandığı anahtar kelimeleri (`Git`, `Commit`, `Branch`, `Diff`, `Composer`, `Token`, `Terminal`, `Debug`) asla zorlama tercüme yapmıyoruz.
   - Yalnızca kullanıcı deneyimini iyileştiren, yönlendirici ve açıklayıcı arayüz metinlerini Türkçeleştiriyoruz.
3. **Pull Request (PR) Gönderme:**
   - `nls-tm.json` veya `cursor-ui-tm.json` üzerinde yaptığınız değişiklikleri test edin:
     ```bash
     python verify_all.py
     ```
   - Doğrulama başarıyla `%100` sonucunu verdikten sonra PR oluşturun.

---

## 🏛️ Note to Anysphere / Cursor Core Developers
We are prepared to hand over all dictionaries and AST maps under the MIT license to be merged natively into Cursor. Please reach out via our [Official Inquiry Form](https://github.com/foztrk/cursor-turkish-localization/issues/new?template=official_inquiry.md) or at `abdurrahmanavci@gmail.com`.
