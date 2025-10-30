"""
historical_load.py
-------------------
Purpose:
    - Fetch full historical NAVs for all funds from MFAPI
    - Truncate nav_history table in PostgreSQL
    - Insert fresh data (clean load)
    - Save single combined CSV backups (raw & processed)

WARNING:
    - This script will delete all old records from nav_history before inserting.
    - Run this only once initially or when you want a complete reload.
"""

import requests
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

# -------------------------------
# CONFIGURATION (Updated Fund List) 
# -------------------------------
funds = {
    "Nippon India Small Cap Fund - Growth": 118778,
    "DSP Midcap Fund – Direct Plan – Growth": 119071,
    "HDFC Large and Mid Cap Fund - Growth": 130498,
    "SBI Large & Midcap Fund - Growth": 119721,
    "ICICI Prudential Large Cap Fund (erstwhile Bluechip Fund) – Direct Plan – Growth": 120586,
    "UTI Nifty 50 Index Fund - Growth": 120716,
    "ICICI Prudential Balanced Advantage Fund - Growth": 120377,
    "HDFC Corporate Bond Fund - Growth": 118987
}

# Folder paths for backup (fixed absolute paths)
raw_folder = Path(r"C:\Users\lenovo\Desktop\mutual_fund_analytics\data\raw")
processed_folder = Path(r"C:\Users\lenovo\Desktop\mutual_fund_analytics\data")

# PostgreSQL connection
engine = create_engine(
    'postgresql+psycopg2://postgres:PnA1165@localhost:5432/mutual_funds_db'
)

# Ensure folders exist
raw_folder.mkdir(parents=True, exist_ok=True)
processed_folder.mkdir(parents=True, exist_ok=True)

# -------------------------------
# HELPER FUNCTION: Fetch NAV
# -------------------------------
def fetch_nav(fund_id, latest=False):
    """Fetch NAV data from MFAPI"""
    url = f"https://api.mfapi.in/mf/{fund_id}/latest" if latest else f"https://api.mfapi.in/mf/{fund_id}"
    response = requests.get(url)
    data = response.json()
    if data['status'] != 'SUCCESS':
        raise ValueError(f"API call failed for fund {fund_id}")
    df = pd.DataFrame(data['data'])
    df['nav_date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df['nav_value'] = pd.to_numeric(df['nav'], errors='coerce')
    df = df[['nav_date', 'nav_value']].sort_values("nav_date")
    return df

# -------------------------------
# STEP 1: TRUNCATE TABLE
# -------------------------------
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE nav_history RESTART IDENTITY;"))
print("[OK] nav_history table truncated (old records removed).")

# -------------------------------
# STEP 2: Fetch & Insert Data
# -------------------------------
all_data = []

for fund_name, fund_id in funds.items():
    try:
        print(f"[INFO] Fetching historical data for {fund_name}...")
        df_hist = fetch_nav(fund_id, latest=False)
        df_hist['fund_name'] = fund_name
        df_db = df_hist[['fund_name', 'nav_date', 'nav_value']]
        all_data.append(df_db)

        # Insert all records
        df_db.to_sql(
            'nav_history', engine, if_exists='append', index=False,
            method='multi'
        )

        print(f"[OK] {len(df_db)} records inserted for {fund_name}.")
    except Exception as e:
        print(f"[ERROR] Failed for {fund_name}: {e}")

# Combine and save single CSVs
if all_data:
    master_df = pd.concat(all_data, ignore_index=True)
    master_df.to_csv(raw_folder / "master_table_raw.csv", index=False)
    master_df.to_csv(processed_folder / "master_table.csv", index=False)
    print(f"[OK] Combined master CSVs created: master_table_raw.csv & master_table.csv")

print("[DONE] All funds loaded successfully into PostgreSQL.")
