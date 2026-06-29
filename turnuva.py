import streamlit as st
import pandas as pd

# Sayfa Genişlik Ayarı (En üstte olmalı)
st.set_page_config(page_title="Tenis Turnuva Yönetimi", layout="wide")
st.title("🎾 Profesyonel Tenis Turnuvası Yönetim Sistemi")

# --- 1. SÜTUN İSİMLERİNİ SABİTLEYELİM (HATA ÖNLEME) ---
GRUP_COL = "Grup"
GUN_COL = "Gün"
ESLESME_COL = "Eşleşme"
BRANS_COL = "Branş"
TAKIM1_COL = "Takım 1"
TAKIM2_COL = "Takım 2"
T1_MAC = "T1 Maç"
T2_MAC = "T2 Maç"
T1_SET = "T1 Set"
T2_SET = "T2 Set"
T1_OYUN = "T1 Oyun"
T2_OYUN = "T2 Oyun"
TIE_KAZANANI = "Tie Kazananı (Galibiyet)"

# --- 2. HAFIZA (SESSION STATE) İLK KURULUMU ---
if 'havuz_listesi' not in st.session_state:
    st.session_state.havuz_listesi = [
        "ATAK PRO SPOR KULÜBÜ  E", "İNCEK TENİS SPOR KULÜBÜ  E", 
        "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E", "TOPSPİN TENİS SPOR KULÜBÜ  E",
        "TOPSPİN KONUTKENT SPOR KULÜBÜ  E", "SETPOİNT TENİS SPOR KULÜBÜ  E",
        "EFE GÜRAY EĞİTİM VE SPOR VAKFI SPOR KULÜBÜ  E", "NEW GEN SPOR KULÜBÜ  E",
        "ATAK PRO SPOR KULÜBÜ", "İNCEK TENİS SPOR KULÜBÜ", 
        "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ", "TOPSPİN TENİS SPOR KULÜBÜ",
        "TOPSPİN KONUTKENT SPOR KULÜBÜ", "SETPOİNT TENİS SPOR KULÜBÜ", "NEW GEN SPOR KULÜBÜ"
    ]

if 'grup_tablosu' not in st.session_state:
    st.session_state.grup_tablosu = pd.DataFrame([
        {"Grup": "ERKEK A GRUBU", "Grup Sırası": "1. Takım", "Seçilen Takım": "ATAK PRO SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK A GRUBU", "Grup Sırası": "2. Takım", "Seçilen Takım": "TOPSPİN TENİS SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK A GRUBU", "Grup Sırası": "3. Takım", "Seçilen Takım": "TOPSPİN KONUTKENT SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK A GRUBU", "Grup Sırası": "4. Takım", "Seçilen Takım": "NEW GEN SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK B GRUBU", "Grup Sırası": "1. Takım", "Seçilen Takım": "İNCEK TENİS SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK B GRUBU", "Grup Sırası": "2. Takım", "Seçilen Takım": "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK B GRUBU", "Grup Sırası": "3. Takım", "Seçilen Takım": "SETPOİNT TENİS SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK B GRUBU", "Grup Sırası": "4. Takım", "Seçilen Takım": "EFE GÜRAY EĞİTİM VE SPOR VAKFI SPOR KULÜBÜ  E"},
    ])

if 'skor_tablosu' not in st.session_state:
    st.session_state.skor_tablosu = pd.DataFrame([
        {GRUP_COL: "ERKEK A GRUBU", GUN_COL: "1. Gün", ESLESME_COL: "1 ve 4", BRANS_COL: "1. Tekler", TAKIM1_COL: "ATAK PRO SPOR KULÜBÜ  E", TAKIM2_COL: "NEW GEN SPOR KULÜBÜ  E", T1_MAC: 1, T2_MAC: 0, T1_SET: 2, T2_SET: 0, T1_OYUN: 12, T2_OYUN: 4, TIE_KAZANANI: "ATAK PRO SPOR KULÜBÜ  E"},
        {GRUP_COL: "ERKEK A GRUBU", GUN_COL: "1. Gün", ESLESME_COL: "1 ve 4", BRANS_COL: "2. Tekler", TAKIM1_COL: "ATAK PRO SPOR KULÜBÜ  E", TAKIM2_COL: "NEW GEN SPOR KULÜBÜ  E", T1_MAC: 1, T2_MAC: 0, T1_SET: 2, T2_SET: 0, T1_OYUN: 12, T2_OYUN: 1, TIE_KAZANANI: "ATAK PRO SPOR KULÜBÜ  E"},
        {GRUP_COL: "ERKEK B GRUBU", GUN_COL: "2. Gün", ESLESME_COL: "2 ve 4", BRANS_COL: "1. Tekler", TAKIM1_COL: "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E", TAKIM2_COL: "EFE GÜRAY EĞİTİM VE SPOR VAKFI SPOR KULÜBÜ  E", T1_MAC: 1, T2_MAC: 0, T1_SET: 2, T2_SET: 0, T1_OYUN: 10, T2_OYUN: 2, TIE_KAZANANI: "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E"}
    ])

