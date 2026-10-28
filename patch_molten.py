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
    ("`Approve`", "`Onayla`"),
    ("`Approved`", "`Onaylandı`"),
    ("`Approve MCP tool`", "`MCP aracını onayla`"),
    ("`Approve file deletion`", "`Dosya silmeyi onayla`"),
    ("`Approve file edit`", "`Dosya düzenlemeyi onayla`"),
    ("`Approve pending action`", "`Bekleyen eylemi onayla`"),
    ("`Approve terminal command`", "`Terminal komutunu onayla`"),
    ("`Allow all`", "`Tümüne izin ver`"),
    ("`Allow`", "`İzin Ver`"),
    ("`Allow Members to Publish`", "`Üyelerin Yayınlamasına İzin Ver`"),
    ("`Allow PR Approval`", "`PR Onayına İzin Ver`"),
    ("`Allowlist Options`", "`İzin Listesi Seçenekleri`"),
    ("`(Blocked by admin)`", "`(Yönetici tarafından engellendi)`"),
    ("`(Default Branch)`", "`(Varsayılan Dal)`"),
    ("`(Optional)`", "`(İsteğe bağlı)`"),
    ("`(optional)`", "`(isteğe bağlı)`"),
    ("`Awaiting Admin Approval`", "`Yönetici Onayı Bekleniyor`"),
    ("`1 minute`", "`1 dakika`"),
    ("`5 minutes`", "`5 dakika`"),
    ("`10 minutes`", "`10 dakika`"),
    ("`15 minutes`", "`15 dakika`"),
    ("`30 minutes`", "`30 dakika`"),
    ("`60 minutes`", "`60 dakika`"),
    ("`Ask Agent`", "`Ajana Sor`"),
    ("`Ask Mode`", "`Soru Modu`"),
    ("`Ask questions`", "`Sorular sorun`"),
    ("`Agent Conversations`", "`Ajan Konuşmaları`"),
    ("`Agent Instructions`", "`Ajan Talimatları`"),
    ("`Agent Mode`", "`Ajan Modu`"),
    ("`Agent Window`", "`Ajan Penceresi`"),
    ("`Agent is blocked`", "`Ajan engellendi`"),
    ("`Agent is using this terminal. It's read-only.`", "`Ajan bu terminali kullanıyor. Salt okunurdur.`"),
    ("`Background terminal is still running`", "`Arka plan terminali hâlâ çalışıyor`"),
    ("`Archive Agent with Running Subagents?`", "`Çalışan Alt Ajanları Olan Ajan Arşivlensin mi?`"),
    ("`Archive All Below`", "`Aşağıdakilerin Tümünü Arşivle`"),
    ("`Archive running agent?`", "`Çalışan ajan arşivlendi mi?`"),
    ("`Ask Before Quitting with Running Agents`", "`Çalışan Ajanlar Varken Çıkmadan Önce Sor`"),
    ("`Auto-Approve Mode Transitions`", "`Mod Geçişlerini Otomatik Onayla`"),
    ("`Add memory notes...`", "`Bellek notları ekleyin...`"),
    ("`Add single comment`", "`Tek bir yorum ekle`"),
    ("`Add to Side Chat`", "`Yan Sohbete Ekle`"),
    ("`Add to chat`", "`Sohbete ekle`"),
    ("`Add your own MCP server`", "`Kendi MCP sunucunuzu ekleyin`"),
    ("`Add Another Account`", "`Başka Bir Hesap Ekle`"),
    ("`Add Environment`", "`Ortam Ekle`"),
    ("`Add Metric`", "`Metrik Ekle`"),
    ("`Add Repositories`", "`Depolar Ekle`"),
    ("`Add Secrets`", "`Gizli Diziler Ekle`"),
    ("`Add Tool or MCP`", "`Araç veya MCP Ekle`"),
    ("`Add Trigger`", "`Tetikleyici Ekle`"),
    ("`Add a Custom MCP`", "`Özel MCP Ekle`"),
    ("`Add a comment`", "`Yorum ekle`"),
    ("`Add a comment...`", "`Yorum ekle...`"),
    ("`Add current folder`", "`Geçerli klasörü ekle`"),
    ("`Add description`", "`Açıklama ekle`"),
    ("`Add filter`", "`Filtre ekle`"),
    ("`Added or Removed`", "`Eklendi veya Kaldırıldı`"),
    ("`Adjust Plan`", "`Planı Ayarla`"),
    ("`Adjust on-demand limit`", "`İsteğe bağlı limiti ayarla`"),
    ("`Adjust your on-demand limit`", "`İsteğe bağlı limitinizi ayarlayın`"),
    ("`All Changes`", "`Tüm Değişiklikler`"),
    ("`All Commits`", "`Tüm Commit'ler`"),
    ("`All Fonts`", "`Tüm Yazı Tipleri`"),
    ("`All MCP servers added`", "`Tüm MCP sunucuları eklendi`"),
    ("`All MCP servers from this plugin are already added.`", "`Bu eklentideki tüm MCP sunucuları zaten eklendi.`"),
    ("`All Plugins`", "`Tüm Eklentiler`"),
    ("`All Runs`", "`Tüm Çalıştırmalar`"),
    ("`All issues resolved`", "`Tüm sorunlar çözüldü`"),
    ("`Already in Another Workspace`", "`Zaten Başka Bir Çalışma Alanında`"),
    ("`Always ask`", "`Her zaman sor`"),
    ("`Always run`", "`Her zaman çalıştır`"),
    ("`Any Project`", "`Herhangi Bir Proje`"),
    ("`Any Service`", "`Herhangi Bir Servis`"),
    ("`Any Team`", "`Herhangi Bir Takım`"),
    ("`Anyone with the link`", "`Bağlantıya sahip olan herkes`"),
    ("`Appearance`", "`Görünüm`"),
    ("`Are you sure you want to delete this comment?`", "`Bu yorumu silmek istediğinizden emin misiniz?`"),
    ("`Automate with Hooks`", "`Kancalarla (Hooks) Otomatikleştirin`"),
    ("`Automatically register computers`", "`Bilgisayarları otomatik kaydet`"),
    ("`Automation failed`", "`Otomasyon başarısız oldu`"),
    ("`Available repositories`", "`Kullanılabilir depolar`"),
    ("`Batch edits`", "`Toplu düzenlemeler`"),
    ("`Branch (optional)`", "`Dal (isteğe bağlı)`"),
    ("`Branch name`", "`Dal adı`"),
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
    ("`Search remote repos...`", "`Uzak depolarda ara...`"),
    ("title:`Computer Use`", "title:`Bilgisayar Kullanımı`"),
    ("label:`Computer Use`", "label:`Bilgisayar Kullanımı`"),
    ("=`Computer Use`", "=`Bilgisayar Kullanımı`"),
    ("`Always-allowed apps: Cursor can use these in any chat without asking. Remove one to be asked again.`",
     "`Her zaman izin verilen uygulamalar: Cursor bunları herhangi bir sohbette sormadan kullanabilir. Tekrar sorulması için birini kaldırın.`"),
    ("`No always-allowed apps yet. Choose Always Allow when Cursor asks to use an app.`",
     "`Henüz her zaman izin verilen uygulama yok. Cursor bir uygulamayı kullanmak için izin istediğinde Her Zaman İzin Ver'i seçin.`"),
    ("`Refresh model list`", "`Model Listesini Yenile`"),
    ("`Refreshing model list`", "`Model Listesi Yenileniyor`"),
    ("`Sync your local skills to use them with Cloud Agents. Any changes will update automatically.`",
     "`Bulut Ajanlarıyla kullanmak için yerel becerilerinizi eşitleyin. Yapılan değişiklikler otomatik olarak güncellenir.`"),
    ("offerAction:`Sync`", "offerAction:`Eşitle`"),
    ("offerDismiss:`Not now`", "offerDismiss:`Şimdi Değil`"),
    ("Search This PC...", "Bu Bilgisayarda Ara..."),
    ("Search skills, context, chats", "Becerilerde, bağlamda, sohbetlerde ara"),
    ("Search custom modes", "Özel modlarda ara"),

    # === Yanıt Değerlendirme Tooltipleri (Thumbs Up / Down) ===
    ("t===`up`?`Good Response`:`Bad Response`", "t===`up`?`İyi Yanıt`:`Kötü Yanıt`"),
    ('"aria-label":t===`up`?`Thumbs up`:`Thumbs down`', '"aria-label":t===`up`?`İyi yanıt`:`Kötü yanıt`'),
    ("children:`Good Response`", "children:`İyi Yanıt`"),
    ("children:`Bad Response`", "children:`Kötü Yanıt`"),
    ("s=i===void 0?`Good Response`:i,o=r===void 0?`Bad Response`:r", "s=i===void 0?`İyi Yanıt`:i,o=r===void 0?`Kötü Yanıt`:r"),

    # === Proje ve Ortamlar / Makineler Açılır Menüleri ===
    ("label:`Environments`", "label:`Ortamlar`"),
    ("title:`Environments`", "title:`Ortamlar`"),
    ("children:`Environments`", "children:`Ortamlar`"),
    ("placeholder:`Search environments`", "placeholder:`Ortamlarda ara...`"),
    ("placeholder:`Search environments...`", "placeholder:`Ortamlarda ara...`"),
    ('"aria-label":`Search environments`', '"aria-label":`Ortamlarda ara`'),
    ('"aria-label":`Environments`', '"aria-label":`Ortamlar`'),
    ("ee=`Machines`", "ee=`Makineler`"),
    ("children:`Machines`", "children:`Makineler`"),
    ('"aria-label":`Remote Machines`', '"aria-label":`Uzak Makineler`'),
    ("children:`Remote Machines`", "children:`Uzak Makineler`"),
    ("N=`Search machines and pools`", "N=`Makinelerde ve havuzlarda ara...`"),
    ("title:`My Machines`", "title:`Makinelerim`"),
    ("title:`Pools`", "title:`Havuzlar`"),
    ("[`My Machines`,", "[`Makinelerim`,"),
    ("[`Other Pools`,", "[`Diğer Havuzlar`,"),
    ("[`Any Repo`,", "[`Herhangi Bir Depo`,"),
    ("`Other Pools`", "`Diğer Havuzlar`"),
    ("`Any Repo`", "`Herhangi Bir Depo`"),
    ("`My Machines`", "`Makinelerim`"),

    # === Alt Çubuk Cloud Butonu ===
    ("let n=e??`Cloud`", "let n=e??`Bulut`"),
    ("ariaLabel:e===void 0?`Run on Cloud`:`Run on Cloud and ${e}`", "ariaLabel:e===void 0?`Bulutta Çalıştır`:`Bulutta ve ${e} üzerinde çalıştır`"),
    ("ariaLabel:e===void 0?`Run on Cloud and ${t}`:`Run on Cloud, ${e}`", "ariaLabel:e===void 0?`Bulutta ve ${t} üzerinde çalıştır`:`Bulutta, ${e} üzerinde çalıştır`"),
    ("title:`Target environment: cloud`", "title:`Hedef ortam: bulut`"),
    ("label:`Continue in Cloud`", "label:`Bulutta Devam Et`"),
    (":`Move to Cloud`", ":`Buluta Taşı`"),
    ("label:`Cloud`", "label:`Bulut`"),

    # === Ajan / Proje Menü Aksiyonları ve Kopyalama ===
    ("children:`Copy Branch`", "children:`Dalı Kopyala`"),
    ("children:`Copy Web Link`", "children:`Bağlantıyı Kopyala`"),
    ("children:`Copy Deep Link`", "children:`Derin Bağlantıyı Kopyala`"),
    ("children:`Copy Request ID`", "children:`İstek Kimliğini Kopyala`"),
    ("children:`Copy Transcript`", "children:`Dökümü Kopyala`"),
    ("children:`Open in Web`", "children:`Web'de Aç`"),
    ('{"aria-label":`Move to`', '{"aria-label":`Taşı`'),
    ("children:`Move to`", "children:`Taşı`"),
    ("children:`No destinations available`", "children:`Kullanılabilir hedef yok`"),
    ('{"aria-label":`Add to Project`', '{"aria-label":`Projeye Ekle`'),
    ("children:`Add to Project`", "children:`Projeye Ekle`"),
    ("title:`Couldn't add the agent to the project`", "title:`Ajan projeye eklenemedi`"),
    ("children:`Move to Side Chat`", "children:`Yan Sohbete Taşı`"),
    ("children:`Move to cloud and keep working there.`", "children:`Buluta taşıyın ve orada çalışmaya devam edin.`"),
    ("Move to Recycle Bin", "Geri Dönüşüm Kutusuna Taşı"),
    ("Move to Trash", "Çöp Kutusuna Taşı"),
    ("Move to this machine", "Bu makineye taşı"),
    ("Move to my Cursor account", "Cursor hesabıma taşı"),
    ("Z(`copyLink`,`Copy Link`", "Z(`copyLink`,`Bağlantıyı Kopyala`"),
    ("Z(`copyLink`,`Copy Web Link`", "Z(`copyLink`,`Bağlantıyı Kopyala`"),
    ("case`project`:return`Add to Project`", "case`project`:return`Projeye Ekle`"),
    ("project:`Add to Project`", "project:`Projeye Ekle`"),
    ("children:`New Agent in`", "children:`Şurada Yeni Ajan:`"),

    # === Eklenti Pazarı ve Yönetim (Done / Bitti Butonu) ===
    ("children:l?`Done`:`Edit`", "children:l?`Bitti`:`Düzenle`"),
    ("children:l?\"Done\":\"Edit\"", "children:l?\"Bitti\":\"Düzenle\""),
    ("doneAction:`Done`", "doneAction:`Bitti`"),
    ("doneAction:\"Done\"", "doneAction:\"Bitti\""),
    ("label:`Done`", "label:`Bitti`"),
    ("label:\"Done\"", "label:\"Bitti\""),

    # === Tam Ekran Tooltipleri (Molten) ===
    ("Exit Full Screen", "Tam Ekrandan Çık"),
    ("Enter Full Screen", "Tam Ekrana Geç"),

    # === Eklenti Pazarı Açıklamaları (Google Workspace vb.) ===
    ("Search, read, draft, and manage email.", "E-postaları arayın, okuyun, taslak oluşturun ve yönetin."),
    ("Search events and schedule meetings.", "Etkinlikleri arayın ve toplantıları planlayın."),
    ("Search, read, create, and share files.", "Dosyaları arayın, okuyun, oluşturun ve paylaşın."),
    ("Read, draft, and edit docs.", "Belgeleri okuyun, taslak oluşturun ve düzenleyin."),
    ("Read, write, and format spreadsheets.", "Elektronik tabloları okuyun, yazın ve biçimlendirin."),
    ("Read, edit, and export presentations.", "Sunumları okuyun, düzenleyin ve dışa aktarın."),
    ("Send, receive, and search chat messages.", "Sohbet mesajlarını gönderin, alın ve arayın."),
    ("Slack AI tools for users and developers: interact with messages, channels, and workflows.", "Kullanıcılar ve geliştiriciler için Slack yapay zekâ araçları: mesajlar, kanallar ve iş akışlarıyla etkileşim kurun."),
]


