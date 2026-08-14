import streamlit as st
import json
import os
import pandas as pd

# ----------------------------------------------------------------------
# 📁 YEREL DOSYA YOLLARI
# ----------------------------------------------------------------------
VERI_DOSYASI = "turnuva_verileri.json"
BELGELER_KLASORU = "yuklenen_belgeler"

# ----------------------------------------------------------------------
# 📥 VERİ YÜKLEME (Sisteme Girişte JSON'dan Okur)
# ----------------------------------------------------------------------
def verileri_yukle():
    if os.path.exists(VERI_DOSYASI):
        try:
            with open(VERI_DOSYASI, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Pandas DataFrameleri oluştur
            if 'skor_tablosu' in data and data['skor_tablosu']:
                st.session_state.skor_tablosu = pd.DataFrame(data['skor_tablosu'])
            else:
                st.session_state.skor_tablosu = pd.DataFrame()
                
            if 'mac_programi' in data and data['mac_programi']:
                st.session_state.mac_programi = pd.DataFrame(data['mac_programi'])
            else:
                st.session_state.mac_programi = pd.DataFrame()

            # Sadeleşmiş listeleri ve sözlükleri yükle
            st.session_state.takim_kadrolari = data.get("takim_kadrolari", {})
            st.session_state.grup_formatlari = data.get("grup_formatlari", {})
            st.session_state.grup_kategorileri = data.get("grup_kategorileri", {})
            st.session_state.grup_asamalari = data.get("grup_asamalari", {})
            st.session_state.takim_havuzu = data.get("takim_havuzu", {})
            st.session_state.havuz_kategorileri = data.get("havuz_kategorileri", {})
            st.session_state.takim_pinleri = data.get("takim_pinleri", {})
            st.session_state.esame_kasasi = data.get("esame_kasasi", {})
            st.session_state.esame_onayli = data.get("esame_onayli", {})
            st.session_state.hakem_listesi = data.get("hakem_listesi", [])
            st.session_state.hakem_pinleri = data.get("hakem_pinleri", {})
            st.session_state.grup_gun_takvimi = data.get("grup_gun_takvimi", {})
            st.session_state.grup_tamamlandi = data.get("grup_tamamlandi", {})
            
            return True
        except Exception as e:
            st.error(f"Veri yükleme hatası: {e}")
            return False
    return False

# ----------------------------------------------------------------------
# 💾 VERİ KAYDETME (Her Değişiklikte JSON'a Yazar)
# ----------------------------------------------------------------------
def ortak_veriyi_kaydet():
    try:
        # Dataframe'leri JSON'a uygun liste formatına çevir
        skor_liste = st.session_state.skor_tablosu.to_dict(orient="records") if not st.session_state.skor_tablosu.empty else []
        mac_liste = st.session_state.mac_programi.to_dict(orient="records") if not st.session_state.mac_programi.empty else []
        
        # Sadeleşmiş veritabanı paketi
        data = {
            "skor_tablosu": skor_liste,
            "mac_programi": mac_liste,
            "takim_kadrolari": st.session_state.get("takim_kadrolari", {}),
            "grup_formatlari": st.session_state.get("grup_formatlari", {}),
            "grup_kategorileri": st.session_state.get("grup_kategorileri", {}),
            "grup_asamalari": st.session_state.get("grup_asamalari", {}),
            "takim_havuzu": st.session_state.get("takim_havuzu", {}),
            "havuz_kategorileri": st.session_state.get("havuz_kategorileri", {}),
            "takim_pinleri": st.session_state.get("takim_pinleri", {}),
            "esame_kasasi": st.session_state.get("esame_kasasi", {}),
            "esame_onayli": st.session_state.get("esame_onayli", {}),
            "hakem_listesi": st.session_state.get("hakem_listesi", []),
            "hakem_pinleri": st.session_state.get("hakem_pinleri", {}),
            "grup_gun_takvimi": st.session_state.get("grup_gun_takvimi", {}),
            "grup_tamamlandi": st.session_state.get("grup_tamamlandi", {})
        }
        
        # Klasördeki dosyaya güvenle yaz
        with open(VERI_DOSYASI, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        return True
    except Exception as e:
        st.error(f"Veri kaydetme hatası: {e}")
        return False
