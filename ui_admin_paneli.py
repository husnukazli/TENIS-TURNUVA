import streamlit as st
import pandas as pd
import random
import string
from veritabani_islemleri import ortak_veriyi_kaydet
# Eğer fikstür oluşturma fonksiyonun hesaplama_motoru'ndaysa buradaki yorumu kaldırabilirsin:
# from hesaplama_motoru import fikstur_olustur 

def admin_paneli_goster():
    st.title("⚙️ Başhakem (Admin) Yönetim Paneli")

    # --- SİSTEM KONTROLÜ (SOL MENÜ) ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔴 Sistem Kontrolü")
    sistem_kapali = st.sidebar.checkbox(
        "Sistemi Bakıma Al (Kullanıcı Girişini Kapat)", 
        value=st.session_state.get('sistem_kapali', False)
    )
    if sistem_kapali != st.session_state.get('sistem_kapali', False):
        st.session_state.sistem_kapali = sistem_kapali
        st.success("Sistem durumu güncellendi. (Sayfa yenilendiğinde aktif olur)")

    # --- SEKMELER ---
    sekme1, sekme2, sekme3, sekme4 = st.tabs([
        "📥 Takım Yükle", "🏆 Grup Oluştur", "📅 Takvim", "🔑 PIN Yönetimi"
    ])

    # ---------------------------------------------------------
    # 1. SEKME: EXCEL'DEN TAKIM YÜKLEME (Sadeleştirilmiş)
    # ---------------------------------------------------------
    with sekme1:
        st.subheader("Excel ile Takım Havuzu Oluştur")
        st.info("Sadece Erkekler veya Kadınlar kategorisini seçerek takımları sisteme aktarın. Yaş kategorisi uygulaması kaldırılmıştır.")
        
        kategori = st.selectbox("Turnuva Kategorisi Seçin", ["Erkekler", "Kadınlar"])
        yuklenen_dosya = st.file_uploader(f"{kategori} için Excel Dosyası Seçin", type=["xlsx", "xls"])
        
        if yuklenen_dosya is not None:
            try:
                df = pd.read_excel(yuklenen_dosya)
                # Excel'de 'Takım Adı' adında bir sütun olduğunu varsayıyoruz
                if 'Takım Adı' not in df.columns:
                    st.error("Excel dosyasında 'Takım Adı' adında bir sütun bulunamadı!")
                else:
                    st.dataframe(df.head()) # Önizleme
                    
                    if st.button("Takımları Havuza Ekle"):
                        eklenen_sayi = 0
                        for index, row in df.iterrows():
                            takim_adi = str(row['Takım Adı']).strip()
                            if takim_adi and takim_adi.lower() != "nan":
                                if takim_adi not in st.session_state.takim_havuzu:
                                    st.session_state.takim_havuzu[takim_adi] = []
                                st.session_state.havuz_kategorileri[takim_adi] = kategori
                                eklenen_sayi += 1
                        
                        ortak_veriyi_kaydet()
                        st.success(f"{eklenen_sayi} adet {kategori} takımı başarıyla havuza eklendi!")
                        
            except Exception as e:
                st.error(f"Excel okunurken bir hata oluştu: {e}")

        # Mevcut Havuzu Göster
        with st.expander("Mevcut Takım Havuzunu Gör"):
            havuz_df = pd.DataFrame(
                list(st.session_state.havuz_kategorileri.items()), 
                columns=["Takım Adı", "Kategori"]
            )
            st.dataframe(havuz_df)

    # ---------------------------------------------------------
    # 2. SEKME: GRUP OLUŞTURMA (3 Maçlık Format ve Esnek Seçim)
    # ---------------------------------------------------------
    with sekme2:
        st.subheader("Grup ve Fikstür Oluştur")
        st.markdown("**Not:** Tüm gruplar varsayılan olarak 3 maçlık (2 Tek, 1 Çift) seriler halinde kurulur.")
        
        grup_adi = st.text_input("Grup Adı (Örn: Erkekler A Grubu)")
        grup_kategorisi = st.selectbox("Grubun Kategorisi", ["Erkekler", "Kadınlar"], key="grup_kat")
        asama_secimi = st.selectbox("Aşama (1. Aşama veya Play-off)", ["1. Aşama (Grup Maçları)", "2. Aşama (Final / Sıralama)"])
        
        # Başhakem havuzdaki tüm o kategori takımlarını kısıtlamasız görebilir
        uygun_takimlar = [t for t, kat in st.session_state.havuz_kategorileri.items() if kat == grup_kategorisi]
        secilen_takimlar = st.multiselect("Gruba Eklenecek Takımları Seçin", uygun_takimlar)
        
        if st.button("Grubu Kaydet ve Fikstür Çek"):
            if grup_adi and secilen_takimlar and len(secilen_takimlar) > 1:
                st.session_state.grup_formatlari[grup_adi] = "3 Maç (2 Tek, 1 Çift)" # Sabit Format
                st.session_state.grup_kategorileri[grup_adi] = grup_kategorisi
                st.session_state.grup_asamalari[grup_adi] = asama_secimi
                
                # Fikstür motorunu burada çağırıyoruz (Varsa kendi algoritmanı bağla)
                # fikstur_olustur(grup_adi, secilen_takimlar)
                
                ortak_veriyi_kaydet()
                st.success(f"{grup_adi} başarıyla oluşturuldu! (Format: 3 Maç)")
            else:
                st.warning("Lütfen grup adını girin ve en az 2 takım seçin.")

    # ---------------------------------------------------------
    # 3. SEKME: TAKVİM VE PROGRAM (Tarih Atama)
    # ---------------------------------------------------------
    with sekme3:
        st.subheader("Maç Tarihlerini Belirle")
        if not st.session_state.mac_programi.empty:
            st.dataframe(st.session_state.mac_programi)
            # Burada mevcut maçlara tarih/saat atama arayüzü eklenebilir.
            st.info("Fikstür oluştuktan sonra maçlara kort ve saat ataması buradan yapılacaktır.")
        else:
            st.info("Henüz oluşturulmuş bir fikstür bulunmuyor.")

    # ---------------------------------------------------------
    # 4. SEKME: PIN YÖNETİMİ (Kaptanlar ve Hakemler için)
    # ---------------------------------------------------------
    with sekme4:
        st.subheader("Güvenlik ve PIN Yönetimi")
        
        kolon1, kolon2 = st.columns(2)
        
        with kolon1:
            st.markdown("**Kaptan PIN'leri (Esame Girişi İçin)**")
            if st.button("Kaptan PIN'lerini Üret/Yenile"):
                for takim in st.session_state.takim_havuzu.keys():
                    # 6 Haneli Rastgele Alfanümerik PIN
                    pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    st.session_state.takim_pinleri[takim] = pin
                ortak_veriyi_kaydet()
                st.success("Tüm takımlar için yeni Kaptan PIN'leri üretildi.")
                
            if st.session_state.takim_pinleri:
                pin_df = pd.DataFrame(
                    list(st.session_state.takim_pinleri.items()), 
                    columns=["Takım", "PIN Şifresi"]
                )
                st.dataframe(pin_df)
                
        with kolon2:
            st.markdown("**Hakem PIN'leri (Skor Girişi İçin)**")
            yeni_hakem = st.text_input("Yeni Hakem Adı Ekle")
            if st.button("Hakem Ekle ve PIN Üret"):
                if yeni_hakem and yeni_hakem not in st.session_state.hakem_listesi:
                    st.session_state.hakem_listesi.append(yeni_hakem)
                    pin = ''.join(random.choices(string.digits, k=4)) # 4 Haneli sayısal
                    st.session_state.hakem_pinleri[yeni_hakem] = pin
                    ortak_veriyi_kaydet()
                    st.success(f"{yeni_hakem} sisteme eklendi.")
                    
            if st.session_state.hakem_pinleri:
                h_pin_df = pd.DataFrame(
                    list(st.session_state.hakem_pinleri.items()), 
                    columns=["Hakem Adı", "PIN"]
                )
                st.dataframe(h_pin_df)