MOLTEN_REGEX_REPS = [
    # Mikrofon aygıt etiketleri: "Default - ..." -> "Varsayılan - ...", "Communications - ..." -> "İletişim - ..."
    (re.compile(r'label:([a-zA-Z0-9_$]+)\.label\|\|`Microphone \$\{([a-zA-Z0-9_$]+)\+1\}`'),
     r'label:(\1.label?\1.label.replace(/^Default - /,"Varsayılan - ").replace(/^Communications - /,"İletişim - "):`Mikrofon ${\2+1}`)'),
    # Depo seçici alt menü arama kutuları
    (re.compile(r'placeholder:`Search \$\{([a-zA-Z0-9_$]+)\}\.\.\.`'),
     r'placeholder:`Bu Bilgisayarda ara...`'),
    (re.compile(r'`Search \$\{([a-zA-Z0-9_$]+)\.plural\}\.\.\.`'),
     r'`${\1.plural} içinde ara...`'),
    # Proje başlığı alt açıklaması: "Tracks the decisions, agent work, and follow-through needed to move X forward."
    (re.compile(r'`Tracks the decisions, agent work, and follow-through needed to move \$\{([a-zA-Z0-9_$]+)\} forward\.`'),
     r'`${\1} projesini ileriye taşımak için gereken kararları, ajan çalışmalarını ve takipleri izler.`'),
    # Tarih ayracı: "Today ${...}" -> "Bugün ${...}"
    (re.compile(r'\?`Today \$\{([a-zA-Z0-9_$]+)\}`:'),
     r'?`Bugün ${\1}`:'),
    # Klasör ekleme: "Add folder on ${...}" -> "${...} üzerinde klasör ekle"
    (re.compile(r'l=`Add folder on \$\{([a-zA-Z0-9_$]+)\}`'),
     r'l=`${\1} üzerinde klasör ekle`'),
    (re.compile(r'`Add folder on \$\{([a-zA-Z0-9_$]+)\}`'),
     r'`${\1} üzerinde klasör ekle`'),
    # Yeni Ajan Şablonları: "New Agent in ${...}" -> "${...} içinde Yeni Ajan"
    (re.compile(r'content:`New Agent in \$\{([a-zA-Z0-9_$]+)\.label\}`'),
     r'content:`${\1.label} içinde Yeni Ajan`'),
    (re.compile(r'content:`New Agent in \$\{([a-zA-Z0-9_$]+)\}`'),
     r'content:`${\1} içinde Yeni Ajan`'),
    (re.compile(r':`New Agent in \$\{([a-zA-Z0-9_$]+)\}`'),
     r':`${\1} içinde Yeni Ajan`'),
    # Eklenti Yönetimi "Done" / "Edit" butonu: children:l?`Done`:`Edit` -> children:l?`Bitti`:`Düzenle`
    (re.compile(r'children:([a-zA-Z0-9_$]+)\?`Done`:`Edit`'),
     r'children:\1?`Bitti`:`Düzenle`'),
    (re.compile(r'children:([a-zA-Z0-9_$]+)\?"Done":"Edit"'),
     r'children:\1?"Bitti":"Düzenle"'),
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
