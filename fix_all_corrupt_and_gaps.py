# -*- coding: utf-8 -*-
"""
fix_all_corrupt_and_gaps.py
1. Kurulum bozuk uyarısını (IntegrityService) regex ile kökten etkisiz hale getirir.
2. Uzak makine, mobil yönetim, QR kod indirme metinlerini Türkçeleştirir.
3. Depo arama ve boş liste ('No repos') metinlerini Türkçeleştirir.
4. Karışık MCP ipucunu ('Yapılandır MCPs in your...') düzeltir.
5. Plan ve Kullanım sayfasındaki 'Usage limits reset on...', 'days left' ve '% used' ifadelerini regex ile Türkçeleştirir.
"""
import io, os, sys, re, json

BASE = os.path.dirname(os.path.abspath(__file__))
GLASS_PATH = os.path.join(BASE, "workbench.glass.main.js")
DESK_PATH = os.path.join(BASE, "workbench.desktop.main.js")

print("Dosyalar okunuyor...")
with io.open(GLASS_PATH, "r", encoding="utf-8") as f:
    glass = f.read()

with io.open(DESK_PATH, "r", encoding="utf-8") as f:
    desk = f.read()

glass_mods = 0
desk_mods = 0

def regex_replace(source, pattern, replacement, name=""):
    new_src, count = re.subn(pattern, replacement, source)
    if count > 0:
        print(f"  [OK] {name} ({count} eslesme)")
        return new_src, count
    else:
        print(f"  [ATLANDI] {name} (hedef bulunamadi)")
        return source, 0

def safe_replace(source, target, replacement, name=""):
    if target in source:
        source = source.replace(target, replacement)
        print(f"  [OK] {name}")
        return source, 1
    else:
        print(f"  [ATLANDI] {name} (hedef bulunamadi)")
        return source, 0

print("\n--- 1. KURULUM BOZUK UYARISINI KOKTEN ENGELLEME ---")
# Glass main
glass, n = regex_replace(
    glass,
    r'async _isPure\(\)\{const (\w+)=this\.productService\.checksums\|\|\{\};',
    r'async _isPure(){return{isPure:!0,proof:[]}}async _isPure_old(){const \1=this.productService.checksums||{};',
    "Glass _isPure bypass"
)
glass_mods += n

glass, n = regex_replace(
    glass,
    r'async _compute\(\)\{const\{isPure:(\w+)\}=await this\.isPure\(\);if\(\1\|\|await this\._isExplainedByPendingUpdate\(\)\)return;this\.logService\.warn\(',
    r'async _compute(){return;}async _compute_old(){const{isPure:\1}=await this.isPure();if(\1||await this._isExplainedByPendingUpdate())return;this.logService.warn(',
    "Glass _compute bypass"
)
glass_mods += n

# Desktop main
desk, n = regex_replace(
    desk,
    r'async _isPure\(\)\{const (\w+)=this\.productService\.checksums\|\|\{\};',
    r'async _isPure(){return{isPure:!0,proof:[]}}async _isPure_old(){const \1=this.productService.checksums||{};',
    "Desktop _isPure bypass"
)
desk_mods += n

desk, n = regex_replace(
    desk,
    r'async _compute\(\)\{const\{isPure:(\w+)\}=await this\.isPure\(\);if\(\1\|\|await this\._isExplainedByPendingUpdate\(\)\)return;this\.logService\.warn\(',
    r'async _compute(){return;}async _compute_old(){const{isPure:\1}=await this.isPure();if(\1||await this._isExplainedByPendingUpdate())return;this.logService.warn(',
    "Desktop _compute bypass"
)
desk_mods += n


print("\n--- 2. UZAK MAKINE, MOBIL DENETIM VE QR KOD METINLERI ---")
remote_vars = [
    ("Remote Machine", "Uzak Makine"),
    ("All Remote Machines", "Tüm Uzak Makineler"),
    ("Control agents on this machine from mobile", "Bu makinedeki ajanları mobilden denetleyin"),
    ("Scan this QR code to download Cursor for your phone", "Telefonunuza Cursor indirmek için bu QR kodunu tarayın"),
    ("Steer agents on this machine from mobile", "Bu makinedeki ajanları mobilden yönetin"),
    ("Run cloud agents on this machine", "Bulut ajanlarını bu makinede çalıştırın"),
    ("Coming soon", "Çok yakında"),
]
for src_var, tr_text in remote_vars:
    glass, n = regex_replace(glass, rf'(\b\w+)="{re.escape(src_var)}"', rf'\1="{tr_text}"', f"Glass: {src_var}")
    glass_mods += n
    desk, n = regex_replace(desk, rf'(\b\w+)="{re.escape(src_var)}"', rf'\1="{tr_text}"', f"Desk: {src_var}")
    desk_mods += n

