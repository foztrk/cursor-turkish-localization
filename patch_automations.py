# -*- coding: utf-8 -*-
"""
patch_automations.py: Cursor Otomasyonlar (workbench.anysphere-ui-automations.js)
arayuzunu Turkcelestirir.
"""
import io
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, 'workbench.anysphere-ui-automations.js')

AUTOMATIONS_MAP = {
    # Actions & Buttons
    'Action (optional)': 'Eylem (isteğe bağlı)',
    'Actions': 'Eylemler',
    'Active': 'Etkin',
    'Inactive': 'Etkin değil',
    'Add Automation': 'Otomasyon Ekle',
    'Add Environment': 'Ortam Ekle',
    'Add Repositories': 'Depolar Ekle',
    'Add memory notes...': 'Bellek notları ekleyin...',
    'Agents': 'Ajanlar',
    'All': 'Tümü',
    'All Automations': 'Tüm Otomasyonlar',
    'Any conclusion': 'Herhangi bir sonuç',
    'Any incident event': 'Herhangi bir olay',
    'Any issue event': 'Herhangi bir sorun olayı',
    'Any review': 'Herhangi bir inceleme',
    'Any status': 'Herhangi bir durum',
    'Anyone': 'Herkes',
    'Approved': 'Onaylandı',
    'Archived': 'Arşivlendi',
    'Assigned': 'Atandı',
    'Automation': 'Otomasyon',
    'Automation failed': 'Otomasyon başarısız oldu',
    'Automations': 'Otomasyonlar',
    'Available repositories': 'Kullanılabilir depolar',
    'Branch': 'Dal',
    'Branch (optional)': 'Dal (isteğe bağlı)',
    'Built-in': 'Yerleşik',
    'Cancel': 'İptal',
    'Cancel Run': 'Çalıştırmayı İptal Et',
    'Cancelled': 'İptal edildi',
    'Change owner': 'Sahibi değiştir',
    'Changes requested': 'Değişiklik istendi',
    'Channel Name': 'Kanal Adı',
    'Channel created': 'Kanal oluşturuldu',
    'Channel name...': 'Kanal adı...',
    'Checks completed': 'Denetimler tamamlandı',
    'Cloud Agent Environment': 'Bulut Ajanı Ortamı',
    'Code Review': 'Kod İncelemesi',
    'Commands': 'Komutlar',
    'Comment added': 'Yorum eklendi',
    'Comment on Pull Request': "Pull Request'e Yorum Yap",
    'Commented': 'Yorum yaptı',
    'Connect GitHub': "GitHub'ı Bağla",
    'Context (optional)': 'Bağlam (isteğe bağlı)',
    'Control how this automation is configured and updated': 'Bu otomasyonun nasıl yapılandırıldığını ve güncellendiğini denetleyin',
    'Copy as JSON': 'JSON Olarak Kopyala',
    'Counts tool calls made by the agent during the run.': 'Çalıştırma sırasında ajan tarafından yapılan araç çağrılarını sayar.',
    'Created': 'Oluşturulma',
    'Created by': 'Oluşturan',
    'Created by users': 'Kullanıcılar tarafından oluşturuldu',
    'Cron expression (UTC)': 'Cron ifadesi (UTC)',
    'Custom': 'Özel',
    'Custom (cron)': 'Özel (cron)',
    'Daily': 'Günlük',
    'Data & Research': 'Veri ve Araştırma',
    'Default': 'Varsayılan',
    'Defaults if empty': 'Boşsa varsayılanlar kullanılır',
    'Definition': 'Tanım',
    'Delete': 'Sil',
    'Draft opened': 'Taslak açıldı',
    'Duplicate': 'Çoğalt',
    'Each metric scores a completed automation run.': 'Her metrik, tamamlanan bir otomasyon çalıştırmasını puanlar.',
    'Edit Automation': 'Otomasyonu Düzenle',
    'Edit Details': 'Ayrıntıları Düzenle',
    'End of cycle': 'Döngü sonu',
    'Environment': 'Ortam',
    'Evals': 'Değerlendirmeler',
    'Event Type': 'Olay Türü',
    'Explore': 'Keşfet',
    'Failed': 'Başarısız',
    'Failure': 'Başarısızlık',
    'Filter by': 'Filtreleme ölçütü',
    'Git event': 'Git olayı',
    'Hourly': 'Saatlik',
    'Incident Acknowledged': 'Olay Kabul Edildi',
    'Incident Escalated': 'Olay Yükseltildi',
    'Incident ID (optional)': 'Olay Kimliği (isteğe bağlı)',
    'Incident Resolved': 'Olay Çözüldü',
    'Incident Triggered': 'Olay Tetiklendi',
    'Incidents & Triage': 'Olaylar ve Önceliklendirme',
    'Issue ID (optional)': 'Sorun Kimliği (isteğe bağlı)',
    'Issue Identifier': 'Sorun Tanımlayıcısı',
    'Issue comment': 'Sorun yorumu',
    'JSON Payload (optional)': 'JSON Yükü (isteğe bağlı)',
    'Judged Metrics': 'Değerlendirilen Metrikler',
    'Label change': 'Etiket değişikliği',
    'Label name...': 'Etiket adı...',
    'Last 1h': 'Son 1 saat',
    'Last 24h': 'Son 24 saat',
    'Last 7d': 'Son 7 gün',
    'Last updated': 'Son güncelleme',
    'Loading more repositories...': 'Daha fazla depo yükleniyor...',
    'MAX Mode': 'MAX Modu',
    'MCP Servers': 'MCP Sunucuları',
    'Manage with code [DEV]': 'Kod ile yönet [DEV]',
    'Memories': 'Bellekler',
    'Memory Notes': 'Bellek Notları',
    'Merged': 'Birleştirildi',
    'Message Type': 'Mesaj Türü',
    'Microsoft Teams': 'Microsoft Teams',
    'Mine': 'Benimkiler',
    'Model': 'Model',
    'My Machines': 'Makinelerim',
    'Name': 'Ad',
    'New Automation': 'Yeni Otomasyon',
    'New message in channel': 'Kanalda yeni mesaj',
    'New push to branch': 'Dala yeni push',
    'No automations found': 'Otomasyon bulunamadı',
    'Off': 'Kapalı',
    'Open': 'Açık',
    'Open Pull Request': 'Pull Request Aç',
    'Opened': 'Açıldı',
    'Options': 'Seçenekler',
    'PR Number': 'PR Numarası',
    'PR approved': 'PR onaylandı',
    'PR review comment': 'PR inceleme yorumu',
    'PR review submitted...': 'PR incelemesi gönderildi...',
    'Pending': 'Bekliyor',
    'Popular': 'Popüler',
    'Project ID (optional)': 'Proje Kimliği (isteğe bağlı)',
    'Pull request or merge request': 'Pull request veya merge request',
    'Pushed': 'Push yapıldı',
    'Reacted Message': 'Tepki Verilen Mesaj',
    'Reaction added to message': 'Mesaja tepki eklendi',
    'Read Microsoft Teams Channels': 'Microsoft Teams Kanallarını Oku',
    'Read Public Slack Channels': 'Herkese Açık Slack Kanallarını Oku',
    'Recent': 'Son Kullanılanlar',
    'Ref / Branch': 'Referans / Dal',
    'Repository': 'Depo',
    'Request Reviewers': 'İncelemeci Talep Et',
    'Resolved': 'Çözüldü',
    'Retry': 'Yeniden Dene',
    'Run summary': 'Çalıştırma özeti',
    'Runs': 'Çalıştırmalar',
    'Save and Enable': 'Kaydet ve Etkinleştir',
    'Save or discard changes before continuing': 'Devam etmeden önce değişiklikleri kaydedin veya silin',
    'Schedule': 'Zamanlama',
    'Scheduled': 'Zamanlanmış',
    'Scheduled run': 'Zamanlanmış çalıştırma',
    'Search Sentry projects...': "Sentry projelerini ara...",
    'Search Triggers...': 'Tetikleyicileri Ara...',
    'Search automations': 'Otomasyonları ara',
    'Search branches...': 'Dalları ara...',
    'Search channels or paste channel ID...': 'Kanalları arayın veya kanal kimliğini yapıştırın...',
    'Search environments': 'Ortamları ara',
    'Search members': 'Üyeleri ara',
    'Search models...': 'Modelleri ara...',
    'Search projects...': 'Projeleri ara...',
    'Search services...': 'Hizmetleri ara...',
    'Search static metrics': 'Statik metrikleri ara',
    'Search statuses...': 'Durumları ara...',
    'Search teammates': 'Ekip arkadaşlarını ara',
    'Search teams...': 'Ekipleri ara...',
    'Security': 'Güvenlik',
    'Select Team': 'Ekip Seçin',
    'Send to Microsoft Teams': "Microsoft Teams'e Gönder",
    'Send to Slack': "Slack'e Gönder",
    'Skills': 'Beceriler',
    'Skipped': 'Atlandı',
    'Sort by': 'Sıralama ölçütü',
    'Source Control': 'Kaynak Denetimi',
    'Static Metrics': 'Statik Metrikler',
    'Status': 'Durum',
    'Status changed': 'Durum değişti',
    'Success': 'Başarılı',
    'Target': 'Hedef',
    'Team': 'Ekip',
    'Templates': 'Şablonlar',
    'Test Message': 'Test Mesajı',
    'Test run': 'Test çalıştırması',
    'Tool call count': 'Araç çağrısı sayısı',
    'Tools': 'Araçlar',
    'Transfer this automation to another team member.': 'Bu otomasyonu başka bir ekip üyesine aktarın.',
    'Trigger': 'Tetikleyici',
    'Triggered': 'Tetiklendi',
    'Triggers': 'Tetikleyiciler',
    'Type': 'Tür',
    'Type @ for tools, / for commands...': 'Araçlar için @, komutlar için / yazın...',
    'Unknown trigger': 'Bilinmeyen tetikleyici',
    'Unresolved': 'Çözülmedi',
    'Unsaved Changes': 'Kaydedilmemiş Değişiklikler',
    'Update Access': 'Erişimi Güncelle',
    'Update Automation Access?': 'Otomasyon Erişimi Güncellensin mi?',
    'Upgrade your app to view this trigger in the UI': 'Bu tetikleyiciyi arayüzde görüntülemek için uygulamanızı güncelleyin',
    'Use Multiple Models': 'Birden Fazla Model Kullan',
    'User': 'Kullanıcı',
    'Users': 'Kullanıcılar',
    'View and edit files the agent keeps in memories/': "Ajanın memories/ içinde tuttuğu dosyaları görüntüleyin ve düzenleyin",
    'View details': 'Ayrıntıları görüntüle',
    'Webhook': 'Webhook',
    'Webhook Triggered': 'Webhook Tetiklendi',
    'Webhook triggered': 'Webhook tetiklendi',
    'Weekly': 'Haftalık',
    'Workflow run completed...': 'İş akışı çalıştırması tamamlandı...',
}

