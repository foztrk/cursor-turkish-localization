# -*- coding: utf-8 -*-
"""Gec olusturulan IDE menulerinde kalan son Ingilizce etiketler."""
import io, os

FILES = ['workbench.desktop.main.js', 'workbench.glass.main.js']
MARKER = 'CURSOR_TR_MENU_GAPS_V1'
CORE_MARKERS = [
    'CURSOR_TR_UI_PATCH_V5', 'CURSOR_TR_UI_EXPANSION_V1',
    'CURSOR_TR_IDE_SURFACE_V1', 'CURSOR_TR_IDE_SURFACE_V2',
    'CURSOR_TR_SMALL_DIALOGS_V1', 'CURSOR_TR_SETTINGS_V1',
    'CURSOR_TR_SETTINGS_V2',
]

# Bunlar yalnizca kullaniciya gorunen komut/menu basliklaridir. Kod kimlikleri
# (zenMode, auxiliaryBar vb.) ayridir ve degistirilmez.
STATIC = {
    'loadingAction:"Reading",completedAction:"Read"': 'loadingAction:"Okunuyor",completedAction:"Okundu"',
    'loadingAction:"Using",completedAction:"Used"': 'loadingAction:"Kullanılıyor",completedAction:"Kullanıldı"',
    'loadingAction:c?.loadingAction??"Exploring"': 'loadingAction:c?.loadingAction??"Keşfediliyor"',
    'loadingAction:l?.loadingAction??"Exploring"': 'loadingAction:l?.loadingAction??"Keşfediliyor"',
    'text:o??`${t} file${t===1?"":"s"}`': 'text:o??`${t} dosya`',
    'compactText:o!==void 0?"1 file":void 0': 'compactText:o!==void 0?"1 dosya":void 0',
    'text:o??`${e} file${e===1?"":"s"}`': 'text:o??`${e} dosya`',
    'action:"Clicked"': 'action:"Tıklandı"',
    'action:"Clicked on page"': 'action:"Sayfaya tıklandı"',
    'action:"Navigated to"': 'action:"Gidildi:"',
    'action:"Took snapshot"': 'action:"Anlık görüntü alındı"',
    'action:"Typed"': 'action:"Yazıldı"',
    'action:"Filled"': 'action:"Dolduruldu"',
    '"Add a follow-up"': '"Takip mesajı ekle"',
    '"Add a follow up"': '"Takip mesajı ekle"',
    '"Allow agents on this computer to be controlled remotely from mobile"': '"Bu bilgisayardaki ajanların mobilden uzaktan denetlenmesine izin ver"',
    '"Allow agents on this computer to be controlled remotely from mobile"': '"Bu bilgisayardaki ajanlar\\u0131n mobilden uzaktan denetlenmesine izin ver"',
    '"Turn Remote Control on again to reset this computer"': '"Bu bilgisayar\\u0131 s\\u0131f\\u0131rlamak i\\xe7in Uzaktan Denetim\'i tekrar a\\xe7\\u0131n"',
    '"Trusted Devices"': '"G\\xfcvenilen Cihazlar"',
    '"No other devices are approved for Remote Control yet"': '"Hen\\xfcz Uzaktan Denetim i\\xe7in onaylanm\\u0131\\u015f ba\\u015fka cihaz yok"',
    '"Enable Remote Control for this computer"': '"Bu bilgisayar i\\xe7in Uzaktan Denetim\'i etkinle\\u015ftir"',
    '{id:"mcps",label:"MCPs"}': '{id:"mcps",label:"MCP\'ler"}',
    '{id:"tools",label:"MCPs"}': '{id:"tools",label:"MCP\'ler"}',
    'title:"MCPs"': 'title:"MCP\'ler"',
    'var XQ="No Repository"': 'var XQ="Depo Yok"',
    'placeholder:"Search repositories..."': 'placeholder:"Depolarda ara..."',
    'placeholder:"Search repositories"': 'placeholder:"Depolarda ara"',
    'placeholder:"Search repositories, environments..."': 'placeholder:"Depolarda ve ortamlarda ara..."',
    'ce?"Stopping...":"Stop All Runs"': 'ce?"Durduruluyor...":"T\\xfcm \\xc7al\\u0131\\u015ft\\u0131rmalar\\u0131 Durdur"',
    'breadcrumbLabel:"Runs"': 'breadcrumbLabel:"\\xc7al\\u0131\\u015ft\\u0131rmalar"',
    'placeholder:"Search runs..."': 'placeholder:"\\xc7al\\u0131\\u015ft\\u0131rmalarda ara..."',
    'currentLabel:"Runs"': 'currentLabel:"\\xc7al\\u0131\\u015ft\\u0131rmalar"',
    'title:"Runs"': 'title:"\\xc7al\\u0131\\u015ft\\u0131rmalar"',
    '{href:"#runs",label:"Runs"': '{href:"#runs",label:"\\xc7al\\u0131\\u015ft\\u0131rmalar"',
    'header:"Trigger"': 'header:"Tetikleyici"',
    'header:"Triggered"': 'header:"Tetiklendi"',
    'header:"Duration"': 'header:"S\\xfcre"',
    'header:b??"Automation"': 'header:b??"Otomasyon"',
    'title:"Memory Notes",description:"View and edit files the agent keeps in memories/"': 'title:"Haf\\u0131za Notlar\\u0131",description:"Ajan\\u0131n memories/ dizininde tuttu\\u011fu dosyalar\\u0131 g\\xf6r\\xfcnt\\xfcleyin ve d\\xfczenleyin"',
    'placeholder:"Add memory notes..."': 'placeholder:"Haf\\u0131za notlar\\u0131 ekleyin..."',
    'className:Ie({rootClass:"ui-automations-memories-modal__field-label",stylexStyles:dQt(),className:"automations-memories-modal__field-label"}).className,children:"Content"}': 'className:Ie({rootClass:"ui-automations-memories-modal__field-label",stylexStyles:dQt(),className:"automations-memories-modal__field-label"}).className,children:"\\u0130\\xe7erik"}',
    'disabled:i.isLoadingMemory||u!==null||!i.isDirty,children:"Reset"}': 'disabled:i.isLoadingMemory||u!==null||!i.isDirty,children:"S\\u0131f\\u0131rla"}',
    'children:u==="delete"?"Deleting...":i.feedback.kind==="delete-confirmation"?"Confirm delete":"Delete"': 'children:u==="delete"?"Siliniyor...":i.feedback.kind==="delete-confirmation"?"Silmeyi Onayla":"Sil"',
    'children:"Failed to load memory content. Please try again later."': 'children:"Haf\\u0131za i\\xe7eri\\u011fi y\\xfcklenemedi. L\\xfctfen daha sonra tekrar deneyin."',
    'E=i.isLoadingFiles?"Loading...":"Select a file"': 'E=i.isLoadingFiles?"Y\\xfckleniyor...":"Bir Dosya Se\\xe7in"',
    'u==="save"?"Saving...":"Save"': 'u==="save"?"Kaydediliyor...":"Kaydet"',
    'offerTitle:"Use your skills with Cloud Agents",offerDescription:"Sync your local skills to use them with Cloud Agents. Any changes will update automatically.",offerAction:"Sync",offerDismiss:"Not now"': 'offerTitle:"Becerilerinizi Bulut Ajanlar\\u0131 ile Kullan\\u0131n",offerDescription:"Yerel becerilerinizi Bulut Ajanlar\\u0131 ile kullanmak i\\xe7in e\\u015fitleyin. T\\xfcm de\\u011fi\\u015fiklikler otomatik olarak g\\xfcncellenir.",offerAction:"E\\u015fitle",offerDismiss:"\\u015eimdi De\\u011fil"',
    '"Syncing your skills\\u2026"': '"Becerileriniz e\\u015fitleniyor\\u2026"',
    '"Moving your skills back to this machine\\u2026"': '"Becerileriniz bu makineye geri ta\\u015f\\u0131n\\u0131yor\\u2026"',
    '"Open config"': '"Yap\\u0131land\\u0131rmay\\u0131 A\\xe7"',
    'sourceLabel:"User Rule"': 'sourceLabel:"Kullan\\u0131c\\u0131 Kural\\u0131"',
    'case"plugin":return"Plugin";case"extension":return"Extension";case"user":case void 0:return"User"': 'case"plugin":return"Eklenti";case"extension":return"Uzant\\u0131";case"user":case void 0:return"Kullan\\u0131c\\u0131"',
    'title:"Workspaces"': 'title:"\\xc7al\\u0131\\u015fma Alanlar\\u0131"',
    'workspaces:"Workspaces"': 'workspaces:"\\xc7al\\u0131\\u015fma Alanlar\\u0131"',
    '"No tools, prompts, or resources"': '"Ara\\xe7, istem veya kaynak yok"',
    '${e.enabledToolCount} tools`),(e.promptCount??0)>0&&t.push(`${e.promptCount} prompts`),(e.resourceCount??0)>0&&t.push(`${e.resourceCount} resources`),t.length>0?`${t.join(", ")} enabled`': '${e.enabledToolCount} ara\\xe7`),(e.promptCount??0)>0&&t.push(`${e.promptCount} istem`),(e.resourceCount??0)>0&&t.push(`${e.resourceCount} kaynak`),t.length>0?`${t.join(", ")} etkin`',
    '${t.enabledToolCount} tools`),(t.promptCount??0)>0&&e.push(`${t.promptCount} prompts`),(t.resourceCount??0)>0&&e.push(`${t.resourceCount} resources`),e.length>0?`${e.join(", ")} enabled`': '${t.enabledToolCount} ara\\xe7`),(t.promptCount??0)>0&&e.push(`${t.promptCount} istem`),(t.resourceCount??0)>0&&e.push(`${t.resourceCount} kaynak`),e.length>0?`${e.join(", ")} etkin`',
    "function gxi(e,t,n){if(e.variants.length!==0)return ASn(e,t,n)}": "function gxi(e,t,n){if(e.variants.length!==0){const v=ASn(e,t,n);if(!v)return v;const tr=s=>typeof s===\"string\"?s.replace(\"High Fast\",\"Y\\xfcksek H\\u0131zl\\u0131\").replace(\"Medium Fast\",\"Orta H\\u0131zl\\u0131\").replace(\"Low Fast\",\"D\\xfc\\u015f\\xfck H\\u0131zl\\u0131\").replace(\"No Thinking\",\"D\\xfc\\u015f\\xfcnme Yok\").replace(/\\bHigh$/,\"Y\\xfcksek\").replace(/\\bMedium$/,\"Orta\").replace(/\\bLow$/,\"D\\xfc\\u015f\\xfck\").replace(/\\bMax$/,\"Azami\").replace(/\\bFast$/,\"H\\u0131zl\\u0131\"):s;return{...v,displayName:tr(v.displayName),displayNameOutsidePicker:tr(v.displayNameOutsidePicker)}}}",
    "function Lfn(t,e,n){if(t.variants.length!==0)return Nfn(t,e,n)}": "function Lfn(t,e,n){if(t.variants.length!==0){const v=Nfn(t,e,n);if(!v)return v;const tr=s=>typeof s===\"string\"?s.replace(\"High Fast\",\"Y\\xfcksek H\\u0131zl\\u0131\").replace(\"Medium Fast\",\"Orta H\\u0131zl\\u0131\").replace(\"Low Fast\",\"D\\xfc\\u015f\\xfck H\\u0131zl\\u0131\").replace(\"No Thinking\",\"D\\xfc\\u015f\\xfcnme Yok\").replace(/\\bHigh$/,\"Y\\xfcksek\").replace(/\\bMedium$/,\"Orta\").replace(/\\bLow$/,\"D\\xfc\\u015f\\xfck\").replace(/\\bMax$/,\"Azami\").replace(/\\bFast$/,\"H\\u0131zl\\u0131\"):s;return{...v,displayName:tr(v.displayName),displayNameOutsidePicker:tr(v.displayNameOutsidePicker)}}}",
    "pxi(i,e.parameters,n);return r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name}": "pxi(i,e.parameters,n);return (r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name)?.replace?.(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\")?.replace?.(\"Medium Fast\",\"Orta H\u0131zl\u0131\")?.replace?.(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\")?.replace?.(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(/\\bHigh$/,\"Y\xfcksek\")?.replace?.(/\\bMedium$/,\"Orta\")?.replace?.(/\\bLow$/,\"D\xfc\u015f\xfck\")?.replace?.(/\\bMax$/,\"Azami\")?.replace?.(/\\bFast$/,\"H\u0131zl\u0131\")}",
    "Nfn(i,t.parameters,n);return r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name}": "Nfn(i,t.parameters,n);return (r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name)?.replace?.(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\")?.replace?.(\"Medium Fast\",\"Orta H\u0131zl\u0131\")?.replace?.(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\")?.replace?.(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(/\\bHigh$/,\"Y\xfcksek\")?.replace?.(/\\bMedium$/,\"Orta\")?.replace?.(/\\bLow$/,\"D\xfc\u015f\xfck\")?.replace?.(/\\bMax$/,\"Azami\")?.replace?.(/\\bFast$/,\"H\u0131zl\u0131\")}",
    "gxi(i,e.parameters,n);return r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name}": "gxi(i,e.parameters,n);return (r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name)?.replace?.(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\")?.replace?.(\"Medium Fast\",\"Orta H\u0131zl\u0131\")?.replace?.(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\")?.replace?.(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(/\\bHigh$/,\"Y\xfcksek\")?.replace?.(/\\bMedium$/,\"Orta\")?.replace?.(/\\bLow$/,\"D\xfc\u015f\xfck\")?.replace?.(/\\bMax$/,\"Azami\")?.replace?.(/\\bFast$/,\"H\u0131zl\u0131\")}",
    "Lfn(i,t.parameters,n);return r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name}": "Lfn(i,t.parameters,n);return (r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name)?.replace?.(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\")?.replace?.(\"Medium Fast\",\"Orta H\u0131zl\u0131\")?.replace?.(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\")?.replace?.(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(/\\bHigh$/,\"Y\xfcksek\")?.replace?.(/\\bMedium$/,\"Orta\")?.replace?.(/\\bLow$/,\"D\xfc\u015f\xfck\")?.replace?.(/\\bMax$/,\"Azami\")?.replace?.(/\\bFast$/,\"H\u0131zl\u0131\")}",
    "gxi(i,e.parameters,n);return (r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name)?.replace?.(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\")?.replace?.(\"Medium Fast\",\"Orta H\u0131zl\u0131\")?.replace?.(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\")?.replace?.(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\")}": "gxi(i,e.parameters,n);return (r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name)?.replace?.(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\")?.replace?.(\"Medium Fast\",\"Orta H\u0131zl\u0131\")?.replace?.(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\")?.replace?.(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(/\\bHigh$/,\"Y\xfcksek\")?.replace?.(/\\bMedium$/,\"Orta\")?.replace?.(/\\bLow$/,\"D\xfc\u015f\xfck\")?.replace?.(/\\bMax$/,\"Azami\")?.replace?.(/\\bFast$/,\"H\u0131zl\u0131\")}",
    "Lfn(i,t.parameters,n);return (r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name)?.replace?.(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\")?.replace?.(\"Medium Fast\",\"Orta H\u0131zl\u0131\")?.replace?.(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\")?.replace?.(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\")}": "Lfn(i,t.parameters,n);return (r?.displayNameOutsidePicker??r?.displayName??i.inputboxShortModelName??i.clientDisplayName??i.name)?.replace?.(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\")?.replace?.(\"Medium Fast\",\"Orta H\u0131zl\u0131\")?.replace?.(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\")?.replace?.(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\")?.replace?.(/\\bHigh$/,\"Y\xfcksek\")?.replace?.(/\\bMedium$/,\"Orta\")?.replace?.(/\\bLow$/,\"D\xfc\u015f\xfck\")?.replace?.(/\\bMax$/,\"Azami\")?.replace?.(/\\bFast$/,\"H\u0131zl\u0131\")}",
    "c=i.displayName;let l;if(t[0]!==c||t[1]!==o)": "c=(i.displayName||\"\").replace(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\").replace(\"Medium Fast\",\"Orta H\u0131zl\u0131\").replace(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\").replace(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\").replace(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\").replace(/\\bHigh$/,\"Y\xfcksek\").replace(/\\bMedium$/,\"Orta\").replace(/\\bLow$/,\"D\xfc\u015f\xfck\").replace(/\\bMax$/,\"Azami\").replace(/\\bFast$/,\"H\u0131zl\u0131\");let l;if(t[0]!==c||t[1]!==o)",
    "l=i.displayName;let c;if(e[0]!==l||e[1]!==o)": "l=(i.displayName||\"\").replace(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\").replace(\"Medium Fast\",\"Orta H\u0131zl\u0131\").replace(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\").replace(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\").replace(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\").replace(/\\bHigh$/,\"Y\xfcksek\").replace(/\\bMedium$/,\"Orta\").replace(/\\bLow$/,\"D\xfc\u015f\xfck\").replace(/\\bMax$/,\"Azami\").replace(/\\bFast$/,\"H\u0131zl\u0131\");let c;if(e[0]!==l||e[1]!==o)",
    "c=(i.displayName||\"\").replace(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\").replace(\"Medium Fast\",\"Orta H\u0131zl\u0131\").replace(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\").replace(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\").replace(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\");let l;if(t[0]!==c||t[1]!==o)": "c=(i.displayName||\"\").replace(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\").replace(\"Medium Fast\",\"Orta H\u0131zl\u0131\").replace(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\").replace(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\").replace(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\").replace(/\\bHigh$/,\"Y\xfcksek\").replace(/\\bMedium$/,\"Orta\").replace(/\\bLow$/,\"D\xfc\u015f\xfck\").replace(/\\bMax$/,\"Azami\").replace(/\\bFast$/,\"H\u0131zl\u0131\");let l;if(t[0]!==c||t[1]!==o)",
    "l=(i.displayName||\"\").replace(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\").replace(\"Medium Fast\",\"Orta H\u0131zl\u0131\").replace(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\").replace(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\").replace(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\");let c;if(e[0]!==l||e[1]!==o)": "l=(i.displayName||\"\").replace(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\").replace(\"Medium Fast\",\"Orta H\u0131zl\u0131\").replace(\"Low Fast\",\"D\xfc\u015f\xfck H\u0131zl\u0131\").replace(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\").replace(\"No thinking\",\"D\xfc\u015f\xfcnme Yok\").replace(/\\bHigh$/,\"Y\xfcksek\").replace(/\\bMedium$/,\"Orta\").replace(/\\bLow$/,\"D\xfc\u015f\xfck\").replace(/\\bMax$/,\"Azami\").replace(/\\bFast$/,\"H\u0131zl\u0131\");let c;if(e[0]!==l||e[1]!==o)",
    "t[3]!==n?(u=R0(\"div\",{...s,\"data-testid\":\"parameter-submenu-title\",children:n}),t[3]=n,t[4]=u):u=t[4]": "t[3]!==n?(u=R0(\"div\",{...s,\"data-testid\":\"parameter-submenu-title\",children:typeof n===\"string\"?n.replace(\"(fast)\",\"(h\u0131zl\u0131)\").replace(\"(Fast)\",\"(H\u0131zl\u0131)\").replace(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\").replace(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\"):n}),t[3]=n,t[4]=u):u=t[4]",
    "e[3]!==n?(u=Rx(\"div\",{...s,\"data-testid\":\"parameter-submenu-title\",children:n}),e[3]=n,e[4]=u):u=e[4]": "e[3]!==n?(u=Rx(\"div\",{...s,\"data-testid\":\"parameter-submenu-title\",children:typeof n===\"string\"?n.replace(\"(fast)\",\"(h\u0131zl\u0131)\").replace(\"(Fast)\",\"(H\u0131zl\u0131)\").replace(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\").replace(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\"):n}),e[3]=n,e[4]=u):u=e[4]",
    "t[3]!==n?(u=N0(\"div\",{...s,\"data-testid\":\"parameter-submenu-title\",children:n}),t[3]=n,t[4]=u):u=t[4]": "t[3]!==n?(u=N0(\"div\",{...s,\"data-testid\":\"parameter-submenu-title\",children:typeof n===\"string\"?n.replace(\"(fast)\",\"(h\u0131zl\u0131)\").replace(\"(Fast)\",\"(H\u0131zl\u0131)\").replace(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\").replace(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\"):n}),t[3]=n,t[4]=u):u=t[4]",
    "e[3]!==n?(u=Dx(\"div\",{...s,\"data-testid\":\"parameter-submenu-title\",children:n}),e[3]=n,e[4]=u):u=e[4]": "e[3]!==n?(u=Dx(\"div\",{...s,\"data-testid\":\"parameter-submenu-title\",children:typeof n===\"string\"?n.replace(\"(fast)\",\"(h\u0131zl\u0131)\").replace(\"(Fast)\",\"(H\u0131zl\u0131)\").replace(\"High Fast\",\"Y\xfcksek H\u0131zl\u0131\").replace(\"No Thinking\",\"D\xfc\u015f\xfcnme Yok\"):n}),e[3]=n,e[4]=u):u=e[4]",
    '"No additional models available. Add a non-thinking model in Settings."': '"Kullan\u0131labilir ek model yok. Ayarlar\'dan d\xfc\u015f\xfcnme \xf6zelli\u011fi olmayan bir model ekleyin."',
    '"New Agents Window"': '"Yeni Ajanlar Penceresi"',
    '"Zen Mode"': '"Zen Modu"',
    '"Secondary Side Bar"': '"İkincil Kenar Çubuğu"',
    '"Render Whitespace"': '"Boşluk Karakterlerini Göster"',
    'children:"Ship better code, faster"': 'children:"Daha iyi kodu daha hızlı üretin"',
    'children:"Name"': 'children:"Ad"',
    'children:"Created by"': 'children:"Oluşturan"',
    'children:"Status"': 'children:"Durum"',
    '"Inactive"': '"Etkin Değil"',
    '"Memories"': '"Anılar"',
    '"Toggle automation enabled state"': '"Otomasyonun etkinliğini aç veya kapat"',
    '"Automation detail sections"': '"Otomasyon ayrıntı bölümleri"',
    '"Control agents on this machine from your phone, web, and other devices"': '"Bu makinedeki ajanları telefonunuzdan, web’den ve diğer cihazlardan denetleyin"',
    '"Search agents..."': '"Ajanlarda ara..."',
    '"Search Cursor settings\\u2026"': '"Cursor ayarlarında ara\\u2026"',
    'heading:"Recent"': 'heading:"Son Kullanılanlar"',
    'heading:"Older"': 'heading:"Daha Eski"',
    '"Developer: Reveal User Data Folder"': '"Geliştirici: Kullanıcı Verileri Klasörünü Göster"',
    '"Developer: Delete Old Chats\\u2026"': '"Geliştirici: Eski Sohbetleri Sil\\u2026"',
    '"Personal Usage"': '"Kişisel Kullanım"',
    '"Included in"': '"Dahil Olanlar"',
    '"On Demand"': '"İsteğe Bağlı"',
    '"Sync Skills for Cloud Agents"': '"Bulut Ajanları İçin Becerileri Eşitle"',
    '"Handle"': '"Kullanıcı Adı"',
    '"Email"': '"E-posta"',
    '"Profile Image"': '"Profil Resmi"',
    '"Links"': '"Bağlantılar"',
    '"On-Demand"': '"İsteğe Bağlı"',
    # Checklist Öncelik A - Upsell, Ayarlar ve Placeholderlar
    '"Upgrade to unlock more models"': '"Daha fazla modelin kilidini açmak için yükseltin"',
    '"More models are only available on paid plans."': '"Daha fazla model yalnızca ücretli planlarda kullanılabilir."',
    '"Max mode is required for cloud agents."': '"Bulut ajanları için azami mod gereklidir."',
    '"Show title bar in agent layout."': '"Ajan yerleşiminde başlık çubuğunu göster."',
    '"Show title bar in agent layout"': '"Ajan yerleşiminde başlık çubuğunu göster"',
    '"Entry-level plan with access to premium models, unlimited Tab completions, and more."': '"Premium modellere erişim, sınırsız Sekme tamamlamaları ve daha fazlasını içeren başlangıç düzeyi planı."',
    'placeholder:"Ask questions"': 'placeholder:"Soru sorun"',
    'placeholder:"Debug issues"': 'placeholder:"Sorunları ayıklayın"',
    'placeholder:"Coordinate tasks"': 'placeholder:"Görevleri koordine edin"',
    '"Included Usage"': '"Dahil Edilen Kullanım"',
    '"Free Plan"': '"Ücretsiz Plan"',
    '"$20/mo"': '"20 $/ay"',
    '<span class=minor-version-notification-text>New update available</span>': '<span class=minor-version-notification-text>Yeni güncelleme mevcut</span>',
    '<p class=update-notification-eyebrow>Update to v</p>': '<p class=update-notification-eyebrow>Sürüme güncelle: v</p>',
    '<span>New in </span>': '<span>Yenilikler: </span>',
    'children:"Later"': 'children:"Daha Sonra"',
    'children:"Install Now"': 'children:"Şimdi Yükle"',
    'children:"Changelog"': 'children:"Değişiklik Günlüğü"',
    'children:"Restart to Update"': 'children:"Güncellemek için Yeniden Başlat"',
    'children:"Restart to update"': 'children:"Güncellemek için Yeniden Başlat"',
    'action:"Create Branch"': 'action:"Dal Oluştur"',
    'action:"Update Branch"': 'action:"Dalı Güncelle"',
    'label:"Create Branch & Commit"': 'label:"Dal Oluştur ve İşle"',
    'label:"Create Branch, Commit & Push"': 'label:"Dal Oluştur, İşle ve Gönder"',
    'loadingLabel:"Creating Branch..."': 'loadingLabel:"Dal Oluşturuluyor..."',
    'case"create":return t.branchName?`Create ${t.branchName}`:"Create Branch"': 'case"create":return t.branchName?`${t.branchName} Dalını Oluştur`:"Dal Oluştur"',
    'case"load-more":return"Load more"': 'case"load-more":return"Daha Fazla Yükle"',
    'label:e.length===1?"1 File Changed":`${e.length} Files Changed`': 'label:e.length===1?"1 Dosya Değişti":`${e.length} Dosya Değişti`',
    'Ee(8841,"&&Open View...")': 'Ee(8841,"Görünümü &&Aç...")',
    'Ee(8840,"Open View")': 'Ee(8840,"Görünümü Aç")',
    'Ee(11961,"E&&xit")': 'Ee(11961,"Çı&&kış")',
    '"Open View..."': '"Görünümü Aç..."',
    '"Open View"': '"Görünümü Aç"',
    '"&&Open View..."': '"Görünümü &&Aç..."',
    '"E&&xit"': '"Çı&&kış"',
    '"Build Plan"': '"Plan Oluştur"',
    '"Second Opinion"': '"İkinci Görüş"',
    'children:"Create repo"': 'children:"Depo Oluştur"',
    'children:"Create repository"': 'children:"Depo Oluştur"',
    '"Create repo"': '"Depo Oluştur"',
    '"Create repository"': '"Depo Oluştur"',
    '"Select Repository"': '"Depo Seç"',
    '"Select Workspace"': '"Çalışma Alanı Seç"',
    '"What should we name your repository?"': '"Deponuzun adı ne olsun?"',
    '"Who can see the code?"': '"Kodu kimler görebilir?"',
    'name:Ee(8414,"Outline")': 'name:Ee(8414,"Ana Hat")',
    'name:Ee(8466,"Output")': 'name:Ee(8466,"Çıktı")',
    'name:Ee(8467,"Output")': 'name:Ee(8467,"Çıktı")',
    'Ee(9231,"Source Control")': 'Ee(9231,"Kaynak Denetimi")',
    'Ee(7262,"Explorer")': 'Ee(7262,"Gezgin")',
    'Ee(7263,"Explorer")': 'Ee(7263,"Gezgin")',
    'alt:{id:HDt,title:"Replace Agent",icon:Ie.addTwo}': 'alt:{id:HDt,title:"Ajanı Değiştir",icon:Ie.addTwo}',
    'alt:{id:qan,title:"Replace Agent",icon:bt.addTwo}': 'alt:{id:qan,title:"Ajanı Değiştir",icon:bt.addTwo}',
    'alt:{id:XMt,title:"Replace Agent",icon:Re.addTwo}': 'alt:{id:XMt,title:"Ajanı Değiştir",icon:Re.addTwo}',
    'alt:{id:adn,title:"Replace Agent",icon:_t.addTwo}': 'alt:{id:adn,title:"Ajanı Değiştir",icon:_t.addTwo}',
    'title:"Replace Agent"': 'title:"Ajanı Değiştir"',
    'placeholder:"Search Agents..."': 'placeholder:"Ajanları Ara..."',
    'placeholder="Search Agents\\u2026"title="Search Agents\\u2026"': 'placeholder="Ajanları Ara\\u2026"title="Ajanları Ara\\u2026"',
    'n="Search Agents\\u2026"': 'n="Ajanları Ara\\u2026"',
    'r<=0?"Today":r===1?"Yesterday":r<7?"Previous 7 days":"Older"': 'r<=0?"Bugün":r===1?"Dün":r<7?"Önceki 7 gün":"Daha Eski"',
    '{today:"Today",yesterday:"Yesterday",last7Days:"Last 7 days",last30Days:"Last 30 days",older:"Older"}': '{today:"Bugün",yesterday:"Dün",last7Days:"Son 7 gün",last30Days:"Son 30 gün",older:"Daha Eski"}',
    '`Archived (${W.length})`:"Archived"': '`Arşivlenenler (${W.length})`:"Arşivlenenler"',
    '`Archived (${B.length})`:"Archived"': '`Arşivlenenler (${B.length})`:"Arşivlenenler"',
    '?"Restore":"Archive"': '?"Geri Yükle":"Arşivle"',
    '?"Restore cloud agent":"Archive cloud agent"': '?"Bulut Ajanını Geri Yükle":"Bulut Ajanını Arşivle"',
    '?"Unpin":"Pin"': '?"Sabitlemeyi Kaldır":"Sabitle"',
    'if (key === "New Agent (Ctrl+N) [Alt] Replace Agent")': 'if (key === "New Agent (Ctrl+N) [Alt] Replace Agent" || key === "Yeni Ajan (Ctrl+N) [Alt] Replace Agent" || key.includes("[Alt] Replace Agent"))',
    '"Add File to Codex Thread"': '"Dosyayı Codex Konusuna Ekle"',
    'title:"Add File to Codex Thread"': 'title:"Dosyayı Codex Konusuna Ekle"',
    '"Add to Codex Thread"': '"Codex Konusuna Ekle"',
    'title:"Add to Codex Thread"': 'title:"Codex Konusuna Ekle"',
    'class:"breadcrumbs-action-btn",children:"Undo File"': 'class:"breadcrumbs-action-btn",children:"Dosyayı Geri Al"',
    'class:"breadcrumbs-action-btn",children:"Keep File"': 'class:"breadcrumbs-action-btn",children:"Dosyayı Koru"',
    'class:"breadcrumbs-action-btn",children:"Keep all changes"': 'class:"breadcrumbs-action-btn",children:"Tüm Değişiklikleri Koru"',
    'class:"breadcrumbs-action-btn",children:"Review Next File"': 'class:"breadcrumbs-action-btn",children:"Sonraki Dosyayı İncele"',
    'p()?"Undo":"Undo All"': 'p()?"Geri Al":"Tümünü Geri Al"',
    'p()?"Keep":"Keep All"': 'p()?"Koru":"Tümünü Koru"',
    # Bildirimler (Toasts)
    'Input needed \\u2022 ': 'Girdi gerekli \\u2022 ',
    '"Input needed"': '"Girdi gerekli"',
    '"Open Cursor to answer the agent\'s questions."': '"Ajanın sorularını yanıtlamak için Cursor\'ı açın."',
    'actions:[{type:"button",text:"Accept"},{type:"button",text:"Reject"}]': 'actions:[{type:"button",text:"Kabul Et"},{type:"button",text:"Reddet"}]',
    'Done \\u2022 ': 'Tamamlandı \\u2022 ',
    '"Agent complete"': '"Ajan tamamlandı"',
    '"Open Cursor to view the agent\'s output."': '"Ajanın çıktısını görüntülemek için Cursor\'ı açın."',
    '"Approve pending action"': '"Bekleyen eylemi onayla"',
    '"Return to Cursor to review and approve."': '"İncelemek ve onaylamak için Cursor\'a dönün."',
    '"Approve terminal command"': '"Terminal komutunu onayla"',
    'Approval required to run: ': 'Çalıştırmak için onay gerekli: ',
    '"Approve file edit"': '"Dosya düzenlemesini onayla"',
    'Approval required to edit: ': 'Düzenlemek için onay gerekli: ',
    '"Return to Cursor to review and approve file changes."': '"Dosya değişikliklerini incelemek ve onaylamak için Cursor\'a dönün."',
    '`Approve ${a} file edits`': '`${a} dosya düzenlemesini onayla`',
    '`Return to Cursor to review and approve ${a} file changes.`': '`${a} dosya değişikliğini incelemek ve onaylamak için Cursor\'a dönün.`',
    '"Approve file deletion"': '"Dosya silmeyi onayla"',
    'Approval required to delete: ': 'Silmek için onay gerekli: ',
    '"Return to Cursor to review and approve file deletion."': '"Dosya silmeyi incelemek ve onaylamak için Cursor\'a dönün."',
    '"Approve MCP tool"': '"MCP aracını onayla"',
    'Approval required for MCP tool: ': 'MCP aracı için onay gerekli: ',
    '"Return to Cursor to review and approve the MCP tool execution."': '"MCP aracı yürütmesini incelemek ve onaylamak için Cursor\'a dönün."',
    # Soru / Questionnaire Widget'ı
    '<span class=composer-questionnaire-toolbar-title>Questions</span>': '<span class=composer-questionnaire-toolbar-title>Sorular</span>',
    '<span class=composer-questionnaire-toolbar-stepper-label> of ': '<span class=composer-questionnaire-toolbar-stepper-label> / ',
    '<span class=composer-questionnaire-toolbar-answered-hint> of <!> answered': '<span class=composer-questionnaire-toolbar-answered-hint> / <!> yanıtlandı',
    '("<span>Continue")': '("<span>Devam Et")',
    'class:"composer-skip-button",keybinding:"Esc",style:{"padding-right":0},children:"Skip"': 'class:"composer-skip-button",keybinding:"Esc",style:{"padding-right":0},children:"Atla"',
    'hintText:"Previous question"': 'hintText:"Önceki Soru"',
    'hintText:"Next question"': 'hintText:"Sonraki Soru"',
    'placeholder=Other...': 'placeholder=Diğer...',
    'textInputPlaceholder:"Other..."': 'textInputPlaceholder:"Diğer..."',
    'label:"Other..."': 'label:"Diğer..."',
    'placeholder:"Other..."': 'placeholder:"Diğer..."',
    '"Add more optional details"': '"İsteğe bağlı ek ayrıntılar ekleyin"',
    '"Add more optional details..."': '"İsteğe bağlı ek ayrıntılar ekleyin..."',
    '"Could not skip the questionnaire. Please try again."': '"Sorular atlanamadı. Lütfen tekrar deneyin."',
    '"Could not submit the questionnaire. Please try again."': '"Sorular gönderilemedi. Lütfen tekrar deneyin."',
    # Arka plan terminalleri ve görevler
    'e.totalCount>0&&e.shellCount===e.totalCount?`${e.totalCount} background terminal${t}`:e.totalCount>0&&e.shellCount===0?`${e.totalCount} background subagent${t}`:`${e.totalCount} background task${t}`': 'e.totalCount>0&&e.shellCount===e.totalCount?`${e.totalCount} arka plan terminali`:e.totalCount>0&&e.shellCount===0?`${e.totalCount} arka plan alt ajanı`:`${e.totalCount} arka plan görevi`',
    't.totalCount>0&&t.shellCount===t.totalCount?`${t.totalCount} background terminal${e}`:t.totalCount>0&&t.shellCount===0?`${t.totalCount} background subagent${e}`:`${t.totalCount} background task${e}`': 't.totalCount>0&&t.shellCount===t.totalCount?`${t.totalCount} arka plan terminali`:t.totalCount>0&&t.shellCount===0?`${t.totalCount} arka plan alt ajanı`:`${t.totalCount} arka plan görevi`',
    'Worked for ${': 'Çalışma Süresi: ${',
    'M("glass.terminal.confirmCloseAgent.title","Stop Agent Terminal?")': 'M("glass.terminal.confirmCloseAgent.title","Ajan Terminalini Durdur?")',
    'M("glass.terminal.confirmCloseAgent.message","This is an agent\'s background terminal. Closing it will stop any process currently running in it.")': 'M("glass.terminal.confirmCloseAgent.message","Bu bir ajanın arka plan terminalidir. Kapatmak, içinde çalışan herhangi bir süreci durduracaktır.")',
    'M("glass.terminal.confirmCloseAgent.close","Stop Terminal")': 'M("glass.terminal.confirmCloseAgent.close","Terminali Durdur")',
    # Aktif Kurallar (Görsel 1)
    '<div><div>Active Rules</div><div>': '<div><div>Aktif Kurallar</div><div>',
    '<div>and <!> more': '<div>ve <!> fazlası',
    # Göreceli Zaman / Just now (Görsel 2)
    'nowLabel:"Just now"': 'nowLabel:"Az önce"',
    'return"Just now"': 'return"Az önce"',
    'return"just now"': 'return"az önce"',
    # Çalışma Süresi Düzeltmesi (Görsel 3)
    'return t===void 0?void 0:`for ${t}`': 'return t===void 0?void 0:`: ${t}`',
    'return e===void 0?void 0:`for ${e}`': 'return e===void 0?void 0:`: ${e}`',
    'return e[3]!==o?(a=UUh(o),e[3]=o,e[4]=a):a=e[4],`for ${a}`': 'return e[3]!==o?(a=UUh(o),e[3]=o,e[4]=a):a=e[4],`: ${a}`',
    # Terminal Otomatik Çalıştırma Menüsü (Görsel 3)
    '"Auto-review (with Sandbox)"': '"Otomatik İnceleme (Sanal Alan ile)"',
    '"Auto-review"': '"Otomatik İnceleme"',
    '"Automatically run operations after you approve them once"': '"İşlemleri bir kez onayladıktan sonra otomatik olarak çalıştır"',
    '"Automatically run operations that Auto-review classifies as safe, using sandboxing when possible"': '"Mümkün olduğunda sanal alan kullanarak Otomatik İnceleme\'nin güvenli olarak sınıflandırdığı işlemleri otomatik olarak çalıştır"',
    '"Automatically run operations that Auto-review classifies as safe"': '"Otomatik İnceleme\'nin güvenli olarak sınıflandırdığı işlemleri otomatik olarak çalıştır"',
    '"Automatically run all operations without asking for permission"': '"İzin istemeden tüm işlemleri otomatik olarak çalıştır"',
    '"Ask for permission before running each operation"': '"Her işlemi çalıştırmadan önce izin iste"',
    '"Tools will auto-run in a sandbox if possible, otherwise respect the allowlist or ask for approval"': '"Araçlar mümkünse sanal alanda otomatik çalışır, aksi takdirde izin listesine uyar veya onay ister"',
    '"Copy Command"': '"Komutu Kopyala"',
    # Düşünce Süresi / Thought briefly (Görsel 4)
    'h=v?K:"Thought"': 'h=v?K:"Düşündü"',
    'd=f?z:"Thought"': 'd=f?z:"Düşündü"',
    't!==void 0&&t>0&&t<500?n?void 0:"briefly"': 't!==void 0&&t>0&&t<500?n?void 0:"kısaca"',
    'e!==void 0&&e>0&&e<500?n?void 0:"briefly"': 'e!==void 0&&e>0&&e<500?n?void 0:"kısaca"',
    # Kontrol Noktası / Restore Checkpoint (Görsel 5)
    '"Restore Checkpoint"': '"Kontrol Noktasına Geri Dön"',
    # Uzaktan Denetim / Remote Control (Kullanıcı Ayarlar Görseli 1)
    '"Allow agents on this computer to be controlled from your other devices"': '"Bu bilgisayardaki ajanların diğer cihazlarınızdan denetlenmesine izin verin"',
    '"Register eligible computers when you sign in"': '"Oturum açtığınızda uygun bilgisayarları kaydet"',
    '"Computer Name"': '"Bilgisayar Adı"',
    '"Change how this computer appears on other devices"': '"Bu bilgisayarın diğer cihazlarda nasıl görüneceğini değiştirin"',
    '"Disable Remote Control on all of my computers"': '"Tüm bilgisayarlarımda Uzaktan Denetimi devre dışı bırak"',
    '"Unregisters every computer on your account; you can register any of them again later"': '"Hesabınızdaki tüm bilgisayarların kaydını siler; daha sonra herhangi birini tekrar kaydedebilirsiniz"',
    '"Unregister All"': '"Tümünün Kaydını Sil"',
    '"&&Unregister All"': '"&&Tümünün Kaydını Sil"',
    '"Disable Remote Control on all of your computers?"': '"Tüm bilgisayarlarınızda Uzaktan Denetim devre dışı bırakılsın mı?"',
    '"This will turn off Remote Control on every computer associated with your account."': '"Bu işlem, hesabınızla ilişkili her bilgisayarda Uzaktan Denetimi kapatır."',
    '"Couldn\\u2019t unregister some computers. Try again."': '"Bazı bilgisayarların kaydı silinemedi. Tekrar deneyin."',
    '"Couldn\'t unregister some computers. Try again."': '"Bazı bilgisayarların kaydı silinemedi. Tekrar deneyin."',
    '"Paired Devices"': '"Eşleştirilmiş Cihazlar"',
    '"No devices are currently paired with this computer."': '"Şu anda bu bilgisayarla eşleştirilmiş cihaz yok."',
    '"Unnamed device"': '"Adsız Cihaz"',
    '"Disconnect"': '"Bağlantıyı Kes"',
    '"&&Disconnect"': '"&&Bağlantıyı Kes"',
    '"Disconnect from All Computers"': '"Tüm Bilgisayarlardan Bağlantıyı Kes"',
    '"&&Disconnect from All Computers"': '"&&Tüm Bilgisayarlardan Bağlantıyı Kes"',
    '"It won\\u2019t be able to control this computer until it\\u2019s authorized here again."': '"Burada tekrar yetkilendirilene kadar bu bilgisayarı denetleyemez."',
    '"It won\'t be able to control this computer until it\'s authorized here again."': '"Burada tekrar yetkilendirilene kadar bu bilgisayarı denetleyemez."',
    '"It won\\u2019t be able to control any of your computers. To use it again, authorize it as a new device."': '"Bilgisayarlarınızın hiçbirini denetleyemez. Tekrar kullanmak için yeni bir cihaz olarak yetkilendirin."',
    '"It won\'t be able to control any of your computers. To use it again, authorize it as a new device."': '"Bilgisayarlarınızın hiçbirini denetleyemez. Tekrar kullanmak için yeni bir cihaz olarak yetkilendirin."',
    '"Remote Control runs on a cloud agent, which requires data storage that your current privacy mode disables"': '"Uzaktan Denetim, geçerli gizlilik modunuzun devre dışı bıraktığı veri depolamayı gerektiren bir bulut ajanında çalışır"',
    # Self-Hosted Workers (Kullanıcı Ayarlar Görseli 1)
    'sectionTitle:"Self-Hosted Workers"': 'sectionTitle:"Yerel Çalıştırıcılar"',
    'workersLabel:"Enable local self-hosted workers"': 'workersLabel:"Yerel Çalıştırıcıları Etkinleştir"',
    'workersDescription:"Allow cloud agents to run in your local environment."': 'workersDescription:"Bulut ajanlarının yerel ortamınızda çalışmasına izin verin."',
    'label:"Offline"': 'label:"Çevrimdışı"',
    'label:"Connecting\\u2026"': 'label:"Bağlanıyor…"',
    'label:"Connecting..."': 'label:"Bağlanıyor..."',
    # Sohbet Yükleniyor / Loading Chat (Kullanıcı Görseli 2)
    'textOverride||"Loading Chat"': 'textOverride||"Sohbet Yükleniyor"',
    'make-shine">Loading Chat': 'make-shine">Sohbet Yükleniyor',
    '"Loading Chat"': '"Sohbet Yükleniyor"',
    # Tarih Grupları / Time Buckets (Kullanıcı Ajan Arama Görseli 3)
    '{key:"today",label:"Today"}': '{key:"today",label:"Bugün"}',
    '{key:"yesterday",label:"Yesterday"}': '{key:"yesterday",label:"Dün"}',
    '{key:"older",label:"Older"}': '{key:"older",label:"Daha Eski"}',
    # Ayarlar ve Ajan İzinleri (Kullanıcı Ayarlar Arama Görseli 1)
    'label:"Read Access"': 'label:"Okuma Erişimi"',
    'label:"Read Allowlist"': 'label:"Okuma İzin Listesi"',
    '"Run Mode Disabled by Team Admin"': '"Çalıştırma Modu Ekip Yöneticisi Tarafından Devre Dışı Bırakıldı"',
    '"Run Mode Controlled by Team Admin (Sandbox Enabled)"': '"Çalıştırma Modu Ekip Yöneticisince Denetleniyor (Sanal Alan Etkin)"',
    '"Run Mode Controlled by Team Admin"': '"Çalıştırma Modu Ekip Yöneticisince Denetleniyor"',
    # Proje Arama ve Boş Durum (Kullanıcı Projeler Görseli 4)
    'q?"Search projects...":': 'q?"Projelerde ara...":',
    'j?"Search projects, agents, Canvas, files, actions...":': 'j?"Projelerde, ajanlarda, Tuval\'de, dosyalarda ve eylemlerde ara...":',
    'children:"No projects found"': 'children:"Proje bulunamadı"',
    '"No projects found"': '"Proje bulunamadı"',
    '"Browse Files"': '"Dosyalara Göz At"',
    # Görünüm / Sohbet Genişliği (Kullanıcı Ayarlar Görseli 1)
    'label:"Chat Width",description:"Set the maximum width of Agent conversations"': 'label:"Sohbet Genişliği",description:"Ajan konuşmalarının azami genişliğini ayarlayın"',
    'children:"Narrow"': 'children:"Dar"',
    'children:"Wide"': 'children:"Geniş"',
    '"aria-label":"Chat width"': '"aria-label":"Sohbet genişliği"',
    # Beceriler, Bağlam ve Mod Arama (Kullanıcı Menü Görseli 4)
    '"Search skills, context, chats..."': '"Becerilerde, bağlamda ve sohbetlerde ara..."',
    '"Search custom modes..."': '"Özel modlarda ara..."',
    '"Search MCPs..."': '"MCP\'lerde ara..."',
    # Ajan Modları Açıklamaları ve Önerilen Etiketi (Kullanıcı Mod Menüsü Görselleri 1, 2, 3, 4)
    'case"chat":return"Ask Cursor questions about your codebase";case"edit":return"Manually decide what gets added to the context (no tools)";case"plan":return"Create detailed plans for accomplishing tasks";case"spec":return"Create structured plans with implementation steps";case"multitask":return"Run and coordinate multiple tasks in parallel";case"triage":return"Coordinate long-horizon tasks with delegated subagents";': 'case"chat":return"Kod tabanınız hakkında Cursor\'a sorular sorun";case"edit":return"Bağlama neyin ekleneceğine el ile karar verin (araç yok)";case"plan":return"Görevleri gerçekleştirmek için ayrıntılı planlar oluşturun";case"spec":return"Uygulama adımları içeren yapılandırılmış planlar oluşturun";case"multitask":return"Birden fazla görevi paralel olarak çalıştırın ve koordine edin";case"triage":return"Yetkilendirilen alt ajanlarla uzun erimli görevleri koordine edin";case"debug":return"Çalışma zamanı izlerini kullanarak hataları sistematik olarak teşhis edin ve düzeltin";',
    'je.label==="Agent"?"Recommended":void 0': '(je.label==="Agent"||je.label==="Ajan")?"Önerilen":void 0',
    'fe.label==="Agent"?"Recommended":void 0': '(fe.label==="Agent"||fe.label==="Ajan")?"Önerilen":void 0',
    'Gt?un="Recommended":Rt?un="Yalnızca MAX"': 'Gt?un="Önerilen":Rt?un="Yalnızca MAX"',
    'Ve?He="Recommended":Ye?He="Yalnızca MAX"': 'Ve?He="Önerilen":Ye?He="Yalnızca MAX"',
    'labelSuffix:ce===0&&!ae?"Recommended":void 0': 'labelSuffix:ce===0&&!ae?"Önerilen":void 0',
}

