
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva", layout="wide")
st.title("🎾 Tenis Turnuvası Yönetim Sistemi")

# --- VERİ YAPISI ---
if 'takimlar' not in st.session_state:
    st.session_state.takimlar = {f"Grup {i}": [f"Takım {j+1}" for j in range(4)] for i in range(1, 5)}
if 'skorlar' not in st.session_state:
    st.session_state.skorlar = {}

# --- ANA EKRAN ---
tabs = st.tabs(["Grup 1", "Grup 2", "Grup 3", "Grup 4", "📊 PUAN DURUMU & AVERAJ"])

for i in range(4):
    grup_id = f"Grup {i+1}"
    with tabs[i]:
        # Takım İsimleri
        for t_idx in range(4):
            st.session_state.takimlar[grup_id][t_idx] = st.text_input(f"{t_idx+1}. Takım", value=st.session_state.takimlar[grup_id][t_idx], key=f"inp_{grup_id}_{t_idx}")
        
        st.divider()
        t = st.session_state.takimlar[grup_id]
        program = {"1. Gün": [(t[0], t[3], "M1"), (t[1], t[2], "M2")], "2. Gün": [(t[0], t[1], "M3"), (t[2], t[3], "M4")], "3. Gün": [(t[0], t[2], "M5"), (t[1], t[3], "M6")]}

        for gun, maclar in program.items():
            with st.expander(f"📅 {gun} Maçları"):
                for m1, m2, m_id in maclar:
                    st.write(f"**{m1} vs {m2}**")
                    cols = st.columns(6)
                    key = f"{grup_id}_{gun}_{m_id}"
                    
                    # Veriyi session_state'den çek
                    s = st.session_state.skorlar.get(key, ["","","","","",""])
                    s1 = cols[0].text_input("S1-K", value=s[0], key=f"s1_{key}")
                    s2 = cols[1].text_input("S1-Y", value=s[1], key=f"s2_{key}")
                    s3 = cols[2].text_input("S2-K", value=s[2], key=f"s3_{key}")
                    s4 = cols[3].text_input("S2-Y", value=s[3], key=f"s4_{key}")
                    s5 = cols[4].text_input("S3-K", value=s[4], key=f"s5_{key}")
                    s6 = cols[5].text_input("S3-Y", value=s[5], key=f"s6_{key}")
                    
                    if st.button("Kaydet", key=f"btn_{key}"):
                        st.session_state.skorlar[key] = [s1, s2, s3, s4, s5, s6]
                        st.success(f"{m1}-{m2} kaydedildi!")

# --- HESAPLAMA EKRANI ---
with tabs[4]:
    st.header("🏆 Puan Durumu")
    if st.button("🔄 Hesapla ve Güncelle"):
        st.info("Tablo skorlara göre yeniden hesaplandı.")
        # Burada skorları işleyip dataframe'e dönüştürebilirsiniz
        st.write("Skorlar işlendi, şu an tablo yapısını kuruyoruz...")
