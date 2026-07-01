import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Tenis Turnuva Otomasyonu", layout="wide")
st.title("🎾 Profesyonel Tenis Turnuva Yönetim Sistemi")

# --- 1. OTOMASYON MOTORU ---
def eslesmeleri_olustur(grup_adi, takimlar):
    base_matches = [
        {"Gün": "1. Gün", "Eşleşme": "1 ve 4", "Takım 1": takimlar[0], "Takım 2": takimlar[3]},
        {"Gün": "1. Gün", "Eşleşme": "2 ve 3", "Takım 1": takimlar[1], "Takım 2": takimlar[2]},
        {"Gün": "2. Gün", "Eşleşme": "1 ve 3", "Takım 1": takimlar[0], "Takım 2": takimlar[2]},
        {"Gün": "2. Gün", "Eşleşme": "2 ve 4", "Takım 1": takimlar[1], "Takım 2": takimlar[3]},
        {"Gün": "3. Gün", "Eşleşme": "1 ve 2", "Takım 1": takimlar[0], "Takım 2": takimlar[1]},
        {"Gün": "3. Gün", "Eşleşme": "3 ve 4", "Takım 1": takimlar[2], "Takım 2": takimlar[3]},
    ]
    program = []
    for m in base_matches:
        for brans in ["1. Tekler", "2. Tekler", "Çiftler"]:
            satir = m.copy()
            satir["Branş"] = brans
            satir["Grup"] = grup_adi
            satir.update({"1.Set T1": 0, "1.Set T2": 0, "2.Set T1": 0, "2.Set T2": 0, "3.Set T1": 0, "3.Set T2": 0})
            program.append(satir)
    return program

# --- 2. HAFIZA ---
if 'skor_tablosu' not in st.session_state:
    st.session_state.skor_tablosu = pd.DataFrame(columns=["Grup", "Gün", "Eşleşme", "Branş", "Takım 1", "Takım 2", "1.Set T1", "1.Set T2", "2.Set T1", "2.Set T2", "3.Set T1", "3.Set T2"])

# --- 3. SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["👥 1. Grup Ayarları", "✍️ 2. Skor Girişi", "🏆 3. Puan Durumu", "⚙️ 4. Yönetim"])

with tab1:
    st.subheader("Grup Takımlarını Seç ve Eşleşmeleri Oluştur")
    grup_adi = st.text_input("Grup Adı")
    takim_listesi = st.text_area("Takımları Alt Alta Yaz (4 Takım Olmalı)")
    if st.button("🚀 Eşleşmeleri Oluştur"):
        takimlar = [t.strip() for t in takim_listesi.split('\n') if t.strip()]
        if len(takimlar) == 4:
            yeni_maclar = eslesmeleri_olustur(grup_adi, takimlar)
            yeni_df = pd.DataFrame(yeni_maclar)
            st.session_state.skor_tablosu = pd.concat([st.session_state.skor_tablosu, yeni_df], ignore_index=True)
            st.session_state.skor_tablosu.index = range(1, len(st.session_state.skor_tablosu) + 1)
            st.success("Eşleşmeler oluşturuldu!")
            st.rerun()
        else:
            st.error("Lütfen tam olarak 4 takım girin.")

with tab2:
    st.subheader("Maç Skorlarını Girin")
    if not st.session_state.skor_tablosu.empty:
        gruplar = st.session_state.skor_tablosu['Grup'].unique()
        secilen_grup = st.selectbox("Düzenlemek İçin Grup Seç:", gruplar)
        
        df_grup = st.session_state.skor_tablosu[st.session_state.skor_tablosu['Grup'] == secilen_grup].copy()
        edited_dfs = {}
        
        for gun in ["1. Gün", "2. Gün", "3. Gün"]:
            st.markdown(f"### {gun}")
            df_gun = df_grup[df_grup['Gün'] == gun]
            if not df_gun.empty:
                edited_dfs[gun] = st.data_editor(df_gun, use_container_width=True, key=f"editor_{gun}")
        
        if st.button("✅ Tüm Skorları Kaydet"):
            all_edited = pd.concat(edited_dfs.values())
            st.session_state.skor_tablosu.update(all_edited)
            st.success("Skorlar kaydedildi!")
            st.rerun()
    else:
        st.info("Henüz grup oluşturmadınız.")

