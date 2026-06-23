import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva Yönetimi", layout="wide")
st.title("🎾 Tenis Turnuvası Yönetim Sistemi")

# --- KALICI HAFIZA ---
if 'skorlar' not in st.session_state: st.session_state.skorlar = {}
if 'takimlar' not in st.session_state:
    st.session_state.takimlar = {f"Grup {i}": [f"Takım {j+1}" for j in range(4)] for i in range(1, 5)}

# Sekmeleri tanımla
tabs = st.tabs(["Grup 1", "Grup 2", "Grup 3", "Grup 4", "📊 PUAN DURUMU & AVERAJ"])

# --- GRUP VE MAÇ EKRANLARI (GÜNCEL HATA GİDERİCİ) ---
for i in range(4):
    grup_id = f"Grup {i+1}"
    with tabs[i]:
        st.subheader(f"{grup_id} Ayarları")
        for t_idx in range(4):
            # Buradaki key yapısını sabitledik
            st.session_state.takimlar[grup_id][t_idx] = st.text_input(f"{t_idx+1}. Takım", value=st.session_state.takimlar[grup_id][t_idx], key=f"inp_{grup_id}_{t_idx}")
        
        t = st.session_state.takimlar[grup_id]
        program = {"1. Gün": [(t[0], t[3]), (t[1], t[2])], "2. Gün": [(t[0], t[1]), (t[2], t[3])], "3. Gün": [(t[0], t[2]), (t[1], t[3])]}
        
        for gun, maclar in program.items():
            with st.expander(f"📅 {gun} Maçları"):
                for m1, m2 in maclar:
                    st.markdown(f"#### {m1} vs {m2}")
                    for tur in ["Tekler 1", "Tekler 2", "Çiftler"]:
                        st.markdown(f"**{tur}**")
                        key = f"{grup_id}_{gun}_{m1}_{m2}_{tur}"
                        if key not in st.session_state.skorlar: st.session_state.skorlar[key] = ["0","0","0","0","0","0"]
                        
                        cols = st.columns(6)
                        # DİKKAT: Her kutucuk için session_state'deki son değeri doğrudan value'ya atıyoruz
                        # Bu sayede dosya yüklendiğinde kutucuklar anında güncellenecek
                        cols[0].text_input("1.Set(K)", value=st.session_state.skorlar[key][0], key=f"{key}_0")
                        cols[1].text_input("1.Set(V)", value=st.session_state.skorlar[key][1], key=f"{key}_1")
                        cols[2].text_input("2.Set(K)", value=st.session_state.skorlar[key][2], key=f"{key}_2")
                        cols[3].text_input("2.Set(V)", value=st.session_state.skorlar[key][3], key=f"{key}_3")
                        cols[4].text_input("3.Set(K)", value=st.session_state.skorlar[key][4], key=f"{key}_4")
                        cols[5].text_input("3.Set(V)", value=st.session_state.skorlar[key][5], key=f"{key}_5")
                        
                        # Kullanıcının girdiği yeni değeri session_state'e eşitleyelim
                        for idx in range(6):
                            st.session_state.skorlar[key][idx] = st.session_state[f"{key}_{idx}"]

# --- PUAN DURUMU ---
with tabs[4]:
    # --- YEDEKLEME VE GERİ YÜKLEME ---
    col_a, col_b = st.columns(2)
    
    # 1. KAYDETME
    with col_a:
        df_yedek = pd.DataFrame.from_dict({'skorlar': [st.session_state.skorlar], 'takimlar': [st.session_state.takimlar]})
        csv = df_yedek.to_csv(index=False)
        st.download_button("💾 Turnuvayı Kaydet", csv, "turnuva_verisi.csv", "text/csv")
    
    # 2. GERİ YÜKLEME
    with col_b:
        uploaded_file = st.file_uploader("Kayıtlı dosyayı yükle", type="csv")
        if uploaded_file is not None:
            try:
                df_load = pd.read_csv(uploaded_file)
                import ast
                st.session_state.skorlar = ast.literal_eval(df_load['skorlar'][0])
                st.session_state.takimlar = ast.literal_eval(df_load['takimlar'][0])
                st.success("Veriler başarıyla yüklendi! F5 yapın.")
            except:
                st.error("Dosya okunamadı!")

    st.divider()
    st.header("🏆 Detaylı Puan Durumu")
    # ... (Puan tablosu kodunuzun geri kalanı burada aynı şekilde duruyor) ...
    # ... (Geri kalan kodunuz aynı kalıyor) ...
    secilen_grup = st.selectbox("Grup Seçiniz:", ["Grup 1", "Grup 2", "Grup 3", "Grup 4"])
    takimlar = st.session_state.takimlar[secilen_grup]
    cols = ["Seri Gal.", "Alt Maç Alınan", "Alt Maç Verilen", "Set Alınan", "Set Verilen", "Set Averajı", "Oyun Alınan", "Oyun Verilen", "Oyun Averajı"]
    df = pd.DataFrame(0, index=takimlar, columns=cols)
    
    for key, vals in st.session_state.skorlar.items():
        if secilen_grup in key:
            try:
                n = [int(v) if v.isdigit() else 0 for v in vals]
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
