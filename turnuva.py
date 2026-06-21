import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva", layout="wide")
st.title("🎾 Tenis Turnuvası Yönetim Sistemi")

# --- KALICI HAFIZA ---
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
                        
                        # Skor verilerini çek
                        if key not in st.session_state.skorlar:
                            st.session_state.skorlar[key] = ["", "", "", "", "", ""]
                        
                        cols = st.columns(6)
                        for idx in range(6):
                            # Her kutucuk kendi değerini session_state'den alır
                            val_key = f"{key}_{idx}"
                            if val_key not in st.session_state:
                                st.session_state[val_key] = st.session_state.skorlar[key][idx]
                            
                            def update_skor(k=key, i=idx, vk=val_key):
                                st.session_state.skorlar[k][i] = st.session_state[vk]
                            
                            cols[idx].text_input(f"P{idx+1}", key=val_key, on_change=update_skor)

# --- PUAN DURUMU ---
with tabs[4]:
    st.header("🏆 Puan Durumu")
    secilen_grup = st.selectbox("Grup Seçiniz:", ["Grup 1", "Grup 2", "Grup 3", "Grup 4"])
    takimlar = st.session_state.takimlar[secilen_grup]
    df = pd.DataFrame(0, index=takimlar, columns=["Seri Gal.", "Alt Maç Alınan", "Alt Maç Verilen"])
    
    for key, vals in st.session_state.skorlar.items():
        if secilen_grup in key:
            try:
                n = [int(v) if v.isdigit() else 0 for v in vals]
                t1_sets = (1 if n[0]>n[1] else 0) + (1 if n[2]>n[3] else 0) + (1 if n[4]>n[5] else 0)
                t2_sets = (1 if n[1]>n[0] else 0) + (1 if n[3]>n[2] else 0) + (1 if n[5]>n[4] else 0)
                
                parts = key.split('_')
                t1, t2 = parts[2], parts[3]
                
                if t1 in df.index:
                    if t1_sets > t2_sets: 
                        df.loc[t1, "Alt Maç Alınan"] += 1
                        if df.loc[t1, "Alt Maç Alınan"] >= 2: df.loc[t1, "Seri Gal."] = 1
                    else: df.loc[t1, "Alt Maç Verilen"] += 1
                if t2 in df.index:
                    if t2_sets > t1_sets: 
                        df.loc[t2, "Alt Maç Alınan"] += 1
                        if df.loc[t2, "Alt Maç Alınan"] >= 2: df.loc[t2, "Seri Gal."] = 1
                    else: df.loc[t2, "Alt Maç Verilen"] += 1
            except: continue
    st.table(df)
