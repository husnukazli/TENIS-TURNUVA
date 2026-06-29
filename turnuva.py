import pandas as pd

def turnuva_siralamasi_hesapla(skor_dosyasi):
    # 1. Veriyi Oku
    # CSV dosyasını okuyoruz (Türkçe karakterler için encoding eklenebilir, gerekirse 'utf-8-sig' veya 'cp1254' yapın)
    df = pd.read_csv(skor_dosyasi)
    
    # Sadece oynanmış (skoru girilmiş) maçları filtreleyelim (Takım isimleri boş olmayanlar)
    df = df.dropna(subset=['Takım 1', 'Takım 2'])

    # 2. Takım 1 ve Takım 2 İstatistiklerini Ayırma ve Standartlaştırma
    # Takım 1 için istatistikler
    t1_stats = df[['Grup', 'Takım 1', 'T1 Kazanılan Maç', 'T2 Kazanılan Maç', 
                   'T1 Kazanılan Set', 'T2 Kazanılan Set', 'T1 Kazanılan Oyun', 'T2 Kazanılan Oyun', 'Tie Kazananı (Galibiyet)']].copy()
    t1_stats.columns = ['Grup', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun', 'Galibiyet']
    t1_stats['Galibiyet'] = (t1_stats['Galibiyet'] == t1_stats['Takım Adı']).astype(int)

    # Takım 2 için istatistikler
    t2_stats = df[['Grup', 'Takım 2', 'T2 Kazanılan Maç', 'T1 Kazanılan Maç', 
                   'T2 Kazanılan Set', 'T1 Kazanılan Set', 'T2 Kazanılan Oyun', 'T1 Kazanılan Oyun', 'Tie Kazananı (Galibiyet)']].copy()
    t2_stats.columns = ['Grup', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun', 'Galibiyet']
    t2_stats['Galibiyet'] = (t2_stats['Galibiyet'] == t2_stats['Takım Adı']).astype(int)

    # İki veri setini alt alta birleştirme
    all_stats = pd.concat([t1_stats, t2_stats], ignore_index=True)

    # 3. Takımlara Göre Verileri Toplama
    # Her takımın grup bazındaki toplam istatistiklerini alıyoruz
    siralama = all_stats.groupby(['Grup', 'Takım Adı']).sum().reset_index()

    # 4. Averaj Hesaplamaları
    siralama['Maç Averajı'] = siralama['Aldığı Maç'] - siralama['Verdiği Maç']
    siralama['Set Averajı'] = siralama['Aldığı Set'] - siralama['Verdiği Set']
    siralama['Oyun Averajı'] = siralama['Aldığı Oyun'] - siralama['Verdiği Oyun']

    # 5. Sıralama Kriterlerini Uygulama
    # Sıralama önceliği: Galibiyet > Maç Averajı > Set Averajı > Oyun Averajı
    siralama = siralama.sort_values(
        by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'], 
        ascending=[True, False, False, False, False]
    )

    # Sütunları düzenleme (Excel'deki formata uyumlu hale getirme)
    siralama = siralama[['Grup', 'Galibiyet', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Maç Averajı', 
                         'Aldığı Set', 'Verdiği Set', 'Set Averajı', 'Aldığı Oyun', 'Verdiği Oyun', 'Oyun Averajı']]
    
    return siralama

# Fonksiyonu çalıştırma ve sonucu dışa aktarma
dosya_adi = "Turnuva_Dinamik_Formullu.xlsx - Skor Giriş Ekranı.csv"
try:
    sonuc_df = turnuva_siralamasi_hesapla(dosya_adi)
    print(sonuc_df.head(10)) # İlk 10 satırı yazdır
    
    # Sonucu yeni bir CSV olarak kaydetmek istersen:
    # sonuc_df.to_csv("Yeni_Siralama.csv", index=False)
    print("\nSıralama başarıyla hesaplandı!")
except FileNotFoundError:
    print(f"Hata: '{dosya_adi}' dosyası bulunamadı. Lütfen dosya adını ve yolunu kontrol et.")
