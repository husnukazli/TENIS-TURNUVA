import streamlit as st
import pandas as pd

# Sayfa Genişlik Ayarı (En üstte olmalı)
st.set_page_config(page_title="Tenis Turnuva Yönetim Sistemi", layout="wide")
st.title("🎾 Profesyonel Tenis Turnuvası Dinamik Yönetim Sistemi")

# --- 1. HAFIZA (SESSION STATE) KURULUMU ---
# Sistem ilk açıldığında Excel'inizdeki orijinal takımları ve maç şablonunu yüklüyoruz

if 'tum_takimlar' not in st.session_state:
    st.session_state.tum_takimlar = [
        "ATAK PRO SPOR KULÜBÜ  E", "İNCEK TENİS SPOR KULÜBÜ  E", 
        "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E", "TOPSPİN TENİS SPOR KULÜBÜ  E",
        "TOPSPİN KONUTKENT SPOR KULÜBÜ  E", "SETPOİNT TENİS SPOR KULÜBÜ  E",
        "EFE GÜRAY EĞİTİM VE SPOR VAKFI SPOR KULÜBÜ  E", "NEW GEN SPOR KULÜBÜ  E",
        "ATAK PRO SPOR KULÜBÜ", "İNCEK TENİS SPOR KULÜBÜ", 
        "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ", "TOPSPİN TENİS SPOR KULÜBÜ",
        "TOPSPİN KONUTKENT SPOR KULÜBÜ", "SETPOİNT TENİS SPOR KULÜBÜ", "NEW GEN SPOR KULÜBÜ"
    ]

if 'grup_secimleri' not in st.session_state:
    # Orijinal Excel'inizdeki ilk grup eşleşme şablonu
    st.session_state.grup_secimleri = pd.DataFrame([
        {"Grup": "ERKEK A GRUBU", "Sıra": "1. Takım", "Seçilen Takım": "ATAK PRO SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK A GRUBU", "Sıra": "2. Takım", "Seçilen Takım": "TOPSPİN TENİS SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK A GRUBU", "Sıra": "3. Takım", "Seçilen Takım": "TOPSPİN KONUTKENT SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK A GRUBU", "Sıra": "4. Takım", "Seçilen Takım": "NEW GEN SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK B GRUBU", "Sıra": "1. Takım", "Seçilen Takım": "İNCEK TENİS SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK B GRUBU", "Sıra": "2. Takım", "Seçilen Takım": "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK B GRUBU", "Sıra": "3. Takım", "Seçilen Takım": "SETPOİNT TENİS SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK B GRUBU", "Sıra": "4. Takım", "Seçilen Takım": "EFE GÜRAY EĞİTİM VE SPOR VAKFI SPOR KULÜBÜ  E"},
    ])

if 'skor_tablosu' not in st.session_state:
    # Başlangıç maç programı şablonu
    st.session_state.skor_tablosu = pd.DataFrame([
        {"Grup": "ERKEK A GRUBU", "Gün": "1. Gün", "Eşleşme": "1 ve 4", "Branş": "1. Tekler", "Takım 1": "ATAK PRO SPOR KULÜBÜ  E", "Takım 2": "NEW GEN SPOR KULÜBÜ  E", "T1 Set": 2, "T2 Set": 0, "T1 Maç": 1, "T2 Maç": 0, "T1 Oyun": 12, "T2 Oyun": 4, "Tie Kazananı": "ATAK PRO SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK A GRUBU", "Gün": "1. Gün", "Eşleşme": "1 ve 4", "Branş": "2. Tekler", "Takım 1": "ATAK PRO SPOR KULÜBÜ  E", "Takım 2": "NEW GEN SPOR KULÜBÜ  E", "T1 Set": 2, "T2 Set": 0, "T1 Maç": 1, "T2 Maç": 0, "T1 Oyun": 12, "T2 Oyun": 1, "Tie Kazananı": "ATAK PRO SPOR KULÜBÜ  E"},
        {"Grup": "ERKEK B GRUBU", "Gün": "2. Gün", "Eşleşme": "2 ve 4", "Branş": "1. Tekler", "Takım 1": "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E", "Takım 2": "EFE GÜRAY EĞİTİM VE SPOR VAKFI SPOR KULÜBÜ  E", "T1 Set": 2, "T2 Set": 0, "T1 Maç": 1, "T2 Maç": 0, "T1 Oyun": 10, "T2 Oyun": 2, "Tie Kazananı": "ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ  E"}
    ])

# --- 2. SEKME YAPISI ---
sekme1, sekme2, sekme3 = st.tabs(["👥 1. Sekme: Grup Girişleri", "✍️ 2. Sekme: Skor Giriş Ekranı", "🏆 3. Sekme: Grup Sıralamaları"])

# --- 1. SEKME: GRUP GİRİŞLERİ ---
with sekme1:
    st.subheader("Grup Takım Belirleme Ekranı")
    st.caption("Aşağıdaki tabloda gruplara katılacak takımları yanlarındaki açılır listeden (dropdown) seçebilirsiniz.")
    
    # Takım havuzunu dropdown seçeneği olarak data_editor'e bağlıyoruz
    guncel_gruplar = st.data_editor(
        st.session_state.grup_secimleri,
        column_config={
            "Grup": st.column_config.SelectboxColumn("Grup Adı", options=["ERKEK A GRUBU", "ERKEK B GRUBU", "KADIN A GRUBU", "KADIN B GRUBU"], required=True),
            "Sıra": st.column_config.TextColumn("Sıra", disabled=True),
            "Seçilen Takım": st.column_config.SelectboxColumn("Seçilen Takım (Açılır Liste)", options=st.session_state.tum_takimlar, required=True)
        },
        num_rows="dynamic",
        use_container_width=True,
        key="grup_editor"
    )
    st.session_state.grup_secimleri = guncel_gruplar

    # Aktif seçilmiş takımları dinamik liste olarak kaydet (2. sekmede kullanmak üzere)
    aktif_takimlar = guncel_gruplar["Seçilen Takım"].dropna().unique().tolist()
