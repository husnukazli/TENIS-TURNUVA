import os
import json
import pandas as pd
import uuid
import base64
import streamlit as st
from github import Github
from github.GithubException import UnknownObjectException

# ==============================================================================
# 📂 KLASÖR VE DOSYA AYARLARI
# ==============================================================================
SISTEM_KLASORU = os.path.dirname(os.path.abspath(__file__))
BELGELER_KLASORU = os.path.join(SISTEM_KLASORU, "turnuva_belgeleri")
JSON_DOSYA_ADI = "turnuva_verileri.json"

if not os.path.exists(BELGELER_KLASORU):
    os.makedirs(BELGELER_KLASORU)

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# ==============================================================================
# ☁️ GITHUB BAĞLANTISI VE GÜVENLİK
# ==============================================================================
@st.cache_resource
def get_github_repo():
    try:
        # .streamlit/secrets.toml içindeki bilgileri kullanır
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(st.secrets["REPO_NAME"])
        return repo
    except Exception as e:
        st.warning(f"⚠️ GitHub bağlantısı kurulamadı ({e}). Lütfen secrets.toml ayarlarınızı kontrol edin.")
        return None

# ==============================================================================
# 💾 VERİ KAYDETME (GITHUB JSON)
# ==============================================================================
def ortak_veriyi_kaydet(guncellenen_mac_idleri=None):
    """
    Tüm session state verilerini ve skor tablosunu tek bir JSON dosyası
    olarak GitHub deposuna yazar (Eski Supabase mantığının yerini aldı).
    """
    if not st.session_state.skor_tablosu.empty:
        # ID'si olmayan yeni maçlar varsa (ilk kurulum) onlara UUID ata
        missing_id_mask = st.session_state.skor_tablosu['id'].isna() | (st.session_state.skor_tablosu['id'] == "")
        if missing_id_mask.any():
            for idx in st.session_state.skor_tablosu[missing_id_mask].index:
                st.session_state.skor_tablosu.at[idx, 'id'] = str(uuid.uuid4())
                
    maclar_data = st.session_state.skor_tablosu.to_dict(orient="records") if not st.session_state.skor_tablosu.empty else []

    mp_records = []
    if not st.session_state.get("mac_programi", pd.DataFrame()).empty:
        mp_df = st.session_state.mac_programi.copy()
        mp_df = mp_df.where(pd.notnull(mp_df), "")
        mp_records = mp_df.to_dict(orient="records")

    ayarlar = {
        "takim_kadrolari": st.session_state.get("takim_kadrolari", {}),
        "grup_formatlari": st.session_state.get("grup_formatlari", {}),
        "grup_kategorileri": st.session_state.get("grup_kategorileri", {}),
        "grup_asamalari": st.session_state.get("grup_asamalari", {}),
        "duyuru_metni": str(st.session_state.get("duyuru_metni", "")),
        "gunluk_notlar": st.session_state.get("gunluk_notlar", {}),
        "takim_havuzu": st.session_state.get("takim_havuzu", {}),
        "havuz_kategorileri": st.session_state.get("havuz_kategorileri", {}),
        "grup_siralamalari": st.session_state.get("grup_siralamalari", {}),
        "grup_tamamlandi": st.session_state.get("grup_tamamlandi", {}),
        "grup_statuleri": st.session_state.get("grup_statuleri", {}),
        "takim_pinleri": st.session_state.get("takim_pinleri", {}),
        "esame_kasasi": st.session_state.get("esame_kasasi", {}),
        "esame_onayli": st.session_state.get("esame_onayli", {}),
        "mac_programi": mp_records,
        "hakem_listesi": st.session_state.get("hakem_listesi", []),
        "hakem_pinleri": st.session_state.get("hakem_pinleri", {}),
        "grup_gun_takvimi": st.session_state.get("grup_gun_takvimi", {}),
        "yayinlanan_gunler": st.session_state.get("yayinlanan_gunler", {}),
        "sistem_kilitli": st.session_state.get("sistem_kilitli", False)
    }
    
    # Supabase'in yerine her şeyi paketleyip JSON yapıyoruz
    json_data = {
        "maclar": maclar_data,
        "ayarlar": ayarlar
    }
    
    json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
    
    repo = get_github_repo()
    if not repo: return False
    
    try:
        try:
            # Dosya varsa üstüne yaz (Update)
            contents = repo.get_contents(JSON_DOSYA_ADI)
            repo.update_file(contents.path, "Otomatik Sistem Güncellemesi (JSON)", json_str, contents.sha)
        except UnknownObjectException:
            # Dosya yoksa ilk kez oluştur (Create)
            repo.create_file(JSON_DOSYA_ADI, "İlk Veritabanı Kurulumu (JSON)", json_str)
        return True
    except Exception as e:
        st.error(f"GitHub'a kayıt sırasında hata oluştu: {e}")
        return False