# --- 3. SEKMELERİN OLUŞTURULMASI ---
sekme_havuz, sekme_gruplar, sekme_skor, sekme_siralama = st.tabs([
    "🚀 1. Takım Havuzu Girişi", 
    "👥 2. Grup Atamaları", 
    "✍️ 3. Skor Giriş Ekranı", 
    "🏆 4. Grup Sıralamaları"
])

# --- SEKME 1: TAKIM HAVUZU GİRİŞİ ---
with sekme_havuz:
    st.subheader("Turnuvaya Katılabilecek Tüm Takımların Listesi")
    st.info("💡 Yeni takımları en alta ekleyebilir veya silebilirsiniz. Buradaki isimler sonraki sekmelerde açılır liste seçeneği olur.")
    
    # Listeyi dataframe formatına sokup gösteriyoruz
    havuz_df = pd.DataFrame({"Takım Adı": st.session_state.havuz_listesi})
    guncel_havuz = st.data_editor(havuz_df, num_rows="dynamic", use_container_width=True, key="havuz_editor")
    
    # Değişiklikleri kaydet
    st.session_state.havuz_listesi = guncel_havuz["Takım Adı"].dropna().unique().tolist()

# --- SEKME 2: GRUP ATAMALARI ---
with sekme_gruplar:
    st.subheader("Gruplara Takım Atama Ekranı")
    
    guncel_gruplar = st.data_editor(
        st.session_state.grup_tablosu,
        column_config={
            "Grup": st.column_config.SelectboxColumn("Grup Adı", options=["ERKEK A GRUBU", "ERKEK B GRUBU", "KADIN A GRUBU", "KADIN B GRUBU"], required=True),
            "Grup Sırası": st.column_config.TextColumn("Grup Sırası", disabled=True),
            "Seçilen Takım": st.column_config.SelectboxColumn("Seçilen Takım", options=st.session_state.havuz_listesi, required=True)
        },
        num_rows="dynamic",
        use_container_width=True,
        key="grup_editor"
    )
    st.session_state.grup_tablosu = guncel_gruplar
    aktif_secili_takimlar = guncel_gruplar["Seçilen Takım"].dropna().unique().tolist()

# --- SEKME 3: SKOR GİRİŞ EKRANI ---
with sekme_skor:
    st.subheader("Maç Programı ve Skor Giriş Tablosu")
    
    guncel_skorlar = st.data_editor(
        st.session_state.skor_tablosu,
        column_config={
            GRUP_COL: st.column_config.SelectboxColumn("Grup", options=["ERKEK A GRUBU", "ERKEK B GRUBU", "KADIN A GRUBU", "KADIN B GRUBU"]),
            GUN_COL: st.column_config.SelectboxColumn("Gün", options=[f"{i}. Gün" for i in range(1, 11)]),
            ESLESME_COL: st.column_config.TextColumn("Eşleşme"),
            BRANS_COL: st.column_config.SelectboxColumn("Branş", options=["1. Tekler", "2. Tekler", "Çiftler"]),
            TAKIM1_COL: st.column_config.SelectboxColumn("Takım 1", options=aktif_secili_takimlar),
            TAKIM2_COL: st.column_config.SelectboxColumn("Takım 2", options=aktif_secili_takimlar),
            T1_MAC: st.column_config.NumberColumn("T1 Maç", min_value=0, max_value=1, default=0),
            T2_MAC: st.column_config.NumberColumn("T2 Maç", min_value=0, max_value=1, default=0),
            T1_SET: st.column_config.NumberColumn("T1 Set", min_value=0, max_value=3, default=0),
            T2_SET: st.column_config.NumberColumn("T2 Set", min_value=0, max_value=3, default=0),
            T1_OYUN: st.column_config.NumberColumn("T1 Oyun", min_value=0, max_value=20, default=0),
            T2_OYUN: st.column_config.NumberColumn("T2 Oyun", min_value=0, max_value=20, default=0),
            TIE_KAZANANI: st.column_config.SelectboxColumn("Tie Kazananı (Galibiyet)", options=aktif_secili_takimlar)
        },
        num_rows="dynamic",
        use_container_width=True,
        key="skor_editor"
    )
    st.session_state.skor_tablosu = guncel_skorlar

