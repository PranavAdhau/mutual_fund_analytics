"""
master_table_load.py
--------------------
Purpose:
    - Fetch complete NAV history from PostgreSQL (nav_history table)
    - Save combined master table as CSV (raw and processed copies)
    - Acts as a reference dataset for analysis and dashboards

WARNING:
    - This script only reads data (no modification to database)
    - Run this after historical_load.py and daily_update.py
"""

import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine('postgresql+psycopg2://postgres:PnA1165@localhost:5432/mutual_funds_db')

# Folders (fixed absolute paths)
raw_folder = Path(r"C:\Users\lenovo\Desktop\mutual_fund_analytics\data\raw")
processed_folder = Path(r"C:\Users\lenovo\Desktop\mutual_fund_analytics\data")
raw_folder.mkdir(parents=True, exist_ok=True)
processed_folder.mkdir(parents=True, exist_ok=True)

# Fetch all NAV history
query = "SELECT fund_name, nav_date, nav_value FROM nav_history ORDER BY fund_name, nav_date;"
df_master = pd.read_sql(query, engine)

# Save master table CSVs (explicit absolute paths)
df_master.to_csv(raw_folder / "master_table_raw.csv", index=False)
df_master.to_csv(processed_folder / "master_table.csv", index=False)

print(f"[OK] Master table created with {len(df_master)} rows")
