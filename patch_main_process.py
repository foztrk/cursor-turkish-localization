# -*- coding: utf-8 -*-
"""Electron Main Process (out/main.js) icerisindeki Windows Sistem Tepsisi (Tray Menu)
ve ana surec diyaloglarini Turkcelestirir.
"""
import io
import os
import re

MAIN_REPS = [
    # Sistem Tepsisi (Tray Menu)
    ('label:"Clear All Notifications"', 'label:"Tüm Bildirimleri Temizle"'),
    ('label:"Open Cursor"', 'label:"Cursor\'ı Aç"'),
    ('label:"Settings",click:', 'label:"Ayarlar",click:'),
    ('label:"Quit",click:', 'label:"Çıkış",click:'),
    ('label:"No recent agents"', 'label:"Son Kullanılan Ajan Yok"'),
    ('label:"Log In",click:', 'label:"Giriş Yap",click:'),
    ('label:"Sign Up",click:', 'label:"Kaydol",click:'),
    ('label:"Unread",enabled:!1', 'label:"Okunmamış",enabled:!1'),
    ('return`${e} more unread`', 'return`${e} okunmamış daha`'),
    ('newComposerActionLabel??"New Agent"', 'newComposerActionLabel??"Yeni Ajan"'),
    ('this.createComposerMenuItem(s,`Agent ${i+1}`)', 'this.createComposerMenuItem(s,`Ajan ${i+1}`)'),
    ('r.name||`Agent ${s+1}`', 'r.name||`Ajan ${s+1}`'),

    # Harici Baglanti Diyalogu
    ('buttons:["Cancel","Open"],defaultId:0,cancelId:0,title:"Open External Link",message:"Do you want to open this link?",detail:`${e}\n\nThis will open in an external application.`',
     'buttons:["İptal","Aç"],defaultId:0,cancelId:0,title:"Harici Bağlantıyı Aç",message:"Bu bağlantıyı açmak istiyor musunuz?",detail:`${e}\n\nBu bağlantı harici bir uygulamada açılacak.`'),
]


def patch_main(fname='main.js'):
    if not os.path.exists(fname):
        print(f'{fname} bulunamadi, atlaniyor.')
        return

    with io.open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_len = len(content)
    total_reps = 0

    for old_s, new_s in MAIN_REPS:
        cnt = content.count(old_s)
        if cnt > 0:
            content = content.replace(old_s, new_s)
            total_reps += cnt
        else:
            print(f'  [BILGI] Kalip bulunamadi veya zaten uygulanmis: {old_s[:40]}...')

    with io.open(fname, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print(f'[{fname}] Toplam {total_reps} degisim uygulandi. (Boyut farki: {len(content) - orig_len} bayt)')


if __name__ == '__main__':
    patch_main('main.js')
