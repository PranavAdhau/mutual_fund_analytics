-- ===============================================
-- 🔍 VALIDATION SCRIPT FOR MUTUAL FUND DATABASE
-- ===============================================

-- 1️⃣ Check all records from the master table to verify fund details
SELECT * 
FROM fund_master;

-- 2️⃣ Validate that the NAV data is properly loaded
--     → Fetch the 5 most recent NAV entries per fund
--     → Useful for confirming daily update scripts are working correctly
SELECT 
    fund_id,
    nav_date,
    nav_value
FROM (
    SELECT 
        fund_id,
        nav_date,
        nav_value,
        ROW_NUMBER() OVER (PARTITION BY fund_id ORDER BY nav_date DESC) AS rn
    FROM nav_history
) t
WHERE rn <= 5
ORDER BY fund_id, nav_date DESC;

-- 3️⃣ Check total NAV records to confirm data volume after load
SELECT COUNT(*) 
FROM nav_history;

-- 4️⃣ Validate calculated returns for different investment modes
--     (Lump Sum, SIP, and Point-to-Point returns)
SELECT * FROM returns_lumpsum;
SELECT * FROM returns_sip;
SELECT * FROM returns_p2p;

-- 5️⃣ Verify risk metrics (volatility, Sharpe ratio, Sortino ratio, etc.)
SELECT * 
FROM risk_metrics;

-- 6️⃣ Inspect recent daily returns for all funds
--     → Ensures that daily_return script is generating values correctly
SELECT *
FROM daily_return
ORDER BY fund_id ASC, nav_date DESC;

-- 7️⃣ Check rolling returns for a specific fund (example: fund_id = 1)
--     → Filtering for 3-year horizon as sample validation
SELECT *
FROM rolling_return
WHERE fund_id = 1 
  AND horizon IN ('3Y')
ORDER BY fund_id, nav_date DESC, horizon;

-- ===============================================
-- ✅ END OF VALIDATION SCRIPT
-- ===============================================
