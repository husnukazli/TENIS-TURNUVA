import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva", layout="wide")
st.title("🎾 Tenis Turnuvası Yönetim Sistemi")

# --- VERİ BAŞLATMA ---
if 'skorlar' not in st.session_state: st.session_state.skorlar = {}
if 'takimlar' not in st.session_state:
    st.session_state.takimlar = {f"Grup {i}": [f"Takım {j+1}" for j in range(4)] for i in range(1, 5)}

tabs = st.tabs(["Grup 1", "Grup 2", "Grup 3", "Grup 4", "📊 PUAN DURUMU & AVERAJ"])

# --- GRUP SAYFALARI ---
for i in range(4):
    grup_id = f"Grup {i+1}"
    with tabs[i]:
        st.subheader(f"{grup_id} Ayarları")
        for t_idx in range(4):
            st.session_state.takimlar[grup_id][t_idx] = st.text_input(f"{t_idx+1}. Takım", value=st.session_state.takimlar[grup_id][t_idx], key=f"inp_{grup_id}_{t_idx}")
        
        t = st.session_state.takimlar[grup_id]
        program = {"1. Gün": [(t[0], t[3]), (t[1], t[2])], "2. Gün": [(t[0], t[1]), (t[2], t[3])], "3. Gün": [(t[0], t[2]), (t[1], t[3])]}
        
        for gun, maclar in program.items():
            with st.expander(f"📅 {gun} Maçları"):
                for m1, m2 in maclar:
                    st.markdown(f"**{m1} vs {m2}**")
                    for tur in ["Tekler 1", "Tekler 2", "Çiftler"]:
                        key = f"{grup_id}_{gun}_{m1}_{m2}_{tur}"
                        cols = st.columns([1,1,1,1,1,1,2])
                        s = st.session_state.skorlar.get(key, ["","","","","",""])
                        v = [cols[j].text_input(f"S{j//2+1}{'K' if j%2==0 else 'Y'}", value=s[j], key=f"s{j}_{key}") for j in range(6)]
                        if cols[6].button("💾 Kaydet", key=f"btn_{key}"):
                            st.session_state.skorlar[key] = v
                            st.toast(f"{tur} kaydedildi!")

# --- PUAN DURUMU & AVERAJ SEKMESİ ---
with tabs[4]:
    st.header("🏆 Gruplara Göre Puan Durumu")
    secilen_grup = st.selectbox("Grup Seçiniz:", ["Grup 1", "Grup 2", "Grup 3", "Grup 4"])
    
    if st.button("🔄 Tabloyu Güncelle"):
        takimlar = st.session_state.takimlar[secilen_grup]
        # Puan tablosunu sıfırdan oluştur
        df = pd.DataFrame(0, index=takimlar, columns=["Galibiyet", "Mağlubiyet", "Alınan Set", "Verilen Set", "Alınan Oyun", "Verilen Oyun"])
        
        # Skorları işle
        for key, vals in st.session_state.skorlar.items():
            if secilen_grup in key:
                # Basit bir galibiyet mantığı: Skorlar doluysa ve ilk takım (S1-K) büyükse
                try:
                    t1_vals = [int(vals[0]), int(vals[2]), int(vals[4])]
                    t2_vals = [int(vals[1]), int(vals[3]), int(vals[5])]
                    # Bu noktada takım isimlerini maç anahtarından çıkarıp tabloya işleyebiliriz
                    # (Şu anki basit gösterim için tabloyu boş dönecek, 
                    # bir sonraki adımda isim eşleştirmesini tam oturtalım)
                except: continue
        
        st.table(df)
        st.caption("Not: Tablonun tam dolması için maçların kazananlarını sistemin algılaması gerekiyor.")