# ==============================================================================
# 📥 VERİ YÜKLEME (GITHUB JSON)
# ==============================================================================
def ortak_veriyi_yukle():
    data = {}
    maclar_data = []
    
    repo = get_github_repo()
    if repo:
        try:
            file_content = repo.get_contents(JSON_DOSYA_ADI)
            json_data = json.loads(file_content.decoded_content.decode("utf-8"))
            data = json_data.get("ayarlar", {})
            maclar_data = json_data.get("maclar", [])
        except UnknownObjectException:
            # Repo var ama JSON dosyası henüz oluşturulmamış (temiz başlangıç)
            pass
        except Exception as e:
            st.error(f"⚠️ GitHub'dan JSON okunurken hata: {e}")

    # Ayarları hafızaya (Session State) yükle
    st.session_state.sistem_kilitli = data.get("sistem_kilitli", False)
    st.session_state.cevrimdisi_mod = st.session_state.sistem_kilitli 
    
    if data.get("mac_programi"):
        mp_df = pd.DataFrame(data["mac_programi"])
        if "T1 Oyuncu" not in mp_df.columns: mp_df["T1 Oyuncu"] = ""; mp_df["T2 Oyuncu"] = ""
        if "Kazanan" not in mp_df.columns: mp_df["Kazanan"] = ""
        if "Hakem" not in mp_df.columns: mp_df["Hakem"] = ""
        st.session_state.mac_programi = mp_df
    else:
        st.session_state.mac_programi = pd.DataFrame(columns=["Maç Saati", "Tarih", "Gün Adı", "Kort", "Grup", "Gün", "Branş", "Eşleşme", "Takım 1", "Takım 2", "T1 Oyuncu", "T2 Oyuncu", "Skor", "Kazanan", "Hakem"])

    st.session_state.takim_kadrolari = data.get("takim_kadrolari", {})
    st.session_state.grup_formatlari = data.get("grup_formatlari", {})
    st.session_state.grup_kategorileri = data.get("grup_kategorileri", {})
    st.session_state.grup_asamalari = data.get("grup_asamalari", {})
    st.session_state.duyuru_metni = data.get("duyuru_metni", "")
    st.session_state.gunluk_notlar = data.get("gunluk_notlar", {})
    st.session_state.takim_havuzu = data.get("takim_havuzu", {})
    st.session_state.havuz_kategorileri = data.get("havuz_kategorileri", {})
    st.session_state.grup_siralamalari = data.get("grup_siralamalari", {})
    st.session_state.grup_tamamlandi = data.get("grup_tamamlandi", {})
    st.session_state.grup_statuleri = data.get("grup_statuleri", {})
    st.session_state.takim_pinleri = data.get("takim_pinleri", {})
    st.session_state.esame_kasasi = data.get("esame_kasasi", {})
    st.session_state.esame_onayli = data.get("esame_onayli", {})
    st.session_state.hakem_listesi = data.get("hakem_listesi", [])
    st.session_state.hakem_pinleri = data.get("hakem_pinleri", {})
    st.session_state.grup_gun_takvimi = data.get("grup_gun_takvimi", {})
    st.session_state.yayinlanan_gunler = data.get("yayinlanan_gunler", {})
    
    # Maçları (Skor Tablosunu) hafızaya yükle
    if maclar_data:
        st.session_state.skor_tablosu = pd.DataFrame(maclar_data)
    else:
        st.session_state.skor_tablosu = pd.DataFrame(columns=["id", "Grup", "Gün", "Eşleşme", "Branş", "Takım 1", "Takım 2", "T1_Oyuncu", "T2_Oyuncu", "1.Set T1", "1.Set T2", "2.Set T1", "2.Set T2", "3.Set T1", "3.Set T2", "Durum", "STB"])
