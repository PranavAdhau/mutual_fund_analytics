# 📈 Mutual Fund Analytics & Performance Dashboard (Finance & Investment Industry)

---

## 📌 Executive Summary

**Business Problem:**

Individual investors and analysts often struggle to track and compare mutual fund performance due to scattered data, non-standardized returns, and limited access to analytical insights such as risk-adjusted metrics (**Sharpe, Sortino**) or rolling return trends.

**Solution:**

This project builds an end-to-end **Mutual Fund Analytics Pipeline** integrating NAV data from **MFAPI** into a **PostgreSQL** database through automated Python ETL scripts and Jupyter-based KPI computation notebooks. The results are visualized through an interactive **Power BI dashboard** offering **CAGR, Sharpe, Sortino, Volatility, and SIP vs Lumpsum analysis**.

**Impact (Learning Outcomes):**

* Designed a fully automated financial data pipeline aligned with industry **ETL standards**.
* Computed comprehensive fund performance metrics used in asset management.
* Built an interactive dashboard that enables dynamic filtering and fund-level drill-through analysis.
* Demonstrated integration of **Python, SQL, and Power BI** for real-world financial analytics.

---

## 🔎 Business Context

In the investment management domain, understanding fund performance goes beyond simple returns.

Professionals evaluate risk-adjusted metrics, rolling returns, and consistency across time horizons to guide portfolio allocation and investor recommendations.

📊 **Without such an integrated pipeline, analysts struggle to answer:**

* Which mutual funds outperform their peers on a risk-adjusted basis (Sharpe, Sortino)?
* How do small-cap and debt funds differ in volatility and CAGR?
* How does SIP performance (XIRR) compare to Lumpsum over 3Y, 5Y, and 10Y periods?
* What is the historical trend of NAV and rolling returns for each fund?

---

## ⚙️ Methodology

This project follows a modular and automated pipeline design, built around industry ETL and data modeling best practices.

### 1️⃣ Data Ingestion

