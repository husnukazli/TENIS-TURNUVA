import streamlit as st
import pandas as pd
import ast

st.set_page_config(page_title="Tenis Turnuva", layout="wide")
st.title("🎾 Kalıcı Turnuva Yönetim Sistemi")

# --- TEK BİR MERKEZİ HAFIZA ---
if 'data' not in st.session_state:
    st.session_state.data = {
        'takimlar': {f"Grup {i}": [f"Takım {j+1}" for j in range(4)] for i in range(1, 5)},
        'skorlar': {}
    }

# --- YÜKLEME VE KAYDETME PANELİ (EN TEPEDE) ---
with st.sidebar:
    st.header("💾 Veri Yönetimi")
    # Kaydetme
    csv = str(st.session_state.data)
    st.download_button("📥 Tüm Veriyi İndir", csv, "turnuva_tum_veri.txt", "text/plain")
    
    # Yükleme
    uploaded_file = st.file_uploader("Dosyadan Geri Yükle", type="txt")
    if uploaded_file is not None:
        try:
            content = uploaded_file.read().decode("utf-8")
            st.session_state.data = ast.literal_eval(content)
            st.success("Tüm veriler başarıyla yüklendi!")
        except:
            st.error("Dosya geçersiz!")

tabs = st.tabs(["Grup 1", "Grup 2", "Grup 3", "Grup 4", "📊 PUAN DURUMU"])

# --- MAÇ VE İSİM GİRİŞLERİ ---
for i in range(4):
    grup_id = f"Grup {i+1}"
    with tabs[i]:
        st.subheader(f"{grup_id} Ayarları")
        for t_idx in range(4):
            st.session_state.data['takimlar'][grup_id][t_idx] = st.text_input(
                f"{t_idx+1}. Takım Adı", 
                value=st.session_state.data['takimlar'][grup_id][t_idx], 
                key=f"isim_{grup_id}_{t_idx}"
            )
        
        t = st.session_state.data['takimlar'][grup_id]
        program = {"1. Gün": [(t[0], t[3]), (t[1], t[2])], "2. Gün": [(t[0], t[1]), (t[2], t[3])], "3. Gün": [(t[0], t[2]), (t[1], t[3])]}
        
        for gun, maclar in program.items():
            with st.expander(f"📅 {gun} Maçları"):
                for m1, m2 in maclar:
                    st.write(f"**{m1} vs {m2}**")
                    for tur in ["Tekler 1", "Tekler 2", "Çiftler"]:
                        key = f"{grup_id}_{gun}_{m1}_{m2}_{tur}"
                        if key not in st.session_state.data['skorlar']: st.session_state.data['skorlar'][key] = ["0"]*6
                        cols = st.columns(6)
                        for idx in range(6):
                            st.session_state.data['skorlar'][key][idx] = cols[idx].text_input(
                                f"S{idx+1}", value=st.session_state.data['skorlar'][key][idx], key=f"{key}_{idx}"
                            )

# --- PUAN TABLOSU ---
with tabs[4]:
    secilen = st.selectbox("Grup Seçin", ["Grup 1", "Grup 2", "Grup 3", "Grup 4"])
    df = pd.DataFrame(0, index=st.session_state.data['takimlar'][secilen], columns=["Galibiyet", "Set Averajı"])
    for key, vals in st.session_state.data['skorlar'].items():
        if secilen in key:
            n = [int(v) if v.isdigit() else 0 for v in vals]
            t1_sets = (1 if n[0]>n[1] else 0) + (1 if n[2]>n[3] else 0) + (1 if n[4]>n[5] else 0)
            t2_sets = (1 if n[1]>n[0] else 0) + (1 if n[3]>n[2] else 0) + (1 if n[5]>n[4] else 0)
            t1, t2 = key.split('_')[2], key.split('_')[3]
            if t1 in df.index: df.loc[t1, "Galibiyet"] += (1 if t1_sets > t2_sets else 0)
            if t2 in df.index: df.loc[t2, "Galibiyet"] += (1 if t2_sets > t1_sets else 0)
    st.table(df)
    df = pd.DataFrame(0, index=st.session_state.data['takimlar'][secilen], columns=["Galibiyet", "Set Averajı"])
    for key, vals in st.session_state.data['skorlar'].items():
        if secilen in key:
            n = [int(v) if v.isdigit() else 0 for v in vals]
            t1_sets = (1 if n[0]>n[1] else 0) + (1 if n[2]>n[3] else 0) + (1 if n[4]>n[5] else 0)
            t2_sets = (1 if n[1]>n[0] else 0) + (1 if n[3]>n[2] else 0) + (1 if n[5]>n[4] else 0)
            t1, t2 = key.split('_')[2], key.split('_')[3]
            if t1 in df.index: df.loc[t1, "Galibiyet"] += (1 if t1_sets > t2_sets else 0)
            if t2 in df.index: df.loc[t2, "Galibiyet"] += (1 if t2_sets > t1_sets else 0)
    st.table(df)
