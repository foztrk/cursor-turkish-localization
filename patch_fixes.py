# -*- coding: utf-8 -*-
# Kalip disi (baglamli) tekil degisimler: sohbet paneli sekme menusu, ajan eylem
# etiketleri, tarayici ayarlari, bozuk karakter onarimi, Connect butonu.
# apply_all.py tarafindan her yeni surumde yeniden calistirilir.
import io
import re

REPS = [
    # Bozuk karakter onarimi (Codex'ten kalan kodlama hatasi)
    ('Ajan, ba�lam, ara� ekleyin...', 'Ajan, bağlam, araç ekleyin...'),
    ('bulmas�n� veya �zetlemesini', 'bulmasını veya özetlemesini'),
    # Sohbet paneli / sekme menusu
    ('title:"Toggle Chat Pane"', 'title:"Sohbet Panelini Aç/Kapat"'),
    ('value:"Close Tab"', 'value:"Sekmeyi Kapat"'),
    ('value:"Close Other Tabs"', 'value:"Diğer Sekmeleri Kapat"'),
    ('value:"Close All Tabs"', 'value:"Tüm Sekmeleri Kapat"'),
    ('value:"Open Tab as Editor"', 'value:"Sekmeyi Düzenleyici Olarak Aç"'),
    ('"How did the agent do?"', '"Ajan nasıl iş çıkardı?"'),
    # Ajan eylem etiketleri (dokum ozetleri)
    ('action:"Explored"', 'action:"Keşfetti"'),
    ('?"Exploring":"Explored"', '?"Keşfediyor":"Keşfetti"'),
    ('??"Explored"', '??"Keşfetti"'),
    # Git ve PR'lar / Tarayici ayarlari
    ('==="externalBrowser"?"Default Browser":"Inside Cursor"', '==="externalBrowser"?"Varsayılan Tarayıcı":"Cursor İçinde"'),
    ('`Browser Tab: ${', '`Tarayıcı Sekmesi: ${'),
    ('"Browser Tab"', '"Tarayıcı Sekmesi"'),
    ('"Connected to Browser Tab"', '"Tarayıcı Sekmesine Bağlı"'),
    ('"Use a preview box instead of streaming responses directly into the shell"', '"Yanıtları doğrudan kabuğa akıtmak yerine bir önizleme kutusu kullan"'),
    # Connect butonu (karsilastirmayla tutarli cift tarafli degisim)
    ('?"Connect":"Add"', '?"Bağlan":"Ekle"'),
    ('==="Connect")', '==="Bağlan")'),
    ('"Reconnect":"Connect"', '"Yeniden Bağlan":"Bağlan"'),
    ('"idle"?"Connect":', '"idle"?"Bağlan":'),
    ('"Connecting...":"Connect"', '"Bağlanıyor...":"Bağlan"'),
    ('children:"Connect"', 'children:"Bağlan"'),
    ('?I?"Connect":"Save"', '?I?"Bağlan":"Kaydet"'),
    ('title:{value:"Connect Slack",original:"Connect Slack"}', 'title:{value:"Slack\'i Bağla",original:"Connect Slack"}'),
    # Metin Boyutu acilir listesi
    ('case .85:return"Small";case 1:return"Default";case 1.15:return"Large";case 1.3:return"Extra Large"',
     'case .85:return"Küçük";case 1:return"Varsayılan";case 1.15:return"Büyük";case 1.3:return"Çok Büyük"'),
    # Glass ust menu bolme
    ('?"New Worktree":', '?"Yeni Çalışma Ağacı":'),
    # Depo secici menusu (Glass)
    ('"Search folders, repos..."', '"Klasörlerde, depolarda ara..."'),
    ('?"This PC":mr?"This Mac":"This Computer"', '?"Bu Bilgisayar":mr?"Bu Mac":"Bu Bilgisayar"'),
    ('?"This PC":_r?"This Mac":"This Computer"', '?"Bu Bilgisayar":_r?"Bu Mac":"Bu Bilgisayar"'),
    ('?"This PC":Ai?"This Mac":"This Computer"', '?"Bu Bilgisayar":Ai?"Bu Mac":"Bu Bilgisayar"'),
    ('?"Self-Hosted Worker":"Remote Control"', '?"Yerel Çalıştırıcı":"Uzaktan Denetim"'),
    ('label:i?"Searching...":"Loading..."', 'label:i?"Aranıyor...":"Yükleniyor..."'),
    ('h="Loading...":s.length===0&&(h=i?"No branches found":"No branches available")', 'h="Yükleniyor...":s.length===0&&(h=i?"Dal bulunamadı":"Kullanılabilir dal yok")'),
    ('row:{kind:"progress",label:"Loading..."}', 'row:{kind:"progress",label:"Yükleniyor..."}'),
    ('row:{kind:"empty",label:t.query||n?"No branches found":"No branches available"}', 'row:{kind:"empty",label:t.query||n?"Dal bulunamadı":"Kullanılabilir dal yok"}'),
    ('label:n?"Searching...":"Loading..."', 'label:n?"Aranıyor...":"Yükleniyor..."'),
    ('?"Loading more...":"Load more"', '?"Daha Fazla Yükleniyor...":"Daha Fazla Yükle"'),
    ('className:"glass-4b2ntj",children:"Current"', 'className:"glass-4b2ntj",children:"Mevcut"'),
    ('group:A.recent,title:"Recent"', 'group:A.recent,title:"Son Kullanılanlar"'),
    (':"Enter a valid Git branch name":"Enter a branch name"', ':"Geçerli bir Git dal adı girin":"Bir dal adı girin"'),
    ('`On ${', '`${'),
    ('?"Repos":"Workspaces"', '?"Depolar":"Çalışma Alanları"'),
    ('groupLabel:"Repos"', 'groupLabel:"Depolar"'),
    ('?"Cloud":"Repos"', '?"Bulut":"Depolar"'),
    # Gizlilik acilir listesi (HTML govdeli secenekler)
    ('<div><div>Share Data</div><div>Improve Cursor for everyone', '<div><div>Verileri Paylaş</div><div>Cursor\'ı herkes için iyileştirin'),
    ('<div><div>Privacy Mode</div><div>No training. Code may be stored for Background Agent and other features.', '<div><div>Gizlilik Modu</div><div>Eğitim yok. Kod, Arka Plan Ajanı ve diğer özellikler için depolanabilir.'),
    ('<div><div>Privacy Mode (Legacy)</div><div>No training and no storage. Background Agent and other features that require code storage will be disabled.', '<div><div>Gizlilik Modu (Eski)</div><div>Eğitim yok ve depolama yok. Kod depolaması gerektiren Arka Plan Ajanı ve diğer özellikler devre dışı bırakılır.'),
    ('"Share Data"', '"Verileri Paylaş"'),
    # Gorunum ayarlari
    ('"UI Font Family"', '"Arayüz Yazı Tipi Ailesi"'),
    ('"Code Font Family"', '"Kod Yazı Tipi Ailesi"'),
    ('"System font"', '"Sistem Yazı Tipi"'),
    ('"System monospace"', '"Sistem Eş Aralıklı"'),
    ('label:"System"', 'label:"Sistem"'),
    # Ajanlar / Tarayici ayarlari
    ('"Send Right Away"', '"Hemen Gönder"'),
    ('"Open Web Links in Browser"', '"Web Bağlantılarını Tarayıcıda Aç"'),
    # Fark inceleme ipuclari ve baglam paneli
    ('"Accept all changes"', '"Tüm Değişiklikleri Kabul Et"'),
    ('"Context Usage"', '"Bağlam Kullanımı"'),
    ('% Full', '% Dolu'),
    ("don't show again", 'bir daha gösterme'),
    # Hiyerarsik Cursor Ignore (React Ayarlar sayfasi, getter tabanli aciklama -
    # patch_settings.py'deki statik description eslemesi bunu yakalayamiyordu)
    ('label:"Hierarchical Cursor Ignore",get description(){return`Apply .cursorignore files to all subdirectories${n()?" (controlled by admin)":""}. Changing this setting requires restarting Cursor.`',
     'label:"Hiyerarşik Cursor Yoksayması",get description(){return`.cursorignore dosyalarını tüm alt dizinlere uygula${n()?" (yönetici tarafından denetleniyor)":""}. Bu ayarın değiştirilmesi Cursor\'ın yeniden başlatılmasını gerektirir.`'),
    # Profil sayfasi (Glass bundle'inda yasiyor, IDE penceresinde de bu bundle'dan gosteriliyor)
    ('children:["Profile Image",', 'children:["Profil Resmi",'),
    ('children:y===null?"Upload image":"Change image"}', 'children:y===null?"Resim Yükle":"Resmi Değiştir"}'),
    ('description:u?"When enabled, your cursor.com profile page is visible to anyone with the link.":"Public profiles are disabled by your team admin.",label:"Public Profile"',
     'description:u?"Etkinleştirildiğinde, cursor.com profil sayfanız bağlantıya sahip herkese görünür olur.":"Herkese açık profiller ekip yöneticiniz tarafından devre dışı bırakılmış.",label:"Herkese Açık Profil"'),
    ('"aria-label":"Public Profile"', '"aria-label":"Herkese Açık Profil"'),
    ('label:"Email",children:Cw("span",{className:"glass-b3', 'label:"E-posta",children:Cw("span",{className:"glass-b3'),
    ('actionTitle:"Configure Team MCP Servers"', 'actionTitle:"Ekip MCP Sunucularını Yapılandır"'),
    # Mikrofon / Dikte ve Sesli Giris ipuclari (React kbd/degisken yapisina dokunmadan)
    ('children:["Click or hold ",', 'children:["Dikte etmek için tıklayın veya ",'),
    ('," to dictate"]}', '," tuşuna basılı tutun"]}'),
    ('`Voice Input (${', '`Sesli Giriş (${'),
    ('"Starting voice input\\u2026"', '"Sesli Giriş Başlatılıyor\\u2026"'),
    ('"Voice input unavailable"', '"Sesli Giriş Kullanılamıyor"'),
    ('"Start voice input"', '"Sesli Girişi Başlat"'),
    ('"Send voice input"', '"Sesli Girişi Gönder"'),
    ('"Cancel recording"', '"Kaydı İptal Et"'),
    ('"Stop voice recording"', '"Ses Kaydını Durdur"'),
    ('"Voice chat is using the microphone"', '"Sesli sohbet mikrofonu kullanıyor"'),
    # Bildirim Merkezi (Notification Center NLS fallback)
    (',title:Ae(3838,"Clear All Notifications")', ',title:Ae(3838,"Tüm Bildirimleri Temizle")'),
    (',title:At(3838,"Clear All Notifications")', ',title:At(3838,"Tüm Bildirimleri Temizle")'),
    (',title:Ae(3840,"Hide Notifications")', ',title:Ae(3840,"Bildirimleri Gizle")'),
    (',title:At(3840,"Hide Notifications")', ',title:At(3840,"Bildirimleri Gizle")'),
    # Hata Ayiklama / Reproduction Steps Arayuzu
    ('class=debug-logs-title>Debug Logs', 'class=debug-logs-title>Hata Ayıklama Günlükleri'),
    ('children:"Debug Logs"', 'children:"Hata Ayıklama Günlükleri"'),
    ('class=debug-logs-empty>Waiting for log entries...', 'class=debug-logs-empty>Günlük girişleri bekleniyor...'),
    ('class=composer-debug-reproduction-toolbar-title>Reproduction Steps', 'class=composer-debug-reproduction-toolbar-title>Yeniden Oluşturma Adımları'),
    ('children:"Reproduction Steps"', 'children:"Yeniden Oluşturma Adımları"'),
    ('children(){return["Proceed",', 'children(){return["İlerle",'),
    ('fallbackValues:{proceed_instructions:"Issue reproduced, please proceed"', 'fallbackValues:{proceed_instructions:"Sorun yeniden oluşturuldu, lütfen devam edin"'),
    ('??"Issue reproduced, please proceed"', '??"Sorun yeniden oluşturuldu, lütfen devam edin"'),
    ('return"Enter additional context about the issue"', 'return"Sorun hakkında ek bağlam girin"'),
    ('details:"available tools"', 'details:"kullanılabilir araçlar"'),
    # Ajan Aktivite Ozeti Sayaclari (files, searches, fetches, etc.)
    ('director${o===1?"y":"ies"}', 'dizin'),
    ('a=>`${a} file${a===1?"":"s"}`', 'a=>`${a} dosya`'),
    ('compactText:o?"1 file":void 0', 'compactText:o?"1 dosya":void 0'),
    ('${e.searches} search${e.searches===1?"":"es"}', '${e.searches} arama'),
    ('${t.searches} search${t.searches===1?"":"es"}', '${t.searches} arama'),
    ('${e.fetches} fetch${e.fetches===1?"":"es"}', '${e.fetches} istek'),
    ('${t.fetches} fetch${t.fetches===1?"":"es"}', '${t.fetches} istek'),
    ('text:"lints"', 'text:"sorun denetimi"'),
    ('browser action${s===1?"":"s"}', 'tarayıcı eylemi'),
    ('ran ${t} command${t===1?"":"s"}', '${t} komut çalıştırıldı'),
    ('ran ${e} command${e===1?"":"s"}', '${e} komut çalıştırıldı'),
    ('${t} image${t===1?"":"s"}', '${t} görsel'),
    ('${e} image${e===1?"":"s"}', '${e} görsel'),
    ('${t} agent${t===1?"":"s"}', '${t} alt ajan'),
    ('${e} agent${e===1?"":"s"}', '${e} alt ajan'),

    # === Voice (Ses) Ayarları & Mikrofon ===
    ('="Agent Voice"', '="Ajan Sesi"'),
    ('title:"Voice"', 'title:"Ses"'),
    ('accessibleLabel:"Voice"', 'accessibleLabel:"Ses"'),
    (',voice:"Voice",', ',voice:"Ses",'),
    ('placeholder:"Choose a voice"', 'placeholder:"Bir ses seçin"'),
    ('options:[{value:"",label:"System Default"}', 'options:[{value:"",label:"Sistem Varsayılanı"}'),
    ('{auto:"Auto-detect"', '{auto:"Otomatik Algıla"'),
    ('description:"Default voice for voice chats. Changing the voice plays a short sample."', 'description:"Sesli sohbetler için varsayılan ses. Sesi değiştirmek kısa bir örnek oynatır."'),
    ('description:"How quickly the voice speaks in voice chats."', 'description:"Sesin sesli sohbetlerde konuşma hızı."'),
    ('description:"How quickly the voice speaks in voice chats"', 'description:"Sesin sesli sohbetlerde konuşma hızı"'),
    ('{description:"Language used in voice chats.",label:"Language",', '{description:"Sesli sohbetlerde kullanılan dil.",label:"Dil",'),
    ('{label:"Language",description:"Language used in voice chats"', '{label:"Dil",description:"Sesli sohbetlerde kullanılan dil"'),
    ('{description:"Microphone used in voice chats.",label:"Microphone",', '{description:"Sesli sohbetlerde kullanılan mikrofon.",label:"Mikrofon",'),
    ('{label:"Microphone",description:"Microphone used in voice chats"', '{label:"Mikrofon",description:"Sesli sohbetlerde kullanılan mikrofon"'),
    ('voice:{label:"Submit Keywords",description:"Words that send your prompt while you dictate. Voice chats ignore them."}', 'voice:{label:"Gönderme Anahtar Kelimeleri",description:"Dikte ederken isteminizi gönderen kelimeler. Sesli sohbetler bunları yok sayar."}'),
    ('nd("voice","submit-keywords",{label:"Submit Keywords"', 'nd("voice","submit-keywords",{label:"Gönderme Anahtar Kelimeleri"'),
    ('description:"Words that send your prompt while you dictate"', 'description:"Dikte ederken isteminizi gönderen kelimeler"'),

    # === Bağlam Ekleme (Attach / Menüler) ===
    ('{image:"Image",attachments:"Attach","cloud-files":"Attach"}', '{image:"Görsel",attachments:"Ekle","cloud-files":"Ekle"}'),
    ('searchAliases:we==="Attach"?["File","Files"]:void 0', 'searchAliases:we==="Ekle"?["Dosya","Dosyalar","File","Files"]:void 0'),
    ('searchAliases:de==="Attach"?["File","Files"]:void 0', 'searchAliases:de==="Ekle"?["Dosya","Dosyalar","File","Files"]:void 0'),

    # === This PC ve Çalıştırıcı Gösterim Fallback'leri ===
    ('"This PC (Yerel Çalıştırıcı)"', '"Bu Bilgisayar (Yerel Çalıştırıcı)"'),
    ('"This PC (Uzaktan Denetim)"', '"Bu Bilgisayar (Uzaktan Denetim)"'),
    ('"Search This PC..."', '"Bu Bilgisayarda Ara..."'),

    # === Sistem Tepsisi ve Proje Seçici "No Repo" -> "Depo Yok" ===
    ('="No Repo"', '="Depo Yok"'),
    ('TPs="No-repo Automations"', 'TPs="Deposuz Otomasyonlar"'),
    ('"No-repo Automations"', '"Deposuz Otomasyonlar"'),
]

