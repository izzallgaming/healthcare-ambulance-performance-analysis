# Healthcare Ambulance Response Performance Analysis

**Understanding the Impact of EMT Pay and Call Volume on Response Times**

> **Note on data:** This dataset is synthetic. It was generated to reflect real-world patterns I observed over 5 years as an EMT working with Mount Sinai, NYC Health + Hospitals, Rikers transports, nursing homes, and multiple ambulance companies — it is not actual operational data from any of these organizations.

## Project Overview

This project examines simulated ambulance performance data to identify what actually drives better (or worse) response times in NYC hospital systems. Having worked as an EMT across several ambulance companies and hospital systems, I wanted to use data to test what I saw on the ground: that pay rate has a major effect on how fast crews actually move.

## Business Problem

Ambulance delays contribute to ER wait times and overall hospital inefficiency. Hospitals need clear evidence on what levers actually improve performance when awarding contracts.

## Repo Structure

```
HealthCare Problem/
├── README.md
├── CodesHCA1/
│   ├── clean_ambulance_data.py
│   └── SQL/
│       └── ambulance_analysis_queries.sql
├── DataHCA1/
│   ├── ambulance_response_data_messy.csv
│   ├── ambulance_response_data_CLEAN.csv
│   └── SQL_OUTPUT_LowDelt_And_LowVol.csv
└── VisualsHCA1/
    ├── % of Calls On Time Based on Pay Tier.jpg
    ├── Companies Avg Daily Call Vol.jpg
    ├── Dash for Ambulance Response Times.jpg
    ├── Late Count Based on Pay.jpg
    └── Response Time vs Pay Tier.jpg
```

## Data & Cleaning Process

**Python (`CodesHCA1/clean_ambulance_data.py`)**
- Loaded messy raw CSV using pandas
- Standardized messy Company names (MountSinai, MSHS, Mount Sinai EMS, etc. → "Mount Sinai")
- Standardized Call Types and fixed mixed date formats
- Fixed impossible negative response deltas (flagged and clipped)
- Created key columns: Pay_Tier, Is_Late, Had_Negative_Delta
- Removed incomplete rows

**Excel Manual Cleanup**
- Imputed missing Actual_Response_Minutes with column average (~19)
- Removed rows with "Unknown" Shift_Type that had too many missing values
- Final review and formatting

Final clean dataset: ~292 usable records.

## SQL Analysis

All exploratory queries live in a single consolidated file: [`CodesHCA1/SQL/ambulance_analysis_queries.sql`](CodesHCA1/SQL/ambulance_analysis_queries.sql). Analysis was run in DB Browser for SQLite.

**A couple of SQLite-specific quirks worth flagging for anyone reproducing this:**
- On import, SQLite lowercased and truncated some column names (e.g. `Response_Delta_Minutes` became `response_delta_m`). Run `PRAGMA table_info(table_name);` to see the exact column names as stored before adapting the queries.
- `Is_Late` and `Had_Negative_Delta` are stored as the *text* strings `'TRUE'`/`'FALSE'`, not native booleans. Comparisons need to be written as `column = 'TRUE'` — comparing against the boolean literal `TRUE` silently fails and undercounts.

Queries cover:
- Overall average response delta and daily call volume
- High-delta / high-volume call segments
- Late rate by pay tier
- Company-level scorecards (avg delta, late rate), including a window-function ranking
- Pay rate vs. performance rating
- Shift (Day/Night) and Call Type comparisons

## Key Visuals (Power BI)

![% of Calls On Time by Pay Tier](VisualsHCA1/%25%20of%20Calls%20On%20Time%20Based%20on%20Pay%20Tier.jpg)

![Average Daily Call Volume per Company](VisualsHCA1/Companies%20Avg%20Daily%20Call%20Vol.jpg)

![Full Dashboard](VisualsHCA1/Dash%20for%20Ambulance%20Response%20Times.jpg)

![Late Count Based on Pay](VisualsHCA1/Late%20Count%20Based%20on%20Pay.jpg)

![Average Response Time vs Pay Tier](VisualsHCA1/Response%20Time%20vs%20Pay%20Tier.jpg)

## Core Insights

- Higher EMT pay rates ($28–$35/hr) are strongly associated with much better response performance and significantly fewer late calls.
- Low pay brackets show consistently worse deltas and higher late counts.
- Daily call volume has a noticeable but weaker effect. Hospitals can still manage this by more evenly distributing calls across companies to avoid overloading any single provider.

Bottom line: while call volume balancing is something hospitals can control with relatively little resistance, improving EMT compensation appears to be the most impactful lever for reducing response delays.

## Technologies Used

- Python (pandas) – Data cleaning
- SQL (SQLite) – Exploratory analysis
- Power BI – Visualizations & Dashboard
- Excel – Manual validation
