import streamlit as st
import pandas as pd
import random
import string
from veritabani_islemleri import ortak_veriyi_kaydet
from hesaplama_motoru import eslesmeleri_olustur

def grup_ayarlari_ciz(aktif_asama):
    st.subheader(f"⚙️ {aktif_asama} - Grup ve Fikstür Yönetimi")
    st.info("Tüm gruplar varsayılan olarak 3 maçlık (2 Tek, 1 Çift) standart formata göre oluşturulur.")
    
    tab1, tab2 = st.tabs(["📥 Takım Havuzu & Excel Yükle", "🏆 Grup Oluştur & Fikstür Çek"])
    
    with tab1:
        st.markdown("### Excel ile Takım Yükleme")
        kategori = st.selectbox("Kategori Seçin", ["Erkekler", "Kadınlar"], key="excel_kat_sec")
        yuklenen_dosya = st.file_uploader(f"{kategori} için Excel Dosyası Seçin", type=["xlsx", "xls"], key="excel_up_admin")
        
        if yuklenen_dosya is not None:
            try:
                df = pd.read_excel(yuklenen_dosya)
                if 'Takım Adı' not in df.columns:
                    st.error("Excel dosyasında 'Takım Adı' sütunu bulunamadı!")
                else:
                    st.dataframe(df.head())
                    if st.button("Takımları Havuza Kaydet", key="btn_havuz_kaydet"):
                        eklenen = 0
                        for _, row in df.iterrows():
                            t_adi = str(row['Takım Adı']).strip()
                            if t_adi and t_adi.lower() != "nan":
                                if t_adi not in st.session_state.takim_havuzu:
                                    st.session_state.takim_havuzu[t_adi] = []
                                st.session_state.havuz_kategorileri[t_adi] = kategori
                                eklenen += 1
                        ortak_veriyi_kaydet()
                        st.success(f"{eklenen} takım başarıyla havuza eklendi!")
            except Exception as e:
                st.error(f"Hata: {e}")
                
        with st.expander("Mevcut Takım Havuzu"):
            if st.session_state.havuz_kategorileri:
                havuz_df = pd.DataFrame(list(st.session_state.havuz_kategorileri.items()), columns=["Takım Adı", "Kategori"])
                st.dataframe(havuz_df, use_container_width=True)
            else:
                st.info("Havuzda henüz takım yok.")

    with tab2:
        st.markdown("### Grup ve Fikstür Tanımlama")
        grup_adi = st.text_input("Grup Adı (Örn: Erkekler A Grubu)", key="input_grup_adi")
        g_kat = st.selectbox("Grup Kategorisi", ["Erkekler", "Kadınlar"], key="grup_kat_secim")
        
        uygun_takimlar = [t for t, kat in st.session_state.havuz_kategorileri.items() if kat == g_kat]
        secilen_takimlar = st.multiselect("Gruba Eklenecek Takımları Seçin", uygun_takimlar, key="grup_takimlar_ms")
        
        if st.button("Grubu Kaydet ve Fikstür Oluştur", type="primary", key="btn_grup_olustur"):
            if grup_adi and len(secilen_takimlar) >= 2:
                st.session_state.grup_formatlari[grup_adi] = "3 Maç (2 Tek, 1 Çift)"
                st.session_state.grup_kategorileri[grup_adi] = g_kat
                st.session_state.grup_asamalari[grup_adi] = aktif_asama
                
                n = len(secilen_takimlar)
                if n == 2: g_tipi = "2'li Grup"
                elif n == 3: g_tipi = "3'lü Grup"
                elif n == 4: g_tipi = "4'lü Grup"
                elif n == 5: g_tipi = "5'li Grup"
                else: g_tipi = "6'lı Grup"
                
                program = eslesmeleri_olustur(grup_adi, secilen_takimlar, g_tipi, "3 Maçlık (2 Tek, 1 Çift)")
                yeni_df = pd.DataFrame(program)
                
                if st.session_state.skor_tablosu.empty:
                    st.session_state.skor_tablosu = yeni_df
                else:
                    st.session_state.skor_tablosu = pd.concat([st.session_state.skor_tablosu, yeni_df], ignore_index=True)
                    
                ortak_veriyi_kaydet()
                st.success(f"{grup_adi} ve fikstürü başarıyla oluşturuldu!")
                st.rerun()
            else:
                st.warning("Lütfen geçerli bir grup adı girin ve en az 2 takım seçin.")