REGEX_REPS = [
    # Jenerik "This PC" / "This Mac" -> "Bu Bilgisayar" / "Bu Mac" eşleşmesi (tüm sürümlerde çalışır)
    (re.compile(r'([a-zA-Z0-9_$]+)\?"This PC":([a-zA-Z0-9_$]+)\?"This Mac":"This Computer"'),
     r'\1?"Bu Bilgisayar":\2?"Bu Mac":"Bu Bilgisayar"'),
    # Sistem Tepsisi ve Proje Seçicide "No Repo" -> "Depo Yok" (minified değişken atamaları)
    (re.compile(r'([a-zA-Z0-9_$]+)="No Repo"'),
     r'\1="Depo Yok"'),
    (re.compile(r'([a-zA-Z0-9_$]+)="No-repo Automations"'),
     r'\1="Deposuz Otomasyonlar"'),
    # Mikrofon aygıt etiketleri: "Default - ..." -> "Varsayılan - ...", "Communications - ..." -> "İletişim - ..."
    (re.compile(r'label:([a-zA-Z0-9_$]+)\.label\|\|`Microphone \$\{([a-zA-Z0-9_$]+)\+1\}`'),
     r'label:(\1.label?\1.label.replace(/^Default - /,"Varsayılan - ").replace(/^Communications - /,"İletişim - "):`Mikrofon ${\2+1}`)'),
]

if __name__ == '__main__':
    for fname in ['workbench.desktop.main.js', 'workbench.glass.main.js']:
        s = io.open(fname, encoding='utf-8').read()
        n = 0
        for pat, rep in REGEX_REPS:
            s, c = pat.subn(rep, s)
            n += c
        for a, b in REPS:
            c = s.count(a)
            if c:
                s = s.replace(a, b)
                n += c
        io.open(fname, 'w', encoding='utf-8', newline='').write(s)
        print(fname, 'degisim:', n)
