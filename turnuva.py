import streamlit as st
import pandas as pd

# 1. Sayfa konfigürasyonu (MUTLAKA EN ÜSTTE OLMALI)
st.set_page_config(page_title="Turnuva Yonetimi", layout="wide")

st.title("🎾 Dinamik Turnuva Yönetim Sistemi")
st.write("Skorları güncelledikçe grup sıralamaları otomatik olarak hesaplanır.")

# 2. Şablon Veri Kümesi (İlk açılış için temiz veri)
varsayilan_maclar = [
    {"Grup": "ERKEK A GRUBU", "Takim 1": "ATAK PRO SPOR", "Takim 2": "NEW GEN SPOR", "T1 Mac": 1, "T2 Mac": 0, "T1 Set": 2, "T2 Set": 0, "T1 Oyun": 12, "T2 Oyun": 4, "Galibiyet": "ATAK PRO SPOR"},
    {"Grup": "ERKEK A GRUBU", "Takim 1": "TOPSPIN TENIS", "Takim 2": "TOPSPIN KONUTKENT", "T1 Mac": 0, "T2 Mac": 1, "T1 Set": 0, "T2 Set": 2, "T1 Oyun": 3, "T2 Oyun": 12, "Galibiyet": "TOPSPIN KONUTKENT"},
    {"Grup": "KADIN B GRUBU", "Takim 1": "ODTU SPOR KULÜBU", "Takim 2": "INCEK TENIS", "T1 Mac": 1, "T2 Mac": 0, "T1 Set": 2, "T2 Set": 0, "T1 Oyun": 12, "T2 Oyun": 0, "Galibiyet": "ODTU SPOR KULÜBU"}
]

# Hafıza kontrolü
if 'mac_tablosu' not in st.session_state:
    st.session_state.mac_tablosu = pd.DataFrame(varsayilan_maclar)

# 3. Sekmelerin Oluşturulması
sekme_giris, sekme_rapor = st.tabs(["✍️ Skor Giriş Ekranı", "🏆 Grup Sıralamaları"])

# --- SEKME 1: VERİ GİRİŞİ ---
with sekme_giris:
    st.subheader("Maç Skorlarını Buradan Düzenleyin")
    st.caption("Yeni satır eklemek için tablonun altındaki '+' butonunu kullanabilir veya hücrelere çift tıklayarak verileri değiştirebilirsiniz.")
    
    # Güvenli veri editörü
    guncel_df = st.data_editor(
        st.session_state.mac_tablosu,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_sepeti"
    )
    # Hafızayı güncelle
    st.session_state.mac_tablosu = guncel_df

# --- SEKME 2: SIRALAMALAR ---
with sekme_rapor:
    st.subheader("Anlık Puan Durumu ve Sıralama")
    
    df_hesap = guncel_df.copy()
    # Boş bırakılan satırları filtrele
    df_hesap = df_hesap.dropna(subset=['Takim 1', 'Takim 2'])
    
    if df_hesap.empty:
        st.warning("Görüntülenecek maç sonucu bulunamadı.")
    else:
        # Sayısal alanları garantiye al
        for col in ['T1 Mac', 'T2 Mac', 'T1 Set', 'T2 Set', 'T1 Oyun', 'T2 Oyun']:
            df_hesap[col] = pd.to_numeric(df_hesap[col], errors='coerce').fillna(0)
            
        # Takım 1 Penceresi
        t1 = df_hesap[['Grup', 'Takim 1', 'T1 Mac', 'T2 Mac', 'T1 Set', 'T2 Set', 'T1 Oyun', 'T2 Oyun', 'Galibiyet']].copy()
        t1.columns = ['Grup', 'Takım', 'OMac', 'VMac', 'OSet', 'VSet', 'OOyun', 'VOyun', 'Galibiyet_Adayi']
        t1['Galibiyet Puanı'] = (t1['Galibiyet_Adayi'] == t1['Takım']).astype(int)
        
        # Takım 2 Penceresi
        t2 = df_hesap[['Grup', 'Takim 2', 'T2 Mac', 'T1 Mac', 'T2 Set', 'T1 Set', 'T2 Oyun', 'T1 Oyun', 'Galibiyet']].copy()
        t2.columns = ['Grup', 'Takım', 'OMac', 'VMac', 'OSet', 'VSet', 'OOyun', 'VOyun', 'Galibiyet_Adayi']
        t2['Galibiyet Puanı'] = (t2['Galibiyet_Adayi'] == t2['Takım']).astype(int)
        
        # Birleştirme ve Gruplama
        birlikte = pd.concat([t1, t2], ignore_index=True)
        puan_durumu = birlikte.groupby(['Grup', 'Takım']).sum(numeric_only=True).reset_index()
        
        # Averaj Hesapları
        puan_durumu['Maç Averajı'] = puan_durumu['OMac'] - puan_durumu['VMac']
        puan_durumu['Set Averajı'] = puan_durumu['OSet'] - puan_durumu['VSet']
        puan_durumu['Oyun Averajı'] = puan_durumu['OOyun'] - puan_durumu['VOyun']
        
        # Sıralama Kuralları
        puan_durumu = puan_durumu.sort_values(
            by=['Grup', 'Galibiyet Puanı', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'],
            ascending=[True, False, False, False, False]
        )
        
        # Gösterim Sütunlarını Düzenle
        puan_durumu = puan_durumu[[
            'Grup', 'Galibiyet Puanı', 'Takım', 'OMac', 'VMac', 'Maç Averajı',
            'OSet', 'VSet', 'Set Averajı', 'OOyun', 'VOyun', 'Oyun Averajı'
        ]]
        
        # Gruplara Göre Tabloları Bölerek Göster
        for grup_ismi in puan_durumu['Grup'].unique():
            st.markdown(f"### 🏆 {grup_ismi}")
            grup_df = puan_durumu[puan_durumu['Grup'] == grup_ismi].drop(columns=['Grup']).reset_index(drop=True)
            grup_df.index = grup_df.index + 1  # 1'den başlasın
            st.dataframe(grup_df, use_container_width=True)