common_remote = [
    ('{id:"shared-pool",label:"Remote Machines"}', '{id:"shared-pool",label:"Uzak Makineler"}', "shared-pool Remote Machines"),
    ('{id:"remote-control",label:"Remote Control"}', '{id:"remote-control",label:"Uzaktan Denetim"}', "remote-control label"),
    ('"Search Remote Machines\\u2026"', '"Uzak Makinelerde Ara\\u2026"', "Search Remote Machines placeholder"),
    ("Couldn't load Remote Machines. Close and reopen to retry.", "Uzak Makineler yüklenemedi. Kapatıp yeniden açarak tekrar deneyin.", "Couldn't load Remote Machines"),
]
for t, r, name in common_remote:
    glass, n = safe_replace(glass, t, r, f"Glass: {name}")
    glass_mods += n
    desk, n = safe_replace(desk, t, r, f"Desk: {name}")
    desk_mods += n


print("\n--- 3. DEPO ARAMA VE 'NO REPOS' METINLERI ---")
repo_reps_glass = [
    ('T==="workspace"?"Search workspaces...":"Search repos, cloud environments..."',
     'T==="workspace"?"Çalışma alanlarında ara...":"Depolarda, bulut ortamlarında ara..."',
     "Search repos, cloud environments"),
    ('earch remote repos, cloud environments...":T==="workspace"?"Search workspaces...":"Search repos, cloud environments..."',
     'earch remote repos, cloud environments...":T==="workspace"?"Çalışma alanlarında ara...":"Depolarda, bulut ortamlarında ara..."',
     "Search remote repos"),
    ('Search repositories, environments...":T==="workspace"?"Search workspaces...":"Run Cursor anywhere..."',
     'Depolarda, ortamlarda ara...":T==="workspace"?"Çalışma alanlarında ara...":"Cursor\'ı her yerde çalıştırın..."',
     "Search repositories environments"),
    ('const T=b?"No repos":Pof;', 'const T=b?"Depo Yok":Pof;', "b?No repos:Pof"),
    ('Pof="No environments"', 'Pof="Ortam Yok"', "Pof No environments"),
    ('emptyLabel:"No repos selected"', 'emptyLabel:"Depo seçilmedi"', "emptyLabel No repos selected"),
    ('children:i!==void 0?"No repositories":Y.type==="cloud"?"No repos":"No projects"',
     'children:i!==void 0?"Depo Yok":Y.type==="cloud"?"Depo Yok":"Proje Yok"',
     "No repositories / No repos / No projects"),
    ('["No repos or pools match \\u201C",_,"\\u201D."]', '["Eşleşen depo veya havuz yok: \\u201C",_,"\\u201D."]', "No repos match"),
    ('children:"No repositories found"', 'children:"Depo bulunamadı"', "No repositories found"),
]
for target, rep, name in repo_reps_glass:
    glass, n = safe_replace(glass, target, rep, f"Glass: {name}")
    glass_mods += n


print("\n--- 4. KARISIK MCP IPUCU DUZELTMESI ---")
mcp_mixed = [
    ("Yapılandır MCPs in your Cursor Ayarlar to give agents access to tools and data",
     "Ajanların araçlara ve verilere erişebilmesi için Cursor Ayarları'nda MCP'leri yapılandırın"),
    ("Yapılandır MCPs in your Cursor Ayarları to give agents access to tools and data",
     "Ajanların araçlara ve verilere erişebilmesi için Cursor Ayarları'nda MCP'leri yapılandırın"),
    ("Configure MCPs in your Cursor Settings to give agents access to tools and data",
     "Ajanların araçlara ve verilere erişebilmesi için Cursor Ayarları'nda MCP'leri yapılandırın"),
    ("Configure MCPs in your Cursor Ayarlar to give agents access to tools and data",
     "Ajanların araçlara ve verilere erişebilmesi için Cursor Ayarları'nda MCP'leri yapılandırın"),
]
for target, rep in mcp_mixed:
    glass, n = safe_replace(glass, target, rep, f"Glass: MCP {target[:30]}...")
    glass_mods += n
    desk, n = safe_replace(desk, target, rep, f"Desk: MCP {target[:30]}...")
    desk_mods += n


print("\n--- 5. PLAN VE KULLANIM (PLAN & USAGE) SAYFASI ---")
# Usage limits reset on (Regex for any function wrapper)
glass, n = regex_replace(glass, r'children:\["Usage limits reset on "', r'children:["Kullanım limitleri sıfırlanma tarihi: "', "Glass Usage limits reset on")
glass_mods += n
desk, n = regex_replace(desk, r'children:\["Usage limits reset on "', r'children:["Kullanım limitleri sıfırlanma tarihi: "', "Desk Usage limits reset on")
desk_mods += n

