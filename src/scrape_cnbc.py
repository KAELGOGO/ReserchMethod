import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

# === KONFIGURASI RISET CNBC INDONESIA ===
OUTPUT_FILE = "dataset_cnbc.csv"
FILE_TANGGAL = "list_tanggal_full.txt"

if not os.path.exists(FILE_TANGGAL):
    print(f"❌ Error: File {FILE_TANGGAL} tidak ditemukan!")
    exit()

with open(FILE_TANGGAL, 'r') as f:
    target_dates = [line.strip() for line in f.readlines()]

print(f"=== CNBC INVISIBLE SCRAPER: DATA ENRICHMENT MENUJU SCOPUS ===")
print("Catatan: CNBC Indonesia baru rilis Februari 2018. Hasil 0 di Januari 2018 adalah wajar.")

options = uc.ChromeOptions()
# options.add_argument('--headless') # Biarkan terbuka dulu agar aman dari CAPTCHA
driver = uc.Chrome(options=options, version_main=145)

database_cnbc = []
processed_dates = set()

# Resume logic
if os.path.exists(OUTPUT_FILE):
    try:
        df_old = pd.read_csv(OUTPUT_FILE)
        processed_dates = set(df_old['Tanggal'].tolist())
        database_cnbc = df_old.to_dict('records')
        print(f"[i] Resume: {len(processed_dates)} hari aman di database CNBC.")
    except Exception as e: 
        print(f"[!] Gagal membaca database lama: {e}")

try:
    for tgl in target_dates:
        if tgl in processed_dates: continue

        # Format Tanggal Indeks CNBC: YYYY/MM/DD
        d, m, y = tgl.split('-')
        tgl_cnbc_url = f"{y}/{m}/{d}"
        
        # Kunci Filter URL CNBC: YYYYMMDD (Contoh: 20181030)
        url_date_code = f"{y}{m}{d}" 
        
        # URL Indeks Utama CNBC Indonesia
        url = f"https://www.cnbcindonesia.com/indeks?date={tgl_cnbc_url}"
        print(f"[+] Visiting CNBC {tgl}...", end=" ", flush=True)
        
        try:
            driver.get(url)
            time.sleep(random.uniform(4, 7)) 
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            all_links = soup.find_all('a', href=True)
            
            day_count = 0
            for link in all_links:
                judul = link.get_text(strip=True).replace('\n', ' ').replace('\r', '')
                href = link['href']
                
                # FILTER KETAT CNBC:
                # 1. Pastikan link mengandung tanggal target (mencegah berita masa depan masuk)
                # 2. Judul artikel cukup panjang
                # 3. Hindari link tag/profil/video agar teksnya murni berita artikel
                if url_date_code in href and len(judul) > 30 and "/tag/" not in href and "/profil/" not in href and "/video/" not in href:
                    
                    full_url = href if href.startswith('http') else f"https://www.cnbcindonesia.com{href}"
                    
                    database_cnbc.append({
                        "Tanggal": tgl, 
                        "Sumber": "CNBC Indonesia",
                        "Judul": judul, 
                        "Link": full_url
                    })
                    day_count += 1
            
            # De-duplikasi harian
            df_day = pd.DataFrame(database_cnbc[-day_count:] if day_count > 0 else [])
            if not df_day.empty:
                df_day = df_day.drop_duplicates(subset=['Judul'])
                
            print(f"✅ (Bersih: {len(df_day) if not df_day.empty else 0} berita)")
            processed_dates.add(tgl)
            
            # Auto-save tiap 5 hari
            if len(processed_dates) % 5 == 0:
                pd.DataFrame(database_cnbc).drop_duplicates(subset=['Judul']).to_csv(OUTPUT_FILE, index=False)
                
        except Exception as e:
            print(f"⚠️ Skip {tgl} karena error halaman: {e}")
            continue

finally:
    driver.quit()

# Final Save
df_final = pd.DataFrame(database_cnbc).drop_duplicates(subset=['Judul'])
df_final.to_csv(OUTPUT_FILE, index=False)
print(f"\n🎉 DATA CNBC READY! Total {len(df_final)} berita berhasil ditambahkan.")
