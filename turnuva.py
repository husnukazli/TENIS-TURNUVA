import streamlit as st
import pandas as pd

# Sayfa başlığı ve geniş ekran düzeni
st.set_page_config(page_title="Turnuva Sistemi", layout="wide")
st.title("🎾 Dinamik Turnuva Yönetim Sistemi")

# Sekmeleri (Tab) oluşturuyoruz
sekme_veri_girisi, sekme_siralamalar = st.tabs(["✍️ Skor Giriş Ekranı", "🏆 Grup Sıralamaları"])

# Sistemin boş kalmaması için varsayılan bir şablon oluşturuyoruz
# (Kullanıcı bu verileri web üzerinden silip kendi verilerini yazabilir)
if 'skor_verisi' not in st.session_state:
    st.session_state.skor_verisi = pd.DataFrame({
        "Grup": ["ERKEK A GRUBU", "KADIN B GRUBU"],
        "Gün": ["1. Gün", "2. Gün"],
        "Eşleşme": ["1 ve 4", "2 ve 4"],
        "Branş": ["1. Tekler", "1. Tekler"],
        "Takım 1": ["ATAK PRO SPOR KULÜBÜ", "ORTADOĞU TEKNİK ÜNİVERSİTESİ"],
        "Takım 2": ["NEW GEN SPOR KULÜBÜ", "İNCEK TENİS SPOR KULÜBÜ"],
        "T1 Kazanılan Maç": [1, 1],
        "T2 Kazanılan Maç": [0, 0],
        "T1 Kazanılan Set": [2, 2],
        "T2 Kazanılan Set": [0, 0],
        "T1 Kazanılan Oyun": [12, 12],
        "T2 Kazanılan Oyun": [4, 0],
        "Tie Kazananı (Galibiyet)": ["ATAK PRO SPOR KULÜBÜ", "ORTADOĞU TEKNİK ÜNİVERSİTESİ"]
    })

# --- 1. SEKME: DİNAMİK VERİ GİRİŞİ ---
with sekme_veri_girisi:
    st.subheader("Skor ve Eşleşme Giriş Tablosu")
    st.info("💡 Tablodaki hücrelere çift tıklayarak verileri değiştirebilirsiniz. Yeni maç eklemek için tablonun en altındaki boş satırı kullanın.")
    
    # st.data_editor ile Excel benzeri dinamik tablo oluşturuyoruz
    guncel_veri = st.data_editor(
        st.session_state.skor_verisi, 
        num_rows="dynamic", # Yeni satır eklemeye izin ver
        use_container_width=True,
        height=400
    )
    
    # Kullanıcının girdiği güncel veriyi sisteme kaydediyoruz
    st.session_state.skor_verisi = guncel_veri

    # İstenirse tüm girişleri bilgisayara indirme butonu
    st.download_button(
        label="Skor Girişlerini Bilgisayara İndir (CSV)",
        data=guncel_veri.to_csv(index=False).encode('utf-8'),
        file_name='Skor_Girisleri.csv',
        mime='text/csv',
    )


# --- 2. SEKME: GRUP SIRALAMALARI ---
with sekme_siralamalar:
    st.subheader("Güncel Grup Sıralamaları")
    
    # Veri girişindeki dataframe'i alıp hesaplama yapıyoruz
    df = guncel_veri.copy()
    
    # Boş girilmiş satırları temizle
    df = df.dropna(subset=['Takım 1', 'Takım 2'])

    if df.empty:
        st.warning("Henüz hesaplanacak bir veri yok. Lütfen 'Skor Giriş Ekranı' sekmesinden veri giriniz.")
    else:
        try:
            # Sütunların doğru formatta (sayı) olduğundan emin olalım
            sayisal_sutunlar = ['T1 Kazanılan Maç', 'T2 Kazanılan Maç', 'T1 Kazanılan Set', 'T2 Kazanılan Set', 'T1 Kazanılan Oyun', 'T2 Kazanılan Oyun']
            for col in sayisal_sutunlar:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

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

            # Birleştir, Topla ve Averajları Hesapla
            all_stats = pd.concat([t1_stats, t2_stats], ignore_index=True)
            siralama = all_stats.groupby(['Grup', 'Takım Adı']).sum().reset_index()

            siralama['Maç Averajı'] = siralama['Aldığı Maç'] - siralama['Verdiği Maç']
            siralama['Set Averajı'] = siralama['Aldığı Set'] - siralama['Verdiği Set']
            siralama['Oyun Averajı'] = siralama['Aldığı Oyun'] - siralama['Verdiği Oyun']

            siralama = siralama.sort_values(
                by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'], 
                ascending=[True, False, False, False, False]
            )
            
            siralama = siralama[['Grup', 'Galibiyet', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Maç Averajı', 
                                 'Aldığı Set', 'Verdiği Set', 'Set Averajı', 'Aldığı Oyun', 'Verdiği Oyun', 'Oyun Averajı']]

            # Bütün grupları tek bir karmaşık tablo yapmak yerine, gruplara ayırarak gösterelim
            gruplar = siralama['Grup'].unique()
            
            for grup_adi in gruplar:
                st.markdown(f"### 🏆 {grup_adi}")
                grup_verisi = siralama[siralama['Grup'] == grup_adi].drop(columns=['Grup']).reset_index(drop=True)
                # İndeksleri 1'den başlatarak sırayı göster
                grup_verisi.index = grup_verisi.index + 1
                st.dataframe(grup_verisi, use_container_width=True)
                st.markdown("---")

        except Exception as e:
            st.error(f"Sıralama hesaplanırken bir sorun oluştu. Lütfen Skor Giriş tablosunda sayı girilmesi gereken yerlere harf yazmadığınızdan emin olun. Hata: {e}")
