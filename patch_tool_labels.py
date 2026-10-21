# -*- coding: utf-8 -*-
"""Modelin yazisma ve arac cagrilarindaki durum etiketlerini (tool-action-labels.js,
ThinkingLine.js, step-group-display.js) guvenli ve Baslik Duzeni (Title Case)
standardinda Turkcelestirir.
"""
import io
import re

# tool-action-labels.js icindeki 76+ aracin Turkce karsiliklari
TOOL_ACTIONS_TR = {
    "shellToolCall": {"loading": "Çalıştırılıyor", "completed": "Çalıştırıldı", "error": "Çalıştır"},
    "deleteToolCall": {"loading": "Siliniyor", "completed": "Silindi", "error": "Sil"},
    "globToolCall": {"loading": "Dosyalar Aranıyor", "completed": "Dosyalar Arandı", "error": "Dosyaları Ara"},
    "grepToolCall": {"loading": "Metin Aranıyor", "completed": "Metin Arandı", "error": "Metin Ara"},
    "readToolCall": {"loading": "Okunuyor", "completed": "Okundu", "error": "Oku"},
    "updateTodosToolCall": {"loading": "Görevler Güncelleniyor", "completed": "Görevler Güncellendi", "error": "Görevleri Güncelle"},
    "readTodosToolCall": {"loading": "Görevler Okunuyor", "completed": "Görevler Okundu", "error": "Görevleri Oku"},
    "editToolCall": {"loading": "Düzenleniyor", "completed": "Düzenlendi", "error": "Düzenle"},
    "lsToolCall": {"loading": "Listeleniyor", "completed": "Listelendi", "error": "Listele"},
    "readLintsToolCall": {"loading": "Sorunlar Okunuyor", "completed": "Sorunlar Okundu", "error": "Sorunları Oku"},
    "mcpToolCall": {"loading": "Çalıştırılıyor", "completed": "Çalıştırıldı", "error": "Çalıştır"},
    "getMcpToolsToolCall": {"loading": "Araçlar Keşfediliyor", "completed": "Araçlar Keşfedildi", "error": "Araçları Keşfet"},
    "semSearchToolCall": {"loading": "Aranıyor", "completed": "Arandı", "error": "Ara"},
    "createPlanToolCall": {"loading": "Plan Hazırlanıyor", "completed": "Plan Hazırlandı", "error": "Plan Hazırla"},
    "webSearchToolCall": {"loading": "Web'de Aranıyor", "completed": "Web'de Arandı", "error": "Web'de Ara"},
    "xSearchToolCall": {"loading": "X'te Aranıyor", "completed": "X'te Arandı", "error": "X'te Ara"},
    "taskToolCall": {"loading": "Görev Yürütülüyor", "completed": "Görev Tamamlandı", "error": "Görevi Yürüt"},
    "getAgentStatusToolCall": {"loading": "Ajanlar Kontrol Ediliyor", "completed": "Ajanlar Kontrol Edildi", "error": "Ajanları Kontrol Et"},
    "sendToAgentToolCall": {"loading": "Ajana Mesaj Gönderiliyor", "completed": "Ajana Mesaj Gönderildi", "error": "Ajana Mesaj Gönder"},
    "readAgentTranscriptToolCall": {"loading": "Döküm Okunuyor", "completed": "Döküm Okundu", "error": "Dökümü Oku"},
    "createAgentToolCall": {"loading": "Ajan Oluşturuluyor", "completed": "Ajan Oluşturuldu", "error": "Ajan Oluştur"},
    "createProjectToolCall": {"loading": "Proje Oluşturuluyor", "completed": "Proje Oluşturuldu", "error": "Proje Oluştur"},
    "stopAgentToolCall": {"loading": "Ajan Durduruluyor", "completed": "Ajan Durduruldu", "error": "Ajanı Durdur"},
    "listTrackedTasksToolCall": {"loading": "Görevler Listeleniyor", "completed": "Görevler Listelendi", "error": "Görevleri Listele"},
    "createTrackedTasksToolCall": {"loading": "Görevler Oluşturuluyor", "completed": "Görevler Oluşturuldu", "error": "Görevleri Oluştur"},
    "updateTrackedTasksToolCall": {"loading": "Görevler Güncelleniyor", "completed": "Görevler Güncellendi", "error": "Görevleri Güncelle"},
    "deleteTrackedTasksToolCall": {"loading": "Görevler Siliniyor", "completed": "Görevler Silindi", "error": "Görevleri Sil"},
    "updateTrackedTaskStatusesToolCall": {"loading": "Görev Durumları Güncelleniyor", "completed": "Görev Durumları Güncellendi", "error": "Görev Durumlarını Güncelle"},
    "listMcpResourcesToolCall": {"loading": "Kaynaklar Listeleniyor", "completed": "Kaynaklar Listelendi", "error": "Kaynakları Listele"},
    "readMcpResourceToolCall": {"loading": "Kaynak Okunuyor", "completed": "Kaynak Okundu", "error": "Kaynağı Oku"},
    "applyAgentDiffToolCall": {"loading": "Fark Uygulanıyor", "completed": "Fark Uygulandı", "error": "Farkı Uygula"},
    "askQuestionToolCall": {"loading": "Sorular Soruluyor", "completed": "Sorular Soruldu", "error": "Soru Sor"},
    "blameByFilePathToolCall": {"loading": "Git Blame İnceleniyor", "completed": "Git Blame İncelendi", "error": "Git Blame İncele"},
    "awaitToolCall": {"loading": "Bekleniyor", "completed": "Beklendi", "error": "Bekle"},
    "fetchToolCall": {"loading": "Alınıyor", "completed": "Alındı", "error": "Al"},
    "switchModeToolCall": {"loading": "Mod Değiştiriliyor", "completed": "Mod Değiştirildi", "error": "Modu Değiştir"},
    "generateImageToolCall": {"loading": "Görsel Üretiliyor", "completed": "Görsel Üretildi", "error": "Görsel Üret"},
    "generateVideoToolCall": {"loading": "Video Üretiliyor", "completed": "Video Üretildi", "error": "Video Üret"},
    "recordScreenToolCall": {"loading": "Ekran Kaydediliyor", "completed": "Ekran Kaydedildi", "error": "Ekranı Kaydet"},
    "computerUseToolCall": {"loading": "Bilgisayar Kullanılıyor", "completed": "Bilgisayar Kullanıldı", "error": "Bilgisayarı Kullan"},
    "writeShellStdinToolCall": {"loading": "Kabuğa Yazılıyor", "completed": "Kabuğa Yazıldı", "error": "Kabuğa Yaz"},
    "reflectToolCall": {"loading": "Değerlendiriliyor", "completed": "Değerlendirildi", "error": "Değerlendir"},
    "setupVmEnvironmentToolCall": {"loading": "Sanal Makine Kuruluyor", "completed": "Sanal Makine Kuruldu", "error": "Sanal Makine Kur"},
    "replaceEnvToolCall": {"loading": "Ortam Değiştiriliyor", "completed": "Ortam Değiştirildi", "error": "Ortamı Değiştir"},
    "searchConversationsToolCall": {"loading": "Sohbetler Aranıyor", "completed": "Sohbetler Arandı", "error": "Sohbetlerde Ara"},
    "createGoalToolCall": {"loading": "Hedef Oluşturuluyor", "completed": "Hedef Oluşturuldu", "error": "Hedef Oluştur"},
    "updateGoalToolCall": {"loading": "Hedef Güncelleniyor", "completed": "Hedef Güncellendi", "error": "Hedef Güncelle"},
    "truncatedToolCall": {"loading": "İşleniyor", "completed": "İşlendi", "error": "İşle"},
    "startGrindExecutionToolCall": {"loading": "Yürütülüyor", "completed": "Yürütüldü", "error": "Yürüt"},
    "startGrindPlanningToolCall": {"loading": "Planlanıyor", "completed": "Planlandı", "error": "Planla"},
    "webFetchToolCall": {"loading": "Sayfa Alınıyor", "completed": "Sayfa Alındı", "error": "Sayfayı Al"},
    "reportBugfixResultsToolCall": {"loading": "Sonuçlar Bildiriliyor", "completed": "Sonuçlar Bildirildi", "error": "Sonuçları Bildir"},
    "aiAttributionToolCall": {"loading": "Cursor Blame'den Öğreniliyor", "completed": "Cursor Blame'den Öğrenildi", "error": "Cursor Blame'den Öğren"},
    "communicateUpdateToolCall": {"loading": "İlerleme Güncelleniyor", "completed": "İlerleme Güncellendi", "error": "İlerlemeyi Güncelle"},
    "prManagementToolCall": {"loading": "PR Yönetiliyor", "completed": "PR Yönetildi", "error": "PR Yönet"},
    "editPrLabelsToolCall": {"loading": "PR Etiketleri Düzenleniyor", "completed": "PR Etiketleri Düzenlendi", "error": "PR Etiketlerini Düzenle"},
    "fetchCloudAgentDataToolCall": {"loading": "Bulut Ajanı Verisi Alınıyor", "completed": "Bulut Ajanı Verisi Alındı", "error": "Bulut Ajanı Verisini Al"},
    "mcpAuthToolCall": {"loading": "MCP Sunucusu Doğrulanıyor", "completed": "MCP Sunucusu Doğrulandı", "error": "MCP Kimlik Doğrulaması"},
    "connectScmToolCall": {"loading": "GitHub'a Bağlanılıyor", "completed": "GitHub'a Bağlandı", "error": "GitHub'a Bağlan"},
    "reportBugToolCall": {"loading": "Hata Bildiriliyor", "completed": "Hata Bildirildi", "error": "Hata Bildir"},
    "sendFinalSummaryToolCall": {"loading": "Son Özet Kaydediliyor", "completed": "Son Özet Kaydedildi", "error": "Son Özeti Kaydet"},
    "sendMessageToolCall": {"loading": "Mesaj Gönderiliyor", "completed": "Mesaj Gönderildi", "error": "Mesaj Gönder"},
    "sendToUserToolCall": {"loading": "Mesaj Gönderiliyor", "completed": "Mesaj Gönderildi", "error": "Mesaj Gönder"},
    "setActiveBranchToolCall": {"loading": "Üstveri Güncelleniyor", "completed": "Üstveri Güncellendi", "error": "Üstveriyi Güncelle"},
    "updateOriginPrCodeTourToolCall": {"loading": "Kod Turu Güncelleniyor", "completed": "Kod Turu Güncellendi", "error": "Kod Turunu Güncelle"},
    "getOriginPrCodeTourToolCall": {"loading": "Kod Turu Okunuyor", "completed": "Kod Turu Okundu", "error": "Kod Turunu Oku"},
    "writeCanvasToolCall": {"loading": "Canvas'a Yazılıyor", "completed": "Canvas'a Yazıldı", "error": "Canvas'a Yaz"},
    "readCanvasToolCall": {"loading": "Canvas Okunuyor", "completed": "Canvas Okundu", "error": "Canvas'ı Oku"},
    "recordCiInvestigationFindingsToolCall": {"loading": "CI Bulguları Kaydediliyor", "completed": "CI Bulguları Kaydedildi", "error": "CI Bulgularını Kaydet"},
    "piReadToolCall": {"loading": "Okunuyor", "completed": "Okundu", "error": "Oku"},
    "piBashToolCall": {"loading": "Çalıştırılıyor", "completed": "Çalıştırıldı", "error": "Çalıştır"},
    "piEditToolCall": {"loading": "Düzenleniyor", "completed": "Düzenlendi", "error": "Düzenle"},
    "piWriteToolCall": {"loading": "Yazılıyor", "completed": "Yazıldı", "error": "Yaz"},
    "piGrepToolCall": {"loading": "Metin Aranıyor", "completed": "Metin Arandı", "error": "Metin Ara"},
    "piFindToolCall": {"loading": "Dosyalar Aranıyor", "completed": "Dosyalar Arandı", "error": "Dosyaları Ara"},
    "piLsToolCall": {"loading": "Listeleniyor", "completed": "Listelendi", "error": "Listele"},
}