OVERLAY = r'''

/* CURSOR_TR_MENU_GAPS_V1 */
;(() => {
  const translations = new Map([
    ["OUTLINE", "ANA HAT"],
    ["Outline", "Ana Hat"],
    ["OUTPUT", "ÇIKTI"],
    ["Output", "Çıktı"],
    ["SOURCE CONTROL", "KAYNAK DENETİMİ"],
    ["Source Control", "Kaynak Denetimi"],
    ["EXPLORER", "GEZGİN"],
    ["Explorer", "Gezgin"],
    ["Planning next moves", "Sıradaki adımlar planlanıyor"],
    ["Wrapping up", "Tamamlanıyor"],
    ["Thinking", "Düşünülüyor"],
    ["Exploring", "Keşfediliyor"],
    ["Reading", "Okunuyor"],
    ["Reading...", "Okunuyor..."],
    ["Using", "Kullanılıyor"],
    ["Used", "Kullanıldı"],
    ["Generating", "Üretiliyor"],
    ["Generated", "Üretildi"],
    ["Deleting", "Siliniyor"],
    ["Deleted", "Silindi"],
    ["Ran", "Çalıştırıldı"],
    ["Add a follow-up", "Takip Mesajı Ekle"],
    ["Add a follow up", "Takip Mesajı Ekle"],
    ["Ask follow-ups in the worktree", "Çalışma ağacında takip mesajları sorun"],
    ["Send follow-up", "Takip Mesajı Gönder"],
    ["Cycle Effort", "Çaba Düzeyini Değiştir"],
    ["Cycle effort", "Çaba Düzeyini Değiştir"],
    ["Switch Model and Retry", "Model Değiştir ve Yeniden Dene"],
    ["OUTLINE", "ANA HAT"],
    ["Outline", "Ana Hat"],
    ["OUTPUT", "ÇIKTI"],
    ["Output", "Çıktı"],
    ["SOURCE CONTROL", "KAYNAK DENETİMİ"],
    ["Source Control", "Kaynak Denetimi"],
    ["EXPLORER", "GEZGİN"],
    ["Explorer", "Gezgin"],
    ["PROBLEMS", "SORUNLAR"],
    ["Problems", "Sorunlar"],
    ["EXTENSIONS", "UZANTILAR"],
    ["Extensions", "Uzantılar"],
    ["Create repo", "Depo Oluştur"],
    ["Create repository", "Depo Oluştur"],
    ["Create Repository", "Depo Oluştur"],
    ["Select Repository", "Depo Seç"],
    ["Select Workspace", "Çalışma Alanı Seç"],
    ["What should we name your repository?", "Deponuzun adı ne olsun?"],
    ["Who can see the code?", "Kodu kimler görebilir?"],
    ["This PC", "Bu Bilgisayar"],
    ["context used", "bağlam kullanıldı"],
    ["Context", "Bağlam"],
    ["Context Window", "Bağlam Penceresi"],
    ["Context window", "Bağlam Penceresi"],
    ["context window", "bağlam penceresi"],
    ["500k context window", "500 bin bağlam penceresi"],
    ["500K context window", "500 bin bağlam penceresi"],
    ["128k context window", "128 bin bağlam penceresi"],
    ["128K context window", "128 bin bağlam penceresi"],
    ["2M context window", "2 milyon bağlam penceresi"],
    ["SpaceXAI's most powerful model, built for complex coding and knowledge work.", "SpaceXAI'ın karmaşık kodlama ve bilgi işleri için tasarlanmış en güçlü modeli."],
    ["SpaceXAI's most powerful model, great for complex coding and knowledge work.", "SpaceXAI'ın karmaşık kodlama ve bilgi işleri için tasarlanmış en güçlü modeli."],
    ["Significantly faster but consumes more usage", "Belirgin şekilde daha hızlıdır ancak daha fazla kullanım tüketir"],
    ["Restore defaults", "Varsayılanlara Sıfırla"],
    ["tokens", "belirteç"],
    ["Cloud Agent Approval Banners While Focused", "Odaklanmışken Bulut Ajanı Onay Banner'ları"],
    ["Also show the approval banner while Cursor is focused; the request card in the agent conversation always shows", "Cursor odaktayken de onay banner'ını göster; ajan konuşmasındaki istek kartı her zaman gösterilir"],
    ["Origin Notifications", "Origin Bildirimleri"],
    ["Notify when Origin pull requests you follow are merged, closed, reviewed, or fail CI", "Takip ettiğiniz Origin pull request'leri birleştirildiğinde, kapatıldığında, incelendiğinde veya CI başarısız olduğunda bildirim gönder"],
    ["Open View...", "Görünümü Aç..."],
    ["Open View…", "Görünümü Aç…"],
    ["Open View", "Görünümü Aç"],
    ["&&Open View...", "Görünümü &&Aç..."],
    ["E&&xit", "Çı&&kış"],
    ["Exit", "Çıkış"],
    ["Build Plan", "Plan Oluştur"],
    ["Add File to Codex Thread", "Dosyayı Codex Konusuna Ekle"],
    ["Add file to Codex thread", "Dosyayı Codex Konusuna Ekle"],
    ["Add to Codex Thread", "Codex Konusuna Ekle"],
    ["Undo File", "Dosyayı Geri Al"],
    ["Keep File", "Dosyayı Koru"],
    ["Keep all changes", "Tüm Değişiklikleri Koru"],
    ["Review Next File", "Sonraki Dosyayı İncele"],
    ["Undo All", "Tümünü Geri Al"],
    ["Keep All", "Tümünü Koru"],
    ["Search Agents...", "Ajanları Ara..."],
    ["Search Agents…", "Ajanları Ara…"],
    ["Previous 7 days", "Önceki 7 gün"],
    ["Replace Agent", "Ajanı Değiştir"],
    ["Archived", "Arşivlenenler"],
    ["Restore", "Geri Yükle"],
    ["Archive", "Arşivle"],
    ["Pin", "Sabitle"],
    ["Unpin", "Sabitlemeyi Kaldır"],
    ["Restore cloud agent", "Bulut Ajanını Geri Yükle"],
    ["Archive cloud agent", "Bulut Ajanını Arşivle"],
    ["Questions", "Sorular"],
    ["Continue", "Devam Et"],
    ["Skip", "Atla"],
    ["Other...", "Diğer..."],
    ["Other…", "Diğer…"],
    ["Accept", "Kabul Et"],
    ["Reject", "Reddet"],
    ["Input needed", "Girdi gerekli"],
    ["Open Claude Code", "Claude Code'u Aç"],
    ["Previous question", "Önceki Soru"],
    ["Next question", "Sonraki Soru"],
    ["Add more optional details", "İsteğe bağlı ek ayrıntılar ekleyin"],
    ["Add more optional details...", "İsteğe bağlı ek ayrıntılar ekleyin..."],
    ["Agent complete", "Ajan tamamlandı"],
    ["Open Cursor to view the agent's output.", "Ajanın çıktısını görüntülemek için Cursor'ı açın."],
    ["Open Cursor to answer the agent's questions.", "Ajanın sorularını yanıtlamak için Cursor'ı açın."],
    ["background terminal", "arka plan terminali"],
    ["background terminals", "arka plan terminali"],
    ["background subagent", "arka plan alt ajanı"],
    ["background subagents", "arka plan alt ajanı"],
    ["background task", "arka plan görevi"],
    ["background tasks", "arka plan görevi"],
    ["Stop Agent Terminal?", "Ajan Terminalini Durdur?"],
    ["Stop Terminal", "Terminali Durdur"],
    ["Active Rules", "Aktif Kurallar"],
    ["Just now", "Az önce"],
    ["just now", "az önce"],
    ["Auto-review", "Otomatik İnceleme"],
    ["Auto-review (with Sandbox)", "Otomatik İnceleme (Sanal Alan ile)"],
    ["Automatically run operations after you approve them once", "İşlemleri bir kez onayladıktan sonra otomatik olarak çalıştır"],
    ["Automatically run operations that Auto-review classifies as safe, using sandboxing when possible", "Mümkün olduğunda sanal alan kullanarak Otomatik İnceleme'nin güvenli olarak sınıflandırdığı işlemleri otomatik olarak çalıştır"],
    ["Automatically run operations that Auto-review classifies as safe", "Otomatik İnceleme'nin güvenli olarak sınıflandırdığı işlemleri otomatik olarak çalıştır"],
    ["Automatically run all operations without asking for permission", "İzin istemeden tüm işlemleri otomatik olarak çalıştır"],
    ["Copy Command", "Komutu Kopyala"],
    ["Thought briefly", "Kısaca düşündü"],
    ["Thought", "Düşündü"],
    ["briefly", "kısaca"],
    ["Düşündü kısaca", "Kısaca düşündü"],
    ["Restore Checkpoint", "Kontrol Noktasına Geri Dön"],
    ["Restore checkpoint", "Kontrol Noktasına Geri Dön"],
    ["Allow agents on this computer to be controlled from your other devices", "Bu bilgisayardaki ajanların diğer cihazlarınızdan denetlenmesine izin verin"],
    ["Register eligible computers when you sign in", "Oturum açtığınızda uygun bilgisayarları kaydet"],
    ["Computer Name", "Bilgisayar Adı"],
    ["Change how this computer appears on other devices", "Bu bilgisayarın diğer cihazlarda nasıl görüneceğini değiştirin"],
    ["Disable Remote Control on all of my computers", "Tüm bilgisayarlarımda Uzaktan Denetimi devre dışı bırak"],
    ["Unregisters every computer on your account; you can register any of them again later", "Hesabınızdaki tüm bilgisayarların kaydını siler; daha sonra herhangi birini tekrar kaydedebilirsiniz"],
    ["Unregister All", "Tümünün Kaydını Sil"],
    ["Disable Remote Control on all of your computers?", "Tüm bilgisayarlarınızda Uzaktan Denetim devre dışı bırakılsın mı?"],
    ["This will turn off Remote Control on every computer associated with your account.", "Bu işlem, hesabınızla ilişkili her bilgisayarda Uzaktan Denetimi kapatır."],
    ["Couldn’t unregister some computers. Try again.", "Bazı bilgisayarların kaydı silinemedi. Tekrar deneyin."],
    ["Couldn't unregister some computers. Try again.", "Bazı bilgisayarların kaydı silinemedi. Tekrar deneyin."],
    ["Paired Devices", "Eşleştirilmiş Cihazlar"],
    ["No devices are currently paired with this computer.", "Şu anda bu bilgisayarla eşleştirilmiş cihaz yok."],
    ["Unnamed device", "Adsız Cihaz"],
    ["Disconnect", "Bağlantıyı Kes"],
    ["Disconnect from All Computers", "Tüm Bilgisayarlardan Bağlantıyı Kes"],
    ["It won’t be able to control this computer until it’s authorized here again.", "Burada tekrar yetkilendirilene kadar bu bilgisayarı denetleyemez."],
    ["It won't be able to control this computer until it's authorized here again.", "Burada tekrar yetkilendirilene kadar bu bilgisayarı denetleyemez."],
    ["It won’t be able to control any of your computers. To use it again, authorize it as a new device.", "Bilgisayarlarınızın hiçbirini denetleyemez. Tekrar kullanmak için yeni bir cihaz olarak yetkilendirin."],
    ["It won't be able to control any of your computers. To use it again, authorize it as a new device.", "Bilgisayarlarınızın hiçbirini denetleyemez. Tekrar kullanmak için yeni bir cihaz olarak yetkilendirin."],
    ["Remote Control runs on a cloud agent, which requires data storage that your current privacy mode disables", "Uzaktan Denetim, geçerli gizlilik modunuzun devre dışı bıraktığı veri depolamayı gerektiren bir bulut ajanında çalışır"],
    ["Self-Hosted Workers", "Yerel Çalıştırıcılar"],
    ["Enable local self-hosted workers", "Yerel Çalıştırıcıları Etkinleştir"],
    ["Allow cloud agents to run in your local environment.", "Bulut ajanlarının yerel ortamınızda çalışmasına izin verin."],
    ["Offline", "Çevrimdışı"],
    ["Connecting…", "Bağlanıyor…"],
    ["Connecting...", "Bağlanıyor..."],
    ["Loading Chat", "Sohbet Yükleniyor"],
    ["Loading Chat...", "Sohbet Yükleniyor..."],
    ["Loading Chat…", "Sohbet Yükleniyor…"],
    ["Run Mode Disabled by Team Admin", "Çalıştırma Modu Ekip Yöneticisi Tarafından Devre Dışı Bırakıldı"],
    ["Run Mode Controlled by Team Admin (Sandbox Enabled)", "Çalıştırma Modu Ekip Yöneticisince Denetleniyor (Sanal Alan Etkin)"],
    ["Run Mode Controlled by Team Admin", "Çalıştırma Modu Ekip Yöneticisince Denetleniyor"],
    ["Read Access", "Okuma Erişimi"],
    ["Read Allowlist", "Okuma İzin Listesi"],
    ["Today", "Bugün"],
    ["Yesterday", "Dün"],
    ["Older", "Daha Eski"],
    ["Search projects...", "Projelerde ara..."],
    ["Search projects", "Projelerde ara"],
    ["Search projects, agents, Canvas, files, actions...", "Projelerde, ajanlarda, Tuval'de, dosyalarda ve eylemlerde ara..."],
    ["No projects found", "Proje bulunamadı"],
    ["Browse Files", "Dosyalara Göz At"],
    ["System prompt", "Sistem İstemi"],
    ["Tool definitions", "Araç Tanımları"],
    ["MCP & dynamic tools", "MCP ve Dinamik Araçlar"],
    ["Subagent definitions", "Alt Ajan Tanımları"],
    ["Summarized conversation", "Özetlenmiş Konuşma"],
    ["User rules", "Kullanıcı Kuralları"],
    ["Chat Width", "Sohbet Genişliği"],
    ["Set the maximum width of Agent conversations", "Ajan konuşmalarının azami genişliğini ayarlayın"],
    ["Narrow", "Dar"],
    ["Wide", "Geniş"],
    ["Chat width", "Sohbet Genişliği"],
    ["Search skills, context, chats...", "Becerilerde, bağlamda ve sohbetlerde ara..."],
    ["Search custom modes...", "Özel modlarda ara..."],
    ["Search MCPs...", "MCP'lerde ara..."],
    ["Recommended", "Önerilen"],
    ["Run and coordinate multiple tasks in parallel", "Birden fazla görevi paralel olarak çalıştırın ve koordine edin"],
    ["Systematically diagnose and fix bugs using runtime traces", "Çalışma zamanı izlerini kullanarak hataları sistematik olarak teşhis edin ve düzeltin"],
    ["Create detailed plans for accomplishing tasks", "Görevleri gerçekleştirmek için ayrıntılı planlar oluşturun"],
    ["Create structured plans with implementation steps", "Uygulama adımları içeren yapılandırılmış planlar oluşturun"],
    ["Coordinate long-horizon tasks with delegated subagents", "Yetkilendirilen alt ajanlarla uzun erimli görevleri koordine edin"],
    ["Manually decide what gets added to the context (no tools)", "Bağlama neyin ekleneceğine el ile karar verin (araç yok)"],
    ["Plan, search, make edits, run commands", "Planlayın, arayın, düzenlemeler yapın, komutlar çalıştırın"],
    ["Run agents in the background", "Ajanları arka planda çalıştırın"],
    ["Fork Chat", "Sohbeti Çatalla"],
    ["Maximize Chat", "Sohbeti Büyüt"],
    ["Second Opinion", "İkinci Görüş"],
    ["Copy cursor.com link", "cursor.com Bağlantısını Kopyala"],
    ["Share", "Paylaş"],
    ["Runs", "Çalıştırmalar"],
    ["Stop All Runs", "Tüm Çalıştırmaları Durdur"],
    ["Stopping...", "Durduruluyor..."],
    ["Trigger", "Tetikleyici"],
    ["Triggered", "Tetiklendi"],
    ["Duration", "Süre"],
    ["Search runs...", "Çalıştırmalarda ara..."],
    ["Cancel Run", "Çalıştırmayı İptal Et"],
    ["Memory Notes", "Hafıza Notları"],
    ["View and edit files the agent keeps in memories/", "Ajanın memories/ dizininde tuttuğu dosyaları görüntüleyin ve düzenleyin"],
    ["Add memory notes...", "Hafıza notları ekleyin..."],
    ["Content", "İçerik"],
    ["Reset", "Sıfırla"],
    ["Confirm delete", "Silmeyi Onayla"],
    ["Deleting...", "Siliniyor..."],
    ["Saving...", "Kaydediliyor..."],
    ["Select a file", "Bir Dosya Seçin"],
    ["Memory file", "Hafıza Dosyası"],
    ["Discard draft", "Taslağı At"],
    ["Failed to load memory content. Please try again later.", "Hafıza içeriği yüklenemedi. Lütfen daha sonra tekrar deneyin."],
    ["Click Confirm delete to delete this memory file.", "Bu hafıza dosyasını silmek için Silmeyi Onayla düğmesine tıklayın."],
    ["Memory changed elsewhere. Loaded latest content.", "Hafıza başka bir yerde değiştirildi. En son içerik yüklendi."],
    ["Memory tool is disabled for this automation", "Bu otomasyon için hafıza aracı devre dışı"],
    ["Save this automation to enable and configure memory notes", "Hafıza notlarını etkinleştirmek ve yapılandırmak için bu otomasyonu kaydedin"],
    ["Failed to load memory files. Please try again later.", "Hafıza dosyaları yüklenemedi. Lütfen daha sonra tekrar deneyin."],
    ["No memory files yet. The agent will create notes after it runs.", "Henüz hafıza dosyası yok. Ajan çalıştıktan sonra notlar oluşturacak."],
    ["Memory saved", "Hafıza kaydedildi"],
    ["Failed to save", "Kaydetme başarısız oldu"],
    ["Memory deleted", "Hafıza silindi"],
    ["Failed to delete", "Silme işlemi başarısız oldu"],
    ["Automation", "Otomasyon"],
    ["Edit Automation", "Otomasyonu Düzenle"],
    ["Scheduled run", "Zamanlanmış Çalıştırma"],
    ["Test run", "Test Çalıştırması"],
    ["Run summary", "Çalıştırma Özeti"],
    ["Search Triggers...", "Tetikleyicilerde Ara..."],
    ["Search automations", "Otomasyonlarda ara"],
    ["Search environments", "Ortamlarda ara"],
    ["Save and Enable", "Kaydet ve Etkinleştir"],
    ["Save or discard changes before continuing", "Devam etmeden önce değişiklikleri kaydedin veya atın"],
    ["Unsaved Changes", "Kaydedilmemiş Değişiklikler"],
    ["View details", "Ayrıntıları Görüntüle"],
    ["Webhook Triggered", "Web Kancası Tetiklendi"],
    ["Webhook triggered", "Web Kancası Tetiklendi"],
    ["Incident Triggered", "Olay Tetiklendi"],
    ["Incident Acknowledged", "Olay Onaylandı"],
    ["Incident Resolved", "Olay Çözüldü"],
    ["Counts tool calls made by the agent during the run.", "Çalıştırma sırasında ajan tarafından yapılan araç çağrılarını sayar."],
    ["Each metric scores a completed automation run.", "Her metrik, tamamlanan bir otomasyon çalıştırmasını puanlar."],
    ["Control how this automation is configured and updated", "Bu otomasyonun nasıl yapılandırılacağını ve güncelleneceğini denetleyin"],
    ["Transfer this automation to another team member.", "Bu otomasyonu başka bir ekip üyesine aktarın."],
    ["Enter a test message...", "Test mesajı girin..."],
    ["Extra context for the test run...", "Test çalıştırması için ek bağlam..."],
    ["Enter a test Teams message...", "Test Teams mesajı girin..."],
    ["Enter the message that was reacted to...", "Tepki verilen mesajı girin..."],
    ["Allow agents on this computer to be controlled remotely from mobile", "Bu bilgisayardaki ajanların mobilden uzaktan denetlenmesine izin ver"],
    ["Turn Remote Control on again to reset this computer", "Bu bilgisayarı sıfırlamak için Uzaktan Denetim'i tekrar açın"],
    ["Trusted Devices", "Güvenilen Cihazlar"],
    ["No other devices are approved for Remote Control yet", "Henüz Uzaktan Denetim için onaylanmış başka cihaz yok"],
    ["Unnamed device", "Adsız Cihaz"],
    ["Enable Remote Control for this computer", "Bu bilgisayar için Uzaktan Denetim'i etkinleştir"],
    ["Search repositories...", "Depolarda ara..."],
    ["Search repositories", "Depolarda ara"],
    ["Search repositories, environments...", "Depolarda ve ortamlarda ara..."],
    ["Search repositories and environments", "Depolarda ve ortamlarda ara"],
    ["No Repository", "Depo Yok"],
    ["No repository", "Depo Yok"],
    ["No repositories available", "Kullanılabilir depo yok"],
    ["Loading repositories...", "Depolar yükleniyor..."],
    ["Select repository", "Depo Seç"],
    ["Start from scratch", "Sıfırdan Başla"],
    ["MCPs", "MCP'ler"],
    ["Create Branch", "Dal Oluştur"],
    ["Create branch", "Dal Oluştur"],
    ["Update Branch", "Dalı Güncelle"],
    ["Load more", "Daha Fazla Yükle"],
    ["1 File Changed", "1 Dosya Değişti"],
    ["Files Changed", "Dosya Değişti"],
    ["File Changed", "Dosya Değişti"],
    ["New update available", "Yeni güncelleme mevcut"],
    ["Later", "Daha Sonra"],
    ["Install Now", "Şimdi Yükle"],
    ["Changelog", "Değişiklik Günlüğü"],
    ["Update to v", "Sürüme güncelle: v"],
    ["New in", "Yenilikler:"],
    ["Restart to Update", "Güncellemek için Yeniden Başlat"],
    ["Restart to update", "Güncellemek için Yeniden Başlat"],
    ["Attempt Update", "Güncellemeyi Dene"],
    ["Show Console", "Konsolu Göster"],
    ["Enter a URL above, or instruct the Agent to navigate and use the browser", "Yukarıya bir URL girin veya Ajan'a gezinmesini ve tarayıcıyı kullanmasını söyleyin"],
    ["Add files", "Dosya Ekle"],
    ["Click or hold Ctrl M to dictate", "Dikte etmek için Ctrl M'ye tıklayın veya basılı tutun"],
    ["Edit Icon", "Simgeyi Düzenle"],
    ["No destinations available", "Kullanılabilir hedef yok"],
    ["No compatible environments are currently available", "Şu anda uyumlu ortam yok"],
    ["Copy Agent ID", "Ajan Kimliğini Kopyala"],
    ["Copy Transcript", "Dökümü Kopyala"],
    ["Data Sharing Enabled", "Veri Paylaşımı Etkin"],
    ["Privacy Mode", "Gizlilik Modu"],
    ["Privacy Mode (Legacy)", "Gizlilik Modu (Eski)"],
    ["Your codebase, prompts, edits and other usage data will be stored and trained on by Cursor to improve the product.", "Kod tabanınız, istemleriniz, düzenlemeleriniz ve diğer kullanım verileriniz Cursor tarafından ürünü geliştirmek amacıyla saklanacak ve eğitilecektir."],
    ["Your prompts, edits and other usage data will be stored and trained on by Cursor to improve the product.", "İstemleriniz, düzenlemeleriniz ve diğer kullanım verileriniz Cursor tarafından ürünü geliştirmek amacıyla saklanacak ve eğitilecektir."],
    ["Improve Cursor for everyone", "Cursor'ı herkes için iyileştirin"],
    ["No training. Code may be stored for Background Agent and other features.", "Eğitim yapılmaz. Kod, Arka Plan Ajanı ve diğer özellikler için saklanabilir."],
    ["No training and no storage. Background Agent and other features that require code storage will be disabled.", "Eğitim ve depolama yapılmaz. Arka Plan Ajanı ve kod depolaması gerektiren diğer özellikler devre dışı bırakılır."],
    ["Projects", "Projeler"],
    ["Project", "Proje"],
    ["Repos", "Depolar"],
    ["Create a focused chat where Agents coordinate work", "Ajanların çalışmaları koordine ettiği odaklanmış bir sohbet oluşturun"],
    ["Project name", "Proje Adı"],
    ["Meet Grok Bot", "Grok Bot ile Tanışın"],
    ["AI teammates you can give real work to", "Gerçek işler verebileceğiniz yapay zekâ ekip arkadaşları"],
    ["Get Grok Bot", "Grok Bot'u Edin"],
    ["Dismiss", "Kapat"],
    ["Model used to build this plan", "Bu planı oluşturan model"],
    ["Build Locally", "Yerel Olarak Derle"],
    ["Parallel Build", "Paralel Derle"],
    ["New Chat", "Yeni Sohbet"],
    ["Open Local Links in Cursor Browser", "Yerel Bağlantıları Cursor Tarayıcısında Aç"],
    ["Open Web Links in Cursor Browser", "Web Bağlantılarını Cursor Tarayıcısında Aç"],
    ["Select Model", "Model Seç"],
    ["Cycle Effort", "Çaba Düzeyini Değiştir"],
    ["Show Apps", "Uygulamalar Panelini Göster"],
    ["Recents", "Son Kullanılanlar"],
    ["Search branches...", "Dallarda ara..."],
    ["Select branch", "Dal Seç"],
    ["Select Branch", "Dal Seç"],
    ["Select Agent Branch", "Ajan Dalını Seç"],
    ["Loading...", "Yükleniyor..."],
    ["Loading…", "Yükleniyor…"],
    ["Searching...", "Aranıyor..."],
    ["Searching…", "Aranıyor…"],
    ["Loading more...", "Daha Fazla Yükleniyor..."],
    ["Load more", "Daha Fazla Yükle"],
    ["No branches found", "Dal bulunamadı"],
    ["No branches available", "Kullanılabilir dal yok"],
    ["This PC (Remote Control)", "Bu Bilgisayar (Uzaktan Denetim)"],
    ["This PC (Self-Hosted Worker)", "Bu Bilgisayar (Yerel Çalıştırıcı)"],
    ["Bu Bilgisayar (Self-Hosted Worker)", "Bu Bilgisayar (Yerel Çalıştırıcı)"],
    ["Self-Hosted Worker", "Yerel Çalıştırıcı"],
    ["Remote Control", "Uzaktan Denetim"],
    ["Control agents on this machine from your phone, web, and other devices", "Bu makinedeki ajanları telefonunuzdan, web'den ve diğer cihazlardan denetleyin"],
    ["Control agents on this machine from your phone, web, and other devices.", "Bu makinedeki ajanları telefonunuzdan, web'den ve diğer cihazlardan denetleyin."],
    ["Select Instance", "Örnek Seç"],
    ["Remote Machines", "Uzak Makineler"],
    ["Search This PC...", "Bu bilgisayarda ara..."],
    ["Search This PC…", "Bu bilgisayarda ara…"],
    ["Use Existing...", "Mevcut Olanı Kullan..."],
    ["Use Existing…", "Mevcut Olanı Kullan…"],
    ["New Folder", "Yeni Klasör"],
    ["Back", "Geri"],
    ["No environments", "Ortam yok"],
    ["Cursor Default", "Cursor Varsayılan"],
    ["Queue", "Kuyruk"],
    ["Send Immediately", "Hemen Gönder"],
    ["Send immediately without interrupting", "Çalışmayı kesmeden hemen gönder"],
    ["Steer the Agent without stopping it", "Ajanı durdurmadan yönlendir"],
    ["Send immediately by interrupting", "Çalışmayı keserek hemen gönder"],
    ["Stop Agent and send message", "Ajanı durdur ve mesajı gönder"],
    ["Sistem eş aralıklı", "Sistem Eş Aralıklı"],
    ["Sistem yazı tipi", "Sistem Yazı Tipi"],
    ["System font", "Sistem Yazı Tipi"],
    ["System monospace", "Sistem Eş Aralıklı"],
    ["Search Remote Machines...", "Uzak Makinelerde Ara..."],
    ["Search Remote Machines…", "Uzak Makinelerde Ara…"],
    ["Search...", "Ara..."],
    ["Automation filters", "Otomasyon Filtreleri"],
    ["Automation template filters", "Otomasyon Şablonu Filtreleri"],
    ["All Runs", "Tüm Çalıştırmalar"],
    ["Use Find critical bugs template", "Kritik hataları bul şablonunu kullan"],
    ["Use Scan codebase for vulnerabilities template", "Kod tabanını güvenlik açıklarına karşı tara şablonunu kullan"],
    ["Use Generate docs template", "Belgeler oluştur şablonunu kullan"],
    ["Use Add test coverage template", "Test kapsamı ekle şablonunu kullan"],
    ["Loading remote machines...", "Uzak makineler yükleniyor..."],
    ["Loading remote machines…", "Uzak makineler yükleniyor…"],
    ["Connect...", "Bağlan..."],
    ["Search Cursor to find a prior conversation, veya summarize across conversations", "Önceki bir konuşmayı bulmak için Cursor'da arayın veya konuşmalar genelinde özetleyin"],
    ["Search Cursor to find a prior conversation, or summarize across conversations", "Önceki bir konuşmayı bulmak için Cursor'da arayın veya konuşmalar genelinde özetleyin"],
    ["Sor Cursor to find a prior conversation, veya summarize across conversations", "Önceki bir konuşmayı bulmak için Cursor'a sorun veya konuşmalar genelinde özetleyin"],
    ["Ask Cursor to find a prior conversation, or summarize across conversations", "Önceki bir konuşmayı bulmak için Cursor'a sorun veya konuşmalar genelinde özetleyin"],
    ["Automate repetitive tasks with always-on agents and configure Cursor's built-in agents for your team.", "Sürekli açık ajanlarla tekrarlanan görevleri otomatikleştirin ve Cursor'un yerleşik ajanlarını ekibiniz için yapılandırın."],
    ["Messages sent while Cursor is working can steer it mid-run without interrupting - turn it on under New Messages in Agent settings", "Cursor çalışırken gönderilen mesajlar çalışmayı kesmeden akışı yönlendirebilir — bu seçeneği Ajanlar ayarlarındaki Yeni Mesajlar bölümünden açın"],
    ["Includes Cursor Grok and Composer", "Cursor Grok ve Composer dahil"],
    ["Cursor installation appears corrupted. Please reinstall Cursor.", "Cursor kurulumunuz bozuk görünüyor. Lütfen Cursor'u yeniden kurun."],
    ["Show notifications for less urgent issues", "Daha az önemli sorunlar için bildirimleri göster"],
    ["Play a sound when agents finish or need attention", "Ajanlar tamamlandığında veya ilgilenmeniz gerektiğinde ses çal"],
    ["Choose Custom Sound...", "Özel Ses Seç..."],
    ["Choose Custom Sound…", "Özel Ses Seç…"],
    ["Preview", "Önizle"],
    ["Default Sound", "Varsayılan Ses"],
    ["Add keyword", "Anahtar Sözcük Ekle"],
    ["Remove submit", "Gönder Sözcüğünü Kaldır"],
    ["Third-Party Imports", "Üçüncü Taraf İçe Aktarımları"],
    ["Improve Cursor for everyone", "Cursor'u herkes için geliştirin"],
    [". Prompts and limited telemetry may also be shared with model providers when you explicitly select their models", ". İstemler ve sınırlı telemetri, modellerini açıkça seçtiğiniz sağlayıcılarla da paylaşılabilir"],
    ["No training. Code may be stored for Background Agent and other features.", "Eğitim yok. Kod, Arka Plan Ajanı ve diğer özellikler için saklanabilir."],
    ["No training and no storage. Background Agent and other features that require code storage will be disabled.", "Eğitim ve depolama yok. Kod depolaması gerektiren Arka Plan Ajanı ve diğer özellikler devre dışı bırakılır."],
    ["Upload image", "Resim Yükle"],
    ["Change image", "Resmi Değiştir"],
    ["PNG, JPEG, or WebP up to 2 MB", "En fazla 2 MB PNG, JPEG veya WebP"],
    ["Profile image must be smaller than 2 MB.", "Profil resmi 2 MB'den küçük olmalıdır."],
    ["Profile image must be a PNG, JPEG, or WebP file.", "Profil resmi PNG, JPEG veya WebP dosyası olmalıdır."],
    ["Public Profile", "Herkese Açık Profil"],
    ["Make the cursor.com profile page visible to anyone with the link", "cursor.com profil sayfasını bağlantıya sahip herkese görünür yap"],
    ["Allow the agent to celebrate with a shower of confetti", "Ajanın konfeti yağmuruyla kutlama yapmasına izin ver"],
    ["Unavailable while Reduce Motion is on (from settings or your system)", "Hareketi Azalt ayarı açıkken kullanılamaz"],
    ["Override OpenAI Base URL", "OpenAI Temel URL'sini Geçersiz Kıl"],
    ["Change the base URL for OpenAI API requests.", "OpenAI API istekleri için temel URL'yi değiştirin."],
    ["OpenAI API Key", "OpenAI API Anahtarı"],
    ["Anthropic API Key", "Anthropic API Anahtarı"],
    ["Google API Key", "Google API Anahtarı"],
    ["Turn Off Google Key", "Google Anahtarını Kapat"],
    ["Use /goal to set an objective that Cursor keeps pursuing until it is complete", "/goal ile Cursor'un tamamlanana kadar izlemeyi sürdüreceği bir hedef belirleyin"],
    ["Plan Mode improves agent outcomes and accuracy - hit shift+tab to get started", "Plan Modu, ajan sonuçlarını ve doğruluğunu iyileştirir — başlamak için Shift+Tab tuşlarına basın"],
    ["Plan Mode improves agent outcomes and accuracy – hit shift+tab to get started", "Plan Modu, ajan sonuçlarını ve doğruluğunu iyileştirir — başlamak için Shift+Tab tuşlarına basın"],
    ["Hooks let you control and extend the agent loop - use /create-hook to get started", "Kancalar, ajan döngüsünü kontrol edip genişletmenizi sağlar — başlamak için /create-hook kullanın"],
    ["Hooks let you control and extend the agent loop – use /create-hook to get started", "Kancalar, ajan döngüsünü kontrol edip genişletmenizi sağlar — başlamak için /create-hook kullanın"],
    ["Steer agents on this machine from your phone, web, and other devices", "Bu bilgisayardaki ajanları telefonunuzdan, web'den ve diğer cihazlardan yönetin"],
    ["Cursor Grok 4.6\nCursor and SpaceXAI's most powerful model, great for complex coding and knowledge work.\n\n256k context window\n\nVersion: high effort", "Cursor Grok 4.6\nKarmaşık kodlama ve bilgi çalışmaları için SpaceXAI'nin en güçlü modeli.\n\n256 bin bağlam penceresi\n\nSürüm: yüksek çaba"],
    ["Cursor and SpaceXAI's most powerful model, great for complex coding and knowledge work.", "Karmaşık kodlama ve bilgi çalışmaları için SpaceXAI'nin en güçlü modeli."],
    ["Version: high effort", "Sürüm: yüksek çaba"],
    ["256k context window", "256 bin bağlam penceresi"],
    ["300k context window", "300 bin bağlam penceresi"],
    ["Anthropic's large model class, great for difficult tasks.", "Anthropic'in büyük model sınıfı; zor görevler için idealdir."],
    ["Anthropic's most powerful model, great for difficult tasks.", "Anthropic'in en güçlü modeli; zor görevler için idealdir."],
    ["This model has special data retention policies.", "Bu modelin özel veri saklama politikaları vardır."],
    ["Kullan automations to save time on repetitive tasks with always-on agents", "Tekrarlanan görevlerde zaman kazanmak için sürekli açık ajanlarla otomasyonları kullanın"],
    ["Use automations to save time on repetitive tasks with always-on agents", "Tekrarlanan görevlerde zaman kazanmak için sürekli açık ajanlarla otomasyonları kullanın"],
    ["Cursor Grok 4.6 High Fast", "Cursor Grok 4.6 Yüksek Hızlı"],
    ["Cursor Grok 4.6 Medium Fast", "Cursor Grok 4.6 Orta Hızlı"],
    ["Cursor Grok 4.6 Low Fast", "Cursor Grok 4.6 Düşük Hızlı"],
    ["Cursor Grok 4.5 High Fast", "Cursor Grok 4.5 Yüksek Hızlı"],
    ["Cursor Grok 4.5 Medium Fast", "Cursor Grok 4.5 Orta Hızlı"],
    ["Cursor Grok 4.5 Low Fast", "Cursor Grok 4.5 Düşük Hızlı"],
    ["Cursor Grok 4.6 (fast)", "Cursor Grok 4.6 (hızlı)"],
    ["Cursor Grok 4.6 (Fast)", "Cursor Grok 4.6 (Hızlı)"],
    ["Cursor Grok 4.5 (Fast)", "Cursor Grok 4.5 (Hızlı)"],
    ["+ High Fast", "+ Yüksek Hızlı"],
    ["+ Medium Fast", "+ Orta Hızlı"],
    ["+ Low Fast", "+ Düşük Hızlı"],
    ["No Thinking", "Düşünme Yok"],
    ["No thinking", "Düşünme Yok"],
    ["no thinking", "düşünme yok"],
    ["Claude Sonnet 4 No Thinking", "Claude Sonnet 4 Düşünme Yok"],
    ["Meta's flagship model, great for agentic coding.", "Meta'nın amiral gemisi modeli; ajan tabanlı kodlama için idealdir."],
    ["Meta's flagship model, great for coding.", "Meta'nın amiral gemisi modeli; kodlama için idealdir."],
    ["great for agentic coding.", "ajan tabanlı kodlama için idealdir."],
    ["great for agentic coding", "ajan tabanlı kodlama için idealdir"],
    ["Cursor Models", "Cursor Modelleri"],
    ["Other Models", "Diğer Modeller"],
    ["Composer 2.5 (Fast)", "Composer 2.5 (Hızlı)"],
    ["Cursor's fast and efficient model -- great for everyday use.", "Cursor'ın hızlı ve verimli modeli — günlük kullanım için idealdir."],
    ["200k context window", "200 bin bağlam penceresi"],
    ["Cursor Grok 4.6 High", "Cursor Grok 4.6 Yüksek"],
    ["Composer 2.5 Fast", "Composer 2.5 Hızlı"],
    ["Cursor Grok 4.5 (fast)", "Cursor Grok 4.5 (hızlı)"],
    ["The predecessor to Cursor Grok 4.6, built for complex coding and knowledge work.", "Cursor Grok 4.6'nın öncülü; karmaşık kodlama ve bilgi çalışmaları için geliştirildi."],
    ["Cursor Grok 4.5 (fast)\nThe predecessor to Cursor Grok 4.6, built for complex coding and knowledge work.\n\n256k context window\n\nVersion: high effort", "Cursor Grok 4.5 (hızlı)\nCursor Grok 4.6'nın öncülü; karmaşık kodlama ve bilgi çalışmaları için geliştirildi.\n\n256 bin bağlam penceresi\n\nSürüm: yüksek çaba"],
    ["OpenAI's flagship GPT-5.6 model. Strongest agentic coding, biology, and cybersecurity capabilities, with a new max reasoning effort.", "OpenAI'nin amiral gemisi GPT-5.6 modeli. Yeni azami akıl yürütme çabasıyla en güçlü ajan tabanlı kodlama, biyoloji ve siber güvenlik yeteneklerini sunar."],
    ["272k context window", "272 bin bağlam penceresi"],
    ["Version: medium reasoning effort", "Sürüm: orta akıl yürütme çabası"],
    ["GPT-5.6 Sol\nOpenAI's flagship GPT-5.6 model. Strongest agentic coding, biology, and cybersecurity capabilities, with a new max reasoning effort.\n\n272k context window\n\nVersion: medium reasoning effort", "GPT-5.6 Sol\nOpenAI'nin amiral gemisi GPT-5.6 modeli. Yeni azami akıl yürütme çabasıyla en güçlü ajan tabanlı kodlama, biyoloji ve siber güvenlik yeteneklerini sunar.\n\n272 bin bağlam penceresi\n\nSürüm: orta akıl yürütme çabası"],
    ["PNG, JPEG, or WebP ...", "PNG, JPEG veya WebP ..."],
    ["When enabled, your cursor.com profile page is visible to anyone with the link.", "Etkinleştirildiğinde cursor.com profil sayfanız bağlantıya sahip herkes tarafından görünür."],
    ["New Messages", "Yeni Mesajlar"],
    ["Choose the default behavior of messages sent while Agent is working", "Ajan çalışırken gönderilen mesajların varsayılan davranışını seçin"],
    ["Manually Sent Messages from Queue", "Kuyruktan Elle Gönderilen Mesajlar"],
    ["Choose the default behavior of messages sent from the queue", "Kuyruktan gönderilen mesajların varsayılan davranışını seçin"],
    ["Allow agent to switch to modes like Plan or Debug without asking. When off, Cursor asks first, but skips if unanswered within 15 seconds.", "Ajanın Plan veya Hata Ayıklama gibi modlara sormadan geçmesine izin verin. Kapalıyken Cursor önce sorar; 15 saniye içinde yanıtlanmazsa geçişi atlar."],
    ["Choose Origin (cursor.com/codebase), GitHub, or Graphite for pull request links on web and desktop", "Web ve masaüstündeki çekme isteği bağlantıları için Origin (cursor.com/codebase), GitHub veya Graphite'ı seçin"],
    ["Cursor Models · Includes Cursor Grok and Composer", "Cursor Modelleri · Cursor Grok ve Composer dahil"],
    ["Additional usage beyond limits consumes on-demand spend.", "Sınırları aşan ek kullanım, isteğe bağlı harcamadan düşer."],
    ["to start a subagent in its own cloud VM, keeping your local workspace free", "ile yerel çalışma alanınızı boş tutarak bir alt ajanı kendi bulut sanal makinesinde başlatın"],
    ["Kullan /in-cloud to start a subagent in its own cloud VM, keeping your local workspace free", "/in-cloud ile yerel çalışma alanınızı boş tutarak bir alt ajanı kendi bulut sanal makinesinde başlatın"],
    ["high", "yüksek"],
    ["Configure MCPs in your Cursor Settings to give agents access to tools and data", "Ajanların araçlara ve verilere erişebilmesi için Cursor Ayarları'nda MCP'leri yapılandırın"],
    ["Configure MCPs in your Cursor Ayarları to give agents access to tools and data", "Ajanların araçlara ve verilere erişebilmesi için Cursor Ayarları'nda MCP'leri yapılandırın"],
    ["Configure MCPs in your Cursor", "Cursor içinde MCP'leri yapılandırın"],
    ["to give agents access to tools and data", "ve ajanların araçlara ve verilere erişmesini sağlayın"],
    ["New Agents Window", "Yeni Ajanlar Penceresi"],
    ["Close Window", "Pencereyi Kapat"],
    ["Exit", "Çıkış"],
    ["Zen Mode", "Zen Modu"],
    ["Secondary Side Bar", "İkincil Kenar Çubuğu"],
    ["Render Whitespace", "Boşluk Karakterlerini Göster"],
    ["Agents Window ajanına geç", "Ajanlar Penceresine Geç"],
    ["Continue Working", "Çalışmaya Devam Et"],
    ["No Destinations Available", "Kullanılabilir Hedef Yok"],
    ["Send follow-up", "Takip Mesajı Gönder"],
    ["New Automation", "Yeni Otomasyon"],
    ["Ship better code, faster", "Daha iyi kodu daha hızlı üretin"],
    ["Name", "Ad"],
    ["Created By", "Oluşturan"],
    ["Status", "Durum"],
    ["Inactive", "Etkin Değil"],
    ["Type @ for tools, / for commands...", "Araçlar için @, komutlar için / yazın..."],
    ["Type @ for tools, / for commands…", "Araçlar için @, komutlar için / yazın…"],
    ["Memories", "Anılar"],
    ["Test run", "Test Çalıştırması"],
    ["Toggle automation enabled state", "Otomasyonun etkinliğini aç veya kapat"],
    ["Remove Memories", "Anıları Kaldır"],
    ["More actions", "Diğer Eylemler"],
    ["Automation filters", "Otomasyon Filtreleri"],
    ["Automation template filters", "Otomasyon Şablonu Filtreleri"],
    ["Automation detail sections", "Otomasyon Ayrıntı Bölümleri"],
    ["Account", "Hesap"],
    ["Configure", "Yapılandır"],
    ["Agent Conversations", "Ajan Konuşmaları"],
    ["Colors", "Renkler"],
    ["Typography", "Tipografi"],
    ["Motion", "Hareket"],
    ["Decrease", "Azalt"],
    ["Increase", "Artır"],
    ["Tint hue", "Renk Tonu"],
    ["Tint intensity", "Renk Tonu Yoğunluğu"],
    ["Steer a running agent without stopping it", "Çalışan ajanı durdurmadan yönlendirin"],
    ["set New Messages to Send Immediately in your Agent settings", "Ajanlar ayarlarındaki Yeni Mesajlar seçeneğini Hemen Gönder olarak ayarlayın"],
    ["set Yeni Mesajlar to Send Immediately in your Ajanlar settings", "Ajanlar ayarlarındaki Yeni Mesajlar seçeneğini Hemen Gönder olarak ayarlayın"],
    ["Automate repetitive tasks with always-on cloud agents that respond to environment triggers.", "Ortam tetikleyicilerine yanıt veren sürekli açık bulut ajanlarıyla tekrarlanan görevleri otomatikleştirin."],
    ["Total Automations", "Toplam Otomasyon"],
    ["Successful · 7d", "Başarılı · 7 gün"],
    ["Failed · 7d", "Başarısız · 7 gün"],
    ["Run History", "Çalıştırma Geçmişi"],
    ["Mine", "Benim"],
    ["No Automations Yet", "Henüz Otomasyon Yok"],
    ["Run agents on a schedule or automatically in response to events. Billed at plan rates.", "Ajanları bir programa göre veya olaylara yanıt olarak otomatik çalıştırın. Kullanım plan ücretleriyle hesaplanır."],
    ["Popular", "Popüler"],
    ["Code Review", "Kod İncelemesi"],
    ["Security", "Güvenlik"],
    ["Incidents & Triage", "Olaylar ve Önceliklendirme"],
    ["Data & Research", "Veri ve Araştırma"],
    ["Environment", "Ortam"],
    ["Untitled", "Adsız"],
    ["You have view-only access. Contact the owner or a team admin to edit this automation.", "Yalnızca görüntüleme erişiminiz var. Bu otomasyonu düzenlemek için sahibiyle veya ekip yöneticisiyle iletişime geçin."],
    ["Select repository", "Depo Seç"],
    ["By", "Oluşturan"],
    ["Triggers", "Tetikleyiciler"],
    ["Add Trigger", "Tetikleyici Ekle"],
    ["Agent Instructions", "Ajan Talimatları"],
    ["Tools", "Araçlar"],
    ["Add Tool or MCP", "Araç veya MCP Ekle"],
    ["Manage", "Yönet"],
    ["Delete", "Sil"],
    ["Settings", "Ayarlar"],
    ["Find critical bugs", "Kritik Hataları Bul"],
    ["Analyze recent commits for high-severity correctness bugs and submit safe fixes", "Son değişikliklerdeki ciddi doğruluk hatalarını inceleyin ve güvenli düzeltmeler gönderin"],
    ["Scheduled", "Zamanlandı"],
    ["Send Slack", "Slack'e Gönder"],
    ["Scan codebase for vulnerabilities", "Kod Tabanını Güvenlik Açıklarına Karşı Tara"],
    ["Review the full repository on a schedule and alert on validated high-impact security issues", "Tüm depoyu belirli aralıklarla inceleyin ve doğrulanmış yüksek etkili güvenlik sorunlarında uyarı alın"],
    ["Generate docs", "Belgeler Oluştur"],
    ["Create and update developer documentation for recently changed or under-documented code", "Yakın zamanda değişen veya yetersiz belgelenmiş kod için geliştirici belgeleri oluşturun ve güncelleyin"],
    ["Add test coverage", "Test Kapsamı Ekle"],
    ["Switch Model", "Model Değiştir"],
    ["Search or Paste Link", "Ara veya Bağlantı Yapıştır"],
    ["High Contrast", "Yüksek Karşıtlık"],
    ["Follow System High Contrast", "Sistem Yüksek Karşıtlığını İzle"]
    ,["Search Plugins, Skills, MCPs...", "Eklenti, Beceri ve MCP Ara..."]
    ,["Discover", "Keşfet"]
    ,["Featured", "Öne Çıkanlar"]
    ,["Infrastructure", "Altyapı"]
    ,["Add", "Ekle"]
    ,["Added", "Eklendi"]
    ,["Marketplace", "Eklenti Pazarı"]
    ,["Uninstall", "Kaldır"]
    ,["Private", "Özel"]
    ,["Try in Chat", "Sohbette Dene"]
    ,["Skills", "Beceriler"]
    ,["Sor Cursor to find a prior conversation, veya summarize across conversations", "Cursor'dan önceki bir konuşmayı bulmasını veya konuşmalar arasında özet çıkarmasını isteyin"]
    ,["Ask Cursor to find a prior conversation, or summarize across conversations", "Cursor'dan önceki bir konuşmayı bulmasını veya konuşmalar arasında özet çıkarmasını isteyin"]
    ,["Model", "Yapay Zekâ Modeli"]
    ,["Use Datadog directly in Cursor through a preconfigured Datadog MCP server. Query logs, metrics, traces, dashboards, and more through natural conversation. This plugin is in preview.", "Önceden yapılandırılmış Datadog MCP sunucusuyla Datadog'u doğrudan Cursor içinde kullanın. Günlükleri, metrikleri, izleri, panoları ve daha fazlasını doğal dille sorgulayın. Bu eklenti önizleme aşamasındadır."]
    ,["Cursor Plugin for Linear - enables AI assistants to manage issues, projects, documents, and more across your Linear workspace", "Linear çalışma alanınızdaki sorunları, projeleri, belgeleri ve daha fazlasını yapay zekâ ajanlarıyla yönetmenizi sağlar."]
    ,["Slack MCP server. Search channels, send messages, and perform other Slack actions through MCP-compatible clients.", "Slack MCP sunucusu. Kanallarda arama yapın, mesaj gönderin ve MCP uyumlu istemciler üzerinden diğer Slack işlemlerini gerçekleştirin."]
    ,["Official Apify agent skills for web scraping, data extraction, and automation", "Web kazıma, veri çıkarma ve otomasyon için resmi Apify ajan becerileri."]
    ,["Skills for NVIDIAs ecosystem spans GPU acceleration, CUDA, AI agents, inference, robotics, Physical AI, Omniverse, and simulation. This plugin helps you find the right skills to help in building NVIDIA-powered workflows.", "NVIDIA ekosistemi için GPU hızlandırma, CUDA, yapay zekâ ajanları, çıkarım, robotik, Fiziksel Yapay Zekâ, Omniverse ve simülasyon becerileri. NVIDIA destekli iş akışları oluşturmak için doğru becerileri bulmanıza yardımcı olur."]
    ,["Guide developers through adding maps, places search, geocoding, routing, and other geospatial features with Amazon Location Service, including authentication setup, SDK integration, and best practices.", "Amazon Location Service ile harita, yer arama, coğrafi kodlama, rota ve diğer konum özelliklerini ekleme; kimlik doğrulama, SDK entegrasyonu ve iyi uygulamalar konusunda rehberlik eder."]
    ,["The Appwrite plugin for Cursor includes skills and MCP servers, allowing AI agents to access your projects and correctly integrate with your projects.", "Cursor için Appwrite eklentisi, yapay zekâ ajanlarının projelerinize erişmesini ve doğru biçimde entegre olmasını sağlayan beceriler ile MCP sunucuları içerir."]
    ,["Build full-stack apps with AWS Amplify Gen 2 using guided workflows for authentication, data models, storage, GraphQL APIs, and Lambda functions.", "Kimlik doğrulama, veri modelleri, depolama, GraphQL API'leri ve Lambda işlevleri için yönlendirmeli akışlarla AWS Amplify Gen 2 üzerinde tam kapsamlı uygulamalar oluşturun."]
    ,["Build, deploy, and operate applications on AWS. Skills to author infrastructure-as-code (CDK, CloudFormation), use core services (Lambda, API Gateway, Step Functions, ECS/Fargate, ECR, IAM, Amazon Bedrock with Knowledge Bases and Guardrails, Amplify), and complete common tasks across observability (CloudWatch, X-Ray, CloudTrail, ADOT), messaging and streaming (SQS, SNS, EventBridge, Kinesis, MSK), AWS SDKs (boto3, JS v3, Swift), and cost optimization.", "AWS üzerinde uygulama oluşturun, dağıtın ve işletin. Kod olarak altyapı, temel AWS hizmetleri, gözlemlenebilirlik, mesajlaşma ve akış, AWS SDK'ları ile maliyet iyileştirme işlerinde yardımcı olur."]
    ,["Expert database guidance for the AWS database portfolio. Design schemas, execute queries, handle migrations, and choose the right database for your workload.", "AWS veritabanı portföyü için uzman rehberliği sağlar. Şema tasarlayın, sorgu çalıştırın, geçişleri yönetin ve iş yükünüz için doğru veritabanını seçin."]
    ,["Deploy applications to AWS with architecture recommendations, cost estimates, and IaC deployment. Generate validated AWS architecture diagrams as draw.io XML.", "Mimari öneriler, maliyet tahminleri ve kod olarak altyapı dağıtımıyla uygulamaları AWS'ye yayımlayın. Doğrulanmış AWS mimari diyagramlarını draw.io XML biçiminde oluşturun."]
    ,["Design, build, deploy, test, and debug serverless applications with AWS Serverless services.", "AWS Serverless hizmetleriyle sunucusuz uygulamalar tasarlayın, geliştirin, dağıtın, test edin ve hatalarını ayıklayın."]
    ,["Microsoft Azure MCP and Skills integration for cloud resource management, deployments, and Azure services. Manage your Azure infrastructure, monitor applications, and deploy resources directly from Cursor.", "Bulut kaynaklarını, dağıtımları ve Azure hizmetlerini yönetmek için Microsoft Azure MCP ve beceri entegrasyonu. Azure altyapınızı yönetin, uygulamaları izleyin ve kaynakları doğrudan Cursor'dan dağıtın."]
    ,["Railway agent skills and MCP server for deploying, configuring, monitoring, and troubleshooting apps and infrastructure on Railway from Cursor. Manage services, environments, deployments, databases, object storage, networking, and observability.", "Cursor üzerinden Railway'de uygulama ve altyapı dağıtma, yapılandırma, izleme ve sorun giderme için ajan becerileri ile MCP sunucusu. Hizmetleri, ortamları, dağıtımları, veritabanlarını, nesne depolamayı, ağı ve gözlemlenebilirliği yönetin."]
    ,["Review recent changes and add tests for high-risk logic that lacks adequate coverage", "Son değişiklikleri inceleyin ve yeterli kapsamı olmayan yüksek riskli mantık için testler ekleyin"]
    ,["Find vulnerabilities", "Güvenlik Açıklarını Bul"]
    ,["Review pull requests for exploitable security issues and flag only validated findings before merge", "Pull request'leri istismar edilebilir güvenlik sorunları açısından inceleyin ve birleştirmeden önce yalnızca doğrulanmış bulguları işaretleyin"]
    ,["PR opened", "PR Açıldı"]
    ,["PR Comment", "PR Yorumu"]
    ,["Assign PR reviewers", "PR İnceleyicileri Ata"]
    ,["Assign reviewers based on code changes and auto-approve low-risk PRs", "Kod değişikliklerine göre inceleyiciler atayın ve düşük riskli PR'ları otomatik onaylayın"]
    ,["PR pushed", "PR Gönderildi"]
    ,["Request Reviewers", "İnceleyici İste"]
    ,["Autofix PR review comments", "PR İnceleme Yorumlarını Otomatik Düzelt"]
    ,["Take a first pass at addressing inline review comments on PR diffs", "PR farklarındaki satır içi inceleme yorumlarını çözmek için ilk geçişi yapın"]
    ,["PR review comment", "PR İnceleme Yorumu"]
    ,["Monitor engineering invariants", "Mühendislik Değişmezlerini İzle"]
    ,["Re-check critical repository invariants on a schedule and alert only when a rule regresses", "Kritik depo değişmezlerini belirli aralıklarla yeniden denetleyin ve yalnızca bir kural gerilediğinde uyarın"]
    ,["Auto Import for Python", "Python için Otomatik İçe Aktarma"]
    ,["Partial Accepts", "Kısmi Kabuller"]
    ,["User", "Kullanıcı"]
    ,["Team", "Ekip"]
    ,["Always respond in Turkish", "Her zaman Türkçe yanıt ver"]
    ,["Home workspace guidance", "Ana Çalışma Alanı Yönergeleri"]
    ,["Interact with local Chrome browser session (only on explicit user approval after being asked to inspect, debug, or interact with a page open in Chrome)", "Yerel Chrome tarayıcı oturumuyla etkileşim kurar (yalnızca açık bir Chrome sayfasını inceleme, hata ayıklama veya sayfayla etkileşim isteği için kullanıcıdan açık onay alındığında)"]
    ,["See the user's ENTIRE Windows desktop live (all windows — Comet, IDE, terminal, data) via a local screenshot. Use BEFORE acting on the Sentos/Comet flow and whenever the user references what's on their screen, so you never act blind on stale context.", "Kullanıcının TÜM Windows masaüstünü yerel ekran görüntüsüyle canlı görür. Sentos/Comet akışında işlem yapmadan ve kullanıcı ekrandakine atıfta bulunduğunda eski bağlama göre işlem yapmamak için kullanılır."]
    ,["Perform a read-only, defect-first review of a specified code change and return every actionable finding. Use when another agent delegates review of uncommitted changes, a base-branch diff, a commit, or custom review instructions.", "Belirtilen kod değişikliğini salt okunur ve hata odaklı inceler; uygulanabilir tüm bulguları döndürür. Kaydedilmemiş değişiklikler, dal farkı, commit veya özel inceleme talimatları devredildiğinde kullanılır."]
    ,["Plugin that includes the Figma MCP server and Skills for common workflows", "Yaygın iş akışları için Figma MCP sunucusu ve becerilerini içeren eklenti"]
    ,["Skills for NVIDIAs ecosystem spans GPU acceleration, CUDA, AI agents, inference, robotics, Physical AI, Omniverse, and simulation. This plugin helps you understand the pieces, choose a path, validate your setup, and build practical NVIDIA-powered workflows.", "NVIDIA ekosistemi için GPU hızlandırma, CUDA, yapay zekâ ajanları, çıkarım, robotik, Fiziksel Yapay Zekâ, Omniverse ve simülasyon becerileri. Bileşenleri anlamanıza, yol seçmenize, kurulumu doğrulamanıza ve NVIDIA destekli pratik iş akışları oluşturmanıza yardımcı olur."]
    ,["Remediate dependency vulnerabilities", "Bağımlılık Güvenlik Açıklarını Gider"]
    ,["Triage dependency-vulnerability tickets from Linear and open upgrade PRs when the fix is safe", "Linear'daki bağımlılık güvenlik açığı kayıtlarını önceliklendirin ve düzeltme güvenliyse yükseltme PR'ları açın"]
    ,["Issue created", "Sorun Oluşturuldu"]
    ,["Fix bugs reported in Slack", "Slack'te Bildirilen Hataları Düzelt"]
    ,["Monitor a Slack channel for bug reports, investigate the codebase, and fix with a PR", "Hata bildirimleri için bir Slack kanalını izleyin, kod tabanını inceleyin ve bir PR ile düzeltin"]
    ,["New message in channel", "Kanalda Yeni Mesaj"]
    ,["Triage failed GitHub Actions", "Başarısız GitHub Actions Çalıştırmalarını İncele"]
    ,["Investigate failed or cancelled workflow runs and report findings in Slack", "Başarısız veya iptal edilmiş iş akışı çalıştırmalarını inceleyin ve bulguları Slack'te bildirin"]
    ,["Workflow run completed", "İş Akışı Tamamlandı"]
    ,["Fix CI failures", "CI Hatalarını Düzelt"]
    ,["Detect CI failures on main and automatically open PRs", "Ana daldaki CI hatalarını algılayın ve otomatik olarak PR açın"]
    ,["Checks completed", "Denetimler Tamamlandı"]
    ,["Investigate PagerDuty incidents", "PagerDuty Olaylarını İncele"]
    ,["Investigate incidents using Datadog and code context", "Datadog ve kod bağlamını kullanarak olayları inceleyin"]
    ,["Incident triggered", "Olay Tetiklendi"]
    ,["Investigate Sentry issues", "Sentry Sorunlarını İncele"]
    ,["Investigate errors from Sentry, identify root causes, and propose fixes", "Sentry hatalarını inceleyin, temel nedenleri belirleyin ve düzeltmeler önerin"]
    ,["Any issue event", "Herhangi Bir Sorun Olayı"]
    ,["Investigate top Datadog errors", "Önemli Datadog Hatalarını İncele"]
    ,["Investigate recurring production errors from Datadog, identify root causes, and propose fixes", "Datadog'daki yinelenen üretim hatalarını inceleyin, temel nedenleri belirleyin ve düzeltmeler önerin"]
    ,["Triage Linear issues", "Linear Sorunlarını Önceliklendir"]
    ,["Triage new issues by investigating bugs, planning feature requests, and opening PRs for easy fixes", "Yeni sorunları; hataları inceleyerek, özellik isteklerini planlayarak ve kolay düzeltmeler için PR açarak önceliklendirin"]
    ,["Summarize changes daily", "Değişiklikleri Günlük Özetle"]
    ,["Post a daily Slack digest summarizing notable repository changes and risks from the previous day", "Önceki günün önemli depo değişikliklerini ve risklerini özetleyen günlük bir Slack özeti gönderin"]
    ,["Customer Health Monitoring Agent", "Müşteri Sağlığı İzleme Ajanı"]
    ,["Find at-risk customers using usage analytics, call notes, Slack escalations, and Linear blockers", "Kullanım analizleri, görüşme notları, Slack bildirimleri ve Linear engelleriyle risk altındaki müşterileri bulun"]
    ,["Product Analytics Agent", "Ürün Analitiği Ajanı"]
    ,["Weekly product usage, activation, retention, and feature adoption digest from Databricks", "Databricks'ten haftalık ürün kullanımı, etkinleştirme, elde tutma ve özellik benimseme özeti"]
    ,["Product FAQ Agent", "Ürün SSS Ajanı"]
    ,["Answer product questions in a dedicated Slack channel using Slack, Notion, Linear, and GitHub context", "Slack, Notion, Linear ve GitHub bağlamını kullanarak özel bir Slack kanalındaki ürün sorularını yanıtlayın"]
    ,["Product Finance Agent", "Ürün Finans Ajanı"]
    ,["Analyze Stripe revenue, churn signals, and product pricing opportunities", "Stripe gelirini, müşteri kaybı sinyallerini ve ürün fiyatlandırma fırsatlarını analiz edin"]
    ,["Slack Digest Agent", "Slack Özet Ajanı"]
    ,["Summarize important DMs, mentions, and the user's top active Slack channels", "Önemli özel mesajları, bahsetmeleri ve kullanıcının en etkin Slack kanallarını özetleyin"]
    ,["Investigate environment setup failures", "Ortam Kurulum Hatalarını İncele"]
    ,["Monitor environment build health", "Ortam Derleme Sağlığını İzle"]
    ,["Health check of your cloud environment's builds with root cause analysis for failed builds", "Bulut ortamı derlemelerinizin sağlığını denetleyin ve başarısız derlemelerin temel nedenlerini analiz edin"]
    ,["Archive", "Arşivle"]
    ,["Pin", "Sabitle"]
    ,["Unpin", "Sabitlemeyi Kaldır"]
    ,["Delete", "Sil"]
    ,["Remove", "Kaldır"]
    ,["Edit", "Düzenle"]
    ,["Copy", "Kopyala"]
    ,["Open", "Aç"]
    ,["Close", "Kapat"]
    ,["Restore", "Geri Yükle"]
    ,["Rename", "Yeniden Adlandır"]
    ,["Move", "Taşı"]
    ,["Mark as Unread", "Okunmadı Olarak İşaretle"]
    ,["Mark as Read", "Okundu Olarak İşaretle"]
    ,["Fork", "Dallandır"]
    ,["more", "tane daha"]
    ,["Browse", "Göz At"]
    ,["Browse Marketplace", "Eklenti Pazarına Göz At"]
    ,["Search agents, files, actions...", "Ajanları, dosyaları ve eylemleri ara..."]
    ,["Search agents, Canvas, files, actions...", "Ajanlarda, Tuval'de, dosyalarda ve eylemlerde ara..."]
    ,["Search agents, Canvas, files, actions…", "Ajanlarda, Tuval'de, dosyalarda ve eylemlerde ara…"]
    ,["Search agents...", "Ajanlarda ara..."]
    ,["Select Multiple", "Birden Fazla Seç"]
    ,["Recent Agents", "Son Ajanlar"]
    ,["Recent Files", "Son Dosyalar"]
    ,["Recent", "Son Kullanılanlar"]
    ,["Current", "Mevcut"]
    ,["Older", "Daha Eski"]
    ,["Filter results", "Sonuçları Filtrele"]
    ,["Draft", "Taslak"]
    ,["Search actions...", "Eylemlerde ara..."]
    ,["Search Cursor settings...", "Cursor ayarlarında ara..."]
    ,["Search Cursor settings…", "Cursor ayarlarında ara…"]
    ,["Developer: Reveal User Data Folder", "Geliştirici: Kullanıcı Verileri Klasörünü Göster"]
    ,["Developer: Delete Old Chats…", "Geliştirici: Eski Sohbetleri Sil…"]
    ,["Canvas'ı Aç", "Tuval'i Aç"]
    ,["Email", "E-posta"]
    ,["Handle", "Kullanıcı Adı"]
    ,["Personal Usage", "Kişisel Kullanım"]
    ,["Included in", "Dahil Olanlar"]
    ,["On Demand", "İsteğe Bağlı"]
    ,["Sync Skills for Cloud Agents", "Bulut Ajanları İçin Becerileri Eşitle"]
    ,["Profile Image", "Profil Resmi"]
    ,["Links", "Bağlantılar"]
    ,["On-Demand", "İsteğe Bağlı"]
    ,["Account Label", "Hesap Etiketi"]
    ,["Add Folder", "Klasör Ekle"]
    ,["Add or search model", "Model Ekle veya Ara"]
    ,["Add Plugins", "Eklenti Ekle"]
    ,["Add Project Item to Chat", "Proje Öğesini Sohbete Ekle"]
    ,["Add weekly recap email", "Haftalık Özet E-postası Ekle"]
    ,["Add-habit keyboard flow", "Alışkanlık Ekleme Klavye Akışı"]
    ,["Back to tasks", "Görevlere Dön"]
    ,["Build options", "Derleme Seçenekleri"]
    ,["Clear Forced Skill Migration Banner", "Zorunlu Beceri Taşıma Başlığını Temizle"]
    ,["Close Customize", "Özelleştir'i Kapat"]
    ,["Close Pane", "Bölmeyi Kapat"]
    ,["Close subscriptions tray", "Abonelikler Tepsisini Kapat"]
    ,["Collapse queue", "Kuyruğu Daralt"]
    ,["Dismiss queue", "Kuyruğu Kapat"]
    ,["Remove from queue", "Kuyruktan Çıkar"]
    ,["Confirm VS Code import", "VS Code İçe Aktarımını Onayla"]
    ,["Copy artifact", "Yapıtı Kopyala"]
    ,["Debug: Open Skill Publishing Logs", "Hata Ayıklama: Beceri Yayımlama Günlüklerini Aç"]
    ,["Delete automation", "Otomasyonu Sil"]
    ,["Delete old chats", "Eski Sohbetleri Sil"]
    ,["Dismiss outage alert", "Kesinti Uyarısını Kapat"]
    ,["Edit Fetch Domain Allowlist, one domain per line", "Getirme alan adı izin listesini düzenle; her satıra bir alan adı"]
    ,["Edit MCP server", "MCP Sunucusunu Düzenle"]
    ,["Expand full chat", "Sohbetin Tamamını Genişlet"]
    ,["Failed to Apply Suggestion", "Öneri Uygulanamadı"]
    ,["Failed to collect conversation history", "Konuşma geçmişi alınamadı"]
    ,["File filters", "Dosya Filtreleri"]
    ,["Install MCP server", "MCP Sunucusunu Yükle"]
    ,["Loading Cloud Agents settings", "Bulut Ajanları Ayarları Yükleniyor"]
    ,["Move to folder", "Klasöre Taşı"]
    ,["Open project", "Projeyi Aç"]
    ,["Open Pull Request Externally", "PR'ı Dışarıda Aç"]
    ,["Open video preview", "Video Önizlemesini Aç"]
    ,["Project notes selection actions", "Proje Notu Seçim Eylemleri"]
    ,["Queued message actions", "Kuyruğa Alınan Mesaj Eylemleri"]
    ,["Remove Account", "Hesabı Kaldır"]
    ,["Remove screenshot", "Ekran Görüntüsünü Kaldır"]
    ,["Remove Subscription", "Aboneliği Kaldır"]
    ,["Restore edits to the latest checkpoint", "Düzenlemeleri Son Kontrol Noktasına Geri Yükle"]
    ,["Save", "Kaydet"]
    ,["Save All Files", "Tüm Dosyaları Kaydet"]
    ,["Search files", "Dosyalarda ara"]
    ,["Search fonts", "Yazı tiplerinde ara"]
    ,["Search history or enter a URL", "Geçmişte ara veya URL gir"]
    ,["Search MCPs", "MCP'lerde ara"]
    ,["Search pull requests", "PR'larda ara"]
    ,["Share", "Paylaş"]
    ,["Share link", "Paylaşım Bağlantısı"]
    ,["Stack options", "Yığın Seçenekleri"]
    ,["Update Access", "Erişimi Güncelle"]
    ,["Updating privacy settings", "Gizlilik Ayarları Güncelleniyor"]
    ,["Upgrade to a Pro account", "Pro Hesaba Yükselt"]
    ,["Upload profile image", "Profil Resmi Yükle"]
    ,["Claude Code: Open", "Claude Code'u Aç"]
    ,["Switch Agent Mode (Ctrl+.)", "Ajan Modunu Değiştir (Ctrl+.)"]
    ,["Show context usage", "Bağlam Kullanımını Göster"]
    ,["Tab AI Stats (Today): 0/0 lines (0%)", "Sekme Yapay Zekâ İstatistikleri (Bugün): 0/0 satır (%0)"]
    ,["Command Palette...", "Komut Paleti..."]
    ,["View: Open View...", "Görünüm: Görünüm Aç..."]
    ,["Explorer", "Gezgin"]
    ,["Source Control", "Kaynak Denetimi"]
    ,["Problems", "Sorunlar"]
    ,["Output", "Çıktı"]
    ,["Word Wrap", "Sözcük Kaydır"]
    ,["Agent connection lost", "Ajan bağlantısı kesildi"]
    ,["Automatically resume working on agents and their subagents after a reload or restart", "Yeniden yükleme veya yeniden başlatmanın ardından ajanlar ve alt ajanları üzerinde çalışmaya otomatik olarak devam et"]
    ,["Change the base URL for OpenAI API requests.", "OpenAI API istekleri için temel URL'yi değiştirin."]
    ,["Choose a model or use the cost- and availability-aware default", "Bir model seçin veya maliyet ve kullanılabilirliği gözeten varsayılanı kullanın"]
    ,["Choose which models appear in the model picker", "Model seçicide hangi modellerin görüneceğini seçin"]
    ,["Continue Interrupted Agents", "Kesintiye Uğrayan Ajanlara Devam Et"]
    ,["Reset to default sound", "Varsayılan Sese Sıfırla"]
    ,["The agent process restarted or the remote connection dropped before this message was sent. Retry to send it again.", "Bu mesaj gönderilmeden önce ajan işlemi yeniden başladı veya uzak bağlantı kesildi. Yeniden göndermeyi deneyin."]
    ,["Upgrade Available", "Yükseltme Mevcut"]
    ,["your Anthropic key", "Anthropic anahtarınız"]
    ,["your Google AI Studio key", "Google AI Studio anahtarınız"]
    ,["your OpenAI key", "OpenAI anahtarınız"]
    ,["Add Workspace", "Çalışma Alanı Ekle"]
    ,["Any Repo", "Herhangi Bir Depo"]
    ,["More self-hosted machines", "Diğer Yerel Çalıştırıcı Makineleri"]
    ,["Remove From Queue", "Kuyruktan Çıkar"]
    ,["Remove from merge queue?", "Birleştirme kuyruğundan kaldırılsın mı?"]
    ,["Self-Hosted Machines", "Yerel Çalıştırıcı Makineleri"]
    ,["Run in", "Şurada Çalıştır"]
    ,["Run on this machine", "Bu Makinede Çalıştır"]
    ,["Run on Cursor servers", "Cursor Sunucularında Çalıştır"]
    ,["Run on members' machines", "Üyelerin Makinelerinde Çalıştır"]
    ,["Dismiss worker offline banner", "Çalıştırıcı Çevrimdışı Bildirimini Kapat"]
    ,["Start voice conversation", "Sesli Sohbet Başlat"]
    ,["End voice conversation", "Sesli Sohbeti Bitir"]
    ,["Voice conversation in progress", "Sesli Sohbet Devam Ediyor"]
    ,["Enter a valid Git branch name", "Geçerli bir Git dal adı girin"]
    ,["Enter a branch name", "Bir dal adı girin"]
    ,["Remote", "Uzak"]
    ,["Start from scratch", "Sıfırdan Başla"]
    ,["Sor Cursor to find a prior conversation, veya summarize across conversations", "Önceki bir konuşmayı bulması veya konuşmalar arasında özetleme yapması için Cursor'a sorun"]
    ,["Adjust Plan", "Planı Ayarla"]
    ,["Additional usage beyond limits consumes Other Models quota or on-demand spend.", "Sınırları aşan ek kullanım, Diğer Modeller kotasından veya isteğe bağlı harcamadan düşer."]
    ,["Default Model", "Varsayılan Model"]
    ,["Interrupt", "Kesintiye Uğrat"]
    ,["Nightly", "Gecelik"]
    ,["Ajan skills help you customize Cursor for your workflows - use /create-skill to get started", "Ajan becerileri Cursor'u iş akışlarınıza göre özelleştirmenize yardımcı olur; başlamak için /create-skill kullanın"]
    ,["Ask Cursor questions about your codebase", "Kod tabanınız hakkında Cursor'a sorular sorun"]
    ,["Cursor syncs your local skills so they can be used with Cloud Agents. Turn this off to disable syncing.", "Cursor, yerel becerilerinizi Bulut Ajanlarında kullanabilmeniz için eşitler. Eşitlemeyi kapatmak için bu seçeneği devre dışı bırakın."]
    ,["Google API Key", "Google API Anahtarı"]
    ,["With your Cursor Pro subscription, you do not need to use your own Google key!", "Cursor Pro aboneliğinizle kendi Google anahtarınızı kullanmanız gerekmez!"]
    ,["Turn Off Google Key", "Google Anahtarını Kapat"]
    ,["Check for Updates...", "Güncellemeleri Denetle..."]
    ,["Checking for Updates...", "Güncellemeler Denetleniyor..."]
    ,["Downloading Update...", "Güncelleme İndiriliyor..."]
    ,["Installing Update...", "Güncelleme Yükleniyor..."]
    ,["Do you want to open this link?", "Bu bağlantıyı açmak istiyor musunuz?"]
    ,["Connected to remote.", "Uzak makineye bağlandı."]
    ,["Collapse All", "Tümünü Daralt"]
    ,["Expand All", "Tümünü Genişlet"]
    ,["New &&Window", "Yeni &&Pencere"]
    ,["New Canvas", "Yeni Tuval"]
    ,["Open External Link", "Harici Bağlantıyı Aç"]
    ,["Open Folder", "Klasör Aç"]
    ,["Open Recent", "Son Kullanılanları Aç"]
    ,["Show Active File Only", "Yalnızca Etkin Dosyayı Göster"]
    ,["Show Errors", "Hataları Göster"]
    ,["Show Excluded Files", "Hariç Tutulan Dosyaları Göster"]
    ,["Show Infos", "Bilgileri Göster"]
    ,["Show Less", "Daha Az Göster"]
    ,["Show More", "Daha Fazla Göster"]
    ,["Show Warnings", "Uyarıları Göster"]
    ,["Show message in multiple lines", "Mesajı Birden Çok Satırda Göster"]
    ,["Show message in single line", "Mesajı Tek Satırda Göster"]
    ,["No source control providers registered.", "Kayıtlı kaynak denetimi sağlayıcısı yok."]
    ,["Canvas is no longer available", "Tuval artık kullanılamıyor"]
    ,["Could not open Canvas", "Tuval açılamadı"]
    ,["Tool Call Density", "Araç Çağrısı Yoğunluğu"]
    ,["Theme", "Tema"]
    ,["Use", "Kullan"]
    ,["Use automations to save time on repetitive tasks with always-on agents", "Sürekli çalışan ajanlarla tekrarlı görevlerde zaman kazanmak için otomasyonları kullanın"]
    ,["automations to save time on repetitive tasks with always-on agents", "otomasyonlarla sürekli çalışan ajanlarda tekrarlı görevlerde zaman kazanın"]
    ,["Actions", "Eylemler"]
    ,["Dictate", "Dikte Et"]
    ,["Mode", "Mod"]
    ,["Agent Mode", "Ajan Modu"]
    ,["Debug Mode", "Hata Ayıklama Modu"]
    ,["Select", "Seç"]
    ,["Results", "Sonuçlar"]
    ,["New agent", "Yeni Ajan"]
    ,["or", "veya"]
    ,["Change Filter", "Filtreyi Değiştir"]
    ,["Ctrl+ğ or Ctrl+ü Filtreyi Değiştir", "Ctrl+ğ veya Ctrl+ü ile filtreyi değiştir"]
    ,["Configure Display Language", "Görüntüleme Dilini Yapılandır"]
    ,["Previous Tab", "Önceki Sekme"]
    ,["Toggle Design Mode", "Tasarım Modunu Aç/Kapat"]
    ,["Reset choice for 'File operation needs preview'", "'Dosya işlemi için önizleme gerekiyor' seçimini sıfırla"]
    ,["Comments: Go to Next Commented Range", "Yorumlar: Sonraki Yorumlu Aralığa Git"]
    ,["Add User Rule", "Kullanıcı Kuralı Ekle"]
    ,["Add Data Breakpoint at Address", "Adrese Veri Kesme Noktası Ekle"]
    ,["Open Agent Changes", "Ajan Değişikliklerini Aç"]
    ,["Start Agent Review", "Ajan İncelemesini Başlat"]
    ,["Clone Repository", "Depoyu Klonla"]
    ,["Connect", "Bağlan"]
    ,["Code Intelligence", "Kod Zekası"]
    ,["Cursor Tab", "Cursor Sekmesi"]
    ,["Manage scope", "Kapsamı Yönet"]
    ,["Data & Analytics", "Veri ve Analitik"]
    ,["Productivity", "Üretkenlik"]
    ,["Payments", "Ödemeler"]
    ,["Agent Orchestration", "Ajan Orkestrasyonu"]
    ,["Canvas", "Tuval"]
    ,["Filter by source: All", "Kaynağa Göre Filtrele: Tümü"]
    ,["Plugins in Customize", "Özelleştir'deki Eklentiler"]
    ,["Open Plugins in Customize", "Özelleştir'de Eklentileri Aç"]
    ,["Add to Cursor", "Cursor'a Ekle"]
  ]);
  const attrs = ["aria-label", "title", "placeholder", "data-placeholder", "aria-placeholder"];
  const modelTooltipReplacements = [
    ["Cycle Effort", "Çaba Düzeyini Değiştir"],
    ["Cycle effort", "Çaba Düzeyini Değiştir"],
    ["Switch Model", "Model Değiştir"],
    ["Switch model", "Model Değiştir"],
    ["Add a follow up", "Takip Mesajı Ekle"],
    ["Add a follow-up", "Takip Mesajı Ekle"],
    ["Model used to build this plan", "Bu planı oluşturan model"],
    ["Select element", "Öğe Seç"],
    ["Take Screenshot", "Ekran Görüntüsü Al"],
    ["Capture Area Screenshot", "Alan Ekran Görüntüsü Al"],
    ["Hard Reload", "Zorla Yenile"],
    ["Copy Current URL", "Geçerli URL'yi Kopyala"],
    ["Clear Cookies", "Çerezleri Temizle"],
    ["Clear Cache", "Önbelleği Temizle"],
    ["Enter a URL above, or instruct the Agent to navigate and use the browser", "Yukarıya bir URL girin veya Ajan'a gezinmesini ve tarayıcıyı kullanmasını söyleyin"],
    ["Build Locally", "Yerel Olarak Derle"],
    ["Parallel Build", "Paralel Derle"],
    ["Build", "Derle"],
    ["Zoom", "Yakınlaştırma"],
    ["Reset zoom", "Yakınlaştırmayı Sıfırla"],
    ["Coding model from Moonshot AI for long-horizon software engineering", "Uzun süreli yazılım mühendisliği için Moonshot AI kodlama modeli"],
    ["A smaller, faster GPT-5.4 model. Great for simpler coding tasks.", "Daha küçük ve hızlı bir GPT-5.4 modeli. Daha basit kodlama görevleri için idealdir."],
    ["Anthropic's earlier flagship model, great for difficult tasks.", "Anthropic'in önceki amiral gemisi modeli; zor görevler için idealdir."],
    ["Anthropic's large model class, great for difficult tasks.", "Anthropic'in büyük model sınıfı; zor görevler için idealdir."],
    ["Anthropic's mid-size model class, great for everyday use.", "Anthropic'in orta boy model sınıfı; günlük kullanım için idealdir."],
    ["Anthropic's most powerful model, great for difficult tasks.", "Anthropic'in en güçlü modeli; zor görevler için idealdir."],
    ["Anthropic's smartest model, great for difficult tasks.", "Anthropic'in en akıllı modeli; zor görevler için idealdir."],
    ["Balanced GPT-5.6 model for everyday work. Roughly corresponds to mini on earlier GPT models.", "Günlük işler için dengeli GPT-5.6 modeli. Önceki GPT modellerindeki mini sınıfına yaklaşık olarak karşılık gelir."],
    ["Cursor and SpaceXAI's most powerful model, great for complex coding and knowledge work.", "Cursor ve SpaceXAI'nin en güçlü modeli; karmaşık kodlama ve bilgi çalışmaları için idealdir."],
    ["Cursor's fast and efficient model -- great for everyday use.", "Cursor'ın hızlı ve verimli modeli — günlük kullanım için idealdir."],
    ["Earlier Anthropic Fable model, for difficult tasks.", "Zor görevler için önceki Anthropic Fable modeli."],
    ["Earlier Anthropic Opus model, for difficult tasks.", "Zor görevler için önceki Anthropic Opus modeli."],
    ["Earlier Google Flash model, for fast daily use.", "Hızlı günlük kullanım için önceki Google Flash modeli."],
    ["Earlier OpenAI model, for complex tasks.", "Karmaşık görevler için önceki OpenAI modeli."],
    ["Fast, affordable GPT-5.6 tier with strong capability at the lowest GPT-5.6 cost. Roughly corresponds to nano on earlier GPT models.", "En düşük GPT-5.6 maliyetinde güçlü yetenek sunan hızlı ve uygun fiyatlı GPT-5.6 katmanı. Önceki GPT modellerindeki nano sınıfına yaklaşık olarak karşılık gelir."],
    ["Good default for everyday tasks, balanced for quality and speed.", "Günlük görevler için kalite ve hız dengesi sunan iyi bir varsayılan."],
    ["Meta's flagship model, great for agentic coding.", "Meta'nın amiral gemisi modeli; ajan tabanlı kodlama için idealdir."],
    ["Meta's flagship model, great for coding.", "Meta'nın amiral gemisi modeli; kodlama için idealdir."],
    ["Meta's fast model, great for daily use.", "Meta'nın hızlı modeli; günlük kullanım için idealdir."],
    ["great for agentic coding.", "ajan tabanlı kodlama için idealdir."],
    ["great for agentic coding", "ajan tabanlı kodlama için idealdir"],
    ["Anthropic's small, fast model class, great for quick everyday tasks.", "Anthropic'in küçük, hızlı model sınıfı; günlük hızlı görevler için idealdir."],
    ["Anthropic's large model class, great for difficult agentic tasks.", "Anthropic'in büyük model sınıfı; zorlu ajan görevleri için idealdir."],
    ["Anthropic's mid-size model class, great for difficult agentic tasks.", "Anthropic'in orta boy model sınıfı; zorlu ajan görevleri için idealdir."],
    ["Anthropic's small, fast model class", "Anthropic'in küçük, hızlı model sınıfı"],
    ["Anthropic's large model class", "Anthropic'in büyük model sınıfı"],
    ["Anthropic's mid-size model class", "Anthropic'in orta boy model sınıfı"],
    ["great for difficult agentic tasks.", "zorlu ajan görevleri için idealdir."],
    ["great for difficult agentic tasks", "zorlu ajan görevleri için idealdir"],
    ["great for quick everyday tasks.", "günlük hızlı görevler için idealdir."],
    ["great for quick everyday tasks", "günlük hızlı görevler için idealdir"],
    ["Version: no thinking effort", "Sürüm: düşünme yok"],
    ["Version: no thinking", "Sürüm: düşünme yok"],
    ["Version: none reasoning effort", "Sürüm: akıl yürütme yok"],
    ["Version: none effort", "Sürüm: çaba yok"],
    ["Version: off", "Sürüm: kapalı"],
    ["Version: disabled", "Sürüm: devre dışı"],
    ["Claude Sonnet 4 No Thinking", "Claude Sonnet 4 Düşünme Yok"],
    ["No Thinking", "Düşünme Yok"],
    ["No thinking", "Düşünme Yok"],
    ["no thinking", "düşünme yok"],
    ["Google's flash model, great for daily use.", "Google'ın hızlı Flash modeli; günlük kullanım için idealdir."],
    ["Google's latest flagship model, great for daily use.", "Google'ın en yeni amiral gemisi modeli; günlük kullanım için idealdir."],
    ["Google's latest flash model, great for daily use.", "Google'ın en yeni Flash modeli; günlük kullanım için idealdir."],
    ["Great for daily use.", "Günlük kullanım için idealdir."],
    ["Older Google Flash model, for fast, low-cost tasks.", "Hızlı ve düşük maliyetli görevler için eski Google Flash modeli."],
    ["Older OpenAI model, for planning, debugging, and coding.", "Planlama, hata ayıklama ve kodlama için eski OpenAI modeli."],
    ["OpenAI's flagship GPT-5.6 model. Strongest agentic coding, biology, and cybersecurity capabilities, with a new max reasoning effort.", "OpenAI'nin amiral gemisi GPT-5.6 modeli. Yeni azami akıl yürütme düzeyiyle en güçlü ajan tabanlı kodlama, biyoloji ve siber güvenlik yeteneklerini sunar."],
    ["OpenAI's latest flagship model. Great for complex tasks.", "OpenAI'nin en yeni amiral gemisi modeli. Karmaşık görevler için idealdir."],
    ["OpenAI's model specifically for coding. Good for ambitious coding tasks.", "OpenAI'nin özellikle kodlama için geliştirdiği model. İddialı kodlama görevleri için uygundur."],
    ["The smallest GPT-5.4 model. Optimized for speed and low cost.", "En küçük GPT-5.4 modeli. Hız ve düşük maliyet için iyileştirilmiştir."],
    ["The predecessor to Cursor Grok 4.6, built for complex coding and knowledge work.", "Cursor Grok 4.6'nın öncülü; karmaşık kodlama ve bilgi çalışmaları için geliştirilmiştir."],
    ["The cost is 2x when the input exceeds 272k tokens.", "Girdi 272 bin tokenı aştığında maliyet 2 katına çıkar."],
    ["This model has special data retention policies.", "Bu modelin özel veri saklama politikaları vardır."],
    ["The same Claude Opus 4.7 model at 6x the price, using Anthropic's fast mode.", "Aynı Claude Opus 4.7 modeli; Anthropic'in hızlı modu kullanılarak 6 kat fiyatlandırılır."],
    ["The same Claude Opus 4.8 model at 2x the price, using Anthropic's fast mode.", "Aynı Claude Opus 4.8 modeli; Anthropic'in hızlı modu kullanılarak 2 kat fiyatlandırılır."],
    ["The same Claude Opus 5 model at 2x the price, using Anthropic's fast mode.", "Aynı Claude Opus 5 modeli; Anthropic'in hızlı modu kullanılarak 2 kat fiyatlandırılır."],
    ["The same Codex 5.3 model, using OpenAI's fast priority processing at 2x the price.", "Aynı Codex 5.3 modeli; OpenAI'nin hızlı öncelikli işlemesiyle 2 kat fiyatlandırılır."],
    ["The same GPT-5.2 model, using OpenAI's fast priority processing at 2x the price.", "Aynı GPT-5.2 modeli; OpenAI'nin hızlı öncelikli işlemesiyle 2 kat fiyatlandırılır."],
    ["The same GPT-5.4 model, using OpenAI's fast priority processing at 2x the price.", "Aynı GPT-5.4 modeli; OpenAI'nin hızlı öncelikli işlemesiyle 2 kat fiyatlandırılır."],
    ["The same GPT-5.5 model, using OpenAI's fast priority processing at 2.5x the price.", "Aynı GPT-5.5 modeli; OpenAI'nin hızlı öncelikli işlemesiyle 2,5 kat fiyatlandırılır."],
    ["The same GPT-5.6 Luna model, using OpenAI's fast priority processing at 2x the price.", "Aynı GPT-5.6 Luna modeli; OpenAI'nin hızlı öncelikli işlemesiyle 2 kat fiyatlandırılır."],
    ["The same GPT-5.6 Sol model, using OpenAI's fast priority processing at 2x the price.", "Aynı GPT-5.6 Sol modeli; OpenAI'nin hızlı öncelikli işlemesiyle 2 kat fiyatlandırılır."],
    ["The same GPT-5.6 Terra model, using OpenAI's fast priority processing at 2x the price.", "Aynı GPT-5.6 Terra modeli; OpenAI'nin hızlı öncelikli işlemesiyle 2 kat fiyatlandırılır."],
    ["1M context window", "1 milyon bağlam penceresi"],
    ["2M context window", "2 milyon bağlam penceresi"],
    ["128k context window", "128 bin bağlam penceresi"],
    ["128K context window", "128 bin bağlam penceresi"],
    ["200k context window", "200 bin bağlam penceresi"],
    ["256k context window", "256 bin bağlam penceresi"],
    ["256K context window", "256 bin bağlam penceresi"],
    ["262k context window", "262 bin bağlam penceresi"],
    ["272k context window", "272 bin bağlam penceresi"],
    ["300k context window", "300 bin bağlam penceresi"],
    ["500k context window", "500 bin bağlam penceresi"],
    ["500K context window", "500 bin bağlam penceresi"],
    ["SpaceXAI's most powerful model, built for complex coding and knowledge work.", "SpaceXAI'ın karmaşık kodlama ve bilgi işleri için tasarlanmış en güçlü modeli."],
    ["SpaceXAI's most powerful model, great for complex coding and knowledge work.", "SpaceXAI'ın karmaşık kodlama ve bilgi işleri için tasarlanmış en güçlü modeli."],
    ["Significantly faster but consumes more usage", "Belirgin şekilde daha hızlıdır ancak daha fazla kullanım tüketir"],
    ["Version: extra high effort", "Sürüm: ekstra yüksek çaba"],
    ["Version: extra high reasoning effort", "Sürüm: ekstra yüksek akıl yürütme çabası"],
    ["Version: high effort", "Sürüm: yüksek çaba"],
    ["Version: high reasoning effort", "Sürüm: yüksek akıl yürütme çabası"],
    ["Version: low effort", "Sürüm: düşük çaba"],
    ["Version: low reasoning effort", "Sürüm: düşük akıl yürütme çabası"],
    ["Version: max effort", "Sürüm: azami çaba"],
    ["Version: max reasoning effort", "Sürüm: azami akıl yürütme çabası"],
    ["Version: medium effort", "Sürüm: orta çaba"],
    ["Version: medium reasoning effort", "Sürüm: orta akıl yürütme çabası"],
    ["Version: minimal effort", "Sürüm: en düşük çaba"],
    ["Version: none reasoning effort", "Sürüm: akıl yürütme yok"],
    ["Version: preview", "Sürüm: önizleme"],
    ["[Alt] Replace Agent", "[Alt] Ajanı Değiştir"],
    ["Replace Agent", "Ajanı Değiştir"],
    ["Learn more", "Daha fazla bilgi"]
  ];
  const translateModelTooltipValue = (value) => {
    let result = String(value || "");
    for (const [source, translated] of modelTooltipReplacements) {
      if (result.includes(source)) result = result.split(source).join(translated);
    }
    result = result.replace(/(\d+)\s*k\s+context window/gi, "$1 bin bağlam penceresi");
    result = result.replace(/(\d+)\s*m\s+context window/gi, "$1 milyon bağlam penceresi");
    result = result.replace(/(\d+)\s+context window/gi, "$1 bağlam penceresi");
    result = result.replace(/SpaceXAI's most powerful model, built for complex coding and knowledge work\./gi, "SpaceXAI'ın karmaşık kodlama ve bilgi işleri için tasarlanmış en güçlü modeli.");
    return result;
  };
  const protectedSelector = ".monaco-editor, .xterm, textarea, pre, code, [data-component=\"glass-empty-state-rotating-tips\"]";
  const translateValue = (value) => {
    let key = String(value || "").replace(/\s+/g, " ").trim();
    if (translations.has(key)) return translations.get(key);
    const matchExploring = key.match(/^Exploring\s+(\d+)\s+files?$/i);
    if (matchExploring) return `${matchExploring[1]} dosya keşfediliyor`;
    const matchReading = key.match(/^Reading\s+(\d+)\s+files?$/i);
    if (matchReading) return `${matchReading[1]} dosya okunuyor`;
    let matchFilesChanged = key.match(/^(\d+)\s+Files?\s+Changed$/i);
    if (matchFilesChanged) return `${matchFilesChanged[1]} Dosya Değişti`;
    const matchBgTerm = key.match(/^(\d+)\s+background\s+terminals?$/i);
    if (matchBgTerm) return `${matchBgTerm[1]} arka plan terminali`;
    const matchBgSubagent = key.match(/^(\d+)\s+background\s+subagents?$/i);
    if (matchBgSubagent) return `${matchBgSubagent[1]} arka plan alt ajanı`;
    const matchBgTask = key.match(/^(\d+)\s+background\s+tasks?$/i);
    if (matchBgTask) return `${matchBgTask[1]} arka plan görevi`;
    const matchWorkedFor = key.match(/^Worked\s+for\s+(.+)$/i);
    if (matchWorkedFor) return `Çalışma Süresi: ${matchWorkedFor[1]}`;
    const matchCalismaFor = key.match(/^Çalışma Süresi for (.+)$/i);
    if (matchCalismaFor) return `Çalışma Süresi: ${matchCalismaFor[1]}`;
    if (key === "Thought briefly" || key === "Düşündü kısaca" || key === "Düşündü briefly") return "Kısaca düşündü";
    const matchThought = key.match(/^(?:Thought|Düşündü)\s+(\d+(?:\.\d+)?s)$/i);
    if (matchThought) return `${matchThought[1]} düşündü`;
    const matchPairedWith = key.match(/^Paired with this computer\s+·\s+(.+)$/i);
    if (matchPairedWith) {
      let sub = matchPairedWith[1];
      if (sub === "Not used yet") sub = "Henüz kullanılmadı";
      else if (sub.startsWith("Last used ")) sub = "Son kullanım: " + sub.slice("Last used ".length);
      return `Bu bilgisayarla eşleştirildi · ${sub}`;
    }
    const matchApprovalCode = key.match(/^Waiting for approval\s+·\s+code\s+(.+)$/i);
    if (matchApprovalCode) return `Onay bekleniyor · kod ${matchApprovalCode[1]}`;
    const modelTooltipValue = translateModelTooltipValue(value);
    if (modelTooltipValue !== String(value || "")) return modelTooltipValue;
    if (key.startsWith("Search agents, Canvas, files, actions")) {
      return "Ajanlarda, Tuval'de, dosyalarda ve eylemlerde ara...";
    }
    // Dönen alt ipucu güncellemeler arasında kısmen çevrilebildiği için cümleyi
    // tek bir kırılgan tam eşleşme yerine sabit başlangıcından yakala.
    if (key.startsWith("Steer a running agent without stopping it")) {
      return "Çalışan ajanı durdurmadan yönlendirin — Ajanlar ayarlarındaki Yeni Mesajlar seçeneğini Hemen Gönder olarak ayarlayın";
    }
    if (key.startsWith("Edit automation name:")) {
      const automationName = key.slice("Edit automation name:".length).trim();
      return "Otomasyon adını düzenle: " + (translations.get(automationName) || automationName);
    }
    if (key.startsWith("By ")) return "Oluşturan " + key.slice(3);
    // Statik katman bazen yalnızca "Use" parçasını "Kullan" yapar. Tam ipucu
    // aynı düğümde kaldığında bütün mevcut "Use /komut ..." kurallarını yeniden
    // kullanabilmek için yarı çevrilmiş öneki İngilizce eşleme anahtarına döndür.
    if (key.startsWith("Kullan /")) key = "Use /" + key.slice("Kullan /".length);
    if (key.startsWith("Hata Ayıklama Modu ")) key = "Debug Mode " + key.slice("Hata Ayıklama Modu ".length);
    if (key.startsWith("Hata Ayıklama Mod ")) key = "Debug Mode " + key.slice("Hata Ayıklama Mod ".length);
    // Tema adları orijinal İngilizce bırakılır (yalnızca "System" -> "Sistem" çevrilir)
    if (key.startsWith("Cursor Light") || key.startsWith("Cursor Dark")) return null;
    if (translations.has(key)) return translations.get(key);
    let matchToolsRes = key.match(/^(\d+)\s+tools?,\s*(\d+)\s+resources?\s+enabled$/i);
    if (matchToolsRes) return `${matchToolsRes[1]} araç, ${matchToolsRes[2]} kaynak etkin`;
    let matchResOnly = key.match(/^(\d+)\s+resources?\s+enabled$/i);
    if (matchResOnly) return `${matchResOnly[1]} kaynak etkin`;
    let matchToolsOnly = key.match(/^(\d+)\s+tools?\s+enabled$/i);
    if (matchToolsOnly) return `${matchToolsOnly[1]} araç etkin`;
    if (key.includes("High Fast")) return key.replace(/High Fast/g, "Yüksek Hızlı");
    if (key.includes("Medium Fast")) return key.replace(/Medium Fast/g, "Orta Hızlı");
    if (key.includes("Low Fast")) return key.replace(/Low Fast/g, "Düşük Hızlı");
    if (key.includes("No Thinking")) return key.replace(/No Thinking/g, "Düşünme Yok");
    if (key.includes("No thinking")) return key.replace(/No thinking/g, "Düşünme Yok");
    if (key.includes("(fast)")) return key.replace(/\(fast\)/g, "(hızlı)");
    if (key.includes("(Fast)")) return key.replace(/\(Fast\)/g, "(Hızlı)");
    // Model seçicide tek başına çabalar: "Grok 4.7 High", "Claude Opus 5 High" vb.
    if (/\bHigh\b/.test(key) && /\b(Grok|Claude|GPT|Gemini|Composer|Cursor|OpenAI|Sonnet|Haiku|Opus)\b/.test(key))
      return key.replace(/\bHigh\b/g, "Yüksek").replace(/\bMedium\b/g, "Orta").replace(/\bLow\b/g, "Düşük").replace(/\bMax\b/g, "Azami").replace(/\bFast\b/g, "Hızlı");
    if (/\bMedium\b/.test(key) && /\b(Grok|Claude|GPT|Gemini|Composer|Cursor|OpenAI|Sonnet|Haiku|Opus)\b/.test(key))
      return key.replace(/\bHigh\b/g, "Yüksek").replace(/\bMedium\b/g, "Orta").replace(/\bLow\b/g, "Düşük").replace(/\bMax\b/g, "Azami").replace(/\bFast\b/g, "Hızlı");
    if (/\bLow\b/.test(key) && /\b(Grok|Claude|GPT|Gemini|Composer|Cursor|OpenAI|Sonnet|Haiku|Opus)\b/.test(key))
      return key.replace(/\bHigh\b/g, "Yüksek").replace(/\bMedium\b/g, "Orta").replace(/\bLow\b/g, "Düşük").replace(/\bMax\b/g, "Azami").replace(/\bFast\b/g, "Hızlı");
    // Guncelleme statik NLS ile cumlenin baska kelimelerini de kismen
    // Turkcelestirdiyse geri kalan metne baglanma; komut tum ipucunu belirler.
    const hintCommand = key.match(/^Use (\/[A-Za-z0-9_-]+)/i)?.[1];
    if (hintCommand) {
      const commandHints = {
        "/review": "/review ile değişikliklerinizi ajan destekli kod incelemesinden geçirin",
        "/create-rule": "/create-rule ile ajan davranışını sistem düzeyi talimatlarla denetleyin",
        "/create-skill": "/create-skill ile Cursor'u iş akışlarınıza göre özelleştirin",
        "/create-subagent": "/create-subagent ile uzman ajanlar kurun",
        "/create-hook": "/create-hook ile ajan döngüsünü özel betiklerle denetleyip genişletin",
        "/model": "/model ile göreviniz için en uygun modeli seçin",
        "/multitask": "/multitask ile sıradaki mesajlarınızı paralel çalıştırın",
        "/plan": "/plan ile Plan Modu kullanarak ajan yürütmesini iyileştirin",
        "/debug": "/debug ile yeniden üretmesi zor hataları çözün",
        "/split-to-prs": "/split-to-prs ile çalışmanızı küçük ve incelenebilir PR'lara bölün",
        "/automate": "/automate ile ajan sohbetinden ayrılmadan Cursor Otomasyonları oluşturun",
        "/cloud": "/cloud ile ajanları uzaktan çalıştırın",
        "/loop": "/loop ile bir istemi zamanlamaya göre çalıştırın",
        "/shell": "/shell ile terminalde komut çalıştırın",
        "/ask": "/ask ile kod değişikliklerinden önce kod tabanınızı araştırın",
        "/canvas": "/canvas ile Cursor'dan etkileşimli görselleştirmeler alın",
        "/simplify": "/simplify ile değişen dosyaları kod kalitesi ve verimlilik için inceletin",
        "/add-plugin": "/add-plugin ile Cursor Eklenti Pazarı'ndan eklenti yükleyin",
        "/babysit": "/babysit ile PR yorumlarını önceliklendirin, CI hatalarını düzeltin ve çakışmaları temizleyin"
        ,"/goal": "/goal ile Cursor'un tamamlanana kadar izlemeyi sürdüreceği bir hedef belirleyin"
      };
      if (commandHints[hintCommand]) return commandHints[hintCommand];
    }
    let match = key.match(/^(?:Worked|Thought|Çalışma Süresi) for (\d+)s$/);
    if (match) return `Çalışma Süresi: ${match[1]} sn`;
    match = key.match(/^Keşfetti (.+), (\d+) searches?, (\d+) tools?$/);
    if (match) return `Keşfetti ${match[1]}, ${match[2]} arama, ${match[3]} araç`;
    // "Are you sure you want to delete "Untitled"? This cannot be undone."
    match = key.match(/^Are you sure you want to delete "(.+)"\? This cannot be undone\.$/);
    if (match) return `"${match[1]}" öğesini silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.`;
    match = key.match(/^Are you sure you want to delete (.+)\? This cannot be undone\.$/);
    if (match) return `${match[1]} öğesini silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.`;
    match = key.match(/^(?:Show|Göster) (\d+) more$/);
    if (match) return `${match[1]} tane daha göster`;
    match = key.match(/^(\d+)(d|mo|h|m|y)$/);
    if (match) {
      const units = { d: "g", mo: "ay", h: "sa", m: "dk", y: "yıl" };
      return `${match[1]}${units[match[2]]}`;
    }
    match = key.match(/^Search Plugins for (.+)\.\.\.$/);
    if (match) return `${match[1]} için eklentilerde ara...`;
    // "3 sources" gibi dinamik kaynak sayısı
    match = key.match(/^(\d+)\s+sources?$/);
    if (match) return `${match[1]} kaynak`;
    // MCP araç sayısı: "12 tools"
    match = key.match(/^(\d+)\s+tools?$/);
    if (match) return `${match[1]} araç`;
    // Tarih sıfırlanma formatı: "Resets Oct 23, 2026"
    match = key.match(/^Resets\s+([A-Za-z]+)\s+(\d+),\s*(\d+)$/i);
    if (match) {
      const months = { Jan:"Oca", Feb:"Şub", Mar:"Mar", Apr:"Nis", May:"May", Jun:"Haz", Jul:"Tem", Aug:"Ağu", Sep:"Eyl", Oct:"Eki", Nov:"Kas", Dec:"Ara" };
      const m = months[match[1].slice(0, 3)] || match[1];
      return `${match[2]} ${m} ${match[3]} tarihinde sıfırlanır`;
    }
    // Cursor Settings komut paleti: "Cursor Settings: Agents" vb.
    match = key.match(/^Cursor Settings:\s*(.+)$/i);
    if (match) {
      const sub = match[1].trim();
      const subMap = {
        "Agents": "Ajanlar",
        "Beta": "Beta",
        "Browser & Network": "Tarayıcı ve Ağ",
        "General": "Genel",
        "Models": "Modeller",
        "Features": "Özellikler",
        "Rules, Skills, Subagents": "Kurallar, Beceriler, Alt Ajanlar",
        "Cloud Agents": "Bulut Ajanları",
        "Git & PRs": "Git ve PR'lar",
        "Indexing": "Dizinleme",
        "Tab": "Sekme",
        "Docs": "Belgeler",
        "Workspaces": "Çalışma Alanları",
        "Chat": "Sohbet"
      };
      return `Cursor Ayarları: ${subMap[sub] || sub}`;
    }
    // VS Code Ayar Başlıkları: "Files: Auto Save", "Editor: Font Size" vb.
    match = key.match(/^(Editor|Files|Terminal|Workbench):\s*(.+)$/i);
    if (match) {
      const cat = match[1].toLowerCase();
      const prop = match[2].trim();
      const catMap = { editor: "Düzenleyici", files: "Dosyalar", terminal: "Terminal", workbench: "Çalışma Alanı" };
      const propMap = {
        "Auto Save": "Otomatik Kaydetme",
        "Font Size": "Yazı Tipi Boyutu",
        "Font Family": "Yazı Tipi Ailesi",
        "Tab Size": "Sekme Boyutu",
        "Cursor Style": "İmleç Stili",
        "Multi Cursor Modifier": "Çoklu İmleç Değiştiricisi",
        "Insert Spaces": "Boşluk Ekle",
        "Detect Indentation": "Girintiyi Algıla",
        "Word Wrap": "Sözcük Kaydırma",
        "Line Numbers": "Satır Numaraları",
        "Render Whitespace": "Boşlukları Göster",
        "Minimap": "Mini Harita"
      };
      if (propMap[prop]) return `${catMap[cat] || match[1]}: ${propMap[prop]}`;
    }
    match = key.match(/^Use with caution\. Skip symlinks during \.cursorignore file discovery\. Enable only when all \.cursorignore files are reachable without symlinks(?: \(controlled by admin\))?\. Changing this setting requires restarting Cursor\.$/);
    if (match) return "Dikkatli kullanın. .cursorignore dosyaları aranırken sembolik bağlantıları atlayın. Yalnızca tüm .cursorignore dosyalarına sembolik bağlantı olmadan erişilebiliyorsa etkinleştirin. Bu ayarın değiştirilmesi Cursor'ın yeniden başlatılmasını gerektirir.";
    if (key.startsWith("Use Datadog directly in Cursor")) return "Datadog'u doğrudan Cursor içinde kullanın; günlükleri, metrikleri, izleri ve panoları doğal dille sorgulayın.";
    if (key.startsWith("Cursor Plugin for Linear")) return "Linear sorunlarını, projelerini ve belgelerini Cursor içinden yapay zekâ ajanlarıyla yönetin.";
    if (key.startsWith("Slack MCP server.")) return "Slack kanallarında arama yapın, mesaj gönderin ve diğer Slack işlemlerini Cursor içinden yönetin.";
    if (key.startsWith("Official Apify agent skills")) return "Web kazıma, veri çıkarma ve otomasyon için resmi Apify ajan becerileri.";
    if (key.startsWith("Skills for NVIDIAs ecosystem spans")) return "NVIDIA ekosisteminde GPU hızlandırma, CUDA, yapay zekâ, robotik, Omniverse ve simülasyon iş akışları için beceriler.";
    if (key.startsWith("Guide developers through adding maps")) return "Amazon Location Service ile harita, yer arama, coğrafi kodlama, rota ve diğer konum özelliklerini ekleme rehberliği.";
    if (key.startsWith("The Appwrite plugin for Cursor")) return "Appwrite projelerine erişmek ve doğru entegrasyon kurmak için beceriler ile MCP sunucuları.";
    if (key.startsWith("Build full-stack apps with AWS Amplify")) return "AWS Amplify Gen 2 ile tam kapsamlı uygulamalar oluşturma rehberliği.";
    if (key.startsWith("Build, deploy, and operate applications on AWS")) return "AWS üzerinde uygulama oluşturma, dağıtma ve işletme becerileri.";
    if (key.startsWith("Expert database guidance for the AWS database portfolio")) return "AWS veritabanları için tasarım, sorgu, geçiş ve seçim rehberliği.";
    if (key.startsWith("Deploy applications to AWS with architecture recommendations")) return "Mimari öneriler, maliyet tahminleri ve kod olarak altyapıyla AWS dağıtım rehberliği.";
    if (key.startsWith("Design, build, deploy, test, and debug serverless applications")) return "AWS sunucusuz uygulamalarını tasarlama, geliştirme, dağıtma, test etme ve hata ayıklama becerileri.";
    if (key.startsWith("Microsoft Azure MCP and Skills integration")) return "Azure kaynaklarını, dağıtımları ve hizmetleri Cursor içinden yönetmek için MCP ve beceri entegrasyonu.";
    if (key.startsWith("Railway agent skills and MCP server")) return "Railway'de uygulama ve altyapı dağıtma, yapılandırma, izleme ve sorun giderme araçları.";
    if (key.startsWith("CockroachDB plugin for Cursor")) return "Cursor için CockroachDB eklentisi; şemaları keşfedin, iyileştirilmiş SQL yazın, sorgu hatalarını ayıklayın ve dağıtık veritabanı kümelerini ajanınızdan yönetin.";
    if (key.startsWith("Official Convex plugin for Cursor")) return "TypeScript ile reaktif arka uç geliştirme için kurallar, beceriler, MCP entegrasyonu ve otomasyon kancaları içeren resmi Convex eklentisi.";
    if (key.startsWith("Connects Cursor to the Coralogix Observability MCP Server")) return "Cursor'u Coralogix Gözlemlenebilirlik MCP sunucusuna bağlar; günlük, metrik, iz ve RUM sorgulayın, uyarı ve panoları yönetin.";
    if (key.startsWith("Build backends in TypeScript and Go with automatic infrastructure")) return "Otomatik altyapıyla TypeScript ve Go arka uçları oluşturun; hizmetleri inceleyin, veritabanlarını sorgulayın, izleri analiz edin ve uç noktaları çağırın.";
    if (key.startsWith("The official Firebase Cursor plugin")) return "Firebase arka ucu ve yapay zekâ altyapısıyla modern uygulamaları prototipleyin, geliştirin ve çalıştırın.";
    if (key.startsWith("JFrog Platform integration with MCP")) return "MCP, güvenlik becerileri, yazılım tedarik zinciri uygulamaları ve MCP sunucusu yönetişimi için JFrog Platform entegrasyonu.";
    if (key.startsWith("Official Cursor plugin for MongoDB")) return "MongoDB için resmi Cursor eklentisi; veritabanlarına bağlanın, veriyi keşfedin, koleksiyonları yönetin, sorguları iyileştirin ve güvenilir kod üretin.";
    if (key.startsWith("Deploy and operate full applications with Monk")) return "Bulut altyapısı, SaaS entegrasyonları ve kapsayıcı iş yükleri dahil tam uygulamaları tek sohbetten dağıtın ve işletin.";
    if (key.startsWith("Manage your Neon projects and databases")) return "Neon Postgres ajan becerisi ve MCP sunucusuyla Neon projelerinizi ve veritabanlarınızı yönetin.";
    if (key.startsWith("Netlify platform skills")) return "İşlevler, edge işlevleri, bloblar, veritabanı, kimlik, görsel CDN, formlar, CLI, önbellek, yapay zekâ geçidi ve dağıtım için Netlify becerileri.";
    if (key.startsWith("PagerDuty MCP server for Cursor")) return "Olayları, hizmetleri, nöbet çizelgelerini ve daha fazlasını doğrudan Cursor'dan yöneten PagerDuty MCP sunucusu.";
    if (key.startsWith("ParadeDB adds Elastic-quality full-text search")) return "Postgres'e ikinci bir sistem kurmadan Elastic düzeyinde tam metin arama, vektör arama ve toplulaştırma ekler.";
    if (key.startsWith("Pinecone vector database integration for Cursor")) return "Pinecone vektör veritabanı entegrasyonu; dizinleri ve verileri yönetin, anlamsal arama, RAG ve belgeli soru-cevap uygulamaları oluşturun.";
    if (key.startsWith("An authenticated hosted MCP server that accesses your PlanetScale")) return "PlanetScale kuruluşlarınıza, veritabanlarınıza, dallarınıza, şemanıza ve Insights verilerine erişen kimlik doğrulamalı MCP sunucusu.";
    if (key.startsWith("Redis development best practices")) return "Veri yapıları, sorgu motoru, vektör arama, önbellekleme ve performans iyileştirme için Redis geliştirme rehberliği.";
    if (key.startsWith("Deploy, debug, and monitor applications on Render")) return "Render üzerinde uygulamaları dağıtın, hatalarını ayıklayın ve izleyin; tam iş akışı için beceriler, kurallar, komutlar, ajan, MCP ve kancalar içerir.";
    if (key.startsWith("Official ScyllaDB agent skills")) return "ScyllaDB Cloud kurulumu, CQL veri modelleme ve Vektör Arama için yönlendirmeli resmi ajan becerileri.";
    if (key.startsWith("Sentry Plugin for Cursor")) return "MCP ve beceri özellikleriyle hata ayıklamaya yardımcı olan Cursor için Sentry eklentisi.";
    if (key.startsWith("Access your Supabase projects and perform tasks")) return "Supabase projelerinize erişin; tabloları yönetin, yapılandırmayı alın ve verileri sorgulayın.";
    if (key.startsWith("Comprehensive skill for the entire Temporal lifecycle")) return "Uygulama geliştirme, Temporal CLI, Temporal Server ve Temporal Cloud dahil tüm Temporal yaşam döngüsü için kapsamlı beceri.";
    if (key.startsWith("Turbopuffer vector and full-text search database integration")) return "Cursor için turbopuffer vektör ve tam metin arama veritabanı entegrasyonu.";
    if (key.startsWith("Twilio Skills and MCP provide procedural knowledge")) return "Mesajlaşma, Ses, Verify, SendGrid ve 30'dan fazla ürün için doğru API sırasını ve iyi uygulamaları öğreten Twilio becerileri ile MCP.";
    if (key.startsWith("Query cloud costs, manage cost reports")) return "Vantage çalışma alanınızda bulut maliyetlerini sorgulayın; raporları, bütçeleri, uyarıları ve önerileri yönetin.";
    if (key.startsWith("Build and deploy web apps and agents")) return "Web uygulamaları ve ajanları geliştirin ve dağıtın.";
    if (key.startsWith("WorkOS integration skills for AuthKit")) return "AuthKit, SSO, Dizin Eşitleme, RBAC, Vault, Denetim Günlükleri ve geçişler için WorkOS becerileri ile MCP sunucusu.";
    if (key.startsWith("Manage the Zscaler cloud security platform")) return "ZPA, ZIA, ZDX, ZCC, EASM ve Z-Insights dahil Zscaler bulut güvenlik platformunu yönetin; uygulama ekleme, ilke denetimi ve olay inceleme becerileri içerir.";
    if (key.startsWith("Deploy serverless browser automation to Browserbase cloud")) return "Zamanlanmış veya webhook ile tetiklenen tarayıcı görevleri için Browserbase bulutunda sunucusuz otomasyon işlevleri oluşturun, test edin ve yayımlayın.";
    if (key.startsWith("BrowserStack integration for Cursor")) return "Gerçek cihazlarda web sitelerini ve mobil uygulamaları test edin; otomatik testleri çalıştırın, hataları ayıklayın ve test senaryolarını doğal dille yönetin.";
    if (key.startsWith("Clerk authentication toolkit for Cursor")) return "Giriş, MFA, kuruluşlar, faturalandırma, webhook ve test akışları için Clerk kimlik doğrulama araçları, MCP sunucusu ve becerileri.";
    if (key.startsWith("Skills for the Cloudflare developer platform")) return "Workers, Durable Objects, Agents SDK, MCP sunucuları, Wrangler CLI ve web performansı için Cloudflare geliştirme becerileri.";
    if (key.startsWith("Data lake, analytics, and ETL workflows with S3 Tables")) return "S3 Tables, AWS Glue ve Athena ile veri gölü, analitik ve ETL iş akışları; veri alımı, kataloglama, birleşik sorgular ve vektör aramayı kapsar.";
    if (key.startsWith("Access your Azure Cosmos DB accounts")) return "Azure Cosmos DB hesaplarınıza erişin; veritabanlarını yönetin, verileri sorgulayın, vektör araması ve şema keşfi yapın.";
    if (key.startsWith("Connect Cursor to Braintrust")) return "Projelerinize, deneylerinize ve değerlendirme günlüklerinize yapay zekâ destekli erişim için Cursor'u Braintrust'a bağlayın.";
    if (key.startsWith("Web search, content extraction, structured data, and browser automation powered by Bright Data")) return "Bright Data altyapısıyla web araması, içerik çıkarma, yapılandırılmış veri toplama ve tarayıcı otomasyonu yapın.";
    if (key.startsWith("ClickHouse Cursor plugin")) return "ClickHouse iyi uygulamaları, kuralları ve MCP entegrasyonu içeren Cursor eklentisi.";
    if (key.startsWith("Access Confidence feature flags")) return "Confidence özellik bayraklarına, deneylerine ve geçiş araçlarına doğrudan Cursor'dan erişin.";
    if (key.startsWith("Expert guidance for working with Dagster")) return "Dagster ve dg komut satırı aracıyla çalışmak için uzman rehberliği.";
    if (key.startsWith("Elastic skills and documentation")) return "Elasticsearch, Kibana, Gözlemlenebilirlik, Güvenlik, Cloud, ES|QL, OpenTelemetry ve MCP belgeleri için Elastic becerileri.";
    if (key.startsWith("Web search and content extraction powered by Exa AI")) return "Exa AI destekli web araması ve içerik çıkarma araçları.";
    if (key.startsWith("Web scraping, crawling, and search for AI agents")) return "Firecrawl CLI ile yapay zekâ ajanları için web kazıma, tarama ve arama; web içeriğine doğrudan erişim sağlar.";
    if (key.startsWith("Hosted MCP server for AI-assisted Grafana Cloud observability")) return "Yerel kurulum gerektirmeden yapay zekâ destekli Grafana Cloud gözlemlenebilirliği sağlayan barındırılan MCP sunucusu.";
    if (key.startsWith("Skills and rules for developing and using the Grafana Assistant")) return "Grafana Assistant uygulaması ve CLI aracını geliştirmek ve kullanmak için beceriler ile kurallar.";
    if (key.startsWith("AI analytics and data collaboration")) return "Cursor'u MCP üzerinden Hex çalışma alanınıza bağlayan yapay zekâ analitiği ve veri işbirliği araçları.";
    if (key.startsWith("Agent Skills for AI/ML tasks including dataset creation")) return "Hugging Face Hub üzerinde veri kümesi oluşturma, model eğitme, değerlendirme ve araştırma yayımlama için yapay zekâ/makine öğrenmesi becerileri.";
    if (key.startsWith("Mixpanel skills for Cursor")) return "İzleme kurulumu, metrik inceleme ve diğer Mixpanel iş akışları için Cursor becerileri.";
    if (key.startsWith("Explore, query, model, embed, and manage Omni Analytics")) return "Omni Analytics'i REST API ve Embed SDK ile keşfedin, sorgulayın, modelleyin, gömün ve yönetin.";
    if (key.startsWith("OpenSearch skills to help set up and deploy OpenSearch")) return "Anlamsal ve karma arama, günlük analizi, dağıtık izler, RAG ve AWS dağıtımları için OpenSearch kurulum ve kullanım becerileri.";
    if (key.startsWith("Bring Pendo analytics into Cursor")) return "Hesap sağlığı, özellik benimseme, oturum tekrarları ve geri bildirim analizi için Pendo verilerini Cursor'a getirin.";
    if (key.startsWith("Access PostHog analytics")) return "PostHog analizlerine, özellik bayraklarına, deneylere, hata izlemeye ve içgörülere doğrudan Cursor'dan erişin.";
    if (key.startsWith("Full API lifecycle management for Cursor")) return "Koleksiyon eşitleme, istemci kodu üretme, API keşfi, test, sahte servis, belge ve güvenlik denetimiyle tam API yaşam döngüsü yönetimi.";
    if (key.startsWith("The official Prisma plugin for Cursor")) return "Veritabanı geliştirme için MCP sunucusu, kurallar, beceriler ve otomasyon içeren resmi Prisma eklentisi.";
    if (key.startsWith("ThoughtSpot developer documentation")) return "Visual Embed SDK, REST API v2 ve geliştirici rehberlerinde arama sağlayan ThoughtSpot belgeleri.";
    if (key.startsWith("Connect AI agents to ZoomInfo's verified GTM context graph")) return "ZoomInfo'nun doğrulanmış şirket, kişi ve satın alma niyeti verileriyle aday listeleri oluşturun, kayıtları zenginleştirin ve karar vericileri bulun.";
    if (key.startsWith("Box Plugin for Cursor")) return "Box içeriğinde arama yapın, içeriği okuyup yönetin; Box Platform entegrasyonları ve Box AI ile soru-cevap, özetleme ve çıkarma kullanın.";
    if (key.startsWith("Create, edit, review, resize, and brand-check Canva designs")) return "Canva MCP sunucusuyla tasarımlar oluşturun, düzenleyin, inceleyin, boyutlandırın ve marka kurallarını denetleyin.";
    if (key.startsWith("Product requirements in your editor")) return "Kod bağlamından ürün gereksinim belgeleri yazın, şartnamelerden uygulayın ve değişikliklerin gereksinimlerle eşleştiğini doğrulayın.";
    if (key.startsWith("Connect Cursor to your ClickUp workspace")) return "Cursor'u ClickUp çalışma alanınıza bağlayın; görevleri yönetin, zamanı izleyin ve bağlam değiştirmeden işbirliği yapın.";
    if (key.startsWith("Create, configure, and author GitBook documentation sites")) return "GitBook belge siteleri oluşturun ve yapılandırın; Git Sync, marka özelleştirme ve Markdown sayfa yazımını yönetin.";
    if (key.startsWith("Connect Cursor to GitLab with the GitLab MCP server")) return "GitLab MCP sunucusuyla sorunları, birleştirme isteklerini ve işlem hatlarını Cursor'dan planlayıp yönetin.";
    if (key.startsWith("Official Glean plugin for Cursor")) return "Belgelerde, Slack'te ve e-postada arama yapın; depolar arası kodu keşfedin, uzmanları ve paydaşları bulun.";
    if (key.startsWith("Your meetings in your workflow")) return "Granola ile ekip görüşmelerinde konuşulanları, alınan kararları ve verilen taahhütleri Cursor iş akışına taşıyın.";
    if (key.startsWith("Official GSAP skills for Cursor")) return "Animasyonlar, zaman çizelgeleri, ScrollTrigger, eklentiler, React entegrasyonu ve performans için resmi GSAP becerileri.";
    if (key.startsWith("Harness Skills + Harness MCP server")) return "Cursor'dan Harness ile geliştirme, hata ayıklama, dağıtım ve yönetişim için beceriler ile MCP sunucusu.";
    if (key.startsWith("Cursor Plugin for IcePanel")) return "IcePanel ortamınızdaki modelleri, bağlantıları ve diğer mimari öğeleri yapay zekâ ajanlarıyla yönetin.";
    if (key.startsWith("LaunchDarkly agent skills and mcp server")) return "Özellik bayrağı yönetimi, yapay zekâ yapılandırması ve beceri yazımı için LaunchDarkly ajan becerileri ile MCP sunucusu.";
    if (key.startsWith("Give Cursor a multiplayer canvas for your code")) return "Mevcut arayüzü tuvale alın, bileşen kitaplıkları oluşturun, tasarım sistemi temaları uygulayın ve bileşenleri üretim koduna aktarın.";
    if (key.startsWith("Comprehensive reference for building Mintlify documentation sites")) return "Mintlify belge siteleri oluşturmak için kapsamlı başvuru kaynağı.";
    if (key.startsWith("Secure access to Miro boards")) return "Miro panolarına güvenli erişim; yapay zekânın pano bağlamını okumasını, diyagram oluşturmasını ve kod üretmesini sağlar.";
    if (key.startsWith("Seven skills for monday CRM users")) return "monday CRM için ilk kurulum, sabah özeti, tahmin panosu, veri temizliği, çalışma alanı kurulumu ve toplantı-fırsat eşitleme becerileri.";
    if (key.startsWith("Notion Skills + Notion MCP server")) return "Notion becerileri ile Notion MCP sunucusunu içeren Cursor eklentisi.";
    if (key.startsWith("Design on a canvas that Cursor can read and write")) return "Cursor'un okuyup yazabildiği, web standartlarına dayalı bir tuval üzerinde tasarım yapın.";
    if (key.startsWith("Skills and MCP server for the Resend email platform")) return "Resend e-posta platformunda gönderme, alma, şablonlar, CLI, React Email ve teslim edilebilirlik için beceriler ile MCP sunucusu.";
    if (key.startsWith("Sanity plugin for Cursor")) return "MCP sunucusu, ajan becerileri, ajan kuralları ve komutlar içeren Sanity eklentisi.";
    if (key.startsWith("A plugin for all things related to Svelte development")) return "Svelte geliştirme, MCP ve beceriler için kapsamlı Cursor eklentisi.";
    if (key.startsWith("Agentic production engineering for SWE")) return "Gözlemlenebilirlik, CI/CD ve gelişen bilgi tabanlarıyla üretim sorunlarını inceleyip çözmek için ajan destekli mühendislik araçları.";
    if (key.startsWith("Draw and visually collaborate with your agents")) return "Cursor içinde ajanlarınızla çizim yapın ve görsel olarak işbirliği kurun.";
    if (key.startsWith("Production-ready agent skills for Webflow")) return "Webflow için CMS yönetimi, site denetimi, varlık iyileştirme ve güvenli yayımlama becerileri.";
    if (key.startsWith("Build, manage, and deploy Wix sites and apps directly from Cursor")) return "Wix sitelerini ve uygulamalarını Cursor'dan oluşturun, yönetin ve dağıtın; pano, arka uç, widget ve hizmet eklentisi geliştirme becerileri içerir.";
    if (key.startsWith("Connect 9,000+ apps to your AI workflow")) return "9.000'den fazla uygulamayı yapay zekâ iş akışınıza bağlayın; Zapier eylemlerini keşfedin, etkinleştirin ve çalıştırın.";
    if (key.startsWith("Agent-first CLI for trading crypto")) return "Kraken'da kripto, hisse, döviz ve türev işlemleri için ajan odaklı CLI; varsayılan olarak kâğıt üzerinde işlem yapar, canlı işlem API anahtarıyla açılır.";
    if (key.startsWith("Give your agent a wallet")) return "Ajanınıza Phantom cüzdanı verin; desteklenen zincirlerde takas, imzalama ve adres yönetimi yapın.";
    if (key.startsWith("Connect Cursor to Ramp via MCP")) return "Cursor'u MCP üzerinden Ramp'a bağlayın; harcama analizi, onaylar, işlem temizliği ve tedarikçi akışlarını yönetin.";
    if (key.startsWith("Configure your RevenueCat integration")) return "RevenueCat entegrasyonunuzu yapılandırın ve RevenueCat projelerinizdeki verilere erişin.";
    if (key.startsWith("Deep Google Play subscription lifecycle skills")) return "RevenueCat Android SDK için satın alma, plan ve fiyat değişiklikleri, ödeme kurtarma, webhook ve güvenlik dahil Google Play abonelik yaşam döngüsü becerileri.";
    if (key.startsWith("Use the Revolut X CLI")) return "Kripto işlemleri, piyasa verileri, izleme ve grid bot stratejileri için Revolut X CLI aracını kullanın.";
    if (key.startsWith("Shopify developer tools for Cursor")) return "Shopify belgelerinde arama yapın; GraphQL, Liquid ve arayüz uzantısı kodu üretip doğrulayın. Telemetri OPT_OUT_INSTRUMENTATION=true ile kapatılabilir.";
    if (key.startsWith("Stripe plugin for Cursor")) return "Stripe entegrasyonları, iyi uygulamalar, API/SDK yükseltme rehberliği ve Stripe MCP sunucusu içeren Cursor eklentisi.";
    if (key.startsWith("Browser automation for Cursor")) return "Cursor için tarayıcı otomasyonu; sayfalarda gezinme, tıklama, form doldurma, veri çıkarma, ağ yakalama, sekme yönetimi ve ekran görüntüsü sağlar.";
    if (key.startsWith("Connect and operate 1000+ external apps from Cursor")) return "Composio MCP ile 1.000'den fazla harici uygulamayı Cursor'dan bağlayıp yönetin; OAuth, araç yönlendirme ve uzak veri işleme alanı içerir.";
    if (key.startsWith("Brainstorm, plan, debug, review, and compound learnings")) return "Yapay zekâ ajanlarıyla fikir üretin, planlayın, hata ayıklayın, inceleyin ve öğrenimleri biriktirin.";
    if (key.startsWith("Upstash Context7 MCP server")) return "Güncel ve sürüme özel belgeler ile kod örneklerini kaynak depolardan LLM bağlamına getiren Context7 MCP sunucusu.";
    if (key.startsWith("Scaffold and validate new Cursor plugins")) return "Yeni Cursor eklentilerini iskeletleyip doğrulayın; klasör kurulumu, bildirim dosyası üretimi ve pazar öncesi kalite denetimi yapar.";
    if (key.startsWith("A collection of DataRobot agent skills")) return "Model eğitimi, dağıtım, tahmin ve izleme için DataRobot ajan becerileri koleksiyonu.";
    if (key.startsWith("Cursor plugin for Firetiger agentic operations")) return "Beceriler ve MCP erişimiyle Firetiger ajan operasyonlarını Cursor'a getiren eklenti.";
    if (key.startsWith("Skills for working with Langfuse")) return "Açık kaynak LLM mühendislik platformu Langfuse'ta izleme, istem yönetimi ve değerlendirme için beceriler.";
    if (key.startsWith("Connect Cursor to hundreds of enterprise tools")) return "Merge CLI ile Cursor'u Jira, Salesforce, Slack, Gong, Workday ve yüzlerce kurumsal araca bağlayın.";
    if (key.startsWith("Opsera DevSecOps Agent")) return "Kod tabanı için yapay zekâ destekli mimari analiz, güvenlik taraması, uyumluluk denetimi ve SQL güvenliği sağlayan Opsera DevSecOps ajanı.";
    if (key.startsWith("Web search, content extraction, deep research, and data enrichment powered by parallel-cli")) return "parallel-cli ile web araması, içerik çıkarma, derin araştırma ve veri zenginleştirme.";
    if (key.startsWith("Simpler, safer way to run MCPs")) return "MCP, beceri ve ajanları daha güvenli çalıştırın; çalışanları keşfedin, güvenlik ilkelerini uygulayın, sırları koruyun ve denetim izi tutun.";
    if (key.startsWith("UI component and design system framework")) return "Bileşen kayıtlarında arama yapan, kaynak kod olarak bileşen kuran ve projeyi denetleyen shadcn/ui tasarım sistemi araçları.";
    if (key.startsWith("Tools that let coding agents verify and show their work")) return "Kodlama ajanlarının çalışan uygulamanız üzerinde sonuçlarını doğrulayıp göstermesini sağlayan araçlar.";
    if (key.startsWith("Core skills library: TDD")) return "TDD, hata ayıklama, işbirliği kalıpları ve kanıtlanmış teknikler için temel beceri kitaplığı.";
    if (key.startsWith("Search, explore, and investigate your team's remote repositories")) return "Tabnine Context Engine ile uzak depolarda anlamsal kod arama, sembol bulma, dosya gezintisi ve OpenAPI sorgulama.";
    if (key.startsWith("Context Engine CLI (ctx-cli) as focused skills")) return "Kiracı kurulumu, kod ve bilgi grafiği araması, hizmet inceleme, CVE/SAST önceliklendirme ve kodlama ilkesi denetimleri için ctx-cli becerileri.";
    if (key.startsWith("A single unified Auth0 skill")) return "Çerçeveyi ve özelliği algılayarak giriş, MFA, kuruluşlar, özel alan adı, JWT doğrulama, geçiş ve hata ayıklama rehberlerini yükleyen Auth0 becerisi.";
    if (key.startsWith("Buildkite MCP server and skills")) return "İşlem hattı tasarımı, derleme sorun giderme, ajan çalışma zamanı, CLI ve API için Buildkite MCP sunucusu ile becerileri.";
    if (key.startsWith("Secure container images and hardened library dependencies")) return "Chainguard ile güvenli kapsayıcı imajları ve sağlamlaştırılmış bağımlılıklar; imaj, güvenlik duyurusu ve ilke yönetimi sağlar.";
    if (key.startsWith("Connect Cursor to ThousandEyes MCP endpoints")) return "Ağ zekâsı iş akışları için Cursor'u Cisco ThousandEyes MCP uç noktalarına bağlayın.";
    if (key.startsWith("Patterns for designing CLIs that coding agents can run reliably")) return "Ajanların güvenilir çalıştırabileceği CLI araçları için etkileşimsiz bayraklar, örnekli yardım, işlem hatları, anlaşılır hatalar ve dry-run kalıpları.";
    if (key.startsWith("Use Cloudinary directly in Cursor")) return "Cloudinary'yi Cursor içinde kullanın; görsel ve videoları doğal dille yükleyin, yönetin, iyileştirin ve dönüştürün.";
    if (key.startsWith("Incrementally learns durable user preferences")) return "Konuşma değişikliklerinden kalıcı kullanıcı tercihlerini ve çalışma alanı bilgilerini öğrenerek AGENTS.md dosyasını sade maddelerle günceller.";
    if (key.startsWith("Corridor secures your AI-generated code")) return "Yapay zekâ tarafından üretilen kodu Corridor ile güvenceye alır; kullanmak için Corridor API anahtarı gerekir.";
    if (key.startsWith("Build apps, scripts, CI pipelines, and automations on top of the Cursor TypeScript SDK")) return "Cursor TypeScript SDK üzerinde uygulama, betik, CI hattı ve otomasyon geliştirme; çalışma zamanı, kimlik doğrulama, akış ve MCP kalıpları.";
    if (key.startsWith("Internal workflows used by Cursor developers")) return "Cursor geliştiricilerinin CI, kod inceleme, yayımlama, test güvenilirliği, kod temizliği ve iş özeti için kullandığı dahili iş akışları.";
    if (key.startsWith("Dun & Bradstreet empowers teams to execute workflows such as entity resolution, Sales & Marketing")) return "D&B Commercial Graph ile kuruluş eşleştirme, satış, pazarlama, finans, ana veri, tedarik zinciri ve uyumluluk iş akışları.";
    if (key.startsWith("Dun & Bradstreet empowers teams to execute risk workflows")) return "D&B Commercial Graph ile KYC/KYB, kuruluş eşleştirme, tarama, uyarı önceliklendirme ve ölçeklenebilir risk operasyonları.";
    if (key.startsWith("Databricks skills for the CLI")) return "Databricks CLI, Apps, Lakebase, Model Serving, Lakeflow Jobs, bildirimsel işlem hatları ve sunucusuz geçiş için beceriler.";
    if (key.startsWith("Endor Labs skills for setting up endorctl")) return "endorctl kurulumu ve bağımlılık yükseltmelerinin etkisini analiz etmek için Endor Labs becerileri.";
    if (key.startsWith("eToro API integration for Cursor")) return "OAuth SSO, piyasa verileri, işlemler, hesap hesaplamaları, ajan portföyleri ve sosyal özellikler için eToro API entegrasyonu.";
    if (key.startsWith("Forge — Work order management")) return "Yapay zekâ destekli geliştirme için iş emri yönetimi, geliştirici etkinliği takibi ve proje bağlamı.";
    if (key.startsWith("Create HeyGen avatar videos")) return "HeyGen ile avatar videoları, kişiselleştirilmiş mesajlar ve çevrilmiş/dublajlı videolar oluşturun; ses klonlama ve dudak eşitleme içerir.";
    if (key.startsWith("Generate images, videos, and more using Higgsfield")) return "Cursor içinden Higgsfield MCP ile görsel, video ve daha fazlasını üretin.";
    if (key.startsWith("Drive Lovable from Cursor")) return "Cursor'dan Lovable projeleri oluşturun, ajana iş gönderin, bulut veritabanlarını yönetin ve dağıtım yapın.";
    if (key.startsWith("Ideate, diagram, and align teams by connecting Cursor to Lucid")) return "Cursor'u Lucid'e bağlayarak fikir üretin, diyagram hazırlayın ve teknik mimariyi arayıp yönetin.";
    if (key.startsWith("Use Magic Patterns")) return "Kodlama ajanınızdan Magic Patterns ile fikirleri prototipleyin, arayüz ilhamı üretin, yerel arayüz yükleyin ve tasarımları kod tabanına aktarın.";
    if (key.startsWith("Create and share short video updates from agent work")) return "Ajan çalışmalarından kısa video güncellemeleri oluşturun ve paylaşın.";
    if (key.startsWith("Mem0 memory layer for AI applications")) return "Yapay zekâ uygulamalarına kalıcı bellek, kişiselleştirme ve anlamsal arama ekleyen Mem0 bellek katmanı.";
    if (key.startsWith("Microsoft Dataverse plugin for coding agents")) return "CRUD, toplu veri, gelişmiş sorgular, şema yaşam döngüsü ve ortam yönetimini MCP, CLI ve SDK ile birleştiren Dataverse eklentisi.";
    if (key.startsWith("Modern Web Guidance is an agent skill")) return "Yapay zekâ ajanlarının eski geçici çözümler yerine modern, güvenli ve yüksek performanslı web API'leri kullanmasına yardım eden Chrome destekli rehber.";
    if (key.startsWith("Connect Cursor to OneSignal")) return "Cursor'u OneSignal MCP sunucusu üzerinden OneSignal'a bağlayın.";
    if (key.startsWith("Fan a large task out across parallel Cursor cloud agents")) return "Büyük bir görevi Cursor SDK ile paralel bulut ajanlarına dağıtın; planlayıcı, çalışan ve sonuç birleştirme akışlarını yönetir.";
    if (key.startsWith("Connect Cursor to Plain")) return "Cursor'u Plain'e bağlayın; destek konuşmalarını, müşterileri, kiracıları ve yardım merkezi makalelerini düzenleyiciden yönetin.";
    if (key.startsWith("Port MCP Server Gives Cursor's AI agent full engineering context")) return "Port MCP, ajana hizmetler, ekipler, bağımlılıklar, standartlar, sahiplik ve kullanılabilir eylemler hakkında tam mühendislik bağlamı verir.";
    if (key.startsWith("if you want to go fast, go deep first")) return "Daha az fakat daha kaliteli kod için derin ve paralelleştirilebilir ajan iş akışları sunan pstack eklentisi.";
    if (key.startsWith("Create, refine, and vectorize SVG assets")) return "QuiverAI MCP ile SVG varlıkları oluşturun, iyileştirin ve vektörleştirin.";
    if (key.startsWith("Connect Cursor to Raisely")) return "Raisely MCP ile kampanyaları, bağışları, destekçileri ve diğer kayıtları sohbetten sorgulayıp yönetin.";
    if (key.startsWith("Scan, understand, and fix React codebase diagnostics")) return "React Doctor ile React kod tabanı tanılarını tarayın, anlayın ve düzeltin.";
    if (key.startsWith("Use Resolve for investigations")) return "İncelemeler, olaylar ve üretim bağlamı için Resolve kullanın.";
    if (key.startsWith("Administrator skills for managing Resolve integrations")) return "Resolve entegrasyonlarını yönetmek; kaynakları oluşturmak, hata ayıklamak ve yapılandırmak için yönetici becerileri.";
    if (key.startsWith("One-install mobile dev loops on cloud iOS/Android devices")) return "Bulut iOS/Android cihazlarında uygulamayı çalıştırın, değişiklikleri ekran görüntüleriyle doğrulayın ve cihaz kanıtıyla yayımlayın.";
    if (key.startsWith("Roboflow computer vision skills")) return "Veri kümeleri, etiketleme, eğitim, iş akışları, çıkarım ve dağıtım için Roboflow bilgisayarlı görü becerileri ile MCP araçları.";
    if (key.startsWith("AI agent skills for integrating the Scandit Data Capture SDK")) return "Barkod tarama, kimlik yakalama ve akıllı etiket yakalama için Scandit SDK seçim, belge ve uygulama rehberleri.";
    if (key.startsWith("Plugin by Semgrep")) return "Cursor için MCP, kancalar ve beceriler üzerinden Semgrep güvenlik taraması sağlar.";
    if (key.startsWith("Ship faster with Sinch in Cursor")) return "SMS, WhatsApp, RCS, ses, e-posta, doğrulama ve numaralar için Sinch becerileri ile MCP.";
    if (key.startsWith("Snyk security scanning")) return "Cursor için Snyk güvenlik taraması, düzeltme ve bağımlılık sağlığı araçları.";
    if (key.startsWith("Snyk API & Web MCP Server")) return "Hedef ekleme, kimlik doğrulama, DAST taraması ve bulgu önceliklendirme için Snyk API & Web MCP sunucusu.";
    if (key.startsWith("Automatically enforce SonarQube code quality")) return "40'tan fazla dilde 7.000'den fazla kural, sır tarama, ajan analizi ve kalite kapılarıyla SonarQube kalite ve güvenliğini uygular.";
    if (key.startsWith("AI-powered dependency intelligence")) return "Güvenlik açıklarını denetleyin, daha güvenli sürümleri bulun ve Sonatype verileriyle bağımlılık kararlarını iyileştirin.";
    if (key.startsWith("Web search, content extraction, crawling, deep research")) return "Tavily tvly CLI ile web araması, içerik çıkarma, tarama, derin araştırma ve URL keşfi.";
    if (key.startsWith("Thermo-nuclear branch review")) return "Derin doğruluk ve güvenlik denetimleri, sert kod kalitesi ölçütleri, paralel alt ajanlar ve birleştirmeye hazır akışlar sunar.";
    if (key.startsWith("Reports this device's Cursor MCP servers to Zenity")) return "Oturum başında bu cihazdaki Cursor MCP sunucularını Zenity AI Edge'e bildirir; yapılandırmadaki sırları temizler ve iletmez.";
    if (key.startsWith("Prospect, enrich leads, load outreach sequences")) return "Apollo.io ile potansiyel müşteri bulun, verileri zenginleştirin, erişim dizileri yükleyin ve satış analizlerini sorgulayın.";
    if (key.startsWith("Add Arize AX observability to LLM applications")) return "LLM uygulamalarına Arize AX gözlemlenebilirliği; otomatik izleme, veri kümeleri, deneyler ve istem iyileştirme araçları ekler.";
    if (key.startsWith("Connect Cursor to Asana")) return "Cursor'u Asana'ya bağlayın; görev oluşturun, projeleri güncelleyin, çalışma alanında arama yapın ve işleri yönetin.";
    if (key.startsWith("Data engineering plugin - warehouse exploration")) return "Veri ambarı keşfi, veri hattı oluşturma ve Airflow entegrasyonu için veri mühendisliği eklentisi.";
    if (key.startsWith("Atlan is the context layer for enterprise AI")) return "Kurumsal yapay zekâ için bilgi, veri ve anlam katmanı. Güvenilir kurumsal bağlamı arayın, veri soyunu izleyin ve yönetilen tanımlara erişin.";
    if (key.startsWith("Atlassian plugin for Cursor")) return "Jira, Confluence, önceliklendirme, iş listeleri ve durum raporları için MCP ve beceriler içeren Atlassian eklentisi.";
    if (key.startsWith("Forge app builder skill bundle")) return "Atlassian Forge uygulamalarını geliştirme, dağıtma ve sorun giderme için Forge MCP entegrasyonlu beceri paketi.";
    if (key.startsWith("Use Amplitude like an expert")) return "Amplitude ile analitik ölçüm kurun, ürün fırsatlarını keşfedin, grafikleri inceleyin, pano ve deneyleri yönetin.";
    if (key.startsWith("Bring Antimetal's software investigation intelligence")) return "Antimetal'in yazılım inceleme yeteneklerini Cursor'a getirir; sorunları önceliklendirir, temel nedenleri araştırır ve düzeltmeler uygular.";
    if (key.startsWith("Development, customization, testing, and deployment skills for Adobe App Builder")) return "Adobe App Builder projelerini geliştirme, özelleştirme, test etme ve dağıtma becerileri.";
    if (key.startsWith("Quote and execute intent-based (Fusion)")) return "1inch ile zincir içi ve zincirler arası token takasları, limit emirleri, portföy bakiyeleri, fiyatlar ve gaz tahminlerini yönetin.";
    if (key.startsWith("Airwallex CLI plugin for Cursor")) return "Cursor için Airwallex komut satırı eklentisi.";
    if (key.startsWith("Use Chargebee's API integration patterns")) return "Cursor içinde faturalandırma işlemleri için Chargebee API entegrasyonu, webhook, SDK ve şema rehberliği.";
    if (key.startsWith("Ship stablecoin apps faster")) return "USDC ödemeleri, zincirler arası transferler, cüzdanlar ve akıllı sözleşmeler için Circle becerileri ve MCP sunucusu.";
    if (key.startsWith("Build, deploy, and operate AI agents on AWS")) return "AWS üzerinde yapay zekâ ajanları oluşturma, dağıtma ve işletme; araç, bellek, çoklu ajan, gözlemleme ve güvenlik becerileri.";
    if (key.startsWith("Build, train, and deploy AI models with deep AWS AI/ML expertise")) return "Amazon SageMaker AI uzmanlığıyla yapay zekâ modelleri oluşturun, eğitin ve dağıtın.";
    if (key.startsWith("Render documentation — architecture notes")) return "Mimari notları, API başvurularını, çalışma kitaplarını ve kod tabanı anlatımlarını gezilebilir Cursor Tuvali olarak görüntüler.";
    if (key.startsWith("Render PR diffs as interactive Cursor Canvases")) return "PR farklarını önem düzeyine göre düzenlenen, temel değişiklikleri ve riskli kodu vurgulayan etkileşimli Cursor tuvallerinde gösterir.";
    if (key.startsWith("1Password Developer Environments for Cursor")) return "Proje sırlarını oluşturmak, içe aktarmak ve yönetmek için 1Password araçları. macOS veya Linux gerektirir; Windows desteklenmez.";
    if (key.startsWith("CLI-backed repo compatibility scans")) return "Depoların başlatma, doğrulama ve belge uyumluluğunu gerçek davranışa göre denetleyen komut satırı taramaları ve Cursor ajanları.";
    if (key.startsWith("AMD's verified Agent Skills in one plugin")) return "Ryzen AI ve AMD Instinct üzerinde yerel yapay zekâ, LLM sunumu ve GPU/PyTorch performans analizi için doğrulanmış AMD ajan becerileri.";
    if (key.startsWith("Comprehensive integration guide for Chargebee billing platform")) return "Chargebee faturalandırma platformu için kapsamlı entegrasyon rehberi. API ve REST çağrıları, webhook olayları, müşteri yönetimi, abonelik yaşam döngüsü, ödeme, fatura ve diğer faturalandırma entegrasyonlarında kullanılır.";
    if (key.startsWith("Analyze recent cloud agent runs to root-cause environment setup failures")) return "Son bulut ajanı çalıştırmalarını analiz ederek kurulum günlükleri, konuşma dökümleri ve ortam verilerinden ortam kurulum hatalarının temel nedenini bulun";
    if (key.startsWith("Use /add-plugin to install a plugin from the Cursor")) return "Cursor Eklenti Pazarı'ndan eklenti yüklemek için /add-plugin kullanın";
    if (key.startsWith("Use /plan to improve agent execution with Plan Mode")) return "/plan ile Plan Modu'nu kullanarak ajan yürütmesini iyileştirin";
    if (key.startsWith("Use /create-hook to control and extend the agent loop with custom scripts")) return "/create-hook ile ajan döngüsünü özel betiklerle denetleyip genişletin";
    if (key.startsWith("Use /simplify to have Cursor review all changed files for code quality and efficiency")) return "/simplify ile Cursor'un tüm değişen dosyaları kod kalitesi ve verimlilik için incelemesini sağlayın";
    if (key.startsWith("Use /multitask so Cursor can work on your queued messages in parallel")) return "/multitask ile Cursor'un sıradaki mesajlarınız üzerinde paralel çalışmasını sağlayın";
    if (key.startsWith("Use /review to have Cursor find bugs")) return "/review ile Cursor'un hataları, gerilemeleri, güvenlik sorunlarını ve eksik testleri bulmasını sağlayın";
    if (key.startsWith("Use /review for an agentic code review of your changes")) return "/review ile değişikliklerinizi ajan destekli kod incelemesinden geçirin";
    if (key.startsWith("Kullan /review for an agentic code review of your changes")) return "/review ile değişikliklerinizi ajan destekli kod incelemesinden geçirin";
    if (key.startsWith("Debug Mode reproduces and solves your most difficult bugs")) return "Hata Ayıklama Modu en zor hatalarınızı yeniden oluşturup çözer; başlamak için Shift+Tab tuşlarına iki kez basın";
    if (key.startsWith("Use /babysit to triage PR comments")) return "/babysit ile PR yorumlarını önceliklendirin, CI hatalarını düzeltin ve çakışmaları temizleyin";
    if (key.startsWith("Kullan /babysit to triage PR comments")) return "/babysit ile PR yorumlarını önceliklendirin, CI hatalarını düzeltin ve çakışmaları temizleyin";
    if (key.startsWith("Drag and drop agent chats to split your view")) return "Görünümünüzü döşenmiş panellere bölmek için ajan sohbetlerini sürükleyip bırakın";
    if (key.startsWith("Use /multitask to run subagents to parallelize your requests instead of queuing them")) return "/multitask ile isteklerinizi sıraya almak yerine paralel çalıştırmak için alt ajanları kullanın";
    if (key.startsWith("Try a new window for running parallel agents")) return "Paralel ajanları çalıştırmak için yeni bir pencere deneyin";
    if (key.startsWith("After long sessions, use /split-to-prs to turn your work into small, reviewable PRs")) return "Uzun oturumlardan sonra çalışmanızı küçük ve incelenebilir PR'lara bölmek için /split-to-prs kullanın";
    if (key === "After long sessions, use") return "Uzun oturumlardan sonra";
    if (key.startsWith("Voice mode lets you dictate better prompts for your agents")) return "Ses modu, ajanlarınız için daha iyi istemleri dikte etmenizi sağlar";
    if (key.startsWith("Use /ask to research your codebase before starting code changes")) return "Kod değişikliklerine başlamadan önce kod tabanınızı araştırmak için /ask kullanın";
    if (key.startsWith("Ask Mode uses read-only agents to research your codebase")) return "Sor Modu, kod tabanınızı araştırmak için salt okunur ajanlar kullanır; başlamak için Shift+Tab tuşlarına basın";
    if (key.startsWith("Sor Mod uses read-only agents to research your codebase")) return "Sor Modu, kod tabanınızı araştırmak için salt okunur ajanlar kullanır; başlamak için Shift+Tab tuşlarına basın";
    if (key.startsWith("Cursor can respond with interactive visualizations alongside text")) return "Cursor, metnin yanında etkileşimli görselleştirmelerle yanıt verebilir; başlamak için /canvas kullanın";
    if (key.startsWith("Use /canvas to get interactive visualizations like dashboards from Cursor")) return "/canvas ile Cursor'dan pano gibi etkileşimli görselleştirmeler alın";
    if (key.startsWith("Use /automate to create Cursor Automations without leaving your agent chat")) return "/automate ile ajan sohbetinden ayrılmadan Cursor Otomasyonları oluşturun";
    if (key.startsWith("Use /cloud or /local to move agent sessions between runtimes")) return "/cloud veya /local ile ajan oturumlarını çalışma ortamları arasında taşıyın";
    if (key.startsWith("Use /cloud to run agents remotely for better parallelization and durable execution")) return "/cloud ile daha iyi paralelleştirme ve kalıcı yürütme için ajanları uzaktan çalıştırın";
    if (key.startsWith("Use /create-rule to control agent behavior through system-level instructions")) return "/create-rule ile ajan davranışını sistem düzeyi talimatlarla denetleyin";
    if (key.startsWith("Use /create-skill to customize Cursor for your workflows")) return "/create-skill ile Cursor'u iş akışlarınıza göre özelleştirin";
    if (key.startsWith("Use /create-subagent to set up specialized agents that Cursor can use to parallelize work")) return "/create-subagent ile Cursor'un işi paralelleştirmek için kullanabileceği uzman ajanlar kurun";
    if (key.startsWith("Use /debug to solve bugs that are hard to reproduce or understand")) return "/debug ile yeniden üretmesi veya anlaması zor hataları çözün";
    if (key.startsWith("Use /in-cloud to start a subagent in its own cloud VM")) return "/in-cloud ile yerel çalışma alanınızı boş tutarak alt ajanı kendi bulut VM'inde başlatın";
    if (key.startsWith("Use /loop to run a prompt on a schedule")) return "/loop ile bir istemi zamanlamaya göre çalıştırın";
    if (key.startsWith("Use /model to pick the best model for your task")) return "/model ile göreviniz için en uygun modeli seçin; maliyet-yetenek dengesi için Composer'ı kullanın";
    if (key.startsWith("Use /shell to run commands in the terminal")) return "/shell ile terminalde komut çalıştırın";
    if (key.startsWith("Use /split-to-prs")) return "/split-to-prs ile çalışmanızı küçük PR'lara ayırın";
    if (key === "Use /automate") return "/automate kullan";
    if (key === "Use /cloud") return "/cloud kullan";
    if (key === "Use /cloud or /local") return "/cloud veya /local kullan";
    if (key === "Use /create-rule") return "/create-rule kullan";
    if (key === "Use /create-skill") return "/create-skill kullan";
    if (key === "Use /create-subagent") return "/create-subagent kullan";
    if (key === "Use /debug") return "/debug kullan";
    if (key === "Use /in-cloud") return "/in-cloud kullan";
    if (key === "Use /loop") return "/loop kullan";
    if (key === "Use /model") return "/model kullan";
    if (key === "Use /shell") return "/shell kullan";
    if (key === "Use /review") return "/review kullan";
    if (key === "Kullan /review") return "/review kullan";
    if (key === "Use /plan") return "/plan kullan";
    if (key === "Use /ask") return "/ask kullan";
    if (key === "Use /canvas") return "/canvas kullan";
    if (key === "Use /multitask") return "/multitask kullan";
    if (key === "Use /simplify") return "/simplify kullan";
    if (key === "Use /add-plugin") return "/add-plugin kullan";
    if (key.startsWith("Use @browser to inspect page elements")) return "@browser ile sayfa öğelerini inceleyin, konsol günlüklerini görüntüleyin ve ağ trafiğini analiz edin";
    if (key.startsWith("Kullan @browser to inspect page elements")) return "Sayfa öğelerini incelemek, konsol günlüklerini görüntülemek ve ağ trafiğini analiz etmek için @browser kullanın";
    if (key.startsWith("Ajan skills help you customize Cursor for your workflows")) return "Ajan becerileri Cursor'u iş akışlarınıza göre özelleştirmenize yardımcı olur; başlamak için /create-skill kullanın";
    if (key.startsWith("Cursor syncs your local skills")) return "Cursor, yerel becerilerinizi Bulut Ajanlarında kullanabilmeniz için eşitler. Eşitlemeyi kapatmak için bu seçeneği devre dışı bırakın.";
    if (key.startsWith("Try Plan Mode")) return "Ajan sonuçlarını ve doğruluğunu iyileştirmek için Plan Modunu deneyin";
    if (key.startsWith("With your Cursor Pro subscription")) return "Cursor Pro aboneliğinizle kendi Google anahtarınızı kullanmanız gerekmez!";
    if (key.startsWith("Turn Off Google Key")) return "Google Anahtarını Kapat";
    if (key.startsWith("Google API Key")) return "Google API Anahtarı";
    if (key.startsWith("Anthropic's most powerful model")) return "Anthropic'in en güçlü modeli; zor görevler için idealdir.";
    if (key.startsWith("This model has special data retention policies")) return "Bu modelin özel veri saklama politikaları vardır.";
    const usageReset = key.match(/^Usage limits reset on (.+) \((\d+) days? left\)$/);
    if (usageReset) return `Kullanım sınırları ${usageReset[1]} tarihinde sıfırlanır (${usageReset[2]} gün kaldı)`;
    const usedPercent = key.match(/^(\d+)% used$/);
    if (usedPercent) return `%${usedPercent[1]} kullanıldı`;
    const monthlyPrice = key.match(/^(\$\d+)\/mo$/);
    if (monthlyPrice) return `${monthlyPrice[1]}/ay`;
    if (key.startsWith("to control and extend the agent loop")) return "ile ajan döngüsünü özel betiklerle denetleyip genişletin";
    if (key.startsWith("to research your codebase before starting code changes")) return "ile kod değişikliklerine başlamadan önce kod tabanınızı araştırın";
    if (key.startsWith("for an agentic code review of your changes")) return "ile değişikliklerinizi ajan destekli kod incelemesinden geçirin";
    if (key.startsWith("reproduces and solves your most difficult bugs")) return "en zor hatalarınızı yeniden oluşturup çözer; başlamak için Shift+Tab tuşlarına iki kez basın";
    if (key.startsWith("to have Cursor find bugs, regressions")) return "ile Cursor'un hataları, gerilemeleri, güvenlik sorunlarını ve eksik testleri bulmasını sağlayın";
    if (key.startsWith("to triage PR comments, fix CI failures")) return "ile PR yorumlarını önceliklendirin, CI hatalarını düzeltin ve çakışmaları temizleyin";
    if (key.startsWith("to improve agent execution with Plan Mode")) return "ile Plan Modu'nu kullanarak ajan yürütmesini iyileştirin";
    if (key.startsWith("to have Cursor review all changed files for code quality and efficiency")) return "ile Cursor'un tüm değişen dosyaları kod kalitesi ve verimlilik için incelemesini sağlayın";
    if (key.startsWith("so Cursor can work on your queued messages in parallel")) return "ile Cursor'un sıradaki mesajlarınız üzerinde paralel çalışmasını sağlayın";
    if (key.startsWith(" so Cursor can work on your queued messages in parallel")) return " ile Cursor'un sıradaki mesajlarınız üzerinde paralel çalışmasını sağlayın";
    if (key.startsWith("to turn your work into small, reviewable PRs")) return "ile çalışmanızı küçük ve incelenebilir PR'lara bölün";
    if (key.startsWith("to get interactive visualizations like dashboards from Cursor")) return "ile Cursor'dan pano gibi etkileşimli görselleştirmeler alın";
    if (key.startsWith("to create Cursor Automations without leaving your agent chat")) return "ile ajan sohbetinden ayrılmadan Cursor Otomasyonları oluşturun";
    if (key.startsWith("to create Cursor Otomasyonları without leaving your agent chat")) return "ile ajan sohbetinden ayrılmadan Cursor Otomasyonları oluşturun";
    if (key.startsWith("or /local to move agent sessions between runtimes")) return "veya /local ile ajan oturumlarını çalışma ortamları arasında taşıyın";
    if (key.startsWith("to move agent sessions between runtimes")) return "ile ajan oturumlarını çalışma ortamları arasında taşıyın";
    if (key.startsWith("to run agents remotely for better parallelization and durable execution")) return "ile daha iyi paralelleştirme ve kalıcı yürütme için ajanları uzaktan çalıştırın";
    if (key.startsWith("to control agent behavior through system-level instructions")) return "ile ajan davranışını sistem düzeyi talimatlarla denetleyin";
    if (key.startsWith("to customize Cursor for your workflows")) return "ile Cursor'u iş akışlarınıza göre özelleştirin";
    if (key.startsWith("to set up specialized agents that Cursor can use to parallelize work")) return "ile Cursor'un işi paralelleştirmek için kullanabileceği uzman ajanlar kurun";
    if (key.startsWith("to solve bugs that are hard to reproduce or understand")) return "ile yeniden üretmesi veya anlaması zor hataları çözün";
    if (key.startsWith("to start a subagent in its own cloud VM")) return "ile yerel çalışma alanınızı boş tutarak alt ajanı kendi bulut VM'inde başlatın";
    if (key.startsWith("to run a prompt on a schedule")) return "ile bir istemi zamanlamaya göre çalıştırın";
    if (key.startsWith("to pick the best model for your task")) return "ile göreviniz için en uygun modeli seçin; maliyet-yetenek dengesi için Composer'ı kullanın";
    if (key.startsWith("to run commands in the terminal")) return "ile terminalde komut çalıştırın";
    if (key.startsWith("to run subagents to parallelize your requests")) return "ile isteklerinizi sıraya almak yerine paralel çalıştırmak için alt ajanları kullanın";
    if (key.startsWith("The predecessor to Cursor Grok 4.6")) return "Cursor Grok 4.6'nın öncülü; karmaşık kodlama ve bilgi çalışmaları için geliştirildi.";
    if (key.startsWith("The predecessor to Grok 4.7")) return "Grok 4.7'nin öncülü; karmaşık kodlama ve bilgi çalışmaları için geliştirildi.";
    if (key.startsWith("The predecessor to Grok 4.6")) return "Grok 4.6'nın öncülü; karmaşık kodlama ve bilgi çalışmaları için geliştirildi.";
    if (key.startsWith("The predecessor to Grok 4.5")) return "Grok 4.5'in öncülü; karmaşık kodlama ve bilgi çalışmaları için geliştirildi.";
    if (key.startsWith("OpenAI's flagship GPT-5.6 model.")) return "OpenAI'nin amiral gemisi GPT-5.6 modeli. Yeni azami akıl yürütme çabasıyla en güçlü ajan tabanlı kodlama, biyoloji ve siber güvenlik yeteneklerini sunar.";
    if (key.startsWith("Cursor installation appears corrupted")) return "Cursor kurulumunuz bozuk görünüyor. Lütfen Cursor'u yeniden kurun.";
    if (key.startsWith("Search Cursor to find a prior conversation")) return "Önceki bir konuşmayı bulmak için Cursor'da arayın veya konuşmalar genelinde özetleyin";
    if (key.startsWith("Messages sent while Cursor is working can steer it mid-run")) return "Cursor çalışırken gönderilen mesajlar çalışmayı kesmeden akışı yönlendirebilir — bu seçeneği Ajanlar ayarlarındaki Yeni Mesajlar bölümünden açın";
    if (key.startsWith("Plan Mode improves agent outcomes and accuracy")) return "Plan Modu, ajan sonuçlarını ve doğruluğunu iyileştirir — başlamak için Shift+Tab tuşlarına basın";
    if (key === "Includes Cursor Grok and Composer") return "Cursor Grok ve Composer dahil";
    if (key === "256k context window") return "256 bin bağlam penceresi";
    if (key === "272k context window") return "272 bin bağlam penceresi";
    if (key === "Version: medium reasoning effort") return "Sürüm: orta akıl yürütme çabası";
    if (key.startsWith("to inspect page elements")) return "ile sayfa öğelerini inceleyin, konsol günlüklerini görüntüleyin ve ağ trafiğini analiz edin";
    if (key.startsWith("to install a plugin from the Cursor")) return "ile Cursor Eklenti Pazarı'ndan eklenti yükleyin";
    if (key.startsWith("lets you dictate better prompts")) return "ajanlarınız için daha iyi istemleri dikte etmenizi sağlar";
    if (key.startsWith("uses read-only agents to research your codebase")) return "kod tabanınızı araştırmak için salt okunur ajanlar kullanır; başlamak için Shift+Tab tuşlarına basın";
    if (key.startsWith("improves agent outcomes and accuracy")) return "ajan sonuçlarını ve doğruluğunu iyileştirir; başlamak için Shift+Tab tuşlarına basın";
    if (key.startsWith("Tell Cursor to use subagents to break down tasks")) return "Cursor'a görevleri bölmek, paralel çalışmak ve bağlamı korumak için alt ajanları kullanmasını söyleyin";
    if (key.startsWith("Select Composer in your model picker")) return "Zeka ve maliyet arasında iyi denge için model seçicide Composer'ı seçin";
    if (key.startsWith("Seç Composer in your model picker")) return "Zeka ve maliyet arasında iyi denge için model seçicide Composer'ı seçin";
    if (key.startsWith("Composer in your model picker")) return "model seçicide Composer'ı seçin; zeka ve maliyet arasında iyi denge sağlar";
    if (key.startsWith("in your model picker for a great balance")) return "model seçicide; zeka ve maliyet arasında iyi denge sağlar";
    if (key.startsWith("Craft-first interface design for dashboards")) return "Panolar, yönetim panelleri, SaaS uygulamaları, araçlar, ayar sayfaları, veri arayüzleri ve etkileşimli ürünler için görsel kalite odaklı arayüz tasarımı.";
    if (key.startsWith("Use when the task requires automating a real browser from the terminal")) return "Görev terminalden gerçek bir tarayıcıyı otomatikleştirmeyi gerektirdiğinde kullanılır: gezinme, form doldurma, ekran görüntüsü, veri çıkarma ve UI akışı hata ayıklama.";
    if (key.startsWith("Fine-tune models on Azure AI Foundry using SFT")) return "Azure AI Foundry üzerinde SFT, DPO veya RFT ile model ince ayarı yapar; veri hazırlama, eğitim işi gönderme, dağıtım ve değerlendirmeyi kapsar.";
    if (key.startsWith("Discovers available Azure OpenAI model capacity across regions")) return "Bölgeler ve projeler genelinde Azure OpenAI model kapasitesini keşfeder; kota sınırlarını analiz eder ve uygun dağıtım konumlarını önerir.";
    if (key.startsWith("Interactive guided deployment flow for Azure OpenAI models")) return "Azure OpenAI modelleri için tam özelleştirme kontrollü etkileşimli dağıtım akışı; model sürümü, SKU, kapasite ve ilke seçimlerinde adım adım ilerletir.";
    if (key.startsWith("Intelligently deploys Azure OpenAI models to optimal regions")) return "Azure OpenAI modellerini tüm bölgelerdeki kapasiteyi analiz ederek en uygun bölgelere akıllıca dağıtır.";
    if (key.startsWith("Unified Azure OpenAI model deployment skill")) return "Azure OpenAI model dağıtımı için birleşik beceri; hızlı hazır dağıtımlar, tam özelleştirilmiş dağıtımlar ve kapasite keşfini yönetir.";
    if (key.startsWith("Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end")) return "Foundry ajanlarını uçtan uca dağıtma, değerlendirme, ince ayar yapma ve yönetme becerisi.";
    if (key.startsWith("Creates and maintains Figma Code Connect template files")) return "Figma bileşenlerini kod parçacıklarıyla eşleyen Figma Code Connect şablon dosyalarını oluşturur ve bakımını yapar.";
    if (key.startsWith("**MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `create_new_file`")) return "Zorunlu ön koşul: Her `create_new_file` araç çağrısından önce bu beceri kullanılmalıdır.";
    if (key.startsWith("**MANDATORY prerequisite** — you MUST invoke this skill BEFORE calling the `get_design_context`")) return "Zorunlu ön koşul: `get_design_context` Figma MCP aracı çağrılmadan önce bu beceri kullanılmalıdır.";
    if (key.startsWith("Use this skill alongside figma-use when the task involves translating an application page")) return "Bir uygulama sayfasını, görünümü veya çok bölümlü yerleşimi Figma'ya çevirmek gerektiğinde bu beceri figma-use ile birlikte kullanılır.";
    if (key.startsWith("MANDATORY prerequisite — load this skill BEFORE every `generate_diagram`")) return "Zorunlu ön koşul: Her `generate_diagram` çağrısından önce bu beceri yüklenmelidir.";
    if (key.startsWith("Build or update a professional-grade design system in Figma")) return "Figma'da kod tabanından profesyonel düzeyde tasarım sistemi oluşturur veya günceller; değişkenler, tokenlar ve bileşen kitaplıklarını kapsar.";
    if (key.startsWith("Translates Figma motion and animations into production-ready")) return "Figma hareket ve animasyonlarını üretime hazır uygulama koduna çevirir.";
    if (key.startsWith("SwiftUI ↔ Figma translation")) return "SwiftUI ve Figma arasında çeviri yapar; Swift, SwiftUI, iOS, iPhone veya iPad işleri için kullanılır.";
    if (key.startsWith("This skill helps agents use Figma's use_figma MCP tool in the FigJam context")) return "Ajanların FigJam bağlamında Figma'nın use_figma MCP aracını kullanmasına yardımcı olur.";
    if (key.startsWith("Motion / animation context for the `use_figma` MCP tool")) return "`use_figma` MCP aracı için hareket ve animasyon bağlamı sağlar.";
    if (key.startsWith("This skill helps agents use Figma's use_figma MCP tool in the Slides context")) return "Ajanların Slides bağlamında Figma'nın use_figma MCP aracını kullanmasına yardımcı olur.";
    match = key.match(/^Tab Stats: (\d+)\/(\d+) \(([^)]+)\)$/);
    if (match) return `Sekme istatistikleri: ${match[1]}/${match[2]} (${match[3]})`;
    match = key.match(/^Agent Stats: (\d+)\/(\d+) \(([^)]+)\)$/);
    if (match) return `Ajan istatistikleri: ${match[1]}/${match[2]} (${match[3]})`;
    match = key.match(/^Agent AI Stats \(Today\): (\d+)\/(\d+) lines \(([^)]+)\)$/);
    if (match) return `Ajan AI istatistikleri (Bugün): ${match[1]}/${match[2]} satır (${match[3]})`;
    if (key.startsWith("let you control and extend the agent loop")) return "ajan döngüsünü kontrol edip genişletmenizi sağlar — başlamak için /create-hook kullanın";
    if (key.startsWith("Automate repetitive tasks with always-on agents")) return "Sürekli açık ajanlarla tekrarlanan görevleri otomatikleştirin ve Cursor'un yerleşik ajanlarını ekibiniz için yapılandırın.";
    return null;
  };
  globalThis.__cursorTrTranslateValue = translateValue;
  globalThis.__cursorTrTranslateModelTooltip = translateModelTooltipValue;
  const translate = (root) => {
    const nodes = [];
    if (root && root.nodeType === Node.ELEMENT_NODE) nodes.push(root);
    if (root && root.querySelectorAll) nodes.push(...root.querySelectorAll(".action-label, .action-menu-item, button, input, textarea, [data-placeholder], [aria-placeholder]"));
    for (const el of nodes) {
      for (const attr of attrs) {
        const value = el.getAttribute && el.getAttribute(attr);
        const translated = translateValue(value);
        if (translated && translated !== value) el.setAttribute(attr, translated);
      }
      if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
        const translated = translateValue(el.placeholder);
        if (translated && translated !== el.placeholder) el.placeholder = translated;
      }
    }
    const textRoot = root?.nodeType === Node.TEXT_NODE ? root.parentElement : root;
    if (!textRoot || !document.createTreeWalker) return;
    const walker = document.createTreeWalker(textRoot, NodeFilter.SHOW_TEXT);
    let textNode;
    while ((textNode = walker.nextNode())) {
      const parent = textNode.parentElement;
      if (!parent || parent.closest(protectedSelector)) continue;
      const value = textNode.nodeValue.trim();
      const translated = translateValue(value);
      if (translated && translated !== value) textNode.nodeValue = textNode.nodeValue.replace(value, translated);
    }
  };
  // Ana ekranin altindaki donen ipuclari React tarafindan parcalara ayrilir.
  // Komut parcasi <code> icinde oldugu icin genel koruma kurali bu alani atlar;
  // ayrica yeni ipucu her zaman MutationObserver'in gordugu bir dugum eklemesiyle
  // gelmez. Bu hedefli tarayici, bicimlendirmeyi bozmadan her metin parcasini cevirir.
  const translateRotatingTips = () => {
    document.querySelectorAll(".glass-empty-state-rotating-tips__text, .agent-panel-empty-state-footer-region").forEach(container => {
      const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
      let textNode;
      while ((textNode = walker.nextNode())) {
        const value = textNode.nodeValue.trim();
        const translated = translateValue(value);
        if (translated && translated !== value) textNode.nodeValue = textNode.nodeValue.replace(value, translated);
      }
    });
  };
  // Sınıf adları Cursor güncellemelerinde değişebiliyor. Ana ekrandaki ipucu
  // her zaman pencerenin alt bandında bulunduğu için sınıftan bağımsız yedek
  // denetim yalnızca bu dar alandaki metin düğümlerini işler.
  const translateBottomBand = () => {
    if (!document.body || !document.createTreeWalker) return;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let textNode;
    while ((textNode = walker.nextNode())) {
      const parent = textNode.parentElement;
      if (!parent || parent.closest(".monaco-editor, .xterm, textarea, pre, [data-component=\"glass-empty-state-rotating-tips\"]")) continue;
      const rect = parent.getBoundingClientRect();
      if (rect.bottom < innerHeight - 140 || rect.top > innerHeight) continue;
      const value = textNode.nodeValue.trim();
      const translated = translateValue(value);
      if (translated && translated !== value) textNode.nodeValue = textNode.nodeValue.replace(value, translated);
    }
  };
  // Dönen ipuçlarının güncel DOM'u sınıf adı taşımıyor ve cümleyi
  // "Use" + <code>/komut</code> + devamı şeklinde üç ayrı düğüme bölüyor.
  // Sınıf/konum tahmini kullanmadan yalnızca benzersiz komut devamlarını bul,
  // baştaki Use/Kullan düğümünü kaldır ve doğal Türkçe devamı yerleştir.
  const commandTipFragments = [
    ["/model", "to pick the best model for your task and select Composer for a great balance of cost vs. capability", " ile göreviniz için en uygun modeli seçin; maliyet ve yetenek dengesi için Composer'ı kullanın"],
    ["/loop", "to run a prompt on a schedule", " ile bir istemi zamanlamaya göre çalıştırın"],
    ["/in-cloud", "to start a subagent in its own cloud VM, keeping your local workspace free", " ile yerel çalışma alanınızı boş tutarak bir alt ajanı kendi bulut sanal makinesinde başlatın"],
    ["/create-hook", "to get started", " — başlamak için /create-hook kullanın"],
    ["/create-hook", "let you control and extend the agent loop", "Kancalar, ajan döngüsünü kontrol edip genişletmenizi sağlar"],
    ["/create-hook", "Kancalar let you control and extend the agent loop", "Kancalar, ajan döngüsünü kontrol edip genişletmenizi sağlar"],
    ["/goal", "to set an objective that Cursor keeps pursuing until it is complete", " ile Cursor'un tamamlanana kadar izlemeyi sürdüreceği bir hedef belirleyin"]
  ];
  const translateCommandTipFragments = () => {
    if (!document.body || !document.createTreeWalker) return;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let textNode;
    while ((textNode = walker.nextNode())) {
      const normalized = textNode.nodeValue.replace(/\s+/g, " ").trim();
      const def = commandTipFragments.find(([, source]) => normalized.startsWith(source));
      if (!def) continue;
      const [command, source, translated] = def;
      let scope = textNode.parentElement;
      for (let i = 0; scope && i < 8; i++, scope = scope.parentElement) {
        const content = (scope.textContent || "").replace(/\s+/g, " ");
        if (!content.includes(command) || !content.includes(source)) continue;
        const prefixWalker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT);
        let prefixNode;
        while ((prefixNode = prefixWalker.nextNode())) {
          if (["Use", "Kullan"].includes(prefixNode.nodeValue.trim())) {
            prefixNode.nodeValue = "";
            break;
          }
        }
        break;
      }
      const leading = (textNode.nodeValue.match(/^\s*/) || [""])[0];
      textNode.nodeValue = leading + translated;
    }
  };
  // Cursor 3.14+ dönen ipucunun ekranda görünen kopyasını data-slot="current"
  // altında, ekran okuyucu kopyasını ise ayrı bir düğümde tutuyor. Metin düğümü
  // değişikliği React animasyonu tarafından geri alınabildiği için görünür kopyayı
  // veri niteliği + CSS ile sun; React'in iç durumuna dokunma.
  const ensureRotatingTipVisualStyle = () => {
    if (document.getElementById("cursor-tr-rotating-tip-visual-style")) return;
    const style = document.createElement("style");
    style.id = "cursor-tr-rotating-tip-visual-style";
    style.textContent =
      '[data-cursor-tr-tip-label]{font-size:0!important}' +
      '[data-cursor-tr-tip-label]>*{display:none!important}' +
      '[data-cursor-tr-tip-label]::after{' +
      'content:attr(data-cursor-tr-tip-label);font-size:14px!important;' +
      'line-height:18px!important;white-space:normal!important}';
    document.head.appendChild(style);
  };
  const markVisibleRotatingTip = () => {
    ensureRotatingTipVisualStyle();
    const items = document.querySelectorAll(
      '[data-component="glass-empty-state-rotating-tips"] [data-has-close-button] > div:first-child, ' +
      '[data-component="glass-empty-state-rotating-tips"], ' +
      '[data-slot="current"]'
    );
    for (const item of items) {
      const scope = item.closest('[data-component="glass-empty-state-rotating-tips"]');
      if (!scope && !item.matches('[data-component="glass-empty-state-rotating-tips"]')) continue;
      const value = (item.textContent || "").replace(/\s+/g, " ").trim();
      if (!value) continue;
      if (/find a prior conversation|across conversations/i.test(value)) {
        item.setAttribute("data-cursor-tr-tip-label", "Önceki bir konuşmayı bulmak için Cursor'a sorun veya konuşmalar genelinde özetleyin");
        continue;
      }
      const lookupValue = value.replace(/\bveya\b/gi, "or")
        .replace(/^Kancalar\b/gi, "Hooks")
        .replace(/^Yapılandır\b/gi, "Configure");
      let translated = translateValue(lookupValue);
      if (!translated && (value.includes("extend the agent loop") || value.includes("control and extend"))) {
        translated = "Kancalar, ajan döngüsünü kontrol edip genişletmenizi sağlar — başlamak için /create-hook kullanın";
      }
      // Bazı komut adlarının bağlacı (/cloud or /local -> /cloud veya /local)
      // daha önce çevrilmiş olabilir. Bu durumda bütün cümle eşleşmez; görünen
      // komut önekini koruyup İngilizce açıklama devamını bağımsız çevir.
      if (!translated && /^Kullan\s+\/[a-z-]+/i.test(value)) {
        const match = value.match(/\s(?=(?:to|for|so|lets|uses|reproduces)\b)/i);
        if (match && typeof match.index === "number") {
          const prefix = value.slice(0, match.index).replace(/^Kullan\s+/i, "");
          const suffix = value.slice(match.index + 1);
          const translatedSuffix = translateValue(suffix) ||
            translateValue(suffix.replace(/\bveya\b/gi, "or"));
          if (translatedSuffix) translated = prefix + " " + translatedSuffix;
        }
      }
      if (translated && translated !== value) {
        item.setAttribute("data-cursor-tr-tip-label", translated);
      } else if (!/find a prior conversation/i.test(value)) {
        item.removeAttribute("data-cursor-tr-tip-label");
      }
    }
  };
  // Model/çaba menüsü React'in seçim mantığında aynı metinleri anahtar olarak
  // kullanıyor. Text node'u değiştirmek seçime tıklanınca pencereyi
  // kilitleyebiliyor. Bu nedenle yalnızca görsel sunumu CSS pseudo-content ile
  // Türkçeleştir; React'in sahip olduğu özgün değerler aynen kalsın.
  const effortVisualLabels = new Map([
    ["Claude Fable 5.1 High", "Claude Fable 5.1 Yüksek"],
    ["Claude Fable 5.1 Medium", "Claude Fable 5.1 Orta"],
    ["Claude Fable 5.1 Low", "Claude Fable 5.1 Düşük"],
    ["Claude Fable 5.1 Max", "Claude Fable 5.1 Azami"],
    ["Claude Fable 5 High", "Claude Fable 5 Yüksek"],
    ["Claude Sonnet 4.6 High", "Claude Sonnet 4.6 Yüksek"],
    ["Claude Sonnet 4.5 High", "Claude Sonnet 4.5 Yüksek"],
    ["Cycle Effort", "Çaba Düzeyini Değiştir"],
    ["Cycle effort", "Çaba Düzeyini Değiştir"],
    ["Switch Model and Retry", "Model Değiştir ve Yeniden Dene"],
    ["Switch Model", "Model Değiştir"],
    ["Switch model", "Model Değiştir"],
    ["Kimi K3 Max", "Kimi K3 Azami"],
    ["Effort", "Çaba"], ["Low", "Düşük"], ["Medium", "Orta"],
    ["High", "Yüksek"], ["Fast", "Hızlı"], ["Context", "Bağlam"],
    ["Grok 4.7 High", "Grok 4.7 Yüksek"],
    ["Grok 4.7 Medium", "Grok 4.7 Orta"],
    ["Grok 4.7 Low", "Grok 4.7 Düşük"],
    ["Grok 4.7 Max", "Grok 4.7 Azami"],
    ["Grok 4.7 High Fast", "Grok 4.7 Yüksek Hızlı"],
    ["Grok 4.7 Fast", "Grok 4.7 Hızlı"],
    ["Grok 4.6 High", "Grok 4.6 Yüksek"],
    ["Grok 4.6 Medium", "Grok 4.6 Orta"],
    ["Grok 4.6 Low", "Grok 4.6 Düşük"],
    ["Grok 4.6 Max", "Grok 4.6 Azami"],
    ["Grok 4.6 High Fast", "Grok 4.6 Yüksek Hızlı"],
    ["Grok 4.5 High", "Grok 4.5 Yüksek"],
    ["Grok 4.5 Medium", "Grok 4.5 Orta"],
    ["Grok 4.5 Low", "Grok 4.5 Düşük"],
    ["Extra High", "Ekstra Yüksek"], ["Extra high", "Ekstra Yüksek"],
    ["High Fast", "Yüksek Hızlı"], ["Medium Fast", "Orta Hızlı"],
    ["Low Fast", "Düşük Hızlı"],
    ["Cursor Grok 4.6 High Fast", "Cursor Grok 4.6 Yüksek Hızlı"],
    ["Cursor Grok 4.6 Medium Fast", "Cursor Grok 4.6 Orta Hızlı"],
    ["Cursor Grok 4.6 Low Fast", "Cursor Grok 4.6 Düşük Hızlı"],
    ["Cursor Grok 4.5 High Fast", "Cursor Grok 4.5 Yüksek Hızlı"],
    ["Cursor Grok 4.5 Medium Fast", "Cursor Grok 4.5 Orta Hızlı"],
    ["Cursor Grok 4.5 Low Fast", "Cursor Grok 4.5 Düşük Hızlı"],
    ["Cursor Grok 4.6 (fast)", "Cursor Grok 4.6 (hızlı)"],
    ["+ High Fast", "+ Yüksek Hızlı"],
    ["+ Medium Fast", "+ Orta Hızlı"],
    ["+ Low Fast", "+ Düşük Hızlı"],
    ["No Thinking", "Düşünme Yok"],
    ["No thinking", "Düşünme Yok"],
    ["no thinking", "düşünme yok"],
    ["Claude Sonnet 4 No Thinking", "Claude Sonnet 4 Düşünme Yok"],
    ["Cloud", "Bulut"], ["Local", "Yerel"], ["Team Pool", "Ekip Havuzu"],
    // Otomasyon context menüsü
    ["Edit Details", "Ayrıntıları Düzenle"],
    ["Duplicate", "Çoğalt"],
    ["Copy as JSON", "JSON Olarak Kopyala"],
    // Silme onay diyaloğu
    ["This cannot be undone.", "Bu işlem geri alınamaz."],
    ["This cannot be undone", "Bu işlem geri alınamaz"],
    ["Uncommitted", "İşlenmemiş"],
    // Eklenti sayfası
    ["Done", "Tamam"],
    // Güvenlik izinleri
    ["Privacy & Data Handling", "Gizlilik ve Veri İşleme"],
    ["API & RPC Privileges", "API ve RPC Ayrıcalıkları"],
    ["Config & Template Injection", "Yapılandırma ve Şablon Enjeksiyonu"],
    ["Filesystem & Resource Access", "Dosya Sistemi ve Kaynak Erişimi"],
    // MCP eklenti yapılandırma modalı
    ["Requires connection", "Bağlantı gerekiyor"],
    ["General Security", "Genel Güvenlik"],
    ["AI & Agent Trust Boundaries", "YZ ve Ajan Güven Sınırları"],
    ["Logout", "Çıkış Yap"],
    ["Add Another Account", "Başka Hesap Ekle"],
    ["Allow all", "Tümüne İzin Ver"],
    ["Allow All", "Tümüne İzin Ver"],
    ["Reads", "Okumalar"],
    ["Writes", "Yazmalar"],
    // Zaman etiketi (otomasyon listesi)
    [" now", " şimdi"],
    ["just now", "az önce"],
    // One or more tools
    ["One or more tools require additional authentication to be used", "Bir veya daha fazla araç kullanım için ek kimlik doğrulama gerektiriyor"],
    // Dinamik kaynak sayısı
    ["1 source", "1 kaynak"],
    ["sources", "kaynak"],
    // Manage butonu
    ["Manage", "Yönet"],
    // ── GÖRSEL CHECKLIST ÖNCELİK A ──
    // Agents Window
    ["Ask questions", "Soru sorun"],
    ["Ask questions...", "Soru sorun..."],
    ["Build from a design", "Bir tasarımdan derleyin"],
    ["Derle from a design", "Bir tasarımdan derleyin"],
    ["build from a design", "bir tasarımdan derleyin"],
    ["derle from a design", "bir tasarımdan derleyin"],
    ["Turn a frame into working UI in this repo", "Bir çerçeveyi bu depoda çalışan bir kullanıcı arayüzüne dönüştürün"],
    ["Deploy my prototype", "Prototipimi dağıt"],
    ["Put it on a live link anyone can open", "Herkesin açabileceği canlı bir bağlantıda yayınlayın"],
    ["Upgrade for Automations, unlimited completions, MAX Mode, and more", "Otomasyonlar, sınırsız tamamlamalar, AZAMİ Mod ve daha fazlası için yükseltin"],
    // Explorer / Kaynak denetimi (boş durum)
    ["You have not yet opened a folder.", "Henüz bir klasör açmadınız."],
    ["You have not yet opened a folder", "Henüz bir klasör açmadınız"],
    ["You can clone a repository locally.", "Bir depoyu yerel olarak klonlayabilirsiniz."],
    ["You can clone a repository locally", "Bir depoyu yerel olarak klonlayabilirsiniz"],
    ["In order to use Git features, you can open a folder containing a Git repository or clone from a URL.", "Git özelliklerini kullanmak için Git deposu içeren bir klasör açabilir veya bir URL'den klonlayabilirsiniz."],
    ["In order to use Git features, you can open a folder containing a Git repository or clone from a URL", "Git özelliklerini kullanmak için Git deposu içeren bir klasör açabilir veya bir URL'den klonlayabilirsiniz"],
    ["To learn more about how to use Git and source control in VS Code read our docs.", "VS Code'da Git ve kaynak denetimini nasıl kullanacağınızı öğrenmek için belgelerimizi okuyun."],
    ["To learn more about how to use Git and source control in VS Code", "VS Code'da Git ve kaynak denetimini nasıl kullanacağınızı öğrenmek için"],
    ["read our docs", "belgelerimizi okuyun"],
    // Cursor Settings
    ["Upgrade to Pro", "Pro'ya Yükselt"],
    ["Entry-level plan with access to premium models, unlimited Tab completions, and more.", "Premium modellere erişim, sınırsız Sekme tamamlamaları ve daha fazlasını içeren başlangıç düzeyi planı."],
    ["Title Bar", "Başlık Çubuğu"],
    ["Show title bar in agent layout.", "Ajan yerleşiminde başlık çubuğunu göster."],
    ["Show title bar in agent layout", "Ajan yerleşiminde başlık çubuğunu göster"],
    ["Included Usage", "Dahil Edilen Kullanım"],
    ["Pro $20/ay", "Pro · 20 $/ay"],
    ["Pro $20/mo", "Pro · 20 $/ay"],
    ["$20/mo", "20 $/ay"],
    ["$20/ay", "20 $/ay"],
    // IDE Composer / upsell
    ["Upgrade to unlock more models", "Daha fazla modelin kilidini açmak için yükseltin"],
    ["More models are only available on paid plans.", "Daha fazla model yalnızca ücretli planlarda kullanılabilir."],
    ["Free Plan", "Ücretsiz Plan"],
    ["Free Plan · Yükselt", "Ücretsiz Plan · Yükselt"],
    // VS Code Settings başlıkları
    ["Files: Auto Save", "Dosyalar: Otomatik Kaydetme"],
    ["Editor: Font Size", "Düzenleyici: Yazı Tipi Boyutu"],
    ["Editor: Font Family", "Düzenleyici: Yazı Tipi Ailesi"],
    ["Editor: Tab Size", "Düzenleyici: Sekme Boyutu"],
    ["Editor: Cursor Style", "Düzenleyici: İmleç Stili"],
    ["Editor: Multi Cursor Modifier", "Düzenleyici: Çoklu İmleç Değiştiricisi"],
    ["Editor: Insert Spaces", "Düzenleyici: Boşluk Ekle"],
    ["Editor: Detect Indentation", "Düzenleyici: Girintiyi Algıla"],
    ["Editor: Word Wrap", "Düzenleyici: Sözcük Kaydırma"],
    ["Editor: Line Numbers", "Düzenleyici: Satır Numaraları"],
    ["Editor: Minimap", "Düzenleyici: Mini Harita"],
    // Komut paleti
    ["Görüntüle: Agents Window ajanına geç", "Görüntüle: Ajanlar Penceresine Geç"],
    ["Switch to Agents Window Agent", "Ajanlar Penceresine Geç"],
    ["Switch to Agents Window", "Ajanlar Penceresine Geç"],
    ["Add XHR/fetch Breakpoint", "XHR/fetch Kesme Noktası Ekle"],
    ["Cursor Deeplink: Debug: Trigger Arbitrary Deeplink", "Cursor Derin Bağlantı: Hata Ayıklama: İsteğe Bağlı Derin Bağlantıyı Tetikle"],
    ["Trigger Arbitrary Deeplink", "İsteğe Bağlı Derin Bağlantıyı Tetikle"],
    ["Cursor Settings: Agents", "Cursor Ayarları: Ajanlar"],
    ["Cursor Settings: Beta", "Cursor Ayarları: Beta"],
    ["Cursor Settings: Browser & Network", "Cursor Ayarları: Tarayıcı ve Ağ"],
    ["Cursor Settings: General", "Cursor Ayarları: Genel"],
    ["Cursor Settings: Models", "Cursor Ayarları: Modeller"],
    ["Cursor Settings: Features", "Cursor Ayarları: Özellikler"],
    ["Cursor Settings: Rules, Skills, Subagents", "Cursor Ayarları: Kurallar, Beceriler, Alt Ajanlar"],
    ["Cursor Settings: Cloud Agents", "Cursor Ayarları: Bulut Ajanları"],
    ["Cursor Settings: Git & PRs", "Cursor Ayarları: Git ve PR'lar"],
    ["Cursor Settings: Indexing", "Cursor Ayarları: Dizinleme"],
    ["Cursor Settings: Tab", "Cursor Ayarları: Sekme"],
    ["Cursor Settings: Docs", "Cursor Ayarları: Belgeler"]
  ]);
  const ensureEffortStyle = () => {
    if (document.getElementById("cursor-tr-effort-visual-style")) return;
    const style = document.createElement("style");
    style.id = "cursor-tr-effort-visual-style";
    style.textContent = '[data-cursor-tr-effort-label]{font-size:0!important;text-align:left!important}' +
      '[data-cursor-tr-effort-label]::after{content:attr(data-cursor-tr-effort-label);font-size:13px!important;order:-1;margin-right:auto;text-align:left!important}' +
      '[placeholder*="Search Remote Machines"],[placeholder*="Uzak Makinelerde Ara"]{text-align:left!important;direction:ltr!important}' +
      '[role="menuitem"]{text-align:left!important;justify-content:flex-start!important}' +
      '[role="menuitem"]>[data-radix-collection-item], [role="menuitem"] svg:last-child{margin-left:auto!important}' +
      '[data-cursor-tr-remote-label]{display:flex!important;align-items:center!important;gap:8px!important;padding-left:4px!important;text-align:left!important;justify-content:flex-start!important}' +
      '[data-cursor-tr-remote-label] svg{position:static!important;flex:0 0 auto!important}' +
      '[data-cursor-tr-remote-label] svg:last-of-type{margin-left:auto!important}';
    document.head.appendChild(style);
  };
  const markRemoteMachineLabels = () => {
    ensureEffortStyle();
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let textNode;
    while ((textNode = walker.nextNode())) {
      const key = textNode.nodeValue.replace(/\s+/g, " ").trim();
      if (!["Remote Machines", "Uzak Makineler"].includes(key)) continue;
      const parent = textNode.parentElement;
      const item = parent?.closest('[role="menuitem"], [role="menu"], [data-radix-menu-content]');
      if (item) item.setAttribute("data-cursor-tr-remote-label", "Uzak Makineler");
    }
  };
  const markEffortLabels = () => {
    ensureEffortStyle();
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let textNode;
    while ((textNode = walker.nextNode())) {
      const key = textNode.nodeValue.trim();
      if (!key) continue;
      let translated = effortVisualLabels.get(key);
      if (!translated) {
        if (["High", "Medium", "Low", "Max", "Extra High"].includes(key)) {
          const effortMap = {
            "High": "Yüksek",
            "Medium": "Orta",
            "Low": "Düşük",
            "Max": "Azami",
            "Extra High": "Ekstra Yüksek"
          };
          translated = effortMap[key];
        }
      }
      if (!translated) continue;
      const parent = textNode.parentElement;
      if (!parent || parent.closest(".monaco-editor, .xterm, textarea, pre")) continue;
      // Birleşik kapalı seçici her yerde güvenle işaretlenebilir. Tek sözcüklü
      // değerler ise yalnızca Effort/Model seçeneklerinin bulunduğu açılır
      // katmanda işaretlenir.
      let allowed = key.includes(" ");
      if (!allowed) {
        // Acik secici farkli Cursor surumlerinde Radix/menu/listbox
        // kapsayicilarindan biriyle olusturuluyor. Metni degistirmeden bu
        // katmanlarda gorunen etiketi isaretlemek guvenlidir.
        allowed = Boolean(parent.closest(
          '[role="menu"], [role="listbox"], [data-radix-menu-content], [data-radix-popper-content-wrapper]'
        ));
      }
      if (!allowed) {
        let scope = parent;
        for (let i = 0; scope && i < 16; i++, scope = scope.parentElement) {
          const content = scope.textContent || "";
          if (content.includes("Effort") && content.includes("Low") &&
              content.includes("Medium") && content.includes("High") &&
              content.includes("Model")) { allowed = true; break; }
        }
      }
      if (!allowed && ["Low", "Medium", "High", "Fast", "Context", "No Thinking", "No thinking"].includes(key)) {
        // Kapali secicide yalnizca secili deger gorunur. Mesaj kutusunun
        // icindeki dar dugmeyi hedefle; ayni kelimelerin editor veya ayarlar
        // ekranindaki kullanimlarina dokunma.
        const button = parent.closest('button, [role="button"]');
        if (button && (button.textContent || "").trim().startsWith(key)) {
          let composer = button.parentElement;
          for (let i = 0; composer && i < 8; i++, composer = composer.parentElement) {
            if (composer.querySelector('textarea, [contenteditable="true"]')) {
              const rect = button.getBoundingClientRect();
              if (rect.width < 180 && rect.height < 64) allowed = true;
              break;
            }
          }
        }
      }
      if (allowed && parent.getAttribute("data-cursor-tr-effort-label") !== translated) parent.setAttribute("data-cursor-tr-effort-label", translated);
    }
  };
  const start = () => {
    translate(document.body);
    translateRotatingTips();
        translateCommandTipFragments();
    markVisibleRotatingTip();
    markEffortLabels();
    markRemoteMachineLabels();
    new MutationObserver(records => {
      for (const record of records) {
        if (record.type === "attributes") {
          translate(record.target);
        }
        if (record.type === "characterData") {
          translate(record.target.parentElement);
          if (record.target.parentElement?.closest(".glass-empty-state-rotating-tips__text")) translateRotatingTips();
        }
        for (const node of record.addedNodes || []) {
          translate(node);
          if (node.parentElement?.closest(".glass-empty-state-rotating-tips__text")) translateRotatingTips();
        }
        translateCommandTipFragments();
        markVisibleRotatingTip();
        markEffortLabels();
        markRemoteMachineLabels();
      }
    }).observe(document.body, {
      subtree: true,
      childList: true,
      characterData: true,
      attributes: true,
      attributeFilter: attrs
    });
    // Cursor ipucu metnini bazen mevcut React dugumlerini yeniden kullanarak
    // degistiriyor. Dusuk maliyetli hedefli kontrol bu durumu da kapsar.
    setInterval(() => {
      translateRotatingTips();
            translateCommandTipFragments();
      markVisibleRotatingTip();
      markEffortLabels();
      markRemoteMachineLabels();
    }, 1500);
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, {once: true});
  else start();
})();
'''

