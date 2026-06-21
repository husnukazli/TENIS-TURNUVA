
# --- PUAN DURUMU & AVERAJ SEKMESİ ---
with tabs[4]:
    st.header("🏆 Gruplara Göre Puan Durumu")
    secilen_grup = st.selectbox("Grup Seçiniz:", ["Grup 1", "Grup 2", "Grup 3", "Grup 4"])
    
    if st.button("🔄 Tabloyu Güncelle"):
        takimlar = st.session_state.takimlar[secilen_grup]
        # Puan tablosunu oluştur
        df = pd.DataFrame(0, index=takimlar, columns=["Galibiyet", "Alınan Set", "Verilen Set", "Alınan Oyun", "Verilen Oyun"])
        
        # Skorları işle
        for key, vals in st.session_state.skorlar.items():
            if secilen_grup in key:
                try:
                    # vals: [S1-K, S1-Y, S2-K, S2-Y, S3-K, S3-Y]
                    nums = [int(v) if v.isdigit() else 0 for v in vals]
                    # Basit galibiyet mantığı: Setleri karşılaştır
                    t1_set = (1 if nums[0]>nums[1] else 0) + (1 if nums[2]>nums[3] else 0) + (1 if nums[4]>nums[5] else 0)
                    t2_set = (1 if nums[1]>nums[0] else 0) + (1 if nums[3]>nums[2] else 0) + (1 if nums[5]>nums[4] else 0)
                    
                    # Takım isimlerini key'den bul (Basit bir eşleşme)
                    parts = key.split('_')
                    t1, t2 = parts[2], parts[3]
                    
                    if t1 in df.index:
                        df.loc[t1, "Alınan Set"] += t1_set
                        df.loc[t1, "Verilen Set"] += t2_set
                        df.loc[t1, "Alınan Oyun"] += sum(nums[0::2])
                        df.loc[t1, "Verilen Oyun"] += sum(nums[1::2])
                        if t1_set > t2_set: df.loc[t1, "Galibiyet"] += 1
                        
                    if t2 in df.index:
                        df.loc[t2, "Alınan Set"] += t2_set
                        df.loc[t2, "Verilen Set"] += t1_set
                        df.loc[t2, "Alınan Oyun"] += sum(nums[1::2])
                        df.loc[t2, "Verilen Oyun"] += sum(nums[0::2])
                        if t2_set > t1_set: df.loc[t2, "Galibiyet"] += 1
                except: continue
        
        # Averajları ekle
        df["Set Averajı"] = df["Alınan Set"] - df["Verilen Set"]
        df["Oyun Averajı"] = df["Alınan Oyun"] - df["Verilen Oyun"]
        st.table(df.sort_values(by=["Galibiyet", "Set Averajı"], ascending=False))
