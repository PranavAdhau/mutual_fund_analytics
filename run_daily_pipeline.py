import subprocess
import time
import os

# --- Define folder paths ---
base_path = r"C:\Users\lenovo\Desktop\mutual_fund_analytics"
scripts_path = os.path.join(base_path, "scripts")
notebooks_path = os.path.join(base_path, "notebooks")

# --- Step 1: Run scripts (02 and 03 only) ---
print("Running Scripts...")
subprocess.run(["python", os.path.join(scripts_path, "02_daily_update.py")], check=True)
subprocess.run(["python", os.path.join(scripts_path, "03_build_master_table.py")], check=True)
print("[OK] Scripts completed successfully.")

# Wait a few seconds between steps
time.sleep(10)

# --- Step 2: Run notebooks in sequence (01 → 04) ---
print("Running Notebooks...")
notebooks = [
    "01_data_cleaning.ipynb",
    "02_advanced_kpis.ipynb",
    "03_return_calculations.ipynb",
    "04_bi_db_load.ipynb"
]

for nb in notebooks:
    notebook_path = os.path.join(notebooks_path, nb)
    print(f"[RUNNING] {nb}")
    subprocess.run([
        "jupyter", "nbconvert", "--to", "notebook",
        "--execute", notebook_path, "--inplace"
    ], check=True)

print("[OK] All notebooks executed successfully.")
