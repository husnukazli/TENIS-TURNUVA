import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tenis Turnuva", layout="wide")

# 1. KALICI VERİ DEPOSU
if 'skorlar' not in st.session_state:
    st.session_state.skorlar = {}

# 2. VERİ KAYIT FONKSİYONU
def veri_kaydet(key, idx):
    # Kullanıcı bir kutucuğa dokunduğunda o kutunun değerini session_state'de günceller
    val = st.session_state[f"inp_{key}_{idx}"]
    if key not in st.session_state.skorlar:
        st.session_state.skorlar[key] = ["0"] * 6
    st.session_state.skorlar[key][idx] = val

# 3. ARAYÜZ
st.title("🎾 Veri Kayıt Testi")

# Örnek bir maç girişi (Sadece 1 tane yapıp test edelim)
key = "Grup1_Mac1"
if key not in st.session_state.skorlar:
    st.session_state.skorlar[key] = ["0"] * 6

st.write("Skorları girin, sayfayı yenileyin, veriler gitmeyecek:")

cols = st.columns(6)
for i in range(6):
    # Değeri session_state içinden alıyoruz
    current_val = st.session_state.skorlar[key][i]
    cols[i].text_input(
        f"P{i+1}", 
        value=current_val, 
        key=f"inp_{key}_{i}", 
        on_change=veri_kaydet, 
        args=(key, i)
    )

st.write("Hafızadaki Veri:", st.session_state.skorlar)
