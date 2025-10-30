CREATE TABLE IF NOT EXISTS fund_master (
    fund_id SERIAL PRIMARY KEY,
    fund_name TEXT UNIQUE,
    cap TEXT,
    fund_type TEXT
);

CREATE TABLE IF NOT EXISTS nav_history (
    id SERIAL PRIMARY KEY,
    fund_id INT REFERENCES fund_master(fund_id),
    nav_date DATE,
    nav_value NUMERIC
);

CREATE TABLE IF NOT EXISTS returns_lumpsum (
    fund_id INT REFERENCES fund_master(fund_id),
    period TEXT,
    cagr NUMERIC
);

CREATE TABLE IF NOT EXISTS returns_sip (
    fund_id INT REFERENCES fund_master(fund_id),
    period TEXT,
    xirr NUMERIC
);

CREATE TABLE IF NOT EXISTS returns_p2p (
    fund_id INT REFERENCES fund_master(fund_id),
    period TEXT,
    p2p_return NUMERIC
);

CREATE TABLE IF NOT EXISTS risk_metrics (
    fund_id INT REFERENCES fund_master(fund_id),
    horizon TEXT,
    cagr NUMERIC,
    volatility NUMERIC,
    sharpe NUMERIC,
    sortino NUMERIC
);

-- Daily Return Table
CREATE TABLE IF NOT EXISTS daily_return (
    fund_id INT REFERENCES fund_master(fund_id),
    nav_date DATE,
    nav_value NUMERIC,
    daily_return NUMERIC
);

-- Rolling Return Table (Updated Long Format)
CREATE TABLE IF NOT EXISTS rolling_return (
    fund_id INT REFERENCES fund_master(fund_id),
    nav_date DATE NOT NULL,
    horizon TEXT NOT NULL,   -- e.g., '1M', '6M', '1Y', '3Y', '5Y'
    cagr NUMERIC(10, 4)     -- CAGR rounded to 4 decimals
);