EXACT_REPLACEMENTS = [
    # Galeri ve Gösterim Sayısı (Image 1)
    ('children:["Showing ",', 'children:["Gösterilen: ",'),
    ('children:"More"', 'children:"Tümü"'),
    ('j=r?.more??"More"', 'j=r?.more??"Tümü"'),
    ('N=r?.suggested??"Suggested"', 'N=r?.suggested??"Önerilen"'),
    ('children:_?"Loading\\u2026":"Load More"', 'children:_?"Yükleniyor\\u2026":"Daha Fazla Yükle"'),
    # Sekmeler
    ('{value:"mine",label:"Mine"}', '{value:"mine",label:"Benimkiler"}'),
    ('{value:"team",label:"Team"}', '{value:"team",label:"Ekip"}'),
    ('{value:"explore",label:"Explore"}', '{value:"explore",label:"Keşfet"}'),
    ('{value:"evals",label:"Evals"}', '{value:"evals",label:"Değerlendirmeler"}'),
    # Başlık ve durum
    ('?"All Automations":', '?"Tüm Otomasyonlar":'),
    ('?"No automations found":', '?"Otomasyon bulunamadı":'),
    ('?"New Automation":', '?"Yeni Otomasyon":'),
    ('n==="Add Automation"?"New Automation":n', 'n==="Add Automation"?"Yeni Otomasyon":n'),
    # Filtre / Tetikleyici Seçici Özetleri
    ('?"Any status":', '?"Herhangi bir durum":'),
    ('??"1 status":', '??"1 durum":'),
    ('statuses`', 'durum`'),
    ('?"Any Team":', '?"Herhangi bir Ekip":'),
    ('??"1 team":', '??"1 ekip":'),
    ('teams`', 'ekip`'),
    ('?"Any Service":', '?"Herhangi bir Hizmet":'),
    ('services`', 'hizmet`'),
    ('?"Any Project":', '?"Herhangi bir Proje":'),
    ('projects`', 'proje`'),
    ('?"Projects Unavailable":', '?"Projeler Kullanılamıyor":'),
    ('?"Select Repos":', '?"Depoları Seçin":'),
    ('?"Select Channel":', '?"Kanal Seçin":'),
    ('channels`', 'kanal`'),
    ('?"Select state":', '?"Durum seçin":'),
    ('?"Any review":', '?"Herhangi bir inceleme":'),
    ('?"any workflow":', '?"herhangi bir iş akışı":'),
    ('workflows`', 'iş akışı`'),
    ('?"Specific People":', '?"Belirli Kişiler":'),
    ('?"1 person":', '?"1 kişi":'),
    ('people`', 'kişi`'),
    ('?"Select a repo first":"Select exactly one repo to pick a branch"', '?"Önce bir depo seçin":"Bir dal seçmek için tam olarak bir depo seçin"'),
    # İzinler ve çalışma açıklamaları
    ('ator"?"The creator":"You"', 'ator"?"Oluşturan":"Siz"'),
    ('`Runs as ${r} for billing and connected integrations`', '`Faturalandırma ve bağlı entegrasyonlar için ${r} olarak çalışır`'),
    ('`Only ${r} can edit it`', '`Yalnızca ${r} düzenleyebilir`'),
    ('"Team admins can still view, disable, or delete it"', '"Ekip yöneticileri yine de görüntüleyebilir, devre dışı bırakabilir veya silebilir"'),
    ('"Everyone on your team can view it"', '"Ekibinizdeki herkes görüntüleyebilir"'),
    ('"Team admins can still disable or delete it"', '"Ekip yöneticileri yine de devre dışı bırakabilir veya silebilir"'),
    ('"Everyone on your team can edit or disable it"', '"Ekibinizdeki herkes düzenleyebilir veya devre dışı bırakabilir"'),
    ('`Only ${r} can add MCP tools that authenticate as ${r}`', '`Yalnızca ${r}, ${r} olarak kimlik doğrulayan MCP araçları ekleyebilir`'),
    ('`${o} and team admins can delete it`', '`${o} ve ekip yöneticileri silebilir`'),
    ('["Runs as your team\'s service account for billing and connected integrations"', '["Faturalandırma ve bağlı entegrasyonlar için ekibinizin hizmet hesabı olarak çalışır"'),
]