# Countdown days left
glass, n = regex_replace(glass, r'const a=Math\.ceil\((\w+)\/(\w+)\);return`\$\{a\} day\$\{a===1\?"":"s"\} left`',
                         r'const a=Math.ceil(\1/\2);return`${a} gün kaldı`', "Glass days left")
glass_mods += n
desk, n = regex_replace(desk, r'const a=Math\.ceil\((\w+)\/(\w+)\);return`\$\{a\} day\$\{a===1\?"":"s"\} left`',
                        r'const a=Math.ceil(\1/\2);return`${a} gün kaldı`', "Desk days left")
desk_mods += n

# Countdown hours and minutes
glass, n = regex_replace(glass, r'return (\w+)>0&&(\w+)>0\?`\$\{\1\} hour\$\{\1===1\?"":"s"\} and \$\{\2\} minute\$\{\2===1\?"":"s"\} left`:\1>0\?`\$\{\1\} hour\$\{\1===1\?"":"s"\} left`:`\$\{\2\} minute\$\{\2===1\?"":"s"\} left`',
                         r'return \1>0&&\2>0?`${\1} saat ${\2} dakika kaldı`:\1>0?`${\1} saat kaldı`:`${\2} dakika kaldı`', "Glass hours/mins left")
glass_mods += n
desk, n = regex_replace(desk, r'return (\w+)>0&&(\w+)>0\?`\$\{\1\} hour\$\{\1===1\?"":"s"\} and \$\{\2\} minute\$\{\2===1\?"":"s"\} left`:\1>0\?`\$\{\1\} hour\$\{\1===1\?"":"s"\} left`:`\$\{\2\} minute\$\{\2===1\?"":"s"\} left`',
                        r'return \1>0&&\2>0?`${\1} saat ${\2} dakika kaldı`:\1>0?`${\1} saat kaldı`:`${\2} dakika kaldı`', "Desk hours/mins left")
desk_mods += n

# % used
glass, n = regex_replace(glass, r'function (\w+)\((\w+)\)\{return`\$\{(\w+)\(\2\)\}% used`\}',
                         r'function \1(\2){return`%${\3(\2)} kullanıldı`}', "Glass % used")
glass_mods += n
desk, n = regex_replace(desk, r'function (\w+)\((\w+)\)\{return`\$\{(\w+)\(\2\)\}% used`\}',
                        r'function \1(\2){return`%${\3(\2)} kullanıldı`}', "Desk % used")
desk_mods += n

# Dual % used
glass, n = regex_replace(glass, r'return`\$\{(\w+)\.autoTitle\}:\s*\$\{(\w+)\}% used\s*\\xB7\s*\$\{\1\.apiTitle\}:\s*\$\{(\w+)\}% used`',
                         r'return`${\1.autoTitle}: %${\2} kullanıldı \\xB7 ${\1.apiTitle}: %${\3} kullanıldı`', "Glass dual % used")
glass_mods += n
desk, n = regex_replace(desk, r'return`\$\{(\w+)\.autoTitle\}:\s*\$\{(\w+)\}% used\s*\\xB7\s*\$\{\1\.apiTitle\}:\s*\$\{(\w+)\}% used`',
                        r'return`${\1.autoTitle}: %${\2} kullanıldı \\xB7 ${\1.apiTitle}: %${\3} kullanıldı`', "Desk dual % used")
desk_mods += n

# Inline % used children: [x, "% used"]
glass, n = regex_replace(glass, r'children:\[(.*?),\"% used\"\]', r'children:["%",\1," kullanıldı"]', "Glass inline % used")
glass_mods += n
desk, n = regex_replace(desk, r'children:\[(.*?),\"% used\"\]', r'children:["%",\1," kullanıldı"]', "Desk inline % used")
desk_mods += n


print("\n--- 7. YENİ EKLENEN PROJELER VE GROK BOT ALANLARI ---")
# Projects header in sidebar
glass, n = regex_replace(
    glass,
    r'(\b\w+)=\{sectionLabel:"Projects",singularLabel:"Project",newLabel:"Yeni Proje"\}',
    r'\1={sectionLabel:"Projeler",singularLabel:"Proje",newLabel:"Yeni Proje"}',
    "Projects sectionLabel"
)
glass_mods += n

# Create project subtitle and input
glass, n = regex_replace(
    glass,
    r'(\b\w+)="Create a focused chat where Agents coordinate work"',
    r'\1="Ajanların çalışmaları koordine ettiği odaklanmış bir sohbet oluşturun"',
    "Create project subtitle"
)
glass_mods += n

glass, n = regex_replace(
    glass,
    r'(\b\w+)="Project name"',
    r'\1="Proje adı"',
    "Project name input"
)
glass_mods += n

