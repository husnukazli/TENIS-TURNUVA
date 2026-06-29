import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva Otomasyonu", layout="wide")
st.title("🎾 Profesyonel Tenis Turnuva Yönetim Sistemi")

# --- 1. OTOMASYON MOTORU: EŞLEŞME OLUŞTURUCU ---
def eslesmeleri_olustur(grup_adi, takimlar):
    # Basit 4'lü grup için round-robin eşleşme mantığı
    # takımlar listesi: [1.Takım, 2.Takım, 3.Takım, 4.Takım]
    if len(takimlar) < 4: return []
    
    # Eşleşme düzeni: 1-4, 2-3 | 1-3, 2-4 | 1-2, 3-4
    program = [
        {"Gün": "1. Gün", "Eşleşme": "1 ve 4", "T1": takimlar[0], "T2": takimlar[3]},
        {"Gün": "1. Gün", "Eşleşme": "2 ve 3", "T1": takimlar[1], "T2": takimlar[2]},
        {"Gün": "2. Gün", "Eşleşme": "1 ve 3", "T1": takimlar[0], "T2": takimlar[2]},
        {"Gün": "2. Gün", "Eşleşme": "2 ve 4", "T1": takimlar[1], "T2": takimlar[3]},
        {"Gün": "3. Gün", "Eşleşme": "1 ve 2", "T1": takimlar[0], "T2": takimlar[1]},
        {"Gün": "3. Gün", "Eşleşme": "3 ve 4", "T1": takimlar[2], "T2": takimlar[3]},
    ]
    for m in program: m["Grup"] = grup_adi
    return program

# --- 2. HAFIZA ---
if 'skor_tablosu' not in st.session_state:
    st.session_state.skor_tablosu = pd.DataFrame(columns=["Grup", "Gün", "Eşleşme", "Takım 1", "Takım 2", "1.Set T1", "1.Set T2", "2.Set T1", "2.Set T2", "3.Set T1", "3.Set T2"])

# --- 3. SEKMELER ---
tab1, tab2, tab3 = st.tabs(["👥 Grup ve Eşleşme Ayarları", "✍️ Detaylı Skor Girişi", "🏆 Canlı Puan Durumu"])

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
            # Sütunları ekle
            for col in ["1.Set T1", "1.Set T2", "2.Set T1", "2.Set T2", "3.Set T1", "3.Set T2"]:
                yeni_df[col] = 0
            
            st.session_state.skor_tablosu = pd.concat([st.session_state.skor_tablosu, yeni_df], ignore_index=True)
            st.success("Eşleşmeler oluşturuldu! 'Skor Girişi' sekmesine gidebilirsiniz.")
        else:
            st.error("Lütfen tam olarak 4 takım girin.")

with tab2:
    st.subheader("Maç Skorlarını Set Set Girin")
    st.info("Sistem, girdiğin set skorlarına göre set kazananlarını otomatik hesaplayacaktır.")
    
    st.session_state.skor_tablosu = st.data_editor(st.session_state.skor_tablosu, use_container_width=True)

with tab3:
    st.subheader("Otomatik Puan Durumu")
    
    if not st.session_state.skor_tablosu.empty:
        df = st.session_state.skor_tablosu.copy()
        
        # --- OTOMATİK HESAPLAMA MANTIĞI ---
        # Set kazananı hesapla
        df['T1_Set_Skor'] = (df['1.Set T1'] > df['1.Set T2']).astype(int) + (df['2.Set T1'] > df['2.Set T2']).astype(int) + (df['3.Set T1'] > df['3.Set T2']).astype(int)
        df['T2_Set_Skor'] = (df['1.Set T2'] > df['1.Set T1']).astype(int) + (df['2.Set T2'] > df['2.Set T1']).astype(int) + (df['3.Set T2'] > df['3.Set T1']).astype(int)
        
        # Maç kazananı
        df['T1_Mac_Win'] = (df['T1_Set_Skor'] > df['T2_Set_Skor']).astype(int)
        df['T2_Mac_Win'] = (df['T2_Set_Skor'] > df['T1_Set_Skor']).astype(int)
        
        # Puanları topla (Bu kısmı Excel'indeki mantığa göre geliştiriyoruz)
        results = []
        for _, row in df.iterrows():
            results.append({"Grup": row['Grup'], "Takım": row['Takım 1'], "Galibiyet": row['T1_Mac_Win'], "Set": row['T1_Set_Skor'], "VerilenSet": row['T2_Set_Skor']})
            results.append({"Grup": row['Grup'], "Takım": row['Takım 2'], "Galibiyet": row['T2_Mac_Win'], "Set": row['T2_Set_Skor'], "VerilenSet": row['T1_Set_Skor']})
        
        final_df = pd.DataFrame(results).groupby(['Grup', 'Takım']).sum().reset_index()
        final_df['Set Averajı'] = final_df['Set'] - final_df['VerilenSet']
        
        st.dataframe(final_df.sort_values(by=['Grup', 'Galibiyet', 'Set Averajı'], ascending=[True, False, False]), use_container_width=True)
    else:
        st.warning("Henüz veri yok.")