* **Source:** MFAPI (https://www.mfapi.in) – daily NAV data for selected active mutual funds.
* **Scripts:**
    * `01_historical_load.py` → Initial full data load.
    * `02_daily_update.py` → Incremental daily updates (safe for scheduler use).
    * `03_build_master_table.py` → Combines and stores master NAV history.

### 2️⃣ Data Transformation & KPI Computation (via Jupyter Notebooks)

* `01_data_cleaning.ipynb` – Cleans and standardizes NAV data, fills missing dates, assigns fund categories and types.
* `02_advanced_kpis.ipynb` – Calculates **Sharpe, Sortino, Volatility**, cumulative returns, and SIP growth.
* `03_return_calculations.ipynb` – Computes **CAGR, XIRR, P2P returns, and rolling returns** using financial formulas.
* `04_bi_db_load.ipynb` – Loads processed metrics into PostgreSQL for BI visualization.

### 3️⃣ Database Modeling (PostgreSQL)

A normalized schema ensures efficient querying and scalability.

Tables include:
* `fund_master` – Fund metadata
* `nav_history` – Complete NAV records
* `returns_lumpsum`, `returns_sip`, `returns_p2p` – Periodic return metrics
* `risk_metrics` – Sharpe, Sortino, and Volatility
* `daily_return` – Day-wise NAV and returns
* `rolling_return` – Time-series of rolling CAGR

#### 📘 ER Diagram:

![ER Diagram](tableau/screenshots/mutual_fund_database_schema_er_diagram.jpg)


### 4️⃣ Automation

`run_daily_pipeline.py` automates:

* Daily NAV updates
* Execution of notebooks sequentially
* Refresh of processed data for BI dashboards

This structure supports scheduling via Task Scheduler, Cron, or GitHub Actions.

### 5️⃣ Visualization – Power BI Dashboard

Interactive visuals for both portfolio-level and fund-level insights.

#### Main Dashboard

Features:

* KPIs – Lumpsum CAGR, Sharpe, Sortino, Volatility, and P2P Returns
* Filters – Investment Type, Fund Category, Period
* Charts – NAV Trend, Risk vs Return Scatter, Fund Category Summary

![Main Dashboard](tableau/screenshots/01_mutual_fund_performance_dashboard_overview.jpg)

#### Drill-Through Fund View

Details include:

* Fund-specific CAGR, XIRR, Volatility, and Max Drawdown
* Rolling return trends
* Sortino vs Volatility bubble visualization
* Table of recent daily returns

![Drillthrough Fund View – Power BI Dashboard](tableau/screenshots/02_mutual_fund_drillthrough_fund_view.jpg)

---

## 🛠️ Skills & Technologies

**Languages & Tools:**

**Python** (Pandas, SQLAlchemy, Requests), Jupyter Notebook, **PostgreSQL, Power BI**

**Core Concepts & Techniques:**

* Financial KPI Computation (CAGR, XIRR, Sharpe, Sortino, Rolling Returns)
* ETL Design & Data Automation
* SQL Data Modeling and Validation
* Data Visualization and Storytelling in BI tools
* Task Automation (Daily Pipeline Execution)

---

## 📊 Results & Business Insights

### ✅ Results

* End-to-end automated mutual fund analytics pipeline with PostgreSQL backend.
* All data is updated dynamically and ready for BI consumption.
* Dashboard reveals clear **risk–return tradeoffs** and fund consistency over time.

### 💡 Business Insights

* Equity Small Cap funds (e.g., Nippon India Small Cap) show the **highest CAGR but higher volatility**.
* Hybrid/Balanced funds deliver stability with moderate risk-adjusted performance.
* Debt funds show lowest volatility but lower returns.
* **SIP investing demonstrates smoother long-term compounding** compared to lumpsum volatility.

---

## 🔮 Next Steps

* Add Benchmark Indices (Nifty 50 TRI, Nifty Midcap 150 TRI) for fund vs. index comparison.
* Integrate AUM, Expense Ratio & Fund Manager data for qualitative scoring.
* Deploy a **Streamlit Web App** for real-time fund comparison.
* Automate Daily BI Refresh using Power BI Service or GitHub Actions.

---

## 📂 Repository Structure

```bash
MUTUAL_FUND_ANALYTICS/
│
├── data/
│   ├── raw/                     # Raw MFAPI NAV data
│   │   ├── master_table_raw.csv
│   │   └── master_table.csv
│   └── processed/               # Processed outputs for DB and BI
│       ├── daily_return.csv
│       ├── lumpsum_cagr.csv
│       ├── p2p_returns.csv
│       ├── rolling_all_funds.csv
│       ├── sharpe.csv
│       ├── sip_xirr.csv
│       └── sortino.csv
│
├── notebooks/                   # Data cleaning and KPI computation
│   ├── 01_data_cleaning.ipynb
│   ├── 02_advanced_kpis.ipynb
│   ├── 03_return_calculations.ipynb
│   └── 04_bi_db_load.ipynb
│
├── scripts/                     # Automated ETL scripts
│   ├── 01_historical_load.py
│   ├── 02_daily_update.py
│   └── 03_build_master_table.py
│
├── sql_scripts/                 # Database setup and validation
│   ├── 01_schema_tables_and_relations.sql
│   └── 02_data_validation_queries.sql
│
├── tableau/                     # Power BI dashboard and screenshots
│   ├── screenshots/
│   │   ├── 01_mutual_fund_performance_dashboard_overview.png
│   │   ├── 02_mutual_fund_drillthrough_fund_view.png
│   │   └── mutual_fund_database_schema_er_diagram.png
│   └── mf_BI_dashboard.pbix
│
├── run_daily_pipeline.py        # Automated daily ETL + notebook runner
├── requirements.txt             # Dependencies
└── README.md

```
