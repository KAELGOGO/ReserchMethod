import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

# === KONFIGURASI RISET KELVIN & OWEN ===
OUTPUT_FILE = "dataset_indofinbert_bersih_tanggalFULLAfter29-10-2023.csv"
FILE_TANGGAL = "list_tanggal_full.txt"

if not os.path.exists(FILE_TANGGAL):
    print(f"❌ Error: File {FILE_TANGGAL} tidak ditemukan!")
    exit()

with open(FILE_TANGGAL, 'r') as f:
    target_dates = [line.strip() for line in f.readlines()]

print(f"=== STRICT INVISIBLE SCRAPER: 969 HARI MENUJU SCOPUS ===")

options = uc.ChromeOptions()
# options.add_argument('--headless')
driver = uc.Chrome(options=options)

database_all = []
processed_dates = set()

# Resume logic
if os.path.exists(OUTPUT_FILE):
    try:
        df_old = pd.read_csv(OUTPUT_FILE)
        processed_dates = set(df_old['Tanggal'].tolist())
        database_all = df_old.to_dict('records')
        print(f"[i] Resume: {len(processed_dates)} hari aman di database.")
    except Exception as e: 
        print(f"[!] Gagal membaca database lama: {e}")

try:
    for tgl in target_dates:
        if tgl in processed_dates: continue

        # Format URL indeks: YYYY-MM-DD
        d, m, y = tgl.split('-')
        tgl_fixed = f"{y}-{m}-{d}"
        
        # KUNCI FILTER: Format tanggal di dalam link berita Bisnis.com (YYYYMMDD)
        # Contoh: 20180111
        url_date_code = f"{y}{m}{d}" 
        
        url = f"https://www.bisnis.com/index?date={tgl_fixed}"
        print(f"[+] Visiting {tgl}...", end=" ", flush=True)
        
        try:
            driver.get(url)
            time.sleep(random.uniform(4, 7)) 
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            all_links = soup.find_all('a', href=True)
            
            day_count = 0
            for link in all_links:
                # Membersihkan judul dari spasi berlebih atau karakter \n
                judul = link.get_text(strip=True).replace('\n', ' ').replace('\r', '')
                href = link['href']
                
                # FILTER GANDA: 
                # 1. Pastikan itu artikel bacaan (/read/)
                # 2. Pastikan kode tanggal di URL sesuai dengan tanggal target (mencegah berita 2026 masuk)
                # 3. Pastikan judul cukup panjang (bukan sekadar navigasi web)
                if "/read/" in href and url_date_code in href and len(judul) > 30:
                    
                    full_url = href if href.startswith('http') else f"https://www.bisnis.com{href}"
                    
                    database_all.append({
                        "Tanggal": tgl, 
                        "Judul": judul, 
                        "Link": full_url
                    })
                    day_count += 1
            
            # Hapus duplikat harian sebelum dimasukkan ke database utama
            df_day = pd.DataFrame(database_all[-day_count:] if day_count > 0 else [])
            if not df_day.empty:
                df_day = df_day.drop_duplicates(subset=['Judul'])
                
            print(f"✅ (Bersih: {len(df_day) if not df_day.empty else 0} berita)")
            processed_dates.add(tgl)
            
            # Auto-save
            if len(processed_dates) % 5 == 0:
                pd.DataFrame(database_all).drop_duplicates(subset=['Judul']).to_csv(OUTPUT_FILE, index=False)
                
        except Exception as e:
            print(f"⚠️ Skip {tgl} karena error halaman: {e}")
            continue

finally:
    driver.quit()

# Final Save & Deep Clean
df_final = pd.DataFrame(database_all).drop_duplicates(subset=['Judul'])
df_final.to_csv(OUTPUT_FILE, index=False)
print(f"\n🎉 DATA BERSIH READY! Total {len(df_final)} berita murni tanpa noise.")