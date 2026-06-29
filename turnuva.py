import streamlit as st
import pandas as pd

st.set_page_config(page_title="Turnuva Yönetimi", layout="wide")
st.title("🎾 Profesyonel Turnuva Yönetim Sistemi")

# --- 1. VERİ YÜKLEME (GERİ YÜKLEME BUTONU) ---
with st.sidebar:
    st.header("Veri Yönetimi")
    uploaded_file = st.file_uploader("Kayıtlı CSV Dosyasını Geri Yükle", type="csv")
    if uploaded_file is not None:
        st.session_state.skor_tablosu = pd.read_csv(uploaded_file)
        st.success("Dosya başarıyla yüklendi!")

# --- 2. HAFIZA KURULUMU ---
if 'skor_tablosu' not in st.session_state:
    st.session_state.skor_tablosu = pd.DataFrame(columns=[
        "Grup", "Gün", "Eşleşme", "Branş", "Takım 1", "Takım 2", 
        "T1 Maç", "T2 Maç", "T1 Set", "T2 Set", "T1 Oyun", "T2 Oyun"
    ])

# --- 3. SEKME YAPISI ---
tab1, tab2, tab3 = st.tabs(["✍️ Skor Giriş Ekranı", "🏆 Grup Sıralamaları", "💾 Kaydet"])

with tab1:
    st.subheader("Maç Skorlarını Girin")
    st.session_state.skor_tablosu = st.data_editor(st.session_state.skor_tablosu, num_rows="dynamic", use_container_width=True)

with tab2:
    st.subheader("Otomatik Puan Durumu")
    if not st.session_state.skor_tablosu.empty:
        df = st.session_state.skor_tablosu.copy()
        
        # --- EŞLEŞME (SERİ) BAZLI GALİBİYET HESABI ---
        # Aynı grupta, aynı gün, aynı eşleşme kodu olan maçları grupla
        seriler = df.groupby(['Grup', 'Gün', 'Eşleşme', 'Takım 1', 'Takım 2']).agg({
            'T1 Maç': 'sum', 'T2 Maç': 'sum',
            'T1 Set': 'sum', 'T2 Set': 'sum',
            'T1 Oyun': 'sum', 'T2 Oyun': 'sum'
        }).reset_index()
        
        # Serinin kazananını belirle (2 veya 3 maç kazanan)
        seriler['T1_Galibiyet'] = (seriler['T1 Maç'] > seriler['T2 Maç']).astype(int)
        seriler['T2_Galibiyet'] = (seriler['T2 Maç'] > seriler['T1 Maç']).astype(int)
        
        # --- HER TAKIM İÇİN TOPLAMLARI HESAPLA ---
        # Takım 1 tarafı
        t1_stats = seriler[['Grup', 'Takım 1', 'T1_Galibiyet', 'T1 Maç', 'T2 Maç', 'T1 Set', 'T2 Set', 'T1 Oyun', 'T2 Oyun']]
        t1_stats.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
        
        # Takım 2 tarafı
        t2_stats = seriler[['Grup', 'Takım 2', 'T2_Galibiyet', 'T2 Maç', 'T1 Maç', 'T2 Set', 'T1 Set', 'T2 Oyun', 'T1 Oyun']]
        t2_stats.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
        
        # Birleştir ve Grupla
        tum_stats = pd.concat([t1_stats, t2_stats]).groupby(['Grup', 'Takım']).sum().reset_index()
        
        # Averajları Hesapla
        tum_stats['Maç Averajı'] = tum_stats['Aldığı Maç'] - tum_stats['Verdiği Maç']
        tum_stats['Set Averajı'] = tum_stats['Aldığı Set'] - tum_stats['Verdiği Set']
        tum_stats['Oyun Averajı'] = tum_stats['Aldığı Oyun'] - tum_stats['Verdiği Oyun']
        
        # Sıralama: Galibiyet > Maç Av > Set Av > Oyun Av
        tum_stats = tum_stats.sort_values(
            by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'],
            ascending=[True, False, False, False, False]
        )
        
        # Grupları ayrı tablo olarak yazdır
        for grup in tum_stats['Grup'].unique():
            st.markdown(f"### 🏆 {grup}")
            st.dataframe(tum_stats[tum_stats['Grup'] == grup].drop(columns=['Grup']), use_container_width=True)
            st.divider()
    else:
        st.info("Skor girilmediği için henüz sıralama oluşmadı.")

with tab3:
    st.subheader("Verileri Kaydet")
    csv = st.session_state.skor_tablosu.to_csv(index=False).encode('utf-8')
    st.download_button("CSV Olarak İndir", data=csv, file_name="turnuva_kayit.csv", mime="text/csv")
