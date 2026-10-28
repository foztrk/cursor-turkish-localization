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

    # === Ortam Seçici (Environment Selector) ===
    ('??"Select Environment"', '??"Ortam Seç"'),
    ('title:"Select Environment"', 'title:"Ortam Seç"'),
    (', select environment`', ', ortam seç`'),

    # === Depo Seçici Alt Menüleri (Bu Bilgisayar / Uzak) ===
    ('"Search remote repos..."', '"Uzak depolarda ara..."'),
    ('children:"No repos"', 'children:"Depo Yok"'),
    ('?"No repos":"No projects"', '?"Depo Yok":"Proje Yok"'),

    # === Bilgisayar Kullanımı (Computer Use) ===
    ('title:"Computer Use"', 'title:"Bilgisayar Kullanımı"'),
    ('label:"Computer Use"', 'label:"Bilgisayar Kullanımı"'),
    ('"Always-allowed apps: Cursor can use these in any chat without asking. Remove one to be asked again."',
     '"Her zaman izin verilen uygulamalar: Cursor bunları herhangi bir sohbette sormadan kullanabilir. Tekrar sorulması için birini kaldırın."'),
    ('"No always-allowed apps yet. Choose Always Allow when Cursor asks to use an app."',
     '"Henüz her zaman izin verilen uygulama yok. Cursor bir uygulamayı kullanmak için izin istediğinde Her Zaman İzin Ver\'i seçin."'),
    ('"Enable Computer Use"', '"Bilgisayar Kullanımını Etkinleştir"'),
    ('"Allow Cursor to use your computer."', '"Cursor\'ın bilgisayarınızı kullanmasına izin verin."'),
    ('"Cursor Computer Use is not available in this build"', '"Cursor Bilgisayar Kullanımı bu derlemede kullanılamıyor"'),
    ('"Computer Use is ready"', '"Bilgisayar Kullanımı hazır"'),

    # === Modeller Sayfası (Refresh model list) ===
    ('?"Refreshing model list":"Refresh model list"', '?"Model Listesi Yenileniyor":"Model Listesini Yenile"'),
    ('?"Refreshing...":"Refresh model list"', '?"Yenileniyor...":"Model Listesini Yenile"'),
    ('"Refresh model list"', '"Model Listesini Yenile"'),

    # === Özelleştir / Beceriler Eşitleme Kartı ===
    ('offerTitle:"Use your skills with Cloud Agents"', 'offerTitle:"Becerilerinizi Bulut Ajanlarıyla kullanın"'),
    ('offerDescription:"Sync your local skills to use them with Cloud Agents. Any changes will update automatically."',
     'offerDescription:"Bulut Ajanlarıyla kullanmak için yerel becerilerinizi eşitleyin. Yapılan değişiklikler otomatik olarak güncellenir."'),
    ('offerAction:"Sync"', 'offerAction:"Eşitle"'),
    ('offerDismiss:"Not now"', 'offerDismiss:"Şimdi Değil"'),
    ('?"Syncing your skills\\u2026":"Moving your skills back to this machine\\u2026"',
     '?"Becerileriniz eşitleniyor\\u2026":"Becerileriniz bu makineye geri taşınıyor\\u2026"'),
    ('{text:"Not now"}', '{text:"Şimdi Değil"}'),

    # === Yanıt Değerlendirme Tooltipleri (Thumbs Up / Down) ===
    ('t==="up"?"Good Response":"Bad Response"', 't==="up"?"İyi Yanıt":"Kötü Yanıt"'),
    ('t===`up`?`Good Response`:`Bad Response`', 't===`up`?`İyi Yanıt`:`Kötü Yanıt`'),
    ('s=i===void 0?"Good Response":i,o=r===void 0?"Bad Response":r', 's=i===void 0?"İyi Yanıt":i,o=r===void 0?"Kötü Yanıt":r'),
    ('value:"up",children:"Good Response"', 'value:"up",children:"İyi Yanıt"'),
    ('value:"down",children:"Bad Response"', 'value:"down",children:"Kötü Yanıt"'),
    ('"aria-label":t==="up"?"Thumbs up":"Thumbs down"', '"aria-label":t==="up"?"İyi yanıt":"Kötü yanıt"'),
    ('children:"Good Response"', 'children:"İyi Yanıt"'),
    ('children:"Bad Response"', 'children:"Kötü Yanıt"'),
    ('children:`Good Response`', 'children:`İyi Yanıt`'),
    ('children:`Bad Response`', 'children:`Kötü Yanıt`'),

    # === Proje ve Ortamlar / Makineler Açılır Menüleri ===
    ('label:"Environments"', 'label:"Ortamlar"'),
    ('title:"Environments"', 'title:"Ortamlar"'),
    ('label:`Environments`', 'label:`Ortamlar`'),
    ('title:`Environments`', 'title:`Ortamlar`'),
    ('children:`Environments`', 'children:`Ortamlar`'),
    ('children:"Environments"', 'children:"Ortamlar"'),
    ('title:"My Machines"', 'title:"Makinelerim"'),
    ('title:`My Machines`', 'title:`Makinelerim`'),
    ('title:"Pools"', 'title:"Havuzlar"'),
    ('title:`Pools`', 'title:`Havuzlar`'),
    ('placeholder:"Search machines and pools"', 'placeholder:"Makinelerde ve havuzlarda ara..."'),
    ('placeholder:`Search machines and pools`', 'placeholder:`Makinelerde ve havuzlarda ara...`'),
    ('placeholder:"Search environments"', 'placeholder:"Ortamlarda ara..."'),
    ('placeholder:`Search environments`', 'placeholder:`Ortamlarda ara...`'),
    ('["My Machines",', '["Makinelerim",'),
    ('[`My Machines`,', '[`Makinelerim`,'),
    ('["Other Pools",', '["Diğer Havuzlar",'),
    ('[`Other Pools`,', '[`Diğer Havuzlar`,'),
    ('["Any Repo",', '["Herhangi Bir Depo",'),
    ('[`Any Repo`,', '[`Herhangi Bir Depo`,'),
    ('ee=`Machines`', 'ee=`Makineler`'),
    ('children:`Machines`', 'children:`Makineler`'),
    ('children:"Machines"', 'children:"Makineler"'),
    ('"aria-label":`Remote Machines`', '"aria-label":`Uzak Makineler`'),
    ('"aria-label":"Remote Machines"', '"aria-label":"Uzak Makineler"'),
    ('children:`Remote Machines`', 'children:`Uzak Makineler`'),
    ('children:"Remote Machines"', 'children:"Uzak Makineler"'),

    # === Alt Çubuk Cloud Butonu ===
    ('let n=e??`Cloud`', 'let n=e??`Bulut`'),
    ('ariaLabel:e===void 0?`Run on Cloud`:`Run on Cloud and ${e}`', 'ariaLabel:e===void 0?`Bulutta Çalıştır`:`Bulutta ve ${e} üzerinde çalıştır`'),
    ('ariaLabel:e===void 0?`Run on Cloud and ${t}`:`Run on Cloud, ${e}`', 'ariaLabel:e===void 0?`Bulutta ve ${t} üzerinde çalıştır`:`Bulutta, ${e} üzerinde çalıştır`'),
    ('title:`Target environment: cloud`', 'title:`Hedef ortam: bulut`'),
    ('label:`Continue in Cloud`', 'label:`Bulutta Devam Et`'),
    (':`Move to Cloud`', ':`Buluta Taşı`'),
    ('label:`Cloud`', 'label:`Bulut`'),
    ('label:"Cloud"', 'label:"Bulut"'),

    # === Sol Menü Ajan / Proje Sağ Tık (Context) Menüsü ===
    ('case"move-agent":return e.isProject?void 0:"Move to"', 'case"move-agent":return e.isProject?void 0:"Taşı"'),
    ('case"move-to-section":return e.isPinned&&!n?void 0:"Move to"', 'case"move-to-section":return e.isPinned&&!n?void 0:"Taşı"'),
    ('case"add-to-project":return"Add to Project"', 'case"add-to-project":return"Projeye Ekle"'),
    ('case"open-agent-in-web":return"Open in Web"', 'case"open-agent-in-web":return"Web\'de Aç"'),
    ('case"open-agent-in-new-window":return"Open in New Window"', 'case"open-agent-in-new-window":return"Yeni Pencerede Aç"'),
    ('case"archive-agents-below":return!e.isArchived&&i.archive?"Archive All Below":void 0', 'case"archive-agents-below":return!e.isArchived&&i.archive?"Aşağıdakilerin Tümünü Arşivle":void 0'),
    ('case"unarchive-agent":return e.isArchived?"Unarchive":void 0', 'case"unarchive-agent":return e.isArchived?"Arşivden Çıkar":void 0'),
    ('case"invite-to-project":return"Invite"', 'case"invite-to-project":return"Davet Et"'),
    ('function gRy(t){return t?"Mark as Read":"Mark as Unread"}', 'function gRy(t){return t?"Okundu Olarak İşaretle":"Okunmadı Olarak İşaretle"}'),

    # === Kopyala (Copy) Alt Menüsü ===
    ('label:"Copy Agent ID"', 'label:"Ajan Kimliğini Kopyala"'),
    ('label:"Copy Branch"', 'label:"Dalı Kopyala"'),
    ('label:"Copy PR Link"', 'label:"PR Bağlantısını Kopyala"'),
    ('label:"Copy Transcript"', 'label:"Dökümü Kopyala"'),
    ('label:"Copy Link"', 'label:"Bağlantıyı Kopyala"'),
    ('label:"Copy Deep Link"', 'label:"Derin Bağlantıyı Kopyala"'),
    ('label:"Copy Request ID"', 'label:"İstek Kimliğini Kopyala"'),

    # === Eklenti / Beceri ve Proje İlişkilendirme ===
    ('project:"Add to Project"', 'project:"Projeye Ekle"'),
    ('team:"Add to Team"', 'team:"Ekibe Ekle"'),
    ('user:"Add for Myself"', 'user:"Kendim İçin Ekle"'),
    ('case"project":return"Add to Project"', 'case"project":return"Projeye Ekle"'),
    ('case"team":return"Add to Team"', 'case"team":return"Ekibe Ekle"'),
    ('case"user":return"Add for Myself"', 'case"user":return"Kendim İçin Ekle"'),
    ('kind==="reparent"?"Add to Project"', 'kind==="reparent"?"Projeye Ekle"'),

    # === Eklenti Yönetimi (Bitti / Done Butonu) ===
    ('children:l?`Done`:`Edit`', 'children:l?`Bitti`:`Düzenle`'),
    ('children:l?"Done":"Edit"', 'children:l?"Bitti":"Düzenle"'),
    ('doneAction:"Done"', 'doneAction:"Bitti"'),
    ('doneAction:`Done`', 'doneAction:`Bitti`'),
    ('actionLabel:"Done"', 'actionLabel:"Bitti"'),
    ('newSecretAction:"New Secret",addAction:"Add",doneAction:"Done"', 'newSecretAction:"Yeni Gizli Dizi",addAction:"Ekle",doneAction:"Bitti"'),
    ('newSecretAction:`New Secret`,addAction:`Add`,doneAction:`Done`', 'newSecretAction:`Yeni Gizli Dizi`,addAction:`Ekle`,doneAction:`Bitti`'),

    # === Allowed Machines (Çalıştırma Konumu, Bulut, Makineler, Ortamlar) ===
    ('N("glass.allowedMachines.cloud","Cloud")', 'N("glass.allowedMachines.cloud","Bulut")'),
    ('N("glass.allowedMachines.oneMachine","1 Machine")', 'N("glass.allowedMachines.oneMachine","1 Makine")'),
    ('N("glass.allowedMachines.machineCount","{0} Machines"', 'N("glass.allowedMachines.machineCount","{0} Makine"'),
    ('N("glass.allowedMachines.runOnCloud","Run on Cloud")', 'N("glass.allowedMachines.runOnCloud","Bulutta Çalıştır")'),
    ('N("glass.allowedMachines.runOnCloudAnd","Run on Cloud and {0}"', 'N("glass.allowedMachines.runOnCloudAnd","Bulutta ve {0} üzerinde çalıştır"'),
    ('N("glass.allowedMachines.runOnCloudEnvironmentsAndMachines","Run on Cloud, {0}, and {1}"', 'N("glass.allowedMachines.runOnCloudEnvironmentsAndMachines","Bulutta, {0} ve {1} üzerinde çalıştır"'),
    ('N("glass.allowedMachines.environmentsMenu","Environments")', 'N("glass.allowedMachines.environmentsMenu","Ortamlar")'),
    ('N("glass.allowedMachines.machinesMenu","Machines")', 'N("glass.allowedMachines.machinesMenu","Makineler")'),
    ('N("glass.allowedMachines.searchPlaceholder","Search machines and pools")', 'N("glass.allowedMachines.searchPlaceholder","Makinelerde ve havuzlarda ara...")'),
    ('N("glass.allowedMachines.myMachinesSection","My Machines")', 'N("glass.allowedMachines.myMachinesSection","Makinelerim")'),
    ('N("glass.allowedMachines.poolsSection","Pools")', 'N("glass.allowedMachines.poolsSection","Havuzlar")'),
    ('N("glass.allowedMachines.reposSection","Repos")', 'N("glass.allowedMachines.reposSection","Depolar")'),
    ('N("glass.allowedMachines.environmentsSection","Environments")', 'N("glass.allowedMachines.environmentsSection","Ortamlar")'),
    ('N("glass.allowedMachines.addFolderOnMachine","Add folder on {0}"', 'N("glass.allowedMachines.addFolderOnMachine","{0} üzerinde klasör ekle"'),
    ('N("glass.allowedMachines.searchEnvironmentsPlaceholder","Search environments")', 'N("glass.allowedMachines.searchEnvironmentsPlaceholder","Ortamlarda ara...")'),
    ('N("glass.allowedMachines.runOnMenuLabel","Run on")', 'N("glass.allowedMachines.runOnMenuLabel","Şurada çalıştır")'),
    ('N("glass.allowedMachines.oneRepo","1 Repo")', 'N("glass.allowedMachines.oneRepo","1 Depo")'),
    ('N("glass.allowedMachines.repoCount","{0} Repos"', 'N("glass.allowedMachines.repoCount","{0} Depo"'),
    ('N("glass.allowedMachines.oneEnvironment","1 Environment")', 'N("glass.allowedMachines.oneEnvironment","1 Ortam")'),
    ('N("glass.allowedMachines.environmentCount","{0} Environments"', 'N("glass.allowedMachines.environmentCount","{0} Ortam"'),
    ('N("glass.allowedMachines.noMatchingTargets","No matching machines or pools")', 'N("glass.allowedMachines.noMatchingTargets","Eşleşen makine veya havuz yok")'),
    ('N("glass.allowedMachines.noMatchingEnvironments","No matching environments")', 'N("glass.allowedMachines.noMatchingEnvironments","Eşleşen ortam yok")'),
    ('N("glass.allowedMachines.loadingEnvironments","Loading environments\\u2026")', 'N("glass.allowedMachines.loadingEnvironments","Ortamlar yükleniyor\\u2026")'),
    ('N("glass.allowedMachines.noEnvironments","No environments")', 'N("glass.allowedMachines.noEnvironments","Ortam yok")'),
    ('N("glass.allowedMachines.offline","Offline")', 'N("glass.allowedMachines.offline","Çevrimdışı")'),
    ('N("glass.allowedMachines.unknownMachine","Unknown machine")', 'N("glass.allowedMachines.unknownMachine","Bilinmeyen makine")'),
    ('N("glass.allowedMachines.addFolder.dialogTitle","Choose a Folder for This Project")', 'N("glass.allowedMachines.addFolder.dialogTitle","Bu Proje İçin Bir Klasör Seçin")'),
    ('N("glass.allowedMachines.addFolder.folderNotLocal","Choose a folder on this computer.")', 'N("glass.allowedMachines.addFolder.folderNotLocal","Bu bilgisayarda bir klasör seçin.")'),

    # === Project Tracker & Notes (Proje Takip Paneli, List/Board/Library/For Review/Done) ===
    ('N("glass.project.document.view.rows","List")', 'N("glass.project.document.view.rows","Liste")'),
    ('N("glass.project.document.view.board","Board")', 'N("glass.project.document.view.board","Pano")'),
    ('N("glass.project.document.view.context","Library")', 'N("glass.project.document.view.context","Kitaplık")'),
    ('N("glass.project.document.view.notes","Notes")', 'N("glass.project.document.view.notes","Notlar")'),
    ('N("glass.project.document.status.forReview","For Review")', 'N("glass.project.document.status.forReview","İncelenecek")'),
    ('N("glass.project.document.status.inProgress","In Progress")', 'N("glass.project.document.status.inProgress","Devam Ediyor")'),
    ('N("glass.project.document.status.queued","Queued")', 'N("glass.project.document.status.queued","Kuyrukta")'),
    ('N("glass.project.document.status.done","Done")', 'N("glass.project.document.status.done","Tamamlandı")'),
    ('N("glass.project.document.status.canceled","Canceled")', 'N("glass.project.document.status.canceled","İptal Edildi")'),
    ('N("glass.project.notes.filter","Filter")', 'N("glass.project.notes.filter","Filtrele")'),
    ('N("glass.project.notes.findPlaceholder","Filter")', 'N("glass.project.notes.findPlaceholder","Filtrele")'),
    ('N("glass.project.notes.filters","Filters")', 'N("glass.project.notes.filters","Filtreler")'),
    ('N("glass.project.notes.filter.add","Add filter")', 'N("glass.project.notes.filter.add","Filtre ekle")'),
    ('N("glass.project.notes.filter.clear","Clear Filters")', 'N("glass.project.notes.filter.clear","Filtreleri Temizle")'),
    ('N("glass.project.filter.status","Status")', 'N("glass.project.filter.status","Durum")'),
    ('N("glass.project.filter.owner","Owner")', 'N("glass.project.filter.owner","Sorumlu")'),
    ('N("glass.project.filter.tags","Tags")', 'N("glass.project.filter.tags","Etiketler")'),
    ('N("glass.project.filter.pr","PR")', 'N("glass.project.filter.pr","PR")'),
    ('{id:"for-review",label:"For Review"', '{id:"for-review",label:"İncelenecek"'),
    ('{id:"queued",label:"Queued"', '{id:"queued",label:"Kuyrukta"'),
    ('{id:"canceled",label:"Canceled"', '{id:"canceled",label:"İptal Edildi"'),
    # Ortam Yönetimi ve Eşitleme Durumları
    ('case"manage-environments":return{label:"Manage Environments"', 'case"manage-environments":return{label:"Ortamları Yönet"'),
    ('label:"Manage Environments"', 'label:"Ortamları Yönet"'),
    ('case"sync-unavailable":return"Context sync is not running"', 'case"sync-unavailable":return"Bağlam eşitlemesi çalışmıyor"'),
    ('case"draft-agent":return"Send a message to initialize agent context"', 'case"draft-agent":return"Ajan bağlamını başlatmak için bir ileti gönderin"'),
    ('case"mount-failed":return`Couldn\'t sync ${e} context`', 'case"mount-failed":return`${e==="team"?"takım":e==="user"?"kullanıcı":"proje"} bağlamı eşitlenemedi`'),
    ('case"probe-failed":return`Couldn\'t load ${e} context`', 'case"probe-failed":return`${e==="team"?"takım":e==="user"?"kullanıcı":"proje"} bağlamı yüklenemedi`'),
    ('case"not-provisioned":return`${e.charAt(0).toUpperCase()}${e.slice(1)} context unavailable`', 'case"not-provisioned":return`${e==="team"?"Takım":e==="user"?"Kullanıcı":"Proje"} bağlamı kullanılamıyor`'),
    # Uygulamalar Paneli Göster / Gizle (Hide / Show Apps)
    ('{show:"Show Apps",hide:"Hide Apps"}', '{show:"Uygulamaları Göster",hide:"Uygulamaları Gizle"}'),
    ('placeholder:"Plan changes",description:"Bir uygulama planı üret"', 'placeholder:"Değişiklikleri planla",description:"Bir uygulama planı üret"'),
    # Kitaplık (Library) Dosya Ağacı Başlığı
    ('heading:"All Files"', 'heading:"Tüm Dosyalar"'),
    # Alt Ajan Paneli / Tepsisi (1 Ajan / Masaüstü / Küçült)
    ('{one:"Agent",other:"Agents"}', '{one:"Ajan",other:"Ajan"}'),
    ('{one:"Terminal",other:"Terminals"}', '{one:"Terminal",other:"Terminal"}'),
    ('Eln(V,"Open"):Eln(q,"Done")', 'Eln(V,"Açık"):Eln(q,"Tamamlandı")'),
    ('Eln(q,"Done")', 'Eln(q,"Tamamlandı")'),
    ('children:"Desktop"', 'children:"Masaüstü"'),
    ('title:p===r?"Internal":void 0', 'title:p===r?"Dahili":void 0'),
    ('{"aria-label":"Minimize",icon:"minus",onClick:e.run,shortcut:Yzs,tooltip:"Minimize"}', '{"aria-label":"Küçült",icon:"minus",onClick:e.run,shortcut:Yzs,tooltip:"Küçült"}'),
    ('{"aria-label":"Minimize",icon:"minus"', '{"aria-label":"Küçült",icon:"minus"'),
    # Görev Çıktı / Belge Rozetleri (Report -> Rapor)
    ('function jYC(t){return{label:t.label||t.name,href:t.href}}', 'function jYC(t){const _l=t.label||t.name;return{label:_l?.toLowerCase()==="report"?"Rapor":_l?.toLowerCase()==="plan"?"Plan":_l,href:t.href}}'),
    ('t.documents.map(o=>o.label||o.name)', 't.documents.map(o=>(o.label||o.name)?.toLowerCase()==="report"?"Rapor":(o.label||o.name))'),
    # Tarih ve Göreceli Zaman Biçimlendirmeleri (Today at / Yesterday at / X ago)
    ('return n===0?`Today at ${e}`:n===1?`Yesterday at ${e}`:n>=2&&n<=6?`${new Date(t).toLocaleDateString(void 0,{weekday:"long"})} at ${e}`:`${new Date(t).toLocaleDateString(void 0,{month:"short",day:"numeric",year:"numeric"})} at ${e}`',
     'return n===0?`Bugün ${e}`:n===1?`Dün ${e}`:n>=2&&n<=6?`${new Date(t).toLocaleDateString("tr-TR",{weekday:"long"})} ${e}`:`${new Date(t).toLocaleDateString("tr-TR",{month:"short",day:"numeric",year:"numeric"})} ${e}`'),
    ('return n<XNs?"just now":n<QNs?`${Math.floor(n/XNs)}m ago`:n<SFn?`${Math.floor(n/QNs)}h ago`:n<utc?`${Math.floor(n/SFn)}d ago`:n<dtc?`${Math.floor(n/utc)}w ago`:n<htc?`${Math.floor(n/dtc)}mo ago`:`${Math.floor(n/htc)}y ago`',
     'return n<XNs?"az önce":n<QNs?`${Math.floor(n/XNs)} dk önce`:n<SFn?`${Math.floor(n/QNs)} sa önce`:n<utc?`${Math.floor(n/SFn)} gün önce`:n<dtc?`${Math.floor(n/utc)} hf önce`:n<htc?`${Math.floor(n/dtc)} ay önce`:`${Math.floor(n/htc)} yıl önce`'),
    ('function Xxn(t,e){return e?`${t} ago`:t}', 'function Xxn(t,e){return e?`${t} önce`:t}'),
    ('h=s?`${s} ago`:"never marked closed"', 'h=s?`${s} önce`:"hiç kapatılmadı"'),
    ('`${oHb(e-t)} ago`', '`${oHb(e-t)} önce`'),
]

