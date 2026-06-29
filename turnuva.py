import streamlit as st
import pandas as pd
import os

# Sayfa başlığı
st.set_page_config(page_title="Turnuva Sıralaması", layout="wide")
st.title("🎾 Turnuva Sıralama Sistemi")

# Okunacak dosyanın tam adını buraya yazıyoruz
DOSYA_ADI = "Turnuva_Dinamik_Formullu.xlsx - Skor Giriş Ekranı.csv"

def turnuva_siralamasi_hesapla(skor_dosyasi):
    df = pd.read_csv(skor_dosyasi)
    df = df.dropna(subset=['Takım 1', 'Takım 2'])

    # Takım 1 İstatistikleri
    t1_stats = df[['Grup', 'Takım 1', 'T1 Kazanılan Maç', 'T2 Kazanılan Maç', 
                   'T1 Kazanılan Set', 'T2 Kazanılan Set', 'T1 Kazanılan Oyun', 'T2 Kazanılan Oyun', 'Tie Kazananı (Galibiyet)']].copy()
    t1_stats.columns = ['Grup', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun', 'Galibiyet']
    t1_stats['Galibiyet'] = (t1_stats['Galibiyet'] == t1_stats['Takım Adı']).astype(int)

    # Takım 2 İstatistikleri
    t2_stats = df[['Grup', 'Takım 2', 'T2 Kazanılan Maç', 'T1 Kazanılan Maç', 
                   'T2 Kazanılan Set', 'T1 Kazanılan Set', 'T2 Kazanılan Oyun', 'T1 Kazanılan Oyun', 'Tie Kazananı (Galibiyet)']].copy()
    t2_stats.columns = ['Grup', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun', 'Galibiyet']
    t2_stats['Galibiyet'] = (t2_stats['Galibiyet'] == t2_stats['Takım Adı']).astype(int)

    # Birleştir ve Topla
    all_stats = pd.concat([t1_stats, t2_stats], ignore_index=True)
    siralama = all_stats.groupby(['Grup', 'Takım Adı']).sum().reset_index()

    # Averajlar
    siralama['Maç Averajı'] = siralama['Aldığı Maç'] - siralama['Verdiği Maç']
    siralama['Set Averajı'] = siralama['Aldığı Set'] - siralama['Verdiği Set']
    siralama['Oyun Averajı'] = siralama['Aldığı Oyun'] - siralama['Verdiği Oyun']

    # Sıralama
    siralama = siralama.sort_values(
        by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'], 
        ascending=[True, False, False, False, False]
    )
    
    siralama = siralama[['Grup', 'Galibiyet', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Maç Averajı', 
                         'Aldığı Set', 'Verdiği Set', 'Set Averajı', 'Aldığı Oyun', 'Verdiği Oyun', 'Oyun Averajı']]
    return siralama


# Web Arayüzü: Dosyayı otomatik okuma
if os.path.exists(DOSYA_ADI):
    try:
        sonuc_df = turnuva_siralamasi_hesapla(DOSYA_ADI)
        st.success("Veriler arka plandan başarıyla çekildi ve sıralama oluşturuldu!")
        
        # Sonucu ekranda tablo olarak göster
        st.dataframe(sonuc_df, use_container_width=True)
        
        # Sonucu indirme butonu
        csv_veri = sonuc_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Sıralamayı İndir (CSV)",
            data=csv_veri,
            file_name='Guncel_Siralama.csv',
            mime='text/csv',
        )
    except Exception as e:
        st.error(f"Dosya okunurken bir hata oluştu. İçeriği kontrol edin. Hata detayı: {e}")
else:
    st.error(f"Hata: '{DOSYA_ADI}' dosyası GitHub'da bulunamadı. Lütfen dosyanın GitHub'da kodunuzla aynı yerde olduğundan ve adının birebir aynı olduğundan emin olun.")
