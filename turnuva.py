import streamlit as st
import pandas as pd

# Sayfa ayarı
st.set_page_config(page_title="Tenis Turnuva Yönetimi", layout="wide")
st.title("🎾 Profesyonel Tenis Turnuvası Yönetim Sistemi")

# --- 1. DİNAMİK HAFIZA (SESSION STATE) TANIMLAMALARI ---
# Uygulama ilk açıldığında Excel'inizdeki orijinal listeleri yüklüyoruz.
if 'havuz_takimlari' not in st.session_state:
    st.session_state.havuz_takimlari = pd.DataFrame({
        "Takım Adı": [
            "ATAK PRO SPOR KULÜBÜ  E", "İNCEK TENİS SPOR KULÜBÜ  E", 
            "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E", "TOPSPİN TENİS SPOR KULÜBÜ  E",
            "TOPSPİN KONUTKENT SPOR KULÜBÜ  E", "SETPOİNT TENİS SPOR KULÜBÜ  E",
            "EFE GÜRAY EĞİTİM VE SPOR VAKFI SPOR KULÜBÜ  E", "NEW GEN SPOR KULÜBÜ  E",
            "ATAK PRO SPOR KULÜBÜ", "İNCEK TENİS SPOR KULÜBÜ", 
            "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ", "TOPSPİN TENİS SPOR KULÜBÜ",
            "TOPSPİN KONUTKENT SPOR KULÜBÜ", "SETPOİNT TENİS SPOR KULÜBÜ", "NEW GEN SPOR KULÜBÜ"
        ]
    })

if 'grup_secimleri' not in st.session_state:
    st.session_state.grup_secimleri = pd.DataFrame([
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
        {"Grup": "ERKEK A GRUBU", "Gün": "1. Gün", "Eşleşme": "1 ve 4", "Branş": "1. Tekler", "Takım 1": "ATAK PRO SPOR KULÜBÜ  E", "Takım 2": "NEW GEN SPOR KULÜBÜ  E", "T1 Maç": 1, "T2 Maç": 0, "T1 Set": 2, "T2 Set": 0, "T1 Oyun": 12, "T2 Oyun": 4, "Tie Kazananı (Galibiyet)": "ATAK PRO SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK A GRUBU", "Gün": "1. Gün", "Eşleşme": "1 ve 4", "Branş": "2. Tekler", "Takım 1": "ATAK PRO SPOR KULÜBÜ  E", "Takım 2": "NEW GEN SPOR KULÜBÜ  E", "T1 Maç": 1, "T2 Maç": 0, "T1 Set": 2, "T2 Set": 0, "T1 Oyun": 12, "T2 Oyun": 1, "Tie Kazananı (Galibiyet)": "ATAK PRO SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK B GRUBU", "Gün": "2. Gün", "Eşleşme": "2 ve 4", "Branş": "1. Tekler", "Takım 1": "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E", "Takım 2": "EFE GÜRAY EĞİTİM VE SPOR VAKFI SPOR KULÜBÜ  E", "T1 Maç": 1, "T2 Maç": 0, "T1 Set": 2, "T2 Set": 0, "T1 Oyun": 10, "T2 Oyun": 2, "Tie Kazananı (Galibiyet)": "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E"}
    ])

# --- 2. SEKMELERİN OLUŞTURULMASI ---
sekme_havuz, sekme_gruplar, sekme_skor, sekme_siralama = st.tabs([
    "🚀 1. Takım Havuzu Girişi", 
    "👥 2. Grup Atamaları", 
    "✍️ 3. Skor Giriş Ekranı", 
    "🏆 4. Grup Sıralamaları"
])

# --- SEKME 1: TAKIM HAVUZU GİRİŞİ ---
with sekme_havuz:
    st.subheader("Turnuvaya Katılabilecek Tüm Takımların Listesi")
    st.info("💡 Gelecek turnuvalardaki yeni takımları buraya ekleyebilir, eskileri silebilirsiniz. Buraya yazdığınız isimler diğer sekmelerde otomatik açılır liste (dropdown) olacaktır.")
    
    guncel_havuz = st.data_editor(
        st.session_state.havuz_takimlari,
        num_rows="dynamic",
        use_container_width=True,
        key="havuz_editor_key"
    )
    st.session_state.havuz_takimlari = guncel_havuz
    # Açılır listeleri besleyecek ana liste
    liste_secenekleri = guncel_havuz["Takım Adı"].dropna().unique().tolist()

# --- SEKME 2: GRUP ATAMALARI ---
with sekme_gruplar:
    st.subheader("Gruplara Takım Atama Ekranı")
    st.caption("1. Sekmede tanımladığınız takımları buradan gruplara dağıtabilirsiniz.")
    
    guncel_gruplar = st.data_editor(
        st.session_state.grup_secimleri,
        column_config={
            "Grup": st.column_config.SelectboxColumn("Grup Adı", options=["ERKEK A GRUBU", "ERKEK B GRUBU", "KADIN A GRUBU", "KADIN B GRUBU"], required=True),
            "Grup Sırası": st.column_config.TextColumn("Grup Sırası", disabled=True),
            "Seçilen Takım": st.column_config.SelectboxColumn("Seçilen Takım", options=liste_secenekleri, required=True)
        },
        num_rows="dynamic",
        use_container_width=True,
        key="grup_editor_key"
    )
    st.session_state.grup_secimleri = guncel_gruplar
    # Sadece gruplara seçilmiş aktif takımlar
    aktif_turnuva_takimlari = guncel_gruplar["Seçilen Takım"].dropna().unique().tolist()

