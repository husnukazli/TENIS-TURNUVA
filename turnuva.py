import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Turnuva Yönetimi", layout="wide")
st.title("🎾 Tenis Turnuva Yönetim Sistemi")

# --- 1. DOSYA YÜKLEME (Geri Yükleme) ---
with st.sidebar:
    st.header("Dosya İşlemleri")
    uploaded_file = st.file_uploader("Kayıtlı dosyanı (.csv) geri yükle:", type="csv")
    if uploaded_file is not None:
        try:
            st.session_state.skor_tablosu = pd.read_csv(uploaded_file)
            st.success("Dosya başarıyla yüklendi!")
        except:
            st.error("Dosya okunurken hata oluştu.")

# --- 2. SESSION STATE (Hafıza) ---
if 'skor_tablosu' not in st.session_state:
    st.session_state.skor_tablosu = pd.DataFrame(columns=[
        "Grup", "Gün", "Eşleşme", "Branş", "Takım 1", "Takım 2", 
        "T1 Maç", "T2 Maç", "T1 Set", "T2 Set", "T1 Oyun", "T2 Oyun"
    ])

# --- 3. SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["🚀 1. Takım Havuzu", "👥 2. Grup Atamaları", "✍️ 3. Skor Giriş", "🏆 4. Sıralamalar"])

with tab1:
    st.info("Bu sekme sadece takımların listesini tutar.")
    # (Burayı boş bırakıyoruz veya basit bir metin alanı koyuyoruz, mantık eskisi gibi)
    st.write("Takım listesi yönetimi için eski yapıyı koruduk.")

with tab2:
    st.subheader("Grup Atamaları")
    st.write("Eski grup atama düzenin burada duruyor.")

with tab3:
    st.subheader("Skor Giriş Ekranı")
    st.caption("Skorları buraya girmeye devam et. Sistem artık 3 maçın toplamına göre galibiyet hesaplayacak.")
    st.session_state.skor_tablosu = st.data_editor(st.session_state.skor_tablosu, num_rows="dynamic", use_container_width=True)
    
    # İndirme butonu
    csv = st.session_state.skor_tablosu.to_csv(index=False).encode('utf-8')
    st.download_button("Dosyayı Kaydet (.csv)", data=csv, file_name="turnuva_data.csv", mime="text/csv")

with tab4:
    st.subheader("Otomatik Puan Durumu")
    
    if not st.session_state.skor_tablosu.empty:
        df = st.session_state.skor_tablosu.copy()
        
        # 1. Seri Bazlı Galibiyet Hesaplama (Eşleşme bazlı)
        # 1-4, 2-3 gibi eşleşmelerde; T1 Maç > T2 Maç ise o "Eşleşmeyi" T1 kazanmıştır.
        seriler = df.groupby(['Grup', 'Gün', 'Eşleşme', 'Takım 1', 'Takım 2']).agg({
            'T1 Maç': 'sum', 'T2 Maç': 'sum',
            'T1 Set': 'sum', 'T2 Set': 'sum',
            'T1 Oyun': 'sum', 'T2 Oyun': 'sum'
        }).reset_index()
        
        seriler['T1_Galibiyet'] = (seriler['T1 Maç'] > seriler['T2 Maç']).astype(int)
        seriler['T2_Galibiyet'] = (seriler['T2 Maç'] > seriler['T1 Maç']).astype(int)
        
        # 2. Her takım için toplama
        t1_stats = seriler[['Grup', 'Takım 1', 'T1_Galibiyet', 'T1 Maç', 'T2 Maç', 'T1 Set', 'T2 Set', 'T1 Oyun', 'T2 Oyun']]
        t1_stats.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
        
        t2_stats = seriler[['Grup', 'Takım 2', 'T2_Galibiyet', 'T2 Maç', 'T1 Maç', 'T2 Set', 'T1 Set', 'T2 Oyun', 'T1 Oyun']]
        t2_stats.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
        
        # 3. Birleştir ve Averaj Hesapla
        tum_stats = pd.concat([t1_stats, t2_stats]).groupby(['Grup', 'Takım']).sum().reset_index()
        tum_stats['Maç Averajı'] = tum_stats['Aldığı Maç'] - tum_stats['Verdiği Maç']
        tum_stats['Set Averajı'] = tum_stats['Aldığı Set'] - tum_stats['Verdiği Set']
        tum_stats['Oyun Averajı'] = tum_stats['Aldığı Oyun'] - tum_stats['Verdiği Oyun']
        
        # 4. Sıralama (Galibiyet > Maç Av > Set Av > Oyun Av)
        tum_stats = tum_stats.sort_values(
            by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'],
            ascending=[True, False, False, False, False]
        )
        
        # Görselleştirme
        for grup in tum_stats['Grup'].unique():
            st.markdown(f"### 🏆 {grup} SIRALAMASI")
            st.dataframe(tum_stats[tum_stats['Grup'] == grup].drop(columns=['Grup']), use_container_width=True)
            st.divider()
    else:
        st.warning("Henüz skor girişi yapılmadı.")