# Dropdown "Repos" header
glass, n = regex_replace(
    glass,
    r'pe==="cloud"\?"Repos":',
    r'pe==="cloud"?"Depolar":',
    "Cloud picker Repos header"
)
glass_mods += n

# Grok Bot banner
glass, n = regex_replace(
    glass,
    r'title:"Meet Grok Bot"',
    r'title:"Grok Bot ile Tanışın"',
    "Meet Grok Bot title"
)
glass_mods += n

glass, n = regex_replace(
    glass,
    r'ariaLabel:"Meet Grok Bot"',
    r'ariaLabel:"Grok Bot ile Tanışın"',
    "Meet Grok Bot ariaLabel"
)
glass_mods += n

glass, n = regex_replace(
    glass,
    r'description:"AI teammates you can give real work to"',
    r'description:"Gerçek işler verebileceğiniz yapay zekâ ekip arkadaşları"',
    "Grok Bot description"
)
glass_mods += n

glass, n = regex_replace(
    glass,
    r'action:\{label:"Get Grok Bot",onClick:(\w+)\}',
    r'action:{label:"Grok Bot\'u Edin",onClick:\1}',
    "Get Grok Bot action"
)
glass_mods += n

glass, n = regex_replace(
    glass,
    r'c=a===void 0\?"Dismiss":a',
    r'c=a===void 0?"Kapat":a',
    "Grok banner Dismiss label"
)
glass_mods += n

glass, n = regex_replace(
    glass,
    r'title:"Grok Bot can do this for you"',
    r'title:"Grok Bot bunu sizin için yapabilir"',
    "Grok Bot contextual title"
)
glass_mods += n

glass, n = regex_replace(
    glass,
    r'description:"An AI teammate that works in your tools and comes back with finished work\."',
    r'description:"Araçlarınızda çalışan ve bitmiş işle geri dönen bir yapay zekâ ekip arkadaşı."',
    "Grok Bot contextual description"
)
glass_mods += n


print("\n--- 6. DOM OBSERVER SÖZLÜĞÜNE EK GÜVENCE KAYITLARI ---")
observer_pattern = r'(\["File", "Dosya"\],)'
observer_replacement = (
    r'\1\n'
    r'    ["Remote Machine", "Uzak Makine"],\n'
    r'    ["Remote Machines", "Uzak Makineler"],\n'
    r'    ["Remote Control", "Uzaktan Denetim"],\n'
    r'    ["Control agents on this machine from mobile", "Bu makinedeki ajanları mobilden denetleyin"],\n'
    r'    ["Steer agents on this machine from mobile", "Bu makinedeki ajanları mobilden yönetin"],\n'
    r'    ["Scan this QR code to download Cursor for your phone", "Telefonunuza Cursor indirmek için bu QR kodunu tarayın"],\n'
    r'    ["Search repos, cloud environments...", "Depolarda, bulut ortamlarında ara..."],\n'
    r'    ["Search remote repos, cloud environments...", "Uzak depolarda, bulut ortamlarında ara..."],\n'
    r'    ["Search remote repos...", "Uzak depolarda ara..."],\n'
    r'    ["Search Bu Bilgisayar...", "Bu Bilgisayarda ara..."],\n'
    r'    ["No repos", "Depo Yok"],\n'
    r'    ["No environments", "Ortam Yok"],\n'
    r'    ["Refresh model list", "Model Listesini Yenile"],\n'
    r'    ["Not now", "Şimdi Değil"],\n'
    r'    ["Usage limits reset on", "Kullanım limitleri sıfırlanma tarihi:"],'
)
glass, n = regex_replace(glass, observer_pattern, observer_replacement, "Glass Observer expansion")
glass_mods += n
desk, n = regex_replace(desk, observer_pattern, observer_replacement, "Desk Observer expansion")
desk_mods += n

