import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva Yönetimi", layout="wide")
st.title("🎾 Tenis Turnuvası Yönetim Sistemi")

# --- KALICI HAFIZA ---
if 'skorlar' not in st.session_state: st.session_state.skorlar = {}
if 'takimlar' not in st.session_state:
    st.session_state.takimlar = {f"Grup {i}": [f"Takım {j+1}" for j in range(4)] for i in range(1, 5)}

tabs = st.tabs(["Grup 1", "Grup 2", "Grup 3", "Grup 4", "📊 PUAN DURUMU & YEDEKLEME"])

# --- GRUP VE MAÇ EKRANLARI ---
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
                        if key not in st.session_state.skorlar: st.session_state.skorlar[key] = ["0"]*6
                        cols = st.columns(6)
                        for idx in range(6):
                            st.session_state.skorlar[key][idx] = cols[idx].text_input(f"P{idx+1}", value=st.session_state.skorlar[key][idx], key=f"{key}_{idx}")

# --- PUAN DURUMU VE YEDEKLEME ---
with tabs[4]:
    st.header("🏆 Puan Durumu ve Veri Yedekleme")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Kayıtlı dosyayı yükle", type="csv")
        if uploaded_file is not None:
            df_y = pd.read_csv(uploaded_file, index_col=0)
            st.session_state.skorlar = {idx: list(row) for idx, row in df_y.iterrows()}
            st.info("Veri yüklendi! Lütfen F5 ile sayfayı yenileyin.")
    with col2:
        df_yedek = pd.DataFrame.from_dict(st.session_state.skorlar, orient='index')
        csv = df_yedek.to_csv()
        st.download_button("📥 Verileri İndir", csv, "turnuva_yedek.csv", "text/csv")
        
    st.divider()
    
    secilen_grup = st.selectbox("Grup Seçiniz:", ["Grup 1", "Grup 2", "Grup 3", "Grup 4"])
    takimlar = st.session_state.takimlar[secilen_grup]
    df = pd.DataFrame(0, index=takimlar, columns=["Seri Gal.", "Alt Maç Alınan", "Alt Maç Verilen", "Set Alınan", "Set Verilen", "Set Averajı", "Oyun Alınan", "Oyun Verilen", "Oyun Averajı"])
    
    for key, vals in st.session_state.skorlar.items():
        if secilen_grup in key:
            try:
                n = [int(str(v)) for v in vals]
                t1_sets = (1 if n[0]>n[1] else 0) + (1 if n[2]>n[3] else 0) + (1 if n[4]>n[5] else 0)
                t2_sets = (1 if n[1]>n[0] else 0) + (1 if n[3]>n[2] else 0) + (1 if n[5]>n[4] else 0)
                t1, t2 = key.split('_')[2], key.split('_')[3]
                if t1 in df.index:
                    df.loc[t1, ["Alt Maç Alınan", "Alt Maç Verilen"]] += [1 if t1_sets > t2_sets else 0, 1 if t2_sets > t1_sets else 0]
                    df.loc[t1, ["Set Alınan", "Set Verilen", "Oyun Alınan", "Oyun Verilen"]] += [t1_sets, t2_sets, sum(n[0::2]), sum(n[1::2])]
                    if t1_sets > t2_sets and df.loc[t1, "Alt Maç Alınan"] >= 2: df.loc[t1, "Seri Gal."] = 1
                if t2 in df.index:
                    df.loc[t2, ["Alt Maç Alınan", "Alt Maç Verilen"]] += [1 if t2_sets > t1_sets else 0, 1 if t1_sets > t2_sets else 0]
                    df.loc[t2, ["Set Alınan", "Set Verilen", "Oyun Alınan", "Oyun Verilen"]] += [t2_sets, t1_sets, sum(n[1::2]), sum(n[0::2])]
                    if t2_sets > t1_sets and df.loc[t2, "Alt Maç Alınan"] >= 2: df.loc[t2, "Seri Gal."] = 1
            except: continue
    df["Set Averajı"] = df["Set Alınan"] - df["Set Verilen"]
    df["Oyun Averajı"] = df["Oyun Alınan"] - df["Oyun Verilen"]
    st.table(df.sort_values(by=["Seri Gal.", "Set Averajı", "Oyun Averajı"], ascending=False))
