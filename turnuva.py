def turnuva_siralamasi_hesapla(veri_metni):
    import io
    # Eğer veri_metni bir string ise StringIO kullan, Streamlit UploadedFile veya DataFrame ise ona göre davran
    if isinstance(veri_metni, str):
        df = pd.read_csv(io.StringIO(veri_metni))
    elif isinstance(veri_metni, pd.DataFrame):
        df = veri_metni.copy()
    else:
        df = pd.read_csv(veri_metni)
        
    df = df.dropna(subset=['Takım 1', 'Takım 2'])

    # Sütun isimleri listesi (Kırılmayı önlemek için alt alta yerleştirildi)
    yeni_sutunlar = [
        'Grup', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 
        'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun', 'Galibiyet'
    ]

    # Takım 1 İstatistikleri
    t1_stats = df[['Grup', 'Takım 1', 'T1 Kazanılan Maç', 'T2 Kazanılan Maç', 
                   'T1 Kazanılan Set', 'T2 Kazanılan Set', 'T1 Kazanılan Oyun', 'T2 Kazanılan Oyun', 'Tie Kazananı (Galibiyet)']].copy()
    t1_stats.columns = yeni_sutunlar
    t1_stats['Galibiyet'] = (t1_stats['Galibiyet'] == t1_stats['Takım Adı']).astype(int)

    # Takım 2 İstatistikleri
    t2_stats = df[['Grup', 'Takım 2', 'T2 Kazanılan Maç', 'T1 Kazanılan Maç', 
                   'T2 Kazanılan Set', 'T1 Kazanılan Set', 'T2 Kazanılan Oyun', 'T1 Kazanılan Oyun', 'Tie Kazananı (Galibiyet)']].copy()
    t2_stats.columns = yeni_sutunlar
    t2_stats['Galibiyet'] = (t2_stats['Galibiyet'] == t2_stats['Takım Adı']).astype(int)

    # Birleştir ve Topla
    all_stats = pd.concat([t1_stats, t2_stats], ignore_index=True)
    siralama = all_stats.groupby(['Grup', 'Takım Adı']).sum().reset_index()

    # Averaj Hesapları
    siralama['Maç Averajı'] = siralama['Aldığı Maç'] - siralama['Verdiği Maç']
    siralama['Set Averajı'] = siralama['Aldığı Set'] - siralama['Verdiği Set']
    siralama['Oyun Averajı'] = siralama['Aldığı Oyun'] - siralama['Verdiği Oyun']

    # Sıralama Kriterleri
    siralama = siralama.sort_values(
        by=['Grup', 'Galibiyet', 'Maç Averajı', 'Set Averajı', 'Oyun Averajı'], 
        ascending=[True, False, False, False, False]
    )
    
    siralama = siralama[['Grup', 'Galibiyet', 'Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Maç Averajı', 
                         'Aldığı Set', 'Verdiği Set', 'Set Averajı', 'Aldığı Oyun', 'Verdiği Oyun', 'Oyun Averajı']]
    return siralama
