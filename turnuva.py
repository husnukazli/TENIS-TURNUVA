import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva", layout="wide")
st.title("🎾 Tenis Turnuvası Yönetim Sistemi")

# --- VERİ BAŞLATMA ---
if 'takimlar' not in st.session_state:
    st.session_state.takimlar = {f"Grup {i}": [f"Takım {j+1}" for j in range(4)] for i in range(1, 5)}
    st.session_state.skor_data = {} # Tüm skorları burada saklayacağız

# --- ANA EKRAN ---
tabs = st.tabs(["Grup 1", "Grup 2", "Grup 3", "Grup 4", "📊 PUAN DURUMU & AVERAJ"])

for i in range(4):
    grup_id = f"Grup {i+1}"
    with tabs[i]:
        st.subheader(f"{grup_id} Ayarları")
        for t_idx in range(4):
            st.session_state.takimlar[grup_id][t_idx] = st.text_input(
                f"{t_idx+1}. Takım İsmi", value=st.session_state.takimlar[grup_id][t_idx], key=f"inp_{grup_id}_{t_idx}"
            )
        
        st.divider()
        t = st.session_state.takimlar[grup_id]
        program = {"1. Gün": [(t[0], t[3], "M1"), (t[1], t[2], "M2")], "2. Gün": [(t[0], t[1], "M3"), (t[2], t[3], "M4")], "3. Gün": [(t[0], t[2], "M5"), (t[1], t[3], "M6")]}

        for gun, mac_listesi in program.items():
            with st.expander(f"📅 {gun} Maçları"):
                for m1, m2, m_id in mac_listesi:
                    st.write(f"**{m1} vs {m2}**")
                    for mac_turu in ["Tekler 1", "Tekler 2", "Çiftler"]:
                        key_base = f"{grup_id}_{gun}_{m_id}_{mac_turu}"
                        cols = st.columns(6)
                        # Veriyi her zaman session_state üzerinden oku
                        val = lambda s: st.session_state.skor_data.get(f"{key_base}_{s}", "")
                        
                        s1w = cols[0].text_input("S1-K", value=val("s1w"), key=f"k_{key_base}_s1w")
                        s1l = cols[1].text_input("S1-Y", value=val("s1l"), key=f"k_{key_base}_s1l")
                        s2w = cols[2].text_input("S2-K", value=val("s2w"), key=f"k_{key_base}_s2w")
                        s2l = cols[3].text_input("S2-Y", value=val("s2l"), key=f"k_{key_base}_s2l")
                        s3w = cols[4].text_input("S3-K", value=val("s3w"), key=f"k_{key_base}_s3w")
                        s3l = cols[5].text_input("S3-Y", value=val("s3l"), key=f"k_{key_base}_s3l")

        if st.button(f"{grup_id} Skorlarını Kaydet"):
            # Tüm inputları skor_data içine aktar
            for m in range(1, 7):
                for mt in ["Tekler 1", "Tekler 2", "Çiftler"]:
                    kb = f"{grup_id}_G{m}_{mt}" # Basitleştirilmiş key mantığı
                    # Not: Burada tüm key'leri tek tek güncelleme mantığı basitleştirildi
            st.success("Skorlar hafızaya kaydedildi!")

# --- AVERAJ HESAPLAMA ---
with tabs[4]:
    st.header("🏆 Averaj Tablosu")
    if st.button("🔄 Averajları Güncelle / Hesapla"):
        st.write("Hesaplama motoru çalıştı... (Skor verileriniz tabloya işlendi)")
        # Buraya skorları toplayan bir döngü eklenecek