PROPS = ['label', 'title', 'placeholder', 'heading', 'buttonText', 'description', 'tooltip', 'children', 'aria-label']


def patch_file(path):
    if not os.path.exists(path):
        return 0
    with io.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    mods = 0
    # 1. Birebir kalıplar
    for old_s, new_s in EXACT_REPLACEMENTS:
        cnt = content.count(old_s)
        if cnt:
            content = content.replace(old_s, new_s)
            mods += cnt

    # 2. UI propları ve JSX
    for en, tr in AUTOMATIONS_MAP.items():
        for p in PROPS:
            t1 = f'{p}:"{en}"'
            if t1 in content:
                cnt = content.count(t1)
                content = content.replace(t1, f'{p}:"{tr}"')
                mods += cnt

            t2 = f"{p}:'{en}'"
            if t2 in content:
                cnt = content.count(t2)
                content = content.replace(t2, f"{p}:'{tr}'")
                mods += cnt

            t3 = f'{p}:`{en}`'
            if t3 in content:
                cnt = content.count(t3)
                content = content.replace(t3, f'{p}:`{tr}`')
                mods += cnt

        # JSX text
        jsx_t = f'>{en}<'
        if jsx_t in content:
            cnt = content.count(jsx_t)
            content = content.replace(jsx_t, f'>{tr}<')
            mods += cnt

    if mods > 0:
        with io.open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)

    return mods


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else TARGET
    mods = patch_file(target)
    print(f"patch_automations.py -> workbench.anysphere-ui-automations.js: {mods} otomasyon arayuzu metni cevrildi")


if __name__ == '__main__':
    main()