REGEX_REPS = [
    # Jenerik "This PC" / "This Mac" -> "Bu Bilgisayar" / "Bu Mac" eşleşmesi (tüm sürümlerde çalışır)
    (re.compile(r'([a-zA-Z0-9_$]+)\?"This PC":([a-zA-Z0-9_$]+)\?"This Mac":"This Computer"'),
     r'\1?"Bu Bilgisayar":\2?"Bu Mac":"Bu Bilgisayar"'),
    # Ortam Seçici Başlığı: Select Environment -> Ortam Seç
    (re.compile(r'title:([a-zA-Z0-9_$]+)\?\.title\?\?"Select Environment"'),
     r'title:\1?.title??"Ortam Seç"'),
    (re.compile(r'\{"aria-label":`\$\{([a-zA-Z0-9_$]+)\},\s*select environment`'),
     r'{"aria-label":`${\1}, ortam seç`'),
    # Depo Seçici Alt Menü Arama Kutuları: `Search ${BQ()}...` -> "Bu Bilgisayarda ara..."
    (re.compile(r'`Search \$\{([a-zA-Z0-9_$]+)\(\)\}\.\.\.`'),
     r'"Bu Bilgisayarda ara..."'),
    (re.compile(r'`Search \$\{([a-zA-Z0-9_$]+)\.name\}\.\.\.`'),
     r'`${\1.name} içinde ara...`'),
    (re.compile(r'"aria-label":`Search \$\{([a-zA-Z0-9_$]+)\.plural\}`,placeholder:`Search \$\{\1\.plural\}\.\.\.`'),
     r'"aria-label":`${\1.plural} içinde ara`,placeholder:`${\1.plural} içinde ara...`'),
    # Bilgisayar Kullanımı (Computer Use) minified değişken ataması
    (re.compile(r'([a-zA-Z0-9_$]+)="Computer Use",([a-zA-Z0-9_$]+)="Always-allowed apps:'),
     r'\1="Bilgisayar Kullanımı",\2="Always-allowed apps:'),
    # Özelleştir sayfası parçalı React dizileri: "Browse Marketplace" ve "Show X more"
    (re.compile(r'children:\["Show ",([a-zA-Z0-9_$]+)," more"\]'),
     r'children:[\1," tane daha göster"]'),
    (re.compile(r'children:\["Browse",([a-zA-Z0-9_$]+)\("span",\{className:"([^"]+)",children:" Marketplace"\}\)\]'),
     r'children:[\1("span",{className:"\2",children:"Eklenti Pazarına"})," Göz At"]'),
    # Sistem Tepsisi ve Proje Seçicide "No Repo" -> "Depo Yok" (minified değişken atamaları)
    (re.compile(r'([a-zA-Z0-9_$]+)="No Repo"'),
     r'\1="Depo Yok"'),
    (re.compile(r'([a-zA-Z0-9_$]+)="No-repo Automations"'),
     r'\1="Deposuz Otomasyonlar"'),
    # Mikrofon aygıt etiketleri: "Default - ..." -> "Varsayılan - ...", "Communications - ..." -> "İletişim - ..."
    (re.compile(r'label:([a-zA-Z0-9_$]+)\.label\|\|`Microphone \$\{([a-zA-Z0-9_$]+)\+1\}`'),
     r'label:(\1.label?\1.label.replace(/^Default - /,"Varsayılan - ").replace(/^Communications - /,"İletişim - "):`Mikrofon ${\2+1}`)'),
    # Gönderme Anahtar Kelimeleri (Submit Keywords / Voice Submit Keywords) jenerik regex (nd, dd, Kl vb.)
    (re.compile(r'([a-zA-Z0-9_$]+)\("voice","submit-keywords",\{label:"Submit Keywords"'),
     r'\1("voice","submit-keywords",{label:"Gönderme Anahtar Kelimeleri"'),
    (re.compile(r'([a-zA-Z0-9_$]+)\("chat","voice-submit-keywords",\{label:"Voice Submit Keywords"'),
     r'\1("chat","voice-submit-keywords",{label:"Sesli Gönderme Anahtar Kelimeleri"'),
    # Bağlam Ekleme (Attach) searchAliases jenerik regex (we, de, ue vb.)
    (re.compile(r'searchAliases:([a-zA-Z0-9_$]+)==="Attach"\?\["File","Files"\]:void 0'),
     r'searchAliases:\1==="Ekle"?["Dosya","Dosyalar","File","Files"]:void 0'),
    # Proje başlığı alt açıklaması: "Tracks the decisions, agent work, and follow-through needed to move X forward."
    (re.compile(r'`Tracks the decisions, agent work, and follow-through needed to move \$\{([a-zA-Z0-9_$]+)\} forward\.`'),
     r'`${\1} projesini ileriye taşımak için gereken kararları, ajan çalışmalarını ve takipleri izler.`'),
    (re.compile(r'"Tracks the decisions, agent work, and follow-through needed to move \$\{([a-zA-Z0-9_$]+)\} forward\."'),
     r'"${\1} projesini ileriye taşımak için gereken kararları, ajan çalışmalarını ve takipleri izler."'),
    # Tarih ayracı: "Today ${...}" -> "Bugün ${...}"
    (re.compile(r'\?`Today \$\{([a-zA-Z0-9_$]+)\}`:'),
     r'?`Bugün ${\1}`:'),
    (re.compile(r'\?"Today \$\{([a-zA-Z0-9_$]+)\}":'),
     r'?"Bugün ${\1}":'),
    # Klasör ekleme: "Add folder on ${...}" -> "${...} üzerinde klasör ekle"
    (re.compile(r'l=`Add folder on \$\{([a-zA-Z0-9_$]+)\}`'),
     r'l=`${\1} üzerinde klasör ekle`'),
    (re.compile(r'`Add folder on \$\{([a-zA-Z0-9_$]+)\}`'),
     r'`${\1} üzerinde klasör ekle`'),
    (re.compile(r'"Add folder on \$\{([a-zA-Z0-9_$]+)\}"'),
     r'"${\1} üzerinde klasör ekle"'),
    # Yeni Ajan Şablonları: "New Agent in ${...}" -> "${...} içinde Yeni Ajan"
    (re.compile(r':`New Agent in \$\{([a-zA-Z0-9_$]+)\.displayName\}`'),
     r':`${\1.displayName} içinde Yeni Ajan`'),
    (re.compile(r':`New Agent in \$\{([a-zA-Z0-9_$]+)\.name\}`'),
     r':`${\1.name} içinde Yeni Ajan`'),
    (re.compile(r':`New Agent in \$\{([a-zA-Z0-9_$]+)\}`'),
     r':`${\1} içinde Yeni Ajan`'),
    (re.compile(r'children:"New Agent in"'),
     r'children:"Şurada Yeni Ajan: "'),
    # Eklenti Yönetimi "Done" / "Edit" butonu: children:c?"Done":"Edit" -> children:c?"Bitti":"Düzenle"
    (re.compile(r'children:([a-zA-Z0-9_$]+)\?"Done":"Edit"'),
     r'children:\1?"Bitti":"Düzenle"'),
    (re.compile(r'children:([a-zA-Z0-9_$]+)\?`Done`:`Edit`'),
     r'children:\1?`Bitti`:`Düzenle`'),
    # Tam Ekran Buton Tooltip'i: "Exit Full Screen" / "Enter Full Screen"
    (re.compile(r'([a-zA-Z0-9_$]+)\?"Exit Full Screen":"Enter Full Screen"'),
     r'\1?"Tam Ekrandan Çık":"Tam Ekrana Geç"'),
    # Yanıt Değerlendirme (Good / Bad Response):
    (re.compile(r'([a-zA-Z0-9_$]+)==="up"\?"Good Response":"Bad Response"'),
     r'\1==="up"?"İyi Yanıt":"Kötü Yanıt"'),
    (re.compile(r'([a-zA-Z0-9_$]+)===`up`\?`Good Response`:`Bad Response`'),
     r'\1===`up`?`İyi Yanıt`:`Kötü Yanıt`'),
    # İletiyi Kopyala (data-tooltip-title ve aria-label)
    (re.compile(r'\[([a-zA-Z0-9_$]+)\]:"Copy Message"'),
     r'[\1]:"İletiyi Kopyala"'),
    (re.compile(r'([a-zA-Z0-9_$]+)\?"Copied":"Copy message"'),
     r'\1?"Kopyalandı":"İletiyi kopyala"'),
    (re.compile(r'([a-zA-Z0-9_$]+)\?"Copied!":"Copy Message"'),
     r'\1?"Kopyalandı!":"İletiyi Kopyala"'),
    (re.compile(r'\{id:"copy",label:([a-zA-Z0-9_$]+)\?"Copy Message":"Copy"'),
     r'{id:"copy",label:\1?"İletiyi Kopyala":"Kopyala"'),
    # Sohbeti Çatalla (data-tooltip-title ve aria-label)
    (re.compile(r'\[([a-zA-Z0-9_$]+)\]:"Fork Chat"'),
     r'[\1]:"Sohbeti Çatalla"'),
    (re.compile(r'([a-zA-Z0-9_$]+)\?"Forking chat":"Fork chat"'),
     r'\1?"Sohbet çatallanıyor...":"Sohbeti çatalla"'),
    # Yanıtla (data-tooltip-title ve aria-label)
    (re.compile(r'\[([a-zA-Z0-9_$]+)\]:"Reply","aria-label":"Reply"'),
     r'[\1]:"Yanıtla","aria-label":"Yanıtla"'),
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