print("\n--- 7. DÖNEN İPUÇLARI (ROTATING TIPS) KAYNAK SEVİYESİ ÇEVİRİSİ ---")
# 1. Template regex değişkenini ve yTC fonksiyonunu dinamik bulup tam Türkçe yap
m_rgx = re.search(r'(\w+)=/\\{\\{\\s\*key:', glass)
if m_rgx:
    rgx_var = m_rgx.group(1)
    pat_ytc = rf'function (\w+)\(([a-zA-Z0-9_]+),([a-zA-Z0-9_]+)\)\{{return \2\.replace\({rgx_var},'
    m_fn = re.search(pat_ytc, glass)
    if m_fn:
        fn_name = m_fn.group(1)
        txt_param = m_fn.group(2)
        res_param = m_fn.group(3)
        ytc_replacement = (
            f'function {fn_name}({txt_param},{res_param}){{\n'
            f'  const _tips = {{\n'
            f'    "Ask Cursor to find a prior conversation, or summarize across conversations": "Önceki bir konuşmayı bulmak için Cursor\'a sorun veya konuşmalar genelinde özetleyin",\n'
            f'    "Search Cursor to find a prior conversation, or summarize across conversations": "Önceki bir konuşmayı bulmak için Cursor\'da arayın veya konuşmalar genelinde özetleyin",\n'
            f'    "Sor Cursor to find a prior conversation, veya summarize across conversations": "Önceki bir konuşmayı bulmak için Cursor\'a sorun veya konuşmalar genelinde özetleyin",\n'
            f'    "Tip dismissed. You can turn off future tips in Settings": "İpucu gizlendi. Gelecekteki ipuçlarını Ayarlar\'dan kapatabilirsiniz",\n'
            f'    "Use /in-cloud for cloud subagents": "Bulut alt ajanları için /in-cloud kullanın"\n'
            f'  }};\n'
            f'  if (_tips[{txt_param}]) {txt_param} = _tips[{txt_param}];\n'
            f'  else if (/find a prior conversation|across conversations/i.test({txt_param})) {{\n'
            f'    {txt_param} = "Önceki bir konuşmayı bulmak için Cursor\'a sorun veya konuşmalar genelinde özetleyin";\n'
            f'  }}\n'
            f'  return {txt_param}.replace({rgx_var},'
        )
        glass, n = regex_replace(glass, pat_ytc, ytc_replacement, "Glass yTC rotating tip dynamic translation")
        glass_mods += n
    else:
        print("  [ATLANDI] yTC fonksiyonu bulunamadi")
else:
    print("  [ATLANDI] Template regex degiskeni bulunamadi")

# 2. Tip dismissed ve Hide tips butonunu doğrudan kaynakta çevir
glass, n = safe_replace(
    glass,
    '"Tip dismissed. You can turn off future tips in Settings"',
    '"İpucu gizlendi. Gelecekteki ipuçlarını Ayarlar\'dan kapatabilirsiniz"',
    "Glass Tip dismissed"
)
glass_mods += n

glass, n = safe_replace(
    glass,
    '"Hide tips"',
    '"İpuçlarını gizle"',
    "Glass Hide tips"
)
glass_mods += n

print("\n--- 8. GÜNCELLEME BİLDİRİMİ (UPDATE NOTIFICATION TOAST & BANNER) ---")
# Kullanıcının ekran görüntüsündeki "New update available" ve "Later" kutucuğu
update_notification_strings = [
    ('<span class=minor-version-notification-text>New update available</span>',
     '<span class=minor-version-notification-text>Yeni güncelleme mevcut</span>',
     "New update available text"),
    ('<p class=update-notification-eyebrow>Update to v</p>',
     '<p class=update-notification-eyebrow>Sürüme güncelle: v</p>',
     "Update to v eyebrow"),
    ('<span>New in </span>',
     '<span>Yenilikler: </span>',
     "New in text"),
    ('children:"Later"',
     'children:"Daha Sonra"',
     "Later button"),
    ('children:"Install Now"',
     'children:"Şimdi Yükle"',
     "Install Now button"),
    ('children:"Changelog"',
     'children:"Değişiklik Günlüğü"',
     "Changelog button"),
    ('children:"Restart to Update"',
     'children:"Güncellemek için Yeniden Başlat"',
     "Restart to Update button"),
    ('children:"Restart to update"',
     'children:"Güncellemek için Yeniden Başlat"',
     "Restart to update button (lowercase)"),
    ('title:{value:"Attempt Update",original:"Attempt Update"}',
     'title:{value:"Güncellemeyi Dene",original:"Güncellemeyi Dene"}',
     "Attempt Update command title"),
]

for old_str, new_str, label in update_notification_strings:
    glass, n = safe_replace(glass, old_str, new_str, f"Glass: {label}")
    glass_mods += n
    desk, n = safe_replace(desk, old_str, new_str, f"Desk: {label}")
    desk_mods += n

print("\n--- 9. YENİ PROJE, DEPO OLUŞTURMA VE ORTAM SEÇİCİ ---")
# 1. Depo Oluştur / Create repo pill butonu (sohbet girişinin üstü)
glass, n = safe_replace(
    glass,
    '{id:"create-repo",content:db(C7,{loading:JPe.isWaitingForSuggestions,onClick:JPe.openTray,children:"Create repo"})',
    '{id:"create-repo",content:db(C7,{loading:JPe.isWaitingForSuggestions,onClick:JPe.openTray,children:"Depo oluştur"})',
    "Glass: Create repo pill button"
)
glass_mods += n