CREATE_FILE_TR = {"loading": "Oluşturuluyor", "completed": "Oluşturuldu", "error": "Oluştur"}

EXTRA_REPS = [
    # Dusunme ve simule dusunme etiketleri
    ('loadingAction:"Thinking",completedAction:u', 'loadingAction:"Düşünülüyor",completedAction:u'),
    ('action:"Thinking",expandable:', 'action:"Düşünülüyor",expandable:'),
    ('r=n??"Planning next moves"', 'r=n??"Sonraki Adımlar Planlanıyor"'),
    ('="Planning next moves",', '="Sonraki Adımlar Planlanıyor",'),
    ('="Wrapping up"', '="Toparlanıyor"'),
    ('h=v?Z:"Thought"', 'h=v?Z:"Düşündü"'),
    ('d=f?K:"Thought"', 'd=f?K:"Düşündü"'),
    ('u=l?o:"Thought"', 'u=l?o:"Düşündü"'),
    ('u=c?o:"Thought"', 'u=c?o:"Düşündü"'),
    # Diger durum etiketleri
    ('loadingAction:"Generating",completedAction:"Generated"', 'loadingAction:"Üretiliyor",completedAction:"Üretildi"'),
    ('loadingAction:"Deleting",completedAction:"Delete"', 'loadingAction:"Siliniyor",completedAction:"Sil"'),
    ('{action:"Wait skipped",details:""}', '{action:"Bekleme Atlandı",details:""}'),
    ('{action:"Asking questions",details:"",loading:!0}', '{action:"Sorular Soruluyor",details:"",loading:!0}'),
    ('{action:"Updating",details:"to-do list"}', '{action:"Güncelleniyor",details:"görev listesi"}'),
    ('{action:"Cleared",details:"to-do list"}', '{action:"Temizlendi",details:"görev listesi"}'),
    ('{action:"Checked",details:"to-do list"}', '{action:"Kontrol Edildi",details:"görev listesi"}'),
    ('completedAction:"Monitored",completedDetails:', 'completedAction:"İzlendi",completedDetails:'),
]