# --- SEKME 4: GRUP SIRALAMALARI ---
with sekme_siralama:
    st.subheader("Canlı Puan Durumu ve Raporlar")
    
    df_hesap = st.session_state.skor_tablosu.copy()
    df_hesap = df_hesap.dropna(subset=[TAKIM1_COL, TAKIM2_COL])
    
    if df_hesap.empty:
        st.warning("Hesaplanacak maç verisi bulunamadı. Lütfen 3. Sekmeden skor giriniz.")
    else:
        try:
            # Sayısal veri zorlaması
            sayisal_sutunlar = [T1_MAC, T2_MAC, T1_SET, T2_SET, T1_OYUN, T2_OYUN]
            for col in sayisal_sutunlar:
                df_hesap[col] = pd.to_numeric(df_hesap[col], errors='coerce').fillna(0)
                
            yeni_sutunlar = ['Grup', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun', 'Galibiyet_Adayi']
            
            # Takım 1 Matrisi
            t1 = df_hesap[[GRUP_COL, TAKIM1_COL, T1_MAC, T2_MAC, T1_SET, T2_SET, T1_OYUN, T2_OYUN, TIE_KAZANANI]].copy()
            t1.columns = yeni_sutunlar
            t1['Galibiyet'] = (t1['Galibiyet_Adayi'] == t1['Takım Adı']).astype(int)
            
            # Takım 2 Matrisi
            t2 = df_hesap[[GRUP_COL, TAKIM2_COL, T2_MAC, T1_MAC, T2_SET, T1_SET, T2_OYUN, T1_OYUN, TIE_KAZANANI]].copy()
            t2.columns = yeni_sutunlar
            t2['Galibiyet'] = (t2['Galibiyet_Adayi'] == t2['Takım Adı']).astype(int)
            
            # Birleştirme ve Matematiksel Toplamlar
            birlikte = pd.concat([t1, t2], ignore_index=True)
            siralama = birlikte.groupby(['Grup', 'Takım Adı']).sum(numeric_only=True).reset_index()
            
            # Excel İle Birebir Eşit Averaj Hesapları
            siralama['Maç Averajı'] = siralama['Aldığı Maç'] - siralama['Verdiği Maç']
            siralama['Set Averajı'] = siralama['Aldığı Set'] - siralama['Verdiği Set']
            siralama['Oyun Averajı'] = siralama['Aldığı Oyun'] - siralama['Verdiği Oyun']
            
            # Turnuva Kriterlerine Göre Sıralama Önceliği
            siralama = siralama.sort_values(
                by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'],
                ascending=[True, False, False, False, False]
            )
            
            # Sütun yerleşimi
            siralama = siralama[[
                'Grup', 'Galibiyet', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Maç Averajı',
                'Aldığı Set', 'Verdiği Set', 'Set Averajı', 'Aldığı Oyun', 'Verdiği Oyun', 'Oyun Averajı'
            ]]
            
            # Her grubu kendi başlığı altında yayınlama
            for grup_ismi in siralama['Grup'].unique():
                st.markdown(f"### 🏆 {grup_ismi} SIRALAMASI")
                grup_df = siralama[siralama['Grup'] == grup_ismi].drop(columns=['Grup']).reset_index(drop=True)
                grup_df.index = grup_df.index + 1
                st.dataframe(grup_df, use_container_width=True)
                st.markdown("---")
                
        except Exception as e:
            st.error(f"Sıralama hesaplanırken bir senkronizasyon hatası oluştu: {e}")
