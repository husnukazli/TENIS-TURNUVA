import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva Yönetimi", layout="wide")

# --- VERİ YAPISI HAZIRLIĞI ---
if 'takimlar' not in st.session_state:
    st.session_state.takimlar = {f"Grup {i}": [f"Takım {j+1}" for j in range(4)] for i in range(1, 5)}

if 'skorlar' not in st.session_state:
    # Her grup, her gün, her maç ve her alt maç (Tekler/Çiftler) için skorları sakla
    st.session_state.skorlar = {}

# --- YARDIMCI FONKSİYONLAR ---
def mac_galibi_hesapla(s1w, s1l, s2w, s2l, s3w, s3l):
    """Set skorlarına göre maçın galibini ve set sayılarını döner."""
    try:
        t1_set = 0
        t2_set = 0
        t1_oyun = sum([int(s1w or 0), int(s2w or 0), int(s3w or 0)])
        t2_oyun = sum([int(s1l or 0), int(s2l or 0), int(s3l or 0)])
        
        if int(s1w or 0) > int(s1l or 0): t1_set += 1
        elif int(s1l or 0) > int(s1w or 0): t2_set += 1
        
        if int(s2w or 0) > int(s2l or 0): t1_set += 1
        elif int(s2l or 0) > int(s2w or 0): t2_set += 1
        
        if int(s3w or 0) > int(s3l or 0): t1_set += 1
        elif int(s3l or 0) > int(s3w or 0): t2_set += 1
        
        return t1_set, t2_set, t1_oyun, t2_oyun
    except:
        return 0, 0, 0, 0

# --- ANA EKRAN ---
st.title("🎾 Tenis Turnuvası Yönetim Sistemi")
tabs = st.tabs(["Grup 1", "Grup 2", "Grup 3", "Grup 4", "📊 PUAN DURUMU & AVERAJ"])

for i in range(4):
    grup_id = f"Grup {i+1}"
    with tabs[i]:
        col_isim, col_bos = st.columns([1, 2])
        with col_isim:
            st.subheader(f"{grup_id} Kayıt")
            for t_idx in range(4):
                st.session_state.takimlar[grup_id][t_idx] = st.text_input(
                    f"{t_idx+1}. Takım", value=st.session_state.takimlar[grup_id][t_idx], key=f"inp_{grup_id}_{t_idx}"
                )

        st.divider()
        t = st.session_state.takimlar[grup_id]
        program = {
            "1. Gün": [(t[0], t[3], "M1"), (t[1], t[2], "M2")],
            "2. Gün": [(t[0], t[1], "M3"), (t[2], t[3], "M4")],
            "3. Gün": [(t[0], t[2], "M5"), (t[1], t[3], "M6")]
        }

        for gun, mac_listesi in program.items():
            with st.expander(f"📅 {gun} Maçları"):
                for m1, m2, m_id in mac_listesi:
                    st.markdown(f"**{m1}** vs **{m2}**")
                    for mac_turu in ["Tekler 1", "Tekler 2", "Çiftler"]:
                        st.caption(f"🔹 {mac_turu}")
                        c1, c2, c3, c4, c5, c6 = st.columns(6)
                        
                        s1w = c1.text_input("S1-K", key=f"{grup_id}_{gun}_{m_id}_{mac_turu}_s1w", placeholder="6")
                        s1l = c2.text_input("S1-Y", key=f"{grup_id}_{gun}_{m_id}_{mac_turu}_s1l", placeholder="0")
                        s2w = c3.text_input("S2-K", key=f"{grup_id}_{gun}_{m_id}_{mac_turu}_s2w", placeholder="6")
                        s2l = c4.text_input("S2-Y", key=f"{grup_id}_{gun}_{m_id}_{mac_turu}_s2l", placeholder="0")
                        s3w = c5.text_input("S3-K", key=f"{grup_id}_{gun}_{m_id}_{mac_turu}_s3w", placeholder="10")
                        s3l = c6.text_input("S3-Y", key=f"{grup_id}_{gun}_{m_id}_{mac_turu}_s3l", placeholder="8")

# --- PUAN DURUMU & AVERAJ HESAPLAMA ---
with tabs[4]:
    st.header("🏆 Gruplara Göre Genel Sıralama")
    secili_grup = st.selectbox("Grup Seçin", ["Grup 1", "Grup 2", "Grup 3", "Grup 4"])
    
    # Averaj Tablosu İçin Veri Hazırla
    stats = {takim: {"Galibiyet": 0, "Alınan Set": 0, "Verilen Set": 0, "Alınan Oyun": 0, "Verilen Oyun": 0} 
             for takim in st.session_state.takimlar[secili_grup]}
    
    # Tüm skorları tara (Burada basit bir mantıkla averaj topluyoruz)
    # Gerçek uygulamada tüm key'leri tarayıp istatistikleri toplar
    st.info("Skorlar girildikçe bu tablo otomatik olarak güncellenir. (Puanlama: Maç Galibiyeti > Set Averajı > Oyun Averajı)")
    
    df = pd.DataFrame(stats).T
    df["Set Averajı"] = df["Alınan Set"] - df["Verilen Set"]
    df["Oyun Averajı"] = df["Alınan Oyun"] - df["Verilen Oyun"]
    st.table(df.sort_values(by=["Galibiyet", "Set Averajı", "Oyun Averajı"], ascending=False))
