import streamlit as st
import pandas as pd
import os

# Sayfa başlığı
st.set_page_config(page_title="Turnuva Sıralaması", layout="wide")
st.title("🎾 Turnuva Sıralama Sistemi")

# Otomatik olarak aranacak dosya adı
VARSAYILAN_DOSYA = "Turnuva_Dinamik_Formullu.xlsx - Skor Giriş Ekranı.csv"

def turnuva_siralamasi_hesapla(skor_dosyasi):
    # Veriyi oku (Eğer yüklenen dosyaysa doğrudan okunur, yolsa string olarak okunur)
    df = pd.read_csv(skor_dosyasi)
    df = df.dropna(subset=['Takım 1', 'Takım 2'])

    # Takım 1 İstatistikleri
    t1_stats = df[['Grup', 'Takım 1', 'T1 Kazanılan Maç', 'T2 Kazanılan Maç', 
                   'T1 Kazanılan Set', 'T2 Kazanılan Set', 'T1 Kazanılan Oyun', 'T2 Kazanılan Oyun', 'Tie Kazananı (Galibiyet)']].copy()
    t1_stats.columns = ['Grup', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun', 'Galibiyet']
    t1_stats['Galibiyet'] = (t1_stats['Galibiyet'] == t1_stats['Takım Adı']).astype(int)

    # Takım 2 İstatistikleri
    t2_stats = df[['Grup', 'Takım 2', 'T2 Kazanılan Maç', 'T1 Kazanılan Maç', 
                   'T2 Kazanılan Set', 'T1 Kazanılan Set', 'T2 Kazanılan Oyun', 'T1 Kazanılan Oyun', 'Tie Kazananı (Galibiyet)']].copy()
    t2_stats.columns = ['Grup', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun', 'Galibiyet']
    t2_stats['Galibiyet'] = (t2_stats['Galibiyet'] == t2_stats['Takım Adı']).astype(int)

    # Birleştir ve Topla
    all_stats = pd.concat([t1_stats, t2_stats], ignore_index=True)
    siralama = all_stats.groupby(['Grup', 'Takım Adı']).sum().reset_index()

    # Averajlar
    siralama['Maç Averajı'] = siralama['Aldığı Maç'] - siralama['Verdiği Maç']
    siralama['Set Averajı'] = siralama['Aldığı Set'] - siralama['Verdiği Set']
    siralama['Oyun Averajı'] = siralama['Aldığı Oyun'] - siralama['Verdiği Oyun']

    # Sıralama Önceliği
    siralama = siralama.sort_values(
        by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'], 
        ascending=[True, False, False, False, False]
    )
    
    siralama = siralama[['Grup', 'Galibiyet', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Maç Averajı', 
                         'Aldığı Set', 'Verdiği Set', 'Set Averajı', 'Aldığı Oyun', 'Verdiği Oyun', 'Oyun Averajı']]
    return siralama

# --- DOSYA KONTROL VE AKIŞ MANTIĞI ---
hedef_dosya = None

if os.path.exists(VARSAYILAN_DOSYA):
    hedef_dosya = VARSAYILAN_DOSYA
    st.info(f"🔄 '{VARSAYILAN_DOSYA}' dosyası GitHub'dan otomatik olarak yüklendi.")
else:
    st.warning(f"⚠️ '{VARSAYILAN_DOSYA}' dosyası GitHub deponuzda bulunamadı.")
    st.write("Sıralamayı görebilmek için dosyayı aşağıdan manuel olarak yükleyebilir veya GitHub'daki dosya adını kontrol edebilirsiniz.")
    
    # Yedek Plan: Manuel yükleme kutusu
    hedef_dosya = st.file_uploader("Skor Giriş Ekranı CSV dosyasını buraya sürükleyin", type=['csv'])
    
    # Hata tespiti için mevcut klasördeki dosyaları listeleme (Sadece geliştiriciye yardımcı olmak için)
    with st.expander("📂 GitHub Deponuzdaki Mevcut Dosyaları Görün (İsim Kontrolü)"):
        mevcut_dosyalar = [f for f in os.listdir('.') if os.path.isfile(f)]
        st.write("Şu an klasörde olan dosyalar:")
        st.code("\n".join(mevcut_dosyalar))

# --- HESAPLAMA VE GÖSTERİM ---
if hedef_dosya is not None:
    try:
        sonuc_df = turnuva_siralamasi_hesapla(hedef_dosya)
        st.success("Sıralama tablosu başarıyla oluşturuldu!")
        
        # Tabloyu göster
        st.dataframe(sonuc_df, use_container_width=True)
        
        # İndirme Butonu
        csv_veri = sonuc_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Sonuçları İndir (CSV)",
            data=csv_veri,
            file_name='Guncel_Siralama.csv',
            mime='text/csv',
        )
    except Exception as e:
        st.error(f"Veriler işlenirken bir hata oluştu. Hata detayı: {e}")
