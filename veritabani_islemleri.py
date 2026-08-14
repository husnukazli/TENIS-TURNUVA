import streamlit as st
import json
import pandas as pd
from github import Github
import base64

# ----------------------------------------------------------------------
# 📁 GITHUB DEPO AYARLARI
# ----------------------------------------------------------------------
VERI_DOSYASI = "turnuva_verileri.json"

# Bu bilgileri Streamlit Cloud "Secrets" bölümünden veya lokaldeki .streamlit/secrets.toml dosyasından çekeceğiz
# Örnek secrets.toml formatı:
# GITHUB_TOKEN = "ghp_seninGizliTokeninBurada"
# REPO_NAME = "kullaniciadi/repo-adi"

# ----------------------------------------------------------------------
# 📥 VERİ YÜKLEME (Sisteme Girişte GitHub'dan JSON Okur)
# ----------------------------------------------------------------------
def verileri_yukle():
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo_name = st.secrets["REPO_NAME"]
        
        g = Github(token)
        repo = g.get_repo(repo_name)
        
        try:
            # Dosyayı GitHub'dan çek
            contents = repo.get_contents(VERI_DOSYASI)
            decoded_data = contents.decoded_content.decode('utf-8')
            data = json.loads(decoded_data)
            
        except Exception:
            # Eğer repo'da dosya henüz yoksa boş data döndür, sistem taze başlasın
            data = {}

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
        st.error(f"Veri yükleme hatası (GitHub bağlantısını kontrol edin): {e}")
        return False

# ----------------------------------------------------------------------
# 💾 VERİ KAYDETME (Her Değişiklikte GitHub JSON'una Yazar)
# ----------------------------------------------------------------------
def ortak_veriyi_kaydet():
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo_name = st.secrets["REPO_NAME"]
        
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
        
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        
        g = Github(token)
        repo = g.get_repo(repo_name)
        
        try:
            # Dosya zaten varsa üzerine yaz (update)
            contents = repo.get_contents(VERI_DOSYASI)
            repo.update_file(contents.path, "Veritabanı Güncellemesi (Otomatik)", json_data, contents.sha)
        except Exception:
            # Dosya yoksa ilk defa oluştur (create)
            repo.create_file(VERI_DOSYASI, "Veritabanı Oluşturuldu (Otomatik)", json_data)
            
        return True
    except Exception as e:
        st.error(f"Veri kaydetme hatası (GitHub API): {e}")
        return False
