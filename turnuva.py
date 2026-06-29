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

# --- 3. SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["👥 1. Grup ve Eşleşme", "✍️ 2. Skor Girişi", "🏆 3. Puan Durumu", "⚙️ 4. Yönetim"])

with tab1:
    st.subheader("Grup Takımlarını Seç ve Eşleşmeleri Oluştur")
    grup_adi = st.text_input("Grup Adı")
    takim_listesi = st.text_area("Takımları Alt Alta Yaz (4 Takım Olmalı)")
    if st.button("🚀 Eşleşmeleri Oluştur"):
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
    st.subheader("Maç Skorlarını Girin")
    # Filtreleme burada sadece görüntüleme için
    secilen_grup = st.selectbox("Grup Filtrele:", ["Tümü"] + list(st.session_state.skor_tablosu['Grup'].unique()))
    
    df_temp = st.session_state.skor_tablosu if secilen_grup == "Tümü" else st.session_state.skor_tablosu[st.session_state.skor_tablosu['Grup'] == secilen_grup]
    
    # Skor girişi
    edited_df = st.data_editor(df_temp, use_container_width=True)
    
    # Değişiklikleri ana hafızaya geri işle
    if secilen_grup == "Tümü":
        st.session_state.skor_tablosu = edited_df
    else:
        st.session_state.skor_tablosu.update(edited_df)

with tab3:
    st.subheader("Otomatik Puan Durumu")
    if not st.session_state.skor_tablosu.empty:
        df = st.session_state.skor_tablosu.copy()
        df['T1_Set_Skor'] = (df['1.Set T1'] > df['1.Set T2']).astype(int) + (df['2.Set T1'] > df['2.Set T2']).astype(int) + (df['3.Set T1'] > df['3.Set T2']).astype(int)
        df['T2_Set_Skor'] = (df['1.Set T2'] > df['1.Set T1']).astype(int) + (df['2.Set T2'] > df['2.Set T1']).astype(int) + (df['3.Set T2'] > df['3.Set T1']).astype(int)
        df['T1_Match_Win'] = (df['T1_Set_Skor'] > df['T2_Set_Skor']).astype(int)
        df['T2_Match_Win'] = (df['T2_Set_Skor'] > df['T1_Set_Skor']).astype(int)
        
        seriler = df.groupby(['Grup', 'Gün', 'Eşleşme', 'Takım 1', 'Takım 2']).agg({'T1_Match_Win': 'sum', 'T2_Match_Win': 'sum', 'T1_Set_Skor': 'sum', 'T2_Set_Skor': 'sum'}).reset_index()
        seriler['T1_Win'] = (seriler['T1_Match_Win'] >= 2).astype(int)
        seriler['T2_Win'] = (seriler['T2_Match_Win'] >= 2).astype(int)
        
        t1 = seriler[['Grup', 'Takım 1', 'T1_Win', 'T1_Match_Win', 'T2_Match_Win', 'T1_Set_Skor', 'T2_Set_Skor']]
        t1.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set']
        t2 = seriler[['Grup', 'Takım 2', 'T2_Win', 'T2_Match_Win', 'T1_Match_Win', 'T2_Set_Skor', 'T1_Set_Skor']]
        t2.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set']
        
        tum_stats = pd.concat([t1, t2]).groupby(['Grup', 'Takım']).sum().reset_index()
        tum_stats['Maç Av.'] = tum_stats['Aldığı Maç'] - tum_stats['Verdiği Maç']
        tum_stats['Set Av.'] = tum_stats['Aldığı Set'] - tum_stats['Verdiği Set']
        
        for grup in tum_stats['Grup'].unique():
            st.markdown(f"### 🏆 {grup} Puan Durumu")
            st.dataframe(tum_stats[tum_stats['Grup'] == grup].drop(columns=['Grup']).sort_values(by=['Galibiyet', 'Maç Av.'], ascending=False), use_container_width=True)

with tab4:
    st.subheader("⚙️ Yönetim Paneli")
    # Takım İsmi Güncelleme
    grup_sec = st.selectbox("Düzenlenecek Grubu Seç:", st.session_state.skor_tablosu['Grup'].unique())
    if grup_sec:
        takimlar = list(pd.concat([st.session_state.skor_tablosu[st.session_state.skor_tablosu['Grup']==grup_sec]['Takım 1'], 
                                   st.session_state.skor_tablosu[st.session_state.skor_tablosu['Grup']==grup_sec]['Takım 2']]).unique())
        eski_isim = st.selectbox("Değiştirilecek Takım:", takimlar)
        yeni_isim = st.text_input("Yeni İsim:")
        if st.button("Takımı Güncelle"):
            mask1 = (st.session_state.skor_tablosu['Grup'] == grup_sec) & (st.session_state.skor_tablosu['Takım 1'] == eski_isim)
            mask2 = (st.session_state.skor_tablosu['Grup'] == grup_sec) & (st.session_state.skor_tablosu['Takım 2'] == eski_isim)
            st.session_state.skor_tablosu.loc[mask1, 'Takım 1'] = yeni_isim
            st.session_state.skor_tablosu.loc[mask2, 'Takım 2'] = yeni_isim
            st.rerun()

    st.divider()
    if st.button("🚨 TÜM VERİLERİ SIFIRLA"):
        st.session_state.skor_tablosu = pd.DataFrame(columns=["Grup", "Gün", "Eşleşme", "Branş", "Takım 1", "Takım 2", "1.Set T1", "1.Set T2", "2.Set T1", "2.Set T2", "3.Set T1", "3.Set T2"])
        st.rerun()
