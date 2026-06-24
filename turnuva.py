import xlsxwriter

file_path = 'Tenis_Grup_Fiksturu_Sifirdan.xlsx'
wb = xlsxwriter.Workbook(file_path)

# Formats
header_fmt = wb.add_format({'bold': True, 'bg_color': '#203764', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
sub_header_fmt = wb.add_format({'bold': True, 'bg_color': '#D9E1F2', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
team_fmt = wb.add_format({'bold': True, 'bg_color': '#F2F2F2', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
input_fmt = wb.add_format({'border': 1, 'bg_color': '#FFF2CC', 'align': 'center', 'valign': 'vcenter'}) # Sarı kutular
calc_fmt = wb.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_color': '#808080'}) # Gizli/Gri hesaplama alanı

# --- SEKME 1: AYARLAR VE TAKIMLAR ---
ws1 = wb.add_worksheet('1. Ayarlar')
ws1.set_column('A:A', 15)
ws1.set_column('B:B', 25)
ws1.set_column('D:D', 25)

ws1.write('A1', 'Grup Sırası', header_fmt)
ws1.write('B1', 'Seçilen Takım', header_fmt)
ws1.write('D1', 'Tüm Takımlar Listesi (Burayı Güncelleyin)', header_fmt)

# Takım listesi havuzu
sample_teams = ['Zonguldak Tenis Kulübü', 'Ankara ATK', 'İzmir Kültürpark', 'İstanbul TED', 'Antalya ATİK', 'Bursa Podyum', 'Adana ATDSK', 'Mersin Tenis']
for i, team in enumerate(sample_teams):
    ws1.write(i+1, 3, team)

# Seçim alanları ve Dropdown
for i in range(1, 5):
    ws1.write(i, 0, f'{i}. Takım', sub_header_fmt)
    ws1.write(i, 1, sample_teams[i-1], team_fmt)
ws1.data_validation('B2:B5', {'validate': 'list', 'source': '=$D$2:$D$30'})

# --- SEKME 2: FİKSTÜR VE SKORLAR ---
ws2 = wb.add_worksheet('2. Maçlar')
ws2.set_column('A:C', 12)
ws2.set_column('D:E', 22)
ws2.set_column('F:K', 10)
ws2.set_column('L:W', 5) # Hesaplama sütunları (Daraltıldı)

headers_mac = ['Gün', 'Eşleşme', 'Branş', 'Takım 1', 'Takım 2', '1.Set (T1)', '1.Set (T2)', '2.Set (T1)', '2.Set (T2)', '3.Set (T1)', '3.Set (T2)']
for col, h in enumerate(headers_mac):
    ws2.write(0, col, h, header_fmt)

# Fikstür Mantığı:
# 1. Gün: 1-4 ve 2-3
# 2. Gün: 1-3 ve 2-4
# 3. Gün: 1-2 ve 3-4
matchups = [
    ('1. Gün', '1 ve 4', '=\'1. Ayarlar\'!$B$2', '=\'1. Ayarlar\'!$B$5'),
    ('1. Gün', '2 ve 3', '=\'1. Ayarlar\'!$B$3', '=\'1. Ayarlar\'!$B$4'),
    ('2. Gün', '1 ve 3', '=\'1. Ayarlar\'!$B$2', '=\'1. Ayarlar\'!$B$4'),
    ('2. Gün', '2 ve 4', '=\'1. Ayarlar\'!$B$3', '=\'1. Ayarlar\'!$B$5'),
    ('3. Gün', '1 ve 2', '=\'1. Ayarlar\'!$B$2', '=\'1. Ayarlar\'!$B$3'),
    ('3. Gün', '3 ve 4', '=\'1. Ayarlar\'!$B$4', '=\'1. Ayarlar\'!$B$5'),
]

row = 1
for day, desc, tA, tB in matchups:
    for branch in ['1. Tekler', '2. Tekler', 'Çiftler']:
        ws2.write(row, 0, day, sub_header_fmt)
        ws2.write(row, 1, desc, sub_header_fmt)
        ws2.write(row, 2, branch, sub_header_fmt)
        ws2.write_formula(row, 3, tA, team_fmt)
        ws2.write_formula(row, 4, tB, team_fmt)
        
        # Skor giriş kutuları (F, G, H, I, J, K)
        for col in range(5, 11):
            ws2.write(row, col, '', input_fmt)
            
        # --- ARKA PLAN HESAPLAMALARI (Otomatik) ---
        r = row + 1
        # Set 1 Win
        ws2.write_formula(row, 11, f'=IF(AND(ISNUMBER(F{r}),ISNUMBER(G{r})), IF(F{r}>G{r},1,0), 0)', calc_fmt) # L
        ws2.write_formula(row, 12, f'=IF(AND(ISNUMBER(F{r}),ISNUMBER(G{r})), IF(G{r}>F{r},1,0), 0)', calc_fmt) # M
        # Set 2 Win
        ws2.write_formula(row, 13, f'=IF(AND(ISNUMBER(H{r}),ISNUMBER(I{r})), IF(H{r}>I{r},1,0), 0)', calc_fmt) # N
        ws2.write_formula(row, 14, f'=IF(AND(ISNUMBER(H{r}),ISNUMBER(I{r})), IF(I{r}>H{r},1,0), 0)', calc_fmt) # O
        # Set 3 Win
        ws2.write_formula(row, 15, f'=IF(AND(ISNUMBER(J{r}),ISNUMBER(K{r})), IF(J{r}>K{r},1,0), 0)', calc_fmt) # P
        ws2.write_formula(row, 16, f'=IF(AND(ISNUMBER(J{r}),ISNUMBER(K{r})), IF(K{r}>J{r},1,0), 0)', calc_fmt) # Q
        # Total Sets Won
        ws2.write_formula(row, 17, f'=L{r}+N{r}+P{r}', calc_fmt) # R (T1 Setleri)
        ws2.write_formula(row, 18, f'=M{r}+O{r}+Q{r}', calc_fmt) # S (T2 Setleri)
        # Match Won
        ws2.write_formula(row, 19, f'=IF(R{r}>S{r},1,0)', calc_fmt) # T (T1 Maçı Kazandı)
        ws2.write_formula(row, 20, f'=IF(S{r}>R{r},1,0)', calc_fmt) # U (T2 Maçı Kazandı)
        # Total Games
        ws2.write_formula(row, 21, f'=SUM(F{r},H{r},J{r})', calc_fmt) # V (T1 Oyunları)
        ws2.write_formula(row, 22, f'=SUM(G{r},I{r},K{r})', calc_fmt) # W (T2 Oyunları)
        
        row += 1

# Gruplamak/Gizlemek istersen:
ws2.set_column('L:W', None, None, {'hidden': 1}) # Arka plan hesaplamalarını gizle

# --- SEKME 3: SIRALAMA ---
ws3 = wb.add_worksheet('3. Sıralama')
ws3.set_column('A:A', 22)
ws3.set_column('B:G', 15)

headers_sirala = ['Takım Adı', 'Aldığı Maç', 'Verdiği Maç', 'Aldığı Set', 'Verdiği Set', 'Aldığı Oyun', 'Verdiği Oyun']
for col, h in enumerate(headers_sirala):
    ws3.write(0, col, h, header_fmt)

for i in range(4):
    r_idx = i + 1
    t_ref = f'\'1. Ayarlar\'!B{i+2}'
    ws3.write_formula(r_idx, 0, f'={t_ref}', team_fmt)
    
    # Hesaplama Formülleri (SUMIFS ile T1 ve T2 sütunlarını kontrol ederek toplar)
    # Aldığı Maç = Takım 1 sütunundayken kazandığı maçlar (T sütunu) + Takım 2 sütunundayken kazandığı maçlar (U sütunu)
    ws3.write_formula(r_idx, 1, f'=SUMIFS(\'2. Maçlar\'!$T$2:$T$19, \'2. Maçlar\'!$D$2:$D$19, {t_ref}) + SUMIFS(\'2. Maçlar\'!$U$2:$U$19, \'2. Maçlar\'!$E$2:$E$19, {t_ref})', sub_header_fmt)
    # Verdiği Maç
    ws3.write_formula(r_idx, 2, f'=SUMIFS(\'2. Maçlar\'!$U$2:$U$19, \'2. Maçlar\'!$D$2:$D$19, {t_ref}) + SUMIFS(\'2. Maçlar\'!$T$2:$T$19, \'2. Maçlar\'!$E$2:$E$19, {t_ref})', sub_header_fmt)
    # Aldığı Set (R ve S)
    ws3.write_formula(r_idx, 3, f'=SUMIFS(\'2. Maçlar\'!$R$2:$R$19, \'2. Maçlar\'!$D$2:$D$19, {t_ref}) + SUMIFS(\'2. Maçlar\'!$S$2:$S$19, \'2. Maçlar\'!$E$2:$E$19, {t_ref})', sub_header_fmt)
    # Verdiği Set (S ve R)
    ws3.write_formula(r_idx, 4, f'=SUMIFS(\'2. Maçlar\'!$S$2:$S$19, \'2. Maçlar\'!$D$2:$D$19, {t_ref}) + SUMIFS(\'2. Maçlar\'!$R$2:$R$19, \'2. Maçlar\'!$E$2:$E$19, {t_ref})', sub_header_fmt)
    # Aldığı Oyun (V ve W)
    ws3.write_formula(r_idx, 5, f'=SUMIFS(\'2. Maçlar\'!$V$2:$V$19, \'2. Maçlar\'!$D$2:$D$19, {t_ref}) + SUMIFS(\'2. Maçlar\'!$W$2:$W$19, \'2. Maçlar\'!$E$2:$E$19, {t_ref})', sub_header_fmt)
    # Verdiği Oyun (W ve V)
    ws3.write_formula(r_idx, 6, f'=SUMIFS(\'2. Maçlar\'!$W$2:$W$19, \'2. Maçlar\'!$D$2:$D$19, {t_ref}) + SUMIFS(\'2. Maçlar\'!$V$2:$V$19, \'2. Maçlar\'!$E$2:$E$19, {t_ref})', sub_header_fmt)

wb.close()
file_path
