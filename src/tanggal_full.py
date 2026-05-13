import pandas as pd

# Membuat rentang waktu setiap hari tanpa bolong
dates = pd.date_range(start='2018-01-01', end='2025-12-31')

# Menyimpan ke file teks baru
with open('list_tanggal_full.txt', 'w') as f:
    for d in dates:
        f.write(d.strftime('%d-%m-%Y') + '\n')

print(f"✅ Berhasil membuat {len(dates)} tanggal (Setiap hari dari 2018-2025)!")