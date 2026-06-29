import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva Otomasyonu", layout="wide")
st.title("🎾 Profesyonel Tenis Turnuva Yönetim Sistemi")

# --- 1. OTOMASYON MOTORU ---
def eslesmeleri_olustur(grup_adi, takimlar):
    if len(takimlar) < 4: return []
    base_matches = [
        {"Gün": "1. Gün", "Eşleşme": "1 ve 4", "T1": takimlar[0], "T2": takimlar[3]},
        {"Gün": "1. Gün", "Eşleşme": "2 ve 3", "T1": takimlar[1], "T2": takimlar[2]},
        {"Gün": "2. Gün", "Eşleşme": "1 ve 3", "T1": takimlar[0], "T2": takimlar[2]},
        {"Gün": "2. Gün", "Eşleşme": "2 ve 4", "T1": takimlar[1], "T2": takimlar[3]},
        {"Gün": "3. Gün", "Eşleşme": "1 ve 2", "T1": takimlar[0], "T2": takimlar[1]},
        {"Gün": "3. Gün", "Eşleşme": "3 ve 4", "T1": takimlar[2], "T2": takimlar[3]},
    ]
    program = []
    for m in base_matches:
        for brans in ["1. Tekler", "2. Tekler", "Çiftler"]:
            satir = m.copy()
            satir["Branş"] = brans
            satir["Grup"] = grup_adi
            program.append(satir)
    return program

# --- 2. HAFIZA ---
if 'skor_tablosu' not in st.session_state:
    st.session_state.skor_tablosu = pd.DataFrame(columns=["Grup", "Gün", "Eşleşme", "Branş", "Takım 1", "Takım 2", "1.Set T1", "1.Set T2", "2.Set T1", "2.Set T2", "3.Set T1", "3.Set T2"])

with st.sidebar:
    st.header("Dosya İşlemleri")
    uploaded_file = st.file_uploader("Kayıtlı CSV dosyasını geri yükle:", type="csv")
    if uploaded_file is not None:
        st.session_state.skor_tablosu = pd.read_csv(uploaded_file)
        st.success("Dosya yüklendi!")

# --- 3. SEKMELER ---
tab1, tab2, tab3 = st.tabs(["👥 1. Grup ve Eşleşme Ayarları", "✍️ 2. Detaylı Skor Girişi", "🏆 3. Canlı Puan Durumu"])

with tab1:
    st.subheader("Grup Takımlarını Seç ve Eşleşmeleri Oluştur")
    col1, col2 = st.columns(2)
    with col1:
        grup_adi = st.text_input("Grup Adı (Örn: ERKEK A)")
        takim_listesi = st.text_area("Takımları Alt Alta Yaz (4 Takım Olmalı)")
    
    if st.button("🚀 Eşleşmeleri ve Programı Otomatik Oluştur"):
        takimlar = [t.strip() for t in takim_listesi.split('\n') if t.strip()]
        if len(takimlar) == 4:
            yeni_maclar = eslesmeleri_olustur(grup_adi, takimlar)
            yeni_df = pd.DataFrame(yeni_maclar)
            for col in ["1.Set T1", "1.Set T2", "2.Set T1", "2.Set T2", "3.Set T1", "3.Set T2"]:
                yeni_df[col] = 0
            st.session_state.skor_tablosu = pd.concat([st.session_state.skor_tablosu, yeni_df], ignore_index=True)
            st.success("Eşleşmeler oluşturuldu!")
        else:
            st.error("Lütfen tam olarak 4 takım girin.")

with tab2:
    st.subheader("Maç Skorlarını Set Set Girin")
    # GRUP SEÇİCİ EKLENDİ
    gruplar = ["Hepsi"] + list(st.session_state.skor_tablosu['Grup'].unique())
    secilen_grup = st.selectbox("Görüntülenecek Grubu Seç:", gruplar)
    
    df_goster = st.session_state.skor_tablosu if secilen_grup == "Hepsi" else st.session_state.skor_tablosu[st.session_state.skor_tablosu['Grup'] == secilen_grup]
    st.session_state.skor_tablosu = st.data_editor(st.session_state.skor_tablosu, use_container_width=True) # Düzenleme tüm veri üzerinde yapılır
    
    csv = st.session_state.skor_tablosu.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Verileri Kaydet (CSV)", data=csv, file_name="turnuva_kayit.csv", mime="text/csv")

with tab3:
    st.subheader("Otomatik Puan Durumu (Grup Bazlı)")
    if not st.session_state.skor_tablosu.empty:
        df = st.session_state.skor_tablosu.copy()
        
        # --- İSTATİSTİK HESAPLAMA MOTORU ---
        df['T1_Set_Skor'] = (df['1.Set T1'] > df['1.Set T2']).astype(int) + (df['2.Set T1'] > df['2.Set T2']).astype(int) + (df['3.Set T1'] > df['3.Set T2']).astype(int)
        df['T2_Set_Skor'] = (df['1.Set T2'] > df['1.Set T1']).astype(int) + (df['2.Set T2'] > df['2.Set T1']).astype(int) + (df['3.Set T2'] > df['3.Set T1']).astype(int)
        
        df['T1_Match_Win'] = (df['T1_Set_Skor'] > df['T2_Set_Skor']).astype(int)
        df['T2_Match_Win'] = (df['T2_Set_Skor'] > df['T1_Set_Skor']).astype(int)
        
        seriler = df.groupby(['Grup', 'Gün', 'Eşleşme', 'Takım 1', 'Takım 2']).agg({
            'T1_Match_Win': 'sum', 'T2_Match_Win': 'sum',
            'T1_Set_Skor': 'sum', 'T2_Set_Skor': 'sum'
        }).reset_index()
        
        seriler['T1_Win'] = (seriler['T1_Match_Win'] >= 2).astype(int)
        seriler['T2_Win'] = (seriler['T2_Match_Win'] >= 2).astype(int)
        
        t1 = seriler[['Grup', 'Takım 1', 'T1_Win', 'T1_Match_Win', 'T2_Match_Win', 'T1_Set_Skor', 'T2_Set_Skor']]
        t1.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set']
        t2 = seriler[['Grup', 'Takım 2', 'T2_Win', 'T2_Match_Win', 'T1_Match_Win', 'T2_Set_Skor', 'T1_Set_Skor']]
        t2.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set']
        
        tum_stats = pd.concat([t1, t2]).groupby(['Grup', 'Takım']).sum().reset_index()
        tum_stats['Maç Av.'] = tum_stats['Aldığı Maç'] - tum_stats['Verdiği Maç']
        tum_stats['Set Av.'] = tum_stats['Aldığı Set'] - tum_stats['Verdiği Set']
        
        # --- HER GRUBU AYRI TABLO OLARAK YAZDIR ---
        for grup in tum_stats['Grup'].unique():
            st.markdown(f"### 🏆 {grup} Sıralaması")
            grup_df = tum_stats[tum_stats['Grup'] == grup].sort_values(by=['Galibiyet', 'Maç Av.', 'Set Av.'], ascending=False)
            st.dataframe(grup_df.drop(columns=['Grup']), use_container_width=True)
            st.divider()
    else:
        st.warning("Veri bekleniyor.")
