import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva Yönetimi", layout="wide")
st.title("🎾 Profesyonel Tenis Turnuva Yönetim Sistemi")

# --- 1. VERİ YÜKLEME (GERİ YÜKLEME) ---
with st.sidebar:
    st.header("Dosya İşlemleri")
    uploaded_file = st.file_uploader("Kayıtlı CSV dosyasını geri yükle:", type="csv")
    if uploaded_file is not None:
        st.session_state.skor_tablosu = pd.read_csv(uploaded_file)
        st.success("Dosya başarıyla yüklendi!")

# --- 2. HAFIZA KURULUMU ---
if 'skor_tablosu' not in st.session_state:
    st.session_state.skor_tablosu = pd.DataFrame(columns=[
        "Grup", "Gün", "Eşleşme", "Branş", "Takım 1", "Takım 2", 
        "T1 Maç", "T2 Maç", "T1 Set", "T2 Set", "T1 Oyun", "T2 Oyun"
    ])
if 'havuz_listesi' not in st.session_state:
    st.session_state.havuz_listesi = ["Takım 1", "Takım 2", "Takım 3", "Takım 4"]

# --- 3. SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["🚀 1. Takım Havuzu", "👥 2. Grup Atamaları", "✍️ 3. Skor Girişi", "🏆 4. Sıralamalar"])

with tab1:
    st.subheader("Takım Havuzu")
    st.session_state.havuz_listesi = st.text_area("Takımları her satıra bir tane gelecek şekilde yazın:", 
                                                 value="\n".join(st.session_state.havuz_listesi)).split('\n')

with tab2:
    st.subheader("Grup Atamaları")
    st.info("Grup ve takım eşleşmelerini buradan yönetebilirsiniz.")
    # Basit bir tablo yapısı
    df_gruplar = pd.DataFrame(columns=["Grup", "Takım"])
    st.data_editor(df_gruplar, num_rows="dynamic", use_container_width=True)

with tab3:
    st.subheader("Skor Giriş Ekranı")
    st.session_state.skor_tablosu = st.data_editor(st.session_state.skor_tablosu, num_rows="dynamic", use_container_width=True)
    
    # Kaydetme
    csv = st.session_state.skor_tablosu.to_csv(index=False).encode('utf-8')
    st.download_button("Dosyayı Kaydet (.csv)", data=csv, file_name="turnuva_data.csv", mime="text/csv")

with tab4:
    st.subheader("Otomatik Puan Durumu")
    
    if not st.session_state.skor_tablosu.empty:
        df = st.session_state.skor_tablosu.copy()
        
        # --- HESAPLAMA MOTORU ---
        # 1. Eşleşme bazlı seri galibiyetini hesapla (2 veya 3 maç kazanan)
        # Aynı grupta aynı eşleşmeyi (örn: 1 ve 4) grupla
        seriler = df.groupby(['Grup', 'Gün', 'Eşleşme', 'Takım 1', 'Takım 2']).agg({
            'T1 Maç': 'sum', 'T2 Maç': 'sum',
            'T1 Set': 'sum', 'T2 Set': 'sum',
            'T1 Oyun': 'sum', 'T2 Oyun': 'sum'
        }).reset_index()
        
        # Galibiyet Adayı Belirleme
        seriler['T1_Win'] = (seriler['T1 Maç'] > seriler['T2 Maç']).astype(int)
        seriler['T2_Win'] = (seriler['T2 Maç'] > seriler['T1 Maç']).astype(int)
        
        # 2. Takım bazlı istatistikleri topla
        t1 = seriler[['Grup', 'Takım 1', 'T1_Win', 'T1 Maç', 'T2 Maç', 'T1 Set', 'T2 Set', 'T1 Oyun', 'T2 Oyun']]
        t1.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
        
        t2 = seriler[['Grup', 'Takım 2', 'T2_Win', 'T2 Maç', 'T1 Maç', 'T2 Set', 'T1 Set', 'T2 Oyun', 'T1 Oyun']]
        t2.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
        
        # 3. Birleştir ve Averajları Hesapla
        final = pd.concat([t1, t2]).groupby(['Grup', 'Takım']).sum().reset_index()
        final['Maç Averajı'] = final['Aldığı Maç'] - final['Verdiği Maç']
        final['Set Averajı'] = final['Aldığı Set'] - final['Verdiği Set']
        final['Oyun Averajı'] = final['Aldığı Oyun'] - final['Verdiği Oyun']
        
        # Sıralama: Galibiyet > Maç Av > Set Av > Oyun Av
        final = final.sort_values(by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'], 
                                  ascending=[True, False, False, False, False])
        
        # Gösterim
        for grup in final['Grup'].unique():
            st.markdown(f"### 🏆 {grup}")
            st.dataframe(final[final['Grup'] == grup].drop(columns=['Grup']), use_container_width=True)
            st.divider()
    else:
        st.warning("Skor girişi yapıldığında sıralamalar burada otomatik oluşacaktır.")
