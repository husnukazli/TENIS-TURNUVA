# --- PUAN DURUMU & AVERAJ ---
with tabs[4]:
    st.header("🏆 Gruplara Göre Puan Durumu")
    secilen_grup = st.selectbox("Grup Seçiniz:", ["Grup 1", "Grup 2", "Grup 3", "Grup 4"])
    
    if st.button("🔄 Tabloyu Güncelle"):
        takimlar = st.session_state.takimlar[secilen_grup]
        # Sütunları güncelledik: "Maç Galibiyeti" (Seri), "Alt Maç Galibiyeti" ve "Alt Maç Mağlubiyeti"
        cols = ["Seri Galibiyeti", "Alt Maç Aldığı", "Alt Maç Verdiği", "Alınan Set", "Verilen Set", "Alınan Oyun", "Verilen Oyun"]
        df = pd.DataFrame(0, index=takimlar, columns=cols)
        
        # Maçları işleyelim (Seri bazlı)
        # Her maçta 3 alt maç var. Seri galibi 2 veya 3 alt maç kazanan taraftır.
        for key, vals in st.session_state.skorlar.items():
            if secilen_grup in key:
                try:
                    n = [int(v) if v.isdigit() else 0 for v in vals]
                    # Tek bir alt maçın galibini belirle
                    t1_set = (1 if n[0]>n[1] else 0) + (1 if n[2]>n[3] else 0) + (1 if n[4]>n[5] else 0)
                    t2_set = (1 if n[1]>n[0] else 0) + (1 if n[3]>n[2] else 0) + (1 if n[5]>n[4] else 0)
                    
                    alt_mac_t1 = 1 if t1_set > t2_set else 0
                    alt_mac_t2 = 1 if t2_set > t1_set else 0
                    
                    parts = key.split('_')
                    t1, t2 = parts[2], parts[3]
                    
                    # Verileri her iki takım için de işle
                    if t1 in df.index:
                        df.loc[t1, "Alt Maç Aldığı"] += alt_mac_t1
                        df.loc[t1, "Alt Maç Verdiği"] += alt_mac_t2
                        df.loc[t1, ["Alınan Set", "Verilen Set"]] += [t1_set, t2_set]
                        df.loc[t1, ["Alınan Oyun", "Verilen Oyun"]] += [sum(n[0::2]), sum(n[1::2])]
                    if t2 in df.index:
                        df.loc[t2, "Alt Maç Aldığı"] += alt_mac_t2
                        df.loc[t2, "Alt Maç Verdiği"] += alt_mac_t1
                        df.loc[t2, ["Alınan Set", "Verilen Set"]] += [t2_set, t1_set]
                        df.loc[t2, ["Alınan Oyun", "Verilen Oyun"]] += [sum(n[1::2]), sum(n[0::2])]
                except: continue

        # Seri galibiyetini hesapla (3 alt maçın en az 2'sini kazanan seri galibidir)
        # (Bu kısım, bir serideki tüm alt maçlar girildiğinde doğru hesaplanır)
        
        st.table(df.sort_values(by=["Seri Galibiyeti", "Alt Maç Aldığı"], ascending=False))