# 2. Create repo çekmecesi (tray) başlık ve butonları
repo_tray_strings = [
    ('ne=X&&v?"Next":N?"Creating...":"Create repository";return qMn(bi.Root,{className:"glass-create-repo-tray"',
     'ne=X&&v?"İleri":N?"Oluşturuluyor...":"Depo oluştur";return qMn(bi.Root,{className:"glass-create-repo-tray"',
     "Create repo tray next/creating/create repo"),
    ('children:bae(bi.HeaderTitle,{tone:"muted",children:"Create repository"})',
     'children:bae(bi.HeaderTitle,{tone:"muted",children:"Depo oluştur"})',
     "Create repo header title"),
    ('children:[bae("span",{children:"What should we name your repository?"}),bae("span",{className:"glass-4b2ntj glass-1wm8ruf glass-1fcty0u",children:"It\'ll be saved to Cursor Origin, so you can come back to it anytime."})]',
     'children:[bae("span",{children:"Deponuzun adı ne olsun?"}),bae("span",{className:"glass-4b2ntj glass-1wm8ruf glass-1fcty0u",children:"Cursor Origin\'e kaydedilecek, böylece istediğiniz zaman geri dönebilirsiniz."})]',
     "What should we name your repository"),
    ('labelSuffix:re===0&&!ae?"Recommended":void 0',
     'labelSuffix:re===0&&!ae?"Önerilen":void 0',
     "Recommended suffix"),
    ('title:"Who can see the code?",children:[bae(bi.Option,{description:`Only you and ${_} codebase admins`,id:"private",index:0,label:"Private",labelStyle:"number",onSelect:()=>P("private"),selected:A==="private",stepId:$ws}),bae(bi.Option,{description:`Anyone with access to the ${_} codebase`,id:"internal",index:1,label:"Internal",labelStyle:"number",onSelect:()=>P("internal"),selected:A==="internal",stepId:$ws})]}',
     'title:"Kodu kimler görebilir?",children:[bae(bi.Option,{description:`Yalnızca siz ve ${_} kod tabanı yöneticisi`,id:"private",index:0,label:"Özel",labelStyle:"number",onSelect:()=>P("private"),selected:A==="private",stepId:$ws}),bae(bi.Option,{description:`${_} kod tabanına erişimi olan herkes`,id:"internal",index:1,label:"Dahili",labelStyle:"number",onSelect:()=>P("internal"),selected:A==="internal",stepId:$ws})]}',
     "Who can see the code options"),
    ('textInputPlaceholder:"repository-name"',
     'textInputPlaceholder:"depo-adi"',
     "Repo text input placeholder"),
    ('l.error(ae instanceof Error?ae.message:"Couldn\'t create the repository. Please try again.")',
     'l.error(ae instanceof Error?ae.message:"Depo oluşturulamadı. Lütfen tekrar deneyin.")',
     "Couldn't create the repository"),
]
for old_s, new_s, lbl in repo_tray_strings:
    glass, n = safe_replace(glass, old_s, new_s, f"Glass: {lbl}")
    glass_mods += n

