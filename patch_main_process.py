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
    ('label:r.label,enabled:!1})', 'label:r.label==="No Repo"?"Depo Yok":r.label==="Projects"?"Projeler":r.label,enabled:!1})'),

    # Harici Baglanti Diyalogu
    ('buttons:["Cancel","Open"],defaultId:0,cancelId:0,title:"Open External Link",message:"Do you want to open this link?",detail:`${e}\n\nThis will open in an external application.`',
     'buttons:["İptal","Aç"],defaultId:0,cancelId:0,title:"Harici Bağlantıyı Aç",message:"Bu bağlantıyı açmak istiyor musunuz?",detail:`${e}\n\nBu bağlantı harici bir uygulamada açılacak.`'),
]


MISSING_IPC_MARKER = '/* CURSOR_TR_MISSING_IPC_V1 */'

MISSING_IPC_BLOCK = r'''
/* CURSOR_TR_MISSING_IPC_V1 */
import { ipcMain as __cursorTrIpcMain, app as __cursorTrApp } from "electron";
import * as __cursorTrFs from "node:fs";
import * as __cursorTrPath from "node:path";
import * as __cursorTrOs from "node:os";
(() => {
  try {
    if (globalThis.__cursorTrMissingIpcBound) return;
    globalThis.__cursorTrMissingIpcBound = true;
    const repoDir = __cursorTrPath.join(__cursorTrOs.homedir(), "cursor-turkish-localization");
    const outFile = __cursorTrFs.existsSync(repoDir)
      ? __cursorTrPath.join(repoDir, "eksik-ekran-metinleri.json")
      : __cursorTrPath.join(__cursorTrApp.getPath("userData"), "cursor-tr-missing.json");
    let store = null;
    let timer = null;
    const ensureStore = () => {
      if (store) return store;
      store = {};
      try {
        if (__cursorTrFs.existsSync(outFile)) {
          const parsed = JSON.parse(__cursorTrFs.readFileSync(outFile, "utf8"));
          if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) store = parsed;
        }
      } catch {}
      return store;
    };
    const flush = () => {
      timer = null;
      try {
        if (!store) return;
        __cursorTrFs.writeFileSync(outFile, JSON.stringify(store, null, 2), "utf8");
      } catch {}
    };
    __cursorTrIpcMain.on("vscode:cursorTrMissing", (_ev, batch) => {
      try {
        if (!Array.isArray(batch) || batch.length === 0) return;
        const db = ensureStore();
        let keys = Object.keys(db).length;
        const now = new Date().toISOString();
        let dirty = false;
        for (const item of batch) {
          if (!item || typeof item.text !== "string") continue;
          const text = item.text.trim();
          if (text.length < 2 || text.length > 200) continue;
          const existing = db[text];
          if (existing) {
            existing.count = (existing.count || 1) + 1;
            existing.lastSeen = now;
            dirty = true;
          } else if (keys < 2000) {
            db[text] = {
              count: 1,
              firstSeen: now,
              lastSeen: now,
              kind: typeof item.kind === "string" ? item.kind : "text",
              tag: typeof item.tag === "string" ? item.tag : "",
            };
            keys += 1;
            dirty = true;
          }
        }
        if (dirty && !timer) {
          timer = setTimeout(flush, 3000);
          if (typeof timer.unref === "function") timer.unref();
        }
      } catch {}
    });
  } catch {}
})();
'''.lstrip('\n')


def patch_main(fname='main.js'):
    if not os.path.exists(fname):
        print(f'{fname} bulunamadi, atlaniyor.')
        return

    with io.open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    if MISSING_IPC_MARKER in content:
        content = content[:content.index(MISSING_IPC_MARKER)].rstrip()

    orig_len = len(content)
    total_reps = 0

    for old_s, new_s in MAIN_REPS:
        cnt = content.count(old_s)
        if cnt > 0:
            content = content.replace(old_s, new_s)
            total_reps += cnt
        else:
            print(f'  [BILGI] Kalip bulunamadi veya zaten uygulanmis: {old_s[:40]}...')

    content = content.rstrip() + '\n\n' + MISSING_IPC_BLOCK
    total_reps += 1

    with io.open(fname, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print(f'[{fname}] Toplam {total_reps} degisim uygulandi (eksik-ekran IPC dahil). (Boyut farki: {len(content) - orig_len} bayt)')


if __name__ == '__main__':
    patch_main('main.js')