def build_tool_dict_str(var_name):
    items = []
    for k, v in TOOL_ACTIONS_TR.items():
        items.append(f'{k}:{{loading:"{v["loading"]}",completed:"{v["completed"]}",error:"{v["error"]}"}}')
    return f'{var_name}={{{",".join(items)}}}'


def build_create_dict_str(var_name):
    return f'{var_name}={{loading:"{CREATE_FILE_TR["loading"]}",completed:"{CREATE_FILE_TR["completed"]}",error:"{CREATE_FILE_TR["error"]}"}}'


def patch_file(fname):
    with io.open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_len = len(content)
    total_reps = 0

    # 1. tool-action-labels.js icindeki ana nesneyi degistir (jenerik regex: her Cursor surumunde calisir)
    mod_idx = content.find('tool-action-labels.js')
    if mod_idx != -1:
        m = re.search(r'([a-zA-Z0-9_$]+=\{shellToolCall:\{.*?\}\}),([a-zA-Z0-9_$]+=\{loading:".*?"\})', content[mod_idx:mod_idx+10000])
        if m:
            old_tool_dict, old_create_dict = m.group(1), m.group(2)
            tool_var = old_tool_dict.split('=', 1)[0]
            create_var = old_create_dict.split('=', 1)[0]

            new_tool_dict = build_tool_dict_str(tool_var)
            new_create_dict = build_create_dict_str(create_var)

            content = content[:mod_idx] + content[mod_idx:].replace(old_tool_dict, new_tool_dict, 1).replace(old_create_dict, new_create_dict, 1)
            total_reps += 2
            print(f'[{fname}] tool-action-labels ({tool_var}, {create_var}) basariyla guncellendi.')
        else:
            print(f'[{fname}] UYARI: tool-action-labels regex eslesmesi bulunamadi.')

    # 2. Ek durum ve dusunme etiketleri
    for old_s, new_s in EXTRA_REPS:
        cnt = content.count(old_s)
        if cnt > 0:
            content = content.replace(old_s, new_s)
            total_reps += cnt

    with io.open(fname, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print(f'[{fname}] Toplam {total_reps} degisim uygulandi. (Boyut farki: {len(content) - orig_len} bayt)')


if __name__ == '__main__':
    for f in ['workbench.desktop.main.js', 'workbench.glass.main.js']:
        try:
            patch_file(f)
        except Exception as e:
            print(f'Hata ({f}):', e)