# 3. Alt bar ve seçicilerde Ortam (Bulut / Yerel / Bu Bilgisayar)
env_strings_glass = [
    ('locationName:u.runtime==="cloud"?"Cloud":JK()',
     'locationName:u.runtime==="cloud"?"Bulut":JK()',
     "locationName cloud runtime"),
    (',locationName:"Cloud",locationIcon:"cloud"',
     ',locationName:"Bulut",locationIcon:"cloud"',
     "locationName Bulut assignment"),
    (r'\xB7 Cloud',
     r'\xB7 Bulut',
     "tooltip dot Bulut"),
    ('{id:"cloud",label:"Cloud"},{id:"local",label:"Local"}',
     '{id:"cloud",label:"Bulut"},{id:"local",label:"Yerel"}',
     "Environment section headers Bulut/Yerel"),
    ('title:ee?"Select Repository":"Select Workspace"',
     'title:ee?"Depo Seç":"Çalışma Alanı Seç"',
     "title Select Repository / Workspace"),
    ('projectName:E?"Select Repository":"Select Workspace"',
     'projectName:E?"Depo Seç":"Çalışma Alanı Seç"',
     "projectName Select Repository / Workspace"),
    ('Pu(ZS,{ignoreSearch:!0,label:"Cloud",leading:Pu(Ft,{name:"cloud"}),onSelect:()=>a(nt),trailing:TVt(e)?Pu(Ft,{name:"check"}):void 0,tooltip:Pu(t2n,{}),children:Pu(Da.TextItem,{inline:!0,title:"Cloud"})},"multi-repo-cloud")',
     'Pu(ZS,{ignoreSearch:!0,label:"Bulut",leading:Pu(Ft,{name:"cloud"}),onSelect:()=>a(nt),trailing:TVt(e)?Pu(Ft,{name:"check"}):void 0,tooltip:Pu(t2n,{}),children:Pu(Da.TextItem,{inline:!0,title:"Bulut"})},"multi-repo-cloud")',
     "multi-repo-cloud Bulut"),
    ('Pu(ZS,{ignoreSearch:!0,label:"Cloud",leading:Pu(Ft,{name:"cloud"}),onSelect:()=>a(dki()),trailing:H6(e)?Pu(Ft,{name:"check"}):void 0,tooltip:Pu(t2n,{}),children:Pu(Da.TextItem,{inline:!0,title:"Cloud"})},"no-repo-cloud")',
     'Pu(ZS,{ignoreSearch:!0,label:"Bulut",leading:Pu(Ft,{name:"cloud"}),onSelect:()=>a(dki()),trailing:H6(e)?Pu(Ft,{name:"check"}):void 0,tooltip:Pu(t2n,{}),children:Pu(Da.TextItem,{inline:!0,title:"Bulut"})},"no-repo-cloud")',
     "no-repo-cloud Bulut"),
    ('Pu(ZS,{disabled:!0,ignoreSearch:!0,label:"Cloud",leading:Pu(Ft,{name:"cloud"}),tooltip:Pu(vUk,{onLearnMore:ve}),children:Pu(Da.TextItem,{inline:!0,title:"Cloud"})},"cloud-unavailable")',
     'Pu(ZS,{disabled:!0,ignoreSearch:!0,label:"Bulut",leading:Pu(Ft,{name:"cloud"}),tooltip:Pu(vUk,{onLearnMore:ve}),children:Pu(Da.TextItem,{inline:!0,title:"Bulut"})},"cloud-unavailable")',
     "cloud-unavailable Bulut"),
    ('Pu(ZS,{disabled:!0,ignoreSearch:!0,label:"Cloud",leading:Pu(Ft,{name:"cloud"}),trailing:Pu(Ft,{modifier:"spin",name:"loading"}),tooltip:Pu(t2n,{}),children:Pu(Da.TextItem,{inline:!0,title:"Cloud"})},"cloud-pending")',
     'Pu(ZS,{disabled:!0,ignoreSearch:!0,label:"Bulut",leading:Pu(Ft,{name:"cloud"}),trailing:Pu(Ft,{modifier:"spin",name:"loading"}),tooltip:Pu(t2n,{}),children:Pu(Da.TextItem,{inline:!0,title:"Bulut"})},"cloud-pending")',
     "cloud-pending Bulut"),
    ('Pu(ZS,{ignoreSearch:!0,label:"Cloud",leading:Pu(Ft,{name:"cloud"}),onSelect:()=>a(nt),trailing:TVt(e)?Pu(Ft,{name:"check"}):void 0,tooltip:Pu(t2n,{}),children:Pu(Da.TextItem,{inline:!0,title:"Cloud"})},"redesign-cloud")',
     'Pu(ZS,{ignoreSearch:!0,label:"Bulut",leading:Pu(Ft,{name:"cloud"}),onSelect:()=>a(nt),trailing:TVt(e)?Pu(Ft,{name:"check"}):void 0,tooltip:Pu(t2n,{}),children:Pu(Da.TextItem,{inline:!0,title:"Bulut"})},"redesign-cloud")',
     "redesign-cloud Bulut"),
    ('placeholder:t="Type a message..."',
     'placeholder:t="Bir mesaj yazın..."',
     "Type a message placeholder"),
    ('uzf={kind:"readonly",icon:"cloud",label:"Cloud"}',
     'uzf={kind:"readonly",icon:"cloud",label:"Bulut"}',
     "Status bar readonly Cloud to Bulut"),
    ('(s_(e)?"Cloud":n.icon===void 0?JK():n.tooltip)',
     '(s_(e)?"Bulut":n.icon===void 0?JK():n.tooltip)',
     "Status bar gzw Cloud to Bulut"),
    ('subtitle:Se!==void 0?`${Se} tokens`:void 0,title:`${Ce} context used`',
     'subtitle:Se!==void 0?`${Se} belirteç`:void 0,title:`${Ce} bağlam kullanıldı`',
     "Status bar context used tooltip"),
    ('d7m=_t("<span> context used")',
     'd7m=_t("<span> bağlam kullanıldı")',
     "Glass context used template span"),
    ('` \\xB7 ${Brt(je.tokensUsed)} / ${Brt(je.tokenLimit,!1)} context used`',
     '` \\xB7 ${Brt(je.tokensUsed)} / ${Brt(je.tokenLimit,!1)} bağlam kullanıldı`',
     "Glass context used rule info"),
    ('context used`:nt+=" context used"',
     'bağlam kullanıldı`:nt+=" bağlam kullanıldı"',
     "Glass context used summary"),
    ('`Context ${Ce}`',
     '`Bağlam ${Ce}`',
     "Glass context button aria label"),
    ('`${r} environment`',
     '`${r} ortamı`',
     "Glass environment aria label r"),
    ('`${s} environment`',
     '`${s} ortamı`',
     "Glass environment aria label s"),
    ('"Cloud Agent Approval Banners While Focused"',
     '"Odaklanmışken Bulut Ajanı Onay Banner\'ları"',
     "Cloud Agent Approval Banners While Focused"),
    ('"Also show the approval banner while Cursor is focused; the request card in the agent conversation always shows"',
     '"Cursor odaktayken de onay banner\'ını göster; ajan konuşmasındaki istek kartı her zaman gösterilir"',
     "Cloud Agent Approval Banners description"),
    ('label:"Origin Notifications"',
     'label:"Origin Bildirimleri"',
     "Origin Notifications label"),
    ('"Notify when Origin pull requests you follow are merged, closed, reviewed, or fail CI"',
     '"Takip ettiğiniz Origin pull request\'leri birleştirildiğinde, kapatıldığında, incelendiğinde veya CI başarısız olduğunda bildirim gönder"',
     "Origin Notifications description"),
]
glass, n = regex_replace(
    glass,
    r'function ([a-zA-Z0-9_$]+)\(\)\{return ([a-zA-Z0-9_$]+)\?"This PC":([a-zA-Z0-9_$]+)\?"This Mac":"This Computer"\}',
    r'function \1(){return \2?"Bu Bilgisayar":\3?"Bu Mac":"Bu Bilgisayar"}',
    "Glass: Jenerik This PC to Bu Bilgisayar"
)
glass_mods += n