def hakem_yonetimi_ciz():
    st.subheader("👮‍♂️ Hakem Yönetimi ve PIN Paneli")
    yeni_hakem = st.text_input("Yeni Hakem Adı Soyadı", key="input_yeni_hakem")
    if st.button("Hakem Ekle ve PIN Üret", key="btn_hakem_ekle"):
        if yeni_hakem and yeni_hakem not in st.session_state.hakem_listesi:
            st.session_state.hakem_listesi.append(yeni_hakem)
            pin = ''.join(random.choices(string.digits, k=4))
            st.session_state.hakem_pinleri[yeni_hakem] = pin
            ortak_veriyi_kaydet()
            st.success(f"{yeni_hakem} sisteme eklendi. PIN: {pin}")
            st.rerun()
            
    if st.session_state.hakem_pinleri:
        st.markdown("### Mevcut Hakemler ve PIN'leri")
        h_df = pd.DataFrame(list(st.session_state.hakem_pinleri.items()), columns=["Hakem Adı", "PIN"])
        st.dataframe(h_df, use_container_width=True)

def yonetim_ve_dosya_ciz(aktif_asama):
    st.subheader("⚙️ Sistem Yönetimi ve Veri Kontrolü")
    st.info("GitHub tabanlı JSON veritabanı yönetim araçları.")
    
    if st.button("🔄 Verileri GitHub ile Senkronize Et", key="btn_github_sync"):
        ortak_veriyi_kaydet()
        st.success("Tüm veriler GitHub deposuna kaydedildi.")
        
    st.markdown("---")
    if st.button("⚠️ Tüm Verileri Sıfırla (Dikkat!)", type="primary", key="btn_sifirla"):
        st.session_state.skor_tablosu = pd.DataFrame()
        st.session_state.mac_programi = pd.DataFrame()
        st.session_state.takim_kadrolari = {}
        ortak_veriyi_kaydet()
        st.success("Sistem sıfırlandı.")
        st.rerun()

def esame_kontrol_merkezi_ciz():
    st.subheader("📝 Esame Kontrol Merkezi")
    st.info("Kaptanlar veya hakemler tarafından kasaya gönderilen esame listelerini buradan onaylayabilirsiniz.")
    
    if not st.session_state.esame_kasasi:
        st.info("Şu an kasada bekleyen esame bulunmuyor.")
    else:
        for match_key, takimlar_dict in list(st.session_state.esame_kasasi.items()):
            st.markdown(f"**Eşleşme Anahtarı:** `{match_key}`")
            is_onayli = st.session_state.esame_onayli.get(match_key, False)
            
            for takim_adi, kadro_data in takimlar_dict.items():
                kaynak = kadro_data.get("_kaynak", "Kaptan")
                st.write(f"- **{takim_adi}** ({kaynak} Bildirimi):")
                for brans, oyuncu in kadro_data.items():
                    if not brans.startswith("_"):
                        st.caption(f"  * {brans}: {oyuncu}")
                        
            col_onay, col_red = st.columns(2)
            if not is_onayli:
                if col_onay.button(f"✅ Onayla ve Fikstüre Yansit", key=f"onay_{match_key}"):
                    st.session_state.esame_onayli[match_key] = True
                    ortak_veriyi_kaydet()
                    st.success("Esame onaylandı.")
                    st.rerun()
            else:
                st.success("Bu esame onaylanmış durumda.")
            st.divider()