with tab3:
    st.subheader("Otomatik Puan Durumu")
    if not st.session_state.skor_tablosu.empty:
        df = st.session_state.skor_tablosu.copy()
        df['T1_Oyun'] = df['1.Set T1'] + df['2.Set T1'] + df['3.Set T1']
        df['T2_Oyun'] = df['1.Set T2'] + df['2.Set T2'] + df['3.Set T2']
        df['T1_Set_Skor'] = (df['1.Set T1'] > df['1.Set T2']).astype(int) + (df['2.Set T1'] > df['2.Set T2']).astype(int) + (df['3.Set T1'] > df['3.Set T2']).astype(int)
        df['T2_Set_Skor'] = (df['1.Set T2'] > df['1.Set T1']).astype(int) + (df['2.Set T2'] > df['2.Set T1']).astype(int) + (df['3.Set T2'] > df['3.Set T1']).astype(int)
        df['T1_Match_Win'] = (df['T1_Set_Skor'] > df['T2_Set_Skor']).astype(int)
        df['T2_Match_Win'] = (df['T2_Set_Skor'] > df['T1_Set_Skor']).astype(int)
        
        seriler = df.groupby(['Grup', 'Gün', 'Eşleşme', 'Takım 1', 'Takım 2']).agg({'T1_Match_Win': 'sum', 'T2_Match_Win': 'sum', 'T1_Set_Skor': 'sum', 'T2_Set_Skor': 'sum', 'T1_Oyun': 'sum', 'T2_Oyun': 'sum'}).reset_index()
        seriler['T1_Win'] = (seriler['T1_Match_Win'] >= 2).astype(int)
        seriler['T2_Win'] = (seriler['T2_Match_Win'] >= 2).astype(int)
        
        t1 = seriler[['Grup', 'Takım 1', 'T1_Win', 'T1_Match_Win', 'T2_Match_Win', 'T1_Set_Skor', 'T2_Set_Skor', 'T1_Oyun', 'T2_Oyun']]
        t1.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
        t2 = seriler[['Grup', 'Takım 2', 'T2_Win', 'T2_Match_Win', 'T1_Match_Win', 'T2_Set_Skor', 'T1_Set_Skor', 'T2_Oyun', 'T1_Oyun']]
        t2.columns = ['Grup', 'Takım', 'Galibiyet', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
        
        tum_stats = pd.concat([t1, t2]).groupby(['Grup', 'Takım']).sum().reset_index()
        tum_stats['Maç Av.'] = tum_stats['Aldığı Maç'] - tum_stats['Verdiği Maç']
        tum_stats['Set Av.'] = tum_stats['Aldığı Set'] - tum_stats['Verdiği Set']
        tum_stats['Oyun Av.'] = tum_stats['Aldığı Oyun'] - tum_stats['Verdiği Oyun']
        
        for grup in tum_stats['Grup'].unique():
            st.markdown(f"### 🏆 {grup} Puan Durumu")
            grup_df = tum_stats[tum_stats['Grup'] == grup].drop(columns=['Grup']).sort_values(by=['Galibiyet', 'Maç Av.', 'Oyun Av.'], ascending=False)
            grup_df.index = range(1, len(grup_df) + 1)
            st.dataframe(grup_df, use_container_width=True)

with tab4:
    st.subheader("⚙️ Yönetim Paneli")
    
    # DOSYA İLE YEDEKLEME SİSTEMİ
    st.markdown("### 📁 Veri Dosyası İşlemleri")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = st.session_state.skor_tablosu.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Verileri İndir (Yedekle)", data=csv, file_name='turnuva_verisi.csv', mime='text/csv')
    
    with col2:
        yuklenen_dosya = st.file_uploader("📂 Veri Dosyası Yükle (Geri Yükle)", type=['csv'])
        if yuklenen_dosya is not None:
            if st.button("🔄 Dosyayı Yükle ve Uygula"):
                st.session_state.skor_tablosu = pd.read_csv(yuklenen_dosya)
                st.success("Veri başarıyla geri yüklendi!")
                st.rerun()

    st.divider()
    if not st.session_state.skor_tablosu.empty:
        gruplar = st.session_state.skor_tablosu['Grup'].unique()
        grup_sec = st.selectbox("Düzenlenecek Grubu Seç:", gruplar)
        
        df_grup = st.session_state.skor_tablosu[st.session_state.skor_tablosu['Grup'] == grup_sec]
        tum_takimlar = sorted(list(set(df_grup['Takım 1'].unique().tolist() + df_grup['Takım 2'].unique().tolist())))
        
        eski_isim = st.selectbox("Değiştirilecek Takım:", tum_takimlar)
        yeni_isim = st.text_input("Yeni İsim:")
        
        if st.button("Takımı Güncelle"):
            st.session_state.skor_tablosu.loc[st.session_state.skor_tablosu['Takım 1'] == eski_isim, 'Takım 1'] = yeni_isim
            st.session_state.skor_tablosu.loc[st.session_state.skor_tablosu['Takım 2'] == eski_isim, 'Takım 2'] = yeni_isim
            st.rerun()
            
        st.divider()
        silinecek_grup = st.selectbox("Silinecek Grup:", gruplar)
        if st.button("❌ Bu Grubu Tamamen Sil"):
            st.session_state.skor_tablosu = st.session_state.skor_tablosu[st.session_state.skor_tablosu['Grup'] != silinecek_grup]
            st.session_state.skor_tablosu.index = range(1, len(st.session_state.skor_tablosu) + 1)
            st.rerun()
    else:
        st.info("Henüz grup yok.")

    st.divider()
    if st.button("🚨 TÜM VERİLERİ SIFIRLA"):
        st.session_state.skor_tablosu = pd.DataFrame(columns=["Grup", "Gün", "Eşleşme", "Branş", "Takım 1", "Takım 2", "1.Set T1", "1.Set T2", "2.Set T1", "2.Set T2", "3.Set T1", "3.Set T2"])
        st.rerun()
