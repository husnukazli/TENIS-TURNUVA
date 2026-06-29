import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva Otomasyonu", layout="wide")
st.title("🎾 Profesyonel Tenis Turnuva Yönetim Sistemi")

# --- 1. OTOMASYON MOTORU (3'LÜ MAÇ MANTIĞI) ---
def eslesmeleri_olustur(grup_adi, takimlar):
    if len(takimlar) < 4: return []
    
    # Eşleşme planı
    base_matches = [
        {"Gün": "1. Gün", "Eşleşme": "1 ve 4", "T1": takimlar[0], "T2": takimlar[3]},
        {"Gün": "1. Gün", "Eşleşme": "2 ve 3", "T1": takimlar[1], "T2": takimlar[2]},
        {"Gün": "2. Gün", "Eşleşme": "1 ve 3", "T1": takimlar[0], "T2": takimlar[2]},
        {"Gün": "2. Gün", "Eşleşme": "2 ve 4", "T1": takimlar[1], "T2": takimlar[3]},
        {"Gün": "3. Gün", "Eşleşme": "1 ve 2", "T1": takimlar[0], "T2": takimlar[1]},
        {"Gün": "3. Gün", "Eşleşme": "3 ve 4", "T1": takimlar[2], "T2": takimlar[3]},
    ]
    
    # 3'lü branş yapısını ekle
    program = []
    for m in base_matches:
        for brans in ["1. Tekler", "2. Tekler", "Çiftler"]:
            satir = m.copy()
            satir["Branş"] = brans
            satir["Grup"] = grup_adi
            program.append(satir)
    return program

# --- 2. HAFIZA VE YÜKLEME ---
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
            yeni_df = yeni_df.rename(columns={"T1": "Takım 1", "T2": "Takım 2"})
            for col in ["1.Set T1", "1.Set T2", "2.Set T1", "2.Set T2", "3.Set T1", "3.Set T2"]:
                yeni_df[col] = 0
            st.session_state.skor_tablosu = pd.concat([st.session_state.skor_tablosu, yeni_df], ignore_index=True)
            st.success("Eşleşmeler oluşturuldu! Skor Girişi sekmesine geçebilirsiniz.")
        else:
            st.error("Lütfen tam olarak 4 takım girin.")

with tab2:
    st.subheader("Maç Skorlarını Set Set Girin")
    st.session_state.skor_tablosu = st.data_editor(st.session_state.skor_tablosu, use_container_width=True)
    csv = st.session_state.skor_tablosu.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Verileri Kaydet (CSV)", data=csv, file_name="turnuva_kayit.csv", mime="text/csv")

with tab3:
    st.subheader("Otomatik Puan Durumu (Seri Bazlı)")
    if not st.session_state.skor_tablosu.empty:
        df = st.session_state.skor_tablosu.copy()
        
        # Maç Kazananı Belirle (Sub-match level)
        df['T1_Set_Skor'] = (df['1.Set T1'] > df['1.Set T2']).astype(int) + (df['2.Set T1'] > df['2.Set T2']).astype(int) + (df['3.Set T1'] > df['3.Set T2']).astype(int)
        df['T2_Set_Skor'] = (df['1.Set T2'] > df['1.Set T1']).astype(int) + (df['2.Set T2'] > df['2.Set T1']).astype(int) + (df['3.Set T2'] > df['3.Set T1']).astype(int)
        
        df['T1_Match_Win'] = (df['T1_Set_Skor'] > df['T2_Set_Skor']).astype(int)
        df['T2_Match_Win'] = (df['T2_Set_Skor'] > df['T1_Set_Skor']).astype(int)
        
        # Oyun Toplamları
        df['T1_Oyun'] = df['1.Set T1'] + df['2.Set T1'] + df['3.Set T1']
        df['T2_Oyun'] = df['1.Set T2'] + df['2.Set T2'] + df['3.Set T2']
        
        # --- SERİ (EŞLEŞME) HESAPLAMA ---
        # Aynı Grup + Gün + Eşleşme (1 ve 4 gibi) olan 3 maçı grupla
        seriler = df.groupby(['Grup', 'Gün', 'Eşleşme', 'Takım 1', 'Takım 2']).agg({
            'T1_Match_Win': 'sum', 'T2_Match_Win': 'sum',
            'T1_Set_Skor': 'sum', 'T2_Set_Skor': 'sum',
            'T1_Oyun': 'sum', 'T2_Oyun': 'sum'
        }).reset_index()
        
        # 3 maçın en az 2'sini alan galip
        seriler['T1_Win'] = (seriler['T1_Match_Win'] >= 2).astype(int)
        seriler['T2_Win'] = (seriler['T2_Match_Win'] >= 2).astype(int)
        
        # Takım istatistiklerini topla
        t1 = seriler[['Grup', 'Takım 1', 'T1_Win', 'T1_Match_Win', 'T2_Match_Win', 'T1_Set_Skor', 'T2_Set_Skor', 'T1_Oyun', 'T2_Oyun']]
        t1.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
        
        t2 = seriler[['Grup', 'Takım 2', 'T2_Win', 'T2_Match_Win', 'T1_Match_Win', 'T2_Set_Skor', 'T1_Set_Skor', 'T2_Oyun', 'T1_Oyun']]
        t2.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
        
        final = pd.concat([t1, t2]).groupby(['Grup', 'Takım']).sum().reset_index()
        final['Maç Av.'] = final['Aldığı Maç'] - final['Verdiği Maç']
        final['Set Av.'] = final['Aldığı Set'] - final['Verdiği Set']
        final['Oyun Av.'] = final['Aldığı Oyun'] - final['Verdiği Oyun']
        
        # Sıralama: Galibiyet > Maç Av > Set Av
        st.dataframe(final.sort_values(by=['Grup', 'Galibiyet', 'Maç Av.', 'Set Av.', 'Oyun Av.'], ascending=[True, False, False, False, False]), use_container_width=True)
    else:
        st.warning("Veri bekleniyor.")