# --- SEKME 3: SKOR GİRİŞ EKRANI ---
with sekme_skor:
    st.subheader("Maç Programı ve Skor Giriş Tablosu")
    st.caption("Takım 1, Takım 2 ve Tie Kazananı sütunlarında sadece gruplara atadığınız takımlar açılır liste olarak listelenir.")
    
    guncel_skorlar = st.data_editor(
        st.session_state.skor_tablosu,
        column_config={
            "Grup": st.column_config.SelectboxColumn("Grup", options=["ERKEK A GRUBU", "ERKEK B GRUBU", "KADIN A GRUBU", "KADIN B GRUBU"]),
            "Gün": st.column_config.SelectboxColumn("Gün", options=[f"{i}. Gün" for i in range(1, 11)]),
            "Eşleşme": st.column_config.TextColumn("Eşleşme"),
            "Branş": st.column_config.SelectboxColumn("Branş", options=["1. Tekler", "2. Tekler", "Çiftler"]),
            "Takım 1": st.column_config.SelectboxColumn("Takım 1", options=aktif_turnuva_takimlari),
            "Takım 2": st.column_config.SelectboxColumn("Takım 2", options=aktif_turnuva_takimlari),
            "T1 Maç": st.column_config.NumberColumn("T1 Maç", min_value=0, max_value=1, default=0),
            "T2 Maç": st.column_config.NumberColumn("T2 Maç", min_value=0, max_value=1, default=0),
            "T1 Set": st.column_config.NumberColumn("T1 Set", min_value=0, max_value=3, default=0),
            "T2 Set": st.column_config.NumberColumn("T2 Set", min_value=0, max_value=3, default=0),
            "T1 Oyun": st.column_config.NumberColumn("T1 Oyun", min_value=0, max_value=20, default=0),
            "T2 Oyun": st.column_config.NumberColumn("T2 Oyun", min_value=0, max_value=20, default=0),
            "Tie Kazananı (Galibiyet)": st.column_config.SelectboxColumn("Tie Kazananı (Galibiyet)", options=aktif_turnuva_takimlari)
        },
        num_rows="dynamic",
        use_container_width=True,
        key="skor_editor_key"
    )
    st.session_state.skor_tablosu = guncel_skorlar

# --- SEKME 4: GRUP SIRALAMALARI ---
with sekme_siralama:
    st.subheader("Canlı Puan Durumu ve Raporlar")
    
    df_hesap = guncel_skorlar.copy()
    df_hesap = df_hesap.dropna(subset=['Takım 1', 'Takım 2'])
    
    if df_hesap.empty:
        st.warning("Sıralamaların hesaplanabilmesi için lütfen 3. Sekmeden skor girişi yapın.")
    else:
        try:
            # Sayısal alan dönüşüm güvencesi
            for col in ['T1 Maç', 'T2 Maç', 'T1 Set', 'T2 Set', 'T1 Oyun', 'T2 Oyun']:
                df_hesap[col] = pd.to_numeric(df_hesap[col], errors='coerce').fillna(0)
                
            yeni_sutunlar = ['Grup', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun', 'Galibiyet_Adayi']
            
            # Takım 1 Hesapları
            t1 = df_hesap[['Grup', 'Takım 1', 'T1 Maç', 'T2 Maç', 'T1 Set', 'T2 Set', 'T1 Oyun', 'T2 Oyun', 'Tie Kazananı (Galibiyet)']].copy()
            t1.columns = yeni_sutunlar
            t1['Galibiyet'] = (t1['Galibiyet_Adayi'] == t1['Takım Adı']).astype(int)
            
            # Takım 2 Hesapları
            t2 = df_hesap[['Grup', 'Takım 2', 'T2 Maç', 'T1 Maç', 'T2 Set', 'T1 Set', 'T2 Oyun', 'T1 Oyun', 'Tie Kazananı (Galibiyet)']].copy()
            t2.columns = yeni_sutunlar
            t2['Galibiyet'] = (t2['Galibiyet_Adayi'] == t2['Takım Adı']).astype(int)
            
            # Birleştirme
            birlikte = pd.concat([t1, t2], ignore_index=True)
            siralama = birlikte.groupby(['Grup', 'Takım Adı']).sum(numeric_only=True).reset_index()
            
            # Excel Kurallarına Göre Averajlar
            siralama['Maç Averajı'] = siralama['Aldığı Maç'] - siralama['Verdiği Maç']
            siralama['Set Averajı'] = siralama['Aldığı Set'] - siralama['Verdiği Set']
            siralama['Oyun Averajı'] = siralama['Aldığı Oyun'] - siralama['Verdiği Oyun']
            
            # Öncelikli Sıralama
            siralama = siralama.sort_values(
                by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'],
                ascending=[True, False, False, False, False]
            )
            
            siralama = siralama[[
                'Grup', 'Galibiyet', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Maç Averajı',
                'Aldığı Set', 'Verdiği Set', 'Set Averajı', 'Aldığı Oyun', 'Verdiği Oyun', 'Oyun Averajı'
            ]]
            
            # Her grubu ayrı bir tablo olarak basıyoruz
            for grup_ismi in siralama['Grup'].unique():
                st.markdown(f"### 🏆 {grup_ismi} SIRALAMASI")
                grup_df = siralama[siralama['Grup'] == grup_ismi].drop(columns=['Grup']).reset_index(drop=True)
                grup_df.index = grup_df.index + 1
                st.dataframe(grup_df, use_container_width=True)
                st.markdown("---")
                
        except Exception as e:
            st.error(f"Sıralama motorunda bir hata oluştu: {e}")
