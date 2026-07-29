-- ============================================================
-- Fixed SQL queries
-- Headers Fixed from sqlite standard format (example c8 is now On_Scene_Time_Minutes)
-- Analysis of call_vol(avg)+delt_time(avg) was fixed to be grouped by call_vol NOT On_Scene_Time
-- Ambulance Response Performance Analysis SQL Queries
-- Table: ambulance_response_data_CLEAN
-- ============================================================


-- ------------------------------------------------------------
-- 1. Overall Averages(delta time and call volume)
-- ------------------------------------------------------------
SELECT 
    ROUND(AVG(Response_Delta_Minutes), 2) AS Avg_Response_Delta
    ROUND(AVG(Daily_Call_Volume), 2) AS Avg_Daily_Call_Volume
FROM 
    ambulance_response_data_CLEAN;

-- ------------------------------------------------------------
-- 2. Generate Table for High_Delt COUNT per each Call_Vol level
(Altered this query: Changed ">" signs to "<" for Low_Delt + Low_Call_Vol COUNT per each Call_Vol level)
-- ------------------------------------------------------------
SELECT
    Daily_Call_Volume,
    COUNT(*) AS Quantity
FROM 
    ambulance_response_data_CLEAN
WHERE Response_Delta_Minutes > 12
  AND Daily_Call_Volume > 54
GROUP BY Daily_Call_Volume
ORDER BY Daily_Call_Volume DESC;
-- ------------------------------------------------------------
-- 3. Late Rate by Pay Tier
-- Core insight query; ties directly to the "% of Calls On Time by Pay Tier" visual in the dashboard.
-- Laymens output Pay_Tier || Late_Calls || Late_Calls/Total_Calls
-- The TRUE are text not boolean values so doublecheck the formats and remove quotations if it's coming in as bool
-- ------------------------------------------------------------
RESULTS     FOR       THIS       BELOW
-- ------------------------------------------------------------
Pay_Tier | Total_Calls | Late_Calls | Late_Rate
-- "Low ($19-21)"	"194"	"148"	"0.76"
-- "High ($28-35)"	"98"	"33"	"0.34"

-- ------------------------------------------------------------
SELECT
    Pay_Tier,
    COUNT(*) AS Total_Calls,
    SUM(CASE WHEN Is_Late = 'TRUE' THEN 1 ELSE 0 END) AS Late_Calls,
    ROUND(
        SUM(CASE WHEN Is_Late = 'TRUE' THEN 1 ELSE 0 END) * 1.0 / COUNT(*),
        2
    ) AS Late_Rate
FROM ambulance_response_data_CLEAN
GROUP BY Pay_Tier
ORDER BY Late_Rate DESC;


-- ------------------------------------------------------------
-- 4. Company Perfomance Scorecard
-- Avg delta + late rate per company 
-- useful for a "which vendor underperforms" narrative.
-- ------------------------------------------------------------
RESULTS     FOR       THIS       BELOW
-- ------------------------------------------------------------
Company | Total_Calls | Avg_Delta | Late_Rate
-- "AMR"	"50"	"16.9"	"0.72"
-- "Hunter Ambulance"	"46"	"16.22"	"0.85"
-- "Citywide Ambulance"	"56"	"13.25"	"0.73"
-- "Senior Care Ambulance"	"42"	"10.95"	"0.76"
-- "Ambulnz"	"52"	"8.52"	"0.42"
-- "Mount Sinai"	"46"	"5.46"	"0.24"

-- ------------------------------------------------------------
SELECT
    Company,
    COUNT(*) AS Total_Calls,
    ROUND(AVG(Response_Delta_Minutes), 2) AS Avg_Delta,
    ROUND(
        SUM(CASE WHEN Is_Late = TRUE THEN 1 ELSE 0 END) * 1.0 / COUNT(*),
        2
    ) AS Late_Rate
FROM ambulance_response_data_CLEAN
GROUP BY Company
ORDER BY Avg_Delta DESC;

-- ------------------------------------------------------------
-- 5. Company Ranking by Avg Delta (window function version)
--    Same idea as #4 but demonstrates RANK() over a subquery —
--    good to have both a subquery and a window-function example
--    in the same file.
-- ------------------------------------------------------------
RESULTS     FOR       THIS       BELOW
-- ------------------------------------------------------------
Company | Avg_Delt | Ranking
-- "Mount Sinai"	"5.46"	"1"
-- "Ambulnz"	"8.52"	"2"
-- "Senior Care Ambulance"	"10.95"	"3"
-- "Citywide Ambulance"	"13.25"	"4"
-- "Hunter Ambulance"	"16.22"	"5"
-- "AMR"	"16.9"	"6"

-- ------------------------------------------------------------
SELECT
    Company,
    Avg_Delta,
    RANK() OVER (ORDER BY Avg_Delta ASC) AS Rank_Best_To_Worst
FROM (
    SELECT
        Company,
        ROUND(AVG(Response_Delta_Minutes), 2) AS Avg_Delta
    FROM ambulance_response_data_CLEAN
    GROUP BY Company
) AS company_avg;


-- ------------------------------------------------------------
-- 6. Pay Rate vs Performance Rating
--    Checks whether higher pay also correlates with subjective
--    performance rating, not just response time.
-- ------------------------------------------------------------
RESULTS     FOR       THIS       BELOW
-- ------------------------------------------------------------
rating | total_Calls | avg_Pay
-- "Poor"	"42"	"26.11"
-- "Good"	"67"	"24.18"
-- "Fair"	"73"	"23.98"
-- "Below Average"	"34"	"23.82"
-- "Excellent"	"76"	"23.79"
-- ------------------------------------------------------------
SELECT
    Performance_Rating,
    COUNT(*) AS Total_Calls,
    ROUND(AVG(Pay_Rate_Hourly), 2) AS Avg_Pay
FROM ambulance_response_data_CLEAN
GROUP BY Performance_Rating
ORDER BY Avg_Pay DESC;


-- ------------------------------------------------------------
-- 7. Shift Comparison (Day vs Night)
-- ------------------------------------------------------------
SELECT
    Shift_Type,
    COUNT(*) AS Total_Calls,
    ROUND(AVG(Response_Delta_Minutes), 2) AS Avg_Delta,
    ROUND(
        SUM(CASE WHEN Is_Late = TRUE THEN 1 ELSE 0 END) * 1.0 / COUNT(*),
        2
    ) AS Late_Rate
FROM ambulance_response_data_CLEAN
GROUP BY Shift_Type
ORDER BY Late_Rate DESC;


-- ------------------------------------------------------------
-- 8. Call Type vs Response Delta
--    Do Emergency calls actually get faster responses than
--    Non-Emergency, as you'd expect operationally?
-- ------------------------------------------------------------
SELECT
    Call_Type,
    COUNT(*) AS Total_Calls,
    ROUND(AVG(Response_Delta_Minutes), 2) AS Avg_Delta,
    ROUND(
        SUM(CASE WHEN Is_Late = TRUE THEN 1 ELSE 0 END) * 1.0 / COUNT(*),
        2
    ) AS Late_Rate
FROM ambulance_response_data_CLEAN
GROUP BY Call_Type
ORDER BY Avg_Delta DESC;