if __name__ == '__main__':
    for fname in FILES:
        if not os.path.exists(fname):
            print(fname, 'yok, atlandi')
            continue
        original = io.open(fname, encoding='utf-8').read()
        marker_token = '/* ' + MARKER + ' */'
        # Onceki calismadan kalan katmani ayir. Aksi halde asagidaki statik
        # degisimler ceviri Map'inin Ingilizce anahtarlarini da Turkcelestirir
        # ve dinamik menuler bir sonraki calismada eslesmez.
        text = original
        marker_at = text.find(marker_token)
        if marker_at >= 0:
            text = text[:marker_at].rstrip()
        core_positions = [text.find('/* ' + marker + ' */') for marker in CORE_MARKERS]
        core_positions = [position for position in core_positions if position >= 0]
        if core_positions:
            core_at = min(core_positions)
            prefix, core_suffix = text[:core_at].rstrip(), text[core_at:]
            # Yeni Cursor surumleri alt ipucunu bazen metin dugumunde, bazen
            # kapsayici/altbilgi bolgesinde olusturuyor. Calisan cekirdek katmanin
            # hepsini ayni cumle olarak okuyabilmesi icin secicileri genislet.
            tip_selector = '.glass-empty-state-rotating-tips__text, .glass-empty-state-rotating-tips__content, .glass-empty-state-rotating-tips, [data-component="glass-empty-state-rotating-tips"], .agent-panel-empty-state-footer-region'
            for old_call, new_call in (
                ('element?.matches?.(".glass-empty-state-rotating-tips__text")', f'element?.matches?.("{tip_selector}")'),
                ('element?.closest?.(".glass-empty-state-rotating-tips__text")', f'element?.closest?.("{tip_selector}")'),
                ('querySelectorAll?.(".glass-empty-state-rotating-tips__text")', f'querySelectorAll?.("{tip_selector}")'),
                ('document.querySelectorAll(".glass-empty-state-rotating-tips__text")', f'document.querySelectorAll("{tip_selector}")'),
            ):
                core_suffix = core_suffix.replace(old_call, new_call)
            core_suffix = core_suffix.replace('["No repos", "Depo yok"]', '["No repos", "Depo Yok"]')
            core_suffix = core_suffix.replace('["No environments", "Ortam yok"]', '["No environments", "Ortam Yok"]')

            if 'find a prior conversation' not in core_suffix:
                core_suffix = core_suffix.replace(
                    'let translated = translations.get(key);',
                    'let translated = translations.get(key);\n    if (!translated && /(?:Ask|Search|Sor)\\s+Cursor to find a prior conversation/i.test(key)) translated = "Önceki bir konuşmayı bulmak için Cursor\\\'a sorun veya konuşmalar genelinde özetleyin";'
                )

            # Ekranda gorulen yeni beceri ipucu eski "Use /create-skill" kalibiyla
            # baslamiyor; hem tamamen Ingilizce hem de kismen cevrilmis bicimini yakala.
            if 'Agent skills help you customize Cursor for your workflows' not in core_suffix:
                core_suffix = core_suffix.replace(
                    'let translated = translations.get(key);',
                    'let translated = translations.get(key);\n    if (!translated && /^(?:Agent|Ajan) skills help you customize Cursor for your workflows/i.test(key)) translated = "Ajan becerileri Cursor\\\'u iş akışlarınıza göre özelleştirmenize yardımcı olur — başlamak için /create-skill kullanın";'
                )
            # Calistigi canli ekranda dogrulanan eski tip katmani, React'in
            # parcaladigi cumleyi genel "komutunu kullanin" metnine indiriyordu.
            # Tam cumleyi komuta gore burada uret; sonraki DOM katmanina baglanma.
            if 'Voice mode lets you dictate better prompts for your agents/i.test(key)' not in core_suffix:
                core_suffix = core_suffix.replace(
                    'if (!translated) {\n      const command = key.match(/(\\/[A-Za-z0-9_-]+)/)?.[1];',
                    'if (!translated && /^Voice mode lets you dictate better prompts for your agents/i.test(key)) translated = "Ses modu, ajanlarınız için daha iyi istemleri dikte etmenizi sağlar";\n    if (!translated) {\n      const command = key.match(/(\\/[A-Za-z0-9_-]+)/)?.[1];'
                )
            if '({"/review":' not in core_suffix:
                core_suffix = core_suffix.replace(
                    'translated = `${command} komutunu kullanın`;',
                    'translated = ({"/review":"/review ile değişikliklerinizi ajan destekli kod incelemesinden geçirin","/create-rule":"/create-rule ile ajan davranışını sistem düzeyi talimatlarla denetleyin","/create-skill":"/create-skill ile Cursor\'u iş akışlarınıza göre özelleştirin","/create-subagent":"/create-subagent ile uzman ajanlar kurun","/model":"/model ile göreviniz için en uygun modeli seçin","/multitask":"/multitask ile sıradaki mesajlarınızı paralel çalıştırın","/plan":"/plan ile Plan Modu kullanarak ajan yürütmesini iyileştirin","/debug":"/debug ile yeniden üretmesi zor hataları çözün","/split-to-prs":"/split-to-prs ile çalışmanızı küçük ve incelenebilir PR\'lara bölün","/automate":"/automate ile Cursor Otomasyonları oluşturun","/cloud":"/cloud ile ajanları uzaktan çalıştırın","/loop":"/loop ile bir istemi zamanlamaya göre çalıştırın","/shell":"/shell ile terminalde komut çalıştırın"}[command] || `${command} komutunu kullanın`);'
                )
        else:
            prefix, core_suffix = text.rstrip(), ''
        changed = 0
        for old, new in STATIC.items():
            count = prefix.count(old)
            if count:
                prefix = prefix.replace(old, new)
                changed += count
        text = prefix
        if core_suffix:
            text += '\n\n' + core_suffix.lstrip()
        text = text.rstrip() + OVERLAY
        if text != original:
            changed += 1
        io.open(fname, 'w', encoding='utf-8', newline='').write(text)
        print('%s degisim: %d' % (fname, changed))


