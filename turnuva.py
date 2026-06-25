import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Define file paths
files = {
    'Erkek A': {
        'giris': 'ERKEK A GRUBU.xlsx - ERKEK A GRUBU.csv',
        'maclar': 'ERKEK A GRUBU.xlsx - 2. Maçlar.csv',
        'siralamalar': 'ERKEK A GRUBU.xlsx - 3. Sıralama.csv'
    },
    'Erkek B': {
        'giris': 'ERKEK B GRUBU.xlsx - ERKEK B GRUBU.csv',
        'maclar': 'ERKEK B GRUBU.xlsx - 2. Maçlar.csv',
        'siralamalar': 'ERKEK B GRUBU.xlsx - 3. Sıralama.csv'
    },
    'Kadın A': {
        'giris': 'KADIN A GRUBU.xlsx - KADIN A GRUBU.csv',
        'maclar': 'KADIN A GRUBU.xlsx - 2. Maçlar.csv',
        'siralamalar': 'KADIN A GRUBU.xlsx - 3. Sıralama.csv'
    },
    'Kadın B': {
        'giris': 'KADIN B GRUBU.xlsx - KADINLAR B GRUBU.csv',
        'maclar': 'KADIN B GRUBU.xlsx - 2. Maçlar.csv',
        'siralamalar': 'KADIN B GRUBU.xlsx - 3. Sıralama.csv'
    }
}

# Let's inspect the columns of each file to handle them correctly
for group, paths in files.items():
    print(f"--- {group} ---")
    df_g = pd.read_csv(paths['giris'])
    df_m = pd.read_csv(paths['maclar'])
    df_s = pd.read_csv(paths['siralamalar'])
    print("Giriş:", df_g.columns.tolist(), df_g.shape)
    print("Maçlar:", df_m.columns.tolist()[:10], df_m.shape)
    print("Sıralama:", df_s.columns.tolist(), df_s.shape)