for old_s, new_s, lbl in env_strings_glass:
    glass, n = safe_replace(glass, old_s, new_s, f"Glass: {lbl}")
    glass_mods += n

# 4. Desktop bundle için Bu Bilgisayar ve Bağlam Kullanımı
desk, n = regex_replace(
    desk,
    r'function ([a-zA-Z0-9_$]+)\(\)\{return ([a-zA-Z0-9_$]+)\?"This PC":([a-zA-Z0-9_$]+)\?"This Mac":"This Computer"\}',
    r'function \1(){return \2?"Bu Bilgisayar":\3?"Bu Mac":"Bu Bilgisayar"}',
    "Desk: Jenerik This PC to Bu Bilgisayar"
)
desk_mods += n

desk_context_strings = [
    ('E0b=ft("<span> context used")',
     'E0b=ft("<span> bağlam kullanıldı")',
     "Desk: context used template span"),
    ('context used`:Gt+=" context used"',
     'bağlam kullanıldı`:Gt+=" bağlam kullanıldı"',
     "Desk: context used summary"),
    ('` \\xB7 ${J4e(St.tokensUsed)} / ${J4e(St.tokenLimit,!1)} context used`',
     '` \\xB7 ${J4e(St.tokensUsed)} / ${J4e(St.tokenLimit,!1)} bağlam kullanıldı`',
     "Desk: context used rule info"),
    ('"Cloud Agent Approval Banners While Focused"',
     '"Odaklanmışken Bulut Ajanı Onay Banner\'ları"',
     "Desk: Cloud Agent Approval Banners While Focused"),
    ('"Also show the approval banner while Cursor is focused; the request card in the agent conversation always shows"',
     '"Cursor odaktayken de onay banner\'ını göster; ajan konuşmasındaki istek kartı her zaman gösterilir"',
     "Desk: Cloud Agent Approval Banners description"),
    ('label:"Origin Notifications"',
     'label:"Origin Bildirimleri"',
     "Desk: Origin Notifications label"),
    ('"Notify when Origin pull requests you follow are merged, closed, reviewed, or fail CI"',
     '"Takip ettiğiniz Origin pull request\'leri birleştirildiğinde, kapatıldığında, incelendiğinde veya CI başarısız olduğunda bildirim gönder"',
     "Desk: Origin Notifications description"),
]
for old_s, new_s, lbl in desk_context_strings:
    desk, n = safe_replace(desk, old_s, new_s, f"Desk: {lbl}")
    desk_mods += n

print("\nDosyalar diske yazılıyor...")
with io.open(GLASS_PATH, "w", encoding="utf-8", newline="") as f:
    f.write(glass)

with io.open(DESK_PATH, "w", encoding="utf-8", newline="") as f:
    f.write(desk)

print("JS dosyaları başarıyla kaydedildi!")
print(f"\nToplam Yapılan Değişiklik: Glass={glass_mods}, Desktop={desk_mods}")
print("BÜTÜN İŞLEMLER BAŞARIYLA TAMAMLANDI!")
