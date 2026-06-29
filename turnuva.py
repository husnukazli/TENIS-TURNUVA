import streamlit as st
import pandas as pd
import io

# Sayfa başlığı ve düzeni
st.set_page_config(page_title="Turnuva Sıralaması", layout="wide")
st.title("🎾 Turnuva Sıralama Sistemi")
st.write("Herhangi bir dosya yüklemesi yapılmasına gerek kalmadan, veriler sistemden otomatik olarak listelenmektedir.")

# --- TURNUVA SKOR VERİLERİ (Doğrudan Kodun İçinde) ---
# Buradaki metin alanına dilediğiniz kadar maç skoru satırı ekleyebilirsiniz.
TURNUVA_SKOR_DATA = """Grup,Gün,Eşleşme,Branş,Takım 1,Takım 2,1.Set (T1),1.Set (T2),2.Set (T1),2.Set (T2),3.Set (T1),3.Set (T2),T1 Kazanılan Set,T2 Kazanılan Set,T1 Kazanılan Maç,T2 Kazanılan Maç,T1 Kazanılan Oyun,T2 Kazanılan Oyun,Tie Kazananı (Galibiyet)
ERKEK A GRUBU,1. Gün,1 ve 4,1. Tekler,ATAK PRO SPOR KULÜBÜ  E,NEW GEN SPOR KULÜBÜ  E,6,3,6,1,,,2,0,1,0,12,4,ATAK PRO SPOR KULÜBÜ  E
ERKEK A GRUBU,1. Gün,1 ve 4,2. Tekler,ATAK PRO SPOR KULÜBÜ  E,NEW GEN SPOR KULÜBÜ  E,6,1,6,0,,,2,0,1,0,12,1,ATAK PRO SPOR KULÜBÜ  E
ERKEK A GRUBU,1. Gün,1 ve 4,Çiftler,ATAK PRO SPOR KULÜBÜ  E,NEW GEN SPOR KULÜBÜ  E,6,0,6,2,,,2,0,1,0,12,2,ATAK PRO SPOR KULÜBÜ  E
KADIN B GRUBU,2. Gün,2 ve 4,1. Tekler,ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ,İNCEK TENİS SPOR KULÜBÜ,6,0,6,0,,,2,0,1,0,12,0,ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ
KADIN B GRUBU,2. Gün,2 ve 4,2. Tekler,ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ,İNCEK TENİS SPOR KULÜBÜ,6,0,6,0,,,2,0,1,0,12,0,ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ
KADIN B GRUBU,2. Gün,2 ve 4,Çiftler,ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ,İNCEK TENİS SPOR KULÜBÜ,6,0,6,0,,,2,0,1,0,12,0,ORTADOĞU TEKNİK ÜNİVERSİTESİ SPOR KULÜBÜ
"""

def turnuva_siralamasi_hesapla(veri_metni):
    # Kod içindeki metni tablo verisine (Dataframe) dönüştürüyoruz
    df = pd.read_csv(io.StringIO(veri_metni))
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

    # Averaj Hesapları
    siralama['Maç Averajı'] = siralama['Aldığı Maç'] - siralama['Verdiği Maç']
    siralama['Set Averajı'] = siralama['Aldığı Set'] - siralama['Verdiği Set']
    siralama['Oyun Averajı'] = siralama['Aldığı Oyun'] - siralama['Verdiği Oyun']

    # Sıralama Kriterleri (Galibiyet -> Maç Averajı -> Set Averajı -> Oyun Averajı)
    siralama = siralama.sort_values(
        by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'], 
        ascending=[True, False, False, False, False]
    )
    
    siralama = siralama[['Grup', 'Galibiyet', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Maç Averajı', 
                         'Aldığı Set', 'Verdiği Set', 'Set Averajı', 'Aldığı Oyun', 'Verdiği Oyun', 'Oyun Averajı']]
    return siralama

# --- HESAPLAMA VE EKRANA YAZDIRMA ---
try:
    sonuc_df = turnuva_siralamasi_hesapla(TURNUVA_SKOR_DATA)
    st.success("✅ Sıralama tablosu başarıyla yüklendi!")
    
    # Canlı Tablo Gösterimi
    st.dataframe(sonuc_df, use_container_width=True)
    
    # Excel/CSV olarak indirmek isteyenler için kolaylık butonu
    csv_veri = sonuc_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Sıralama Sonuçlarını İndir (CSV)",
        data=csv_veri,
        file_name='Turnuva_Siralama_Raporu.csv',
        mime='text/csv',
    )
except Exception as e:
    st.error(f"Sistem çalışırken bir sorunla karşılaştı: {e}")
