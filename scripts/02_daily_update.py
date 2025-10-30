"""
daily_update.py
----------------
Purpose:
    - Fetch latest NAV for each fund from MFAPI
    - Append only new records to nav_history (no duplicates)
    - Safe for daily scheduling via Cron, Task Scheduler, or GitHub Actions

WARNING:
    - This script does NOT truncate or reload full data.
    - It only inserts new daily NAV values.
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

# PostgreSQL connection
engine = create_engine(
    'postgresql+psycopg2://postgres:PnA1165@localhost:5432/mutual_funds_db'
)

# Folder paths (fixed absolute paths)
raw_folder = Path(r"C:\Users\lenovo\Desktop\mutual_fund_analytics\data\raw")
processed_folder = Path(r"C:\Users\lenovo\Desktop\mutual_fund_analytics\data")
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
# DAILY UPDATE LOGIC
# -------------------------------
all_latest = []

for fund_name, fund_id in funds.items():
    try:
        print(f"[INFO] Fetching latest NAV for {fund_name}...")
        df_latest = fetch_nav(fund_id, latest=True)
        df_latest['fund_name'] = fund_name

        # Avoid inserting duplicates
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT nav_date FROM nav_history WHERE fund_name = :fname"),
                {"fname": fund_name}
            )
            existing_dates = [row[0] for row in result.fetchall()]

        df_latest = df_latest[~df_latest['nav_date'].isin(existing_dates)]

        if not df_latest.empty:
            df_latest[['fund_name', 'nav_date', 'nav_value']].to_sql(
                'nav_history', engine, if_exists='append', index=False,
                method='multi'
            )
            all_latest.append(df_latest[['fund_name', 'nav_date', 'nav_value']])
            print(f"[OK] {len(df_latest)} new record(s) added for {fund_name}")
        else:
            print(f"[INFO] No new NAV for {fund_name} today.")
    except Exception as e:
        print(f"[ERROR] Failed to update {fund_name}: {e}")

# Save combined latest update
if all_latest:
    latest_df = pd.concat(all_latest, ignore_index=True)
    latest_df.to_csv(raw_folder / "master_table_raw.csv", index=False)
    latest_df.to_csv(processed_folder / "master_table.csv", index=False)
    print(f"[OK] Combined master CSVs updated: master_table_raw.csv & master_table.csv")

print("[DONE] Daily NAV update completed.")
