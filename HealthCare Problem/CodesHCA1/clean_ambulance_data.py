#pandas and numpy to short cuts pd & np
import pandas as pd
import numpy as np

# Load the data in the program df short for dataframe
# Used r' ' to make sure python takes the quote literally
# Keeping it from confusing '\'
df = pd.read_csv(r'C:\Users\INC IzzAll\Desktop\HealthCare Problem\ambulance_response_data_messy.csv')

# Make sure it was loaded properly
"""
# ROWS, COLUMNS
print("Original shape:", df.shape)
# New line + prompt for user ease
print("\n--- First 5 rows ---")
# Default to first 5 rows can be changed by placing number in pareth
print(df.head())
"""
# Standardize comp names
#  Standardize Company names
# First we make a dictionary
# American Medical Response, Amr,
company_mapping = {
    '  Mount Sinai EMS' : 'Mount Sinai',
    'MSHS' : 'Mount Sinai',
    'Mount Sinai EMS' : 'Mount Sinai',
    'Mount Sinai': 'Mount Sinai',
    'MountSinai': 'Mount Sinai',
    'Mt Sinai': 'Mount Sinai',
    '  Mount Sinai  ': 'Mount Sinai',
    '  Ambulnz LLC' : 'Ambulnz',
    'Ambulance Inc' : 'Ambulnz',
    'Ambulnz LLC' : 'Ambulnz',
    'Ambulnz': 'Ambulnz',
    'AMR': 'AMR',
    'American Medical Response' : 'AMR',
    'Amr' : 'AMR',
    'Hunter Ambulance': 'Hunter Ambulance',
    'Senior Care Ambulance': 'Senior Care Ambulance',
    'Citywide Ambulance': 'Citywide Ambulance'
}
# Now we make a new column 'Company_Clean' and set it equal to 'Company' with changes
# str.strip removes whites spaces map remaps column using the dictionary we just made
# fillna(Fill Not A Number) is to make sure anything missed remains unchanged as a precaution (fill missing values)
df['Company_Clean'] = df['Company'].str.strip().map(company_mapping).fillna(df['Company'])

# Standardize Call Types Column
call_type_mapping = {
    'Emergency': 'Emergency',
    '911': 'Emergency',
    'emerg': 'Emergency',
    'Non-Emergency': 'Non-Emergency',
    'IFT': 'Non-Emergency',
    'Interfacility Transfer': 'Non-Emergency',
    'non-emerg': 'Non-Emergency'
}
df['Call_Type_Clean'] = df['Call_Type'].str.strip().map(call_type_mapping).fillna(df['Call_Type'])

# Check if these work (Remove after code)
# Found extras to be added to our dictionarie(s)
#  Ambulnz LLC,   Mount Sinai EMS, Ambulance Inc, Ambulnz LLC, American Medical Response, Amr, MSHS, Mount Sinai EMS
"""
print("\n--- Call Type Standardization ---")
print("\nCleaned:")
print(df['Call_Type_Clean'].value_counts().sort_index())

print("\n--- Company Standardization ---")
print("\nCleaned:")
print(df['Company_Clean'].value_counts().sort_index())
"""
# Output outliers found and dictionary corrected/updated:
"""
--- Company Standardization ---

Cleaned:
Company_Clean
  Ambulnz LLC                 1
  Mount Sinai EMS             1
AMR                          45
Ambulance Inc                 1
Ambulnz                      49
Ambulnz LLC                   1
American Medical Response     2
Amr                           3
Citywide Ambulance           56
Hunter Ambulance             46
MSHS                          2
Mount Sinai                  41
Mount Sinai EMS               2
Senior Care Ambulance        42
"""


# Date Cleaning

# Improved date parsing for mixed formats so pandas doesn't fail correction
df['Date_Clean'] = pd.to_datetime(df['Date'], 
                                  format='mixed', 
                                  errors='coerce')

# Optional: Try to fix remaining dates manually if needed
df['Date_Clean'] = pd.to_datetime(df['Date_Clean'], errors='coerce')

# Check if date cleaning worked
"""
print("\n--- Date & Delta Cleaning Check ---")
print("Date examples:")
print(df[['Date', 'Date_Clean']].head(10))
print("\nNegative deltas found and fixed:", df['Response_Delta_Flag'].sum())
"""

# 5. Fix negative Response Delta (impossible values)
df['Response_Delta_Flag'] = df['Response_Delta_Minutes'] < 0
df['Response_Delta_Minutes_Clean'] = df['Response_Delta_Minutes'].clip(lower=0)

# Check if cleaning worked
"""
print("\n--- Negative Delta Fix ---")
print("Number of negative deltas fixed:", df['Response_Delta_Flag'].sum())
print("Example of cleaned deltas:")
print(df[['Response_Delta_Minutes', 'Response_Delta_Minutes_Clean']].head(10))
"""


# Standardize Shift and Performance Rating

# Standardize Shift_Type
shift_mapping = {
    'Day': 'Day',
    'day': 'Day',
    'DAY': 'Day',
    'Night': 'Night',
    'night': 'Night',
    'NIGHT': 'Night'
}
df['Shift_Type_Clean'] = df['Shift_Type'].str.strip().map(shift_mapping).fillna('Unknown')

# Standardize Performance Rating
perf_mapping = {
    'Excellent': 'Excellent',
    'excellent': 'Excellent',
    'Good': 'Good',
    'good': 'Good',
    'Fair': 'Fair',
    'fair': 'Fair',
    'Below Average': 'Below Average',
    'Poor': 'Poor',
    'poor': 'Poor'
}
df['Performance_Rating_Clean'] = df['Performance_Rating'].str.strip().map(perf_mapping).fillna('Unknown')

# Dictionary Completion Check
"""
print("\n--- Shift & Performance Cleaning ---")
print("Shift Types (Clean):")
print(df['Shift_Type_Clean'].value_counts())
print("\nPerformance Ratings (Clean):")
print(df['Performance_Rating_Clean'].value_counts())
"""

# Create Useful Derived Columns
# Pay Tier based on your real pay insights
df['Pay_Tier'] = pd.cut(df['Pay_Rate_Hourly'], 
                        bins=[0, 22, 27, 100], 
                        labels=['Low ($19-21)', 'Medium ($22-27)', 'High ($28-35)'])

# Flag late responses (>5 minutes past ETA)
df['Is_Late'] = df['Response_Delta_Minutes_Clean'] > 5

# Fill any remaining missing Daily_Call_Volume with median
df['Daily_Call_Volume_Clean'] = df['Daily_Call_Volume'].fillna(df['Daily_Call_Volume'].median())

# New Column + Cleaning Check
"""
print("\n--- Derived Columns Check ---")
print("Pay Tiers:")
print(df['Pay_Tier'].value_counts())
print("\nLate Responses:", df['Is_Late'].sum())
"""

"""
Section 10: Handle Incomplete Rows
"""

# Drop rows that are missing too many key fields (unusable for analysis)
important_cols = ['Company_Clean', 'Pay_Rate_Hourly', 'ETA_Minutes', 
                  'Actual_Response_Minutes', 'Response_Delta_Minutes_Clean']

# Keep only rows that have values in most important columns
clean_df = df.dropna(subset=important_cols, thresh=4).copy()   # at least 4 out of 5 key fields

print(f"\nDropped {len(df) - len(clean_df)} incomplete rows")
print(f"Final usable rows: {len(clean_df)}")

# Save Cleaned Data
# Select only the columns we want for analysis
clean_df = df[['Call_ID', 'Date_Clean', 'Company_Clean', 'Call_Type_Clean', 
               'ETA_Minutes', 'Actual_Response_Minutes', 'Response_Delta_Minutes_Clean',
               'On_Scene_Time_Minutes', 'Transport_Time_Minutes', 'Pay_Rate_Hourly', 
               'Pay_Tier', 'Shift_Type_Clean', 'Daily_Call_Volume_Clean', 
               'Performance_Rating_Clean', 'Is_Late', 'Response_Delta_Flag']].copy()

# Rename columns to look clean
clean_df.columns = ['Call_ID', 'Date', 'Company', 'Call_Type', 
                    'ETA_Minutes', 'Actual_Response_Minutes', 'Response_Delta_Minutes',
                    'On_Scene_Time_Minutes', 'Transport_Time_Minutes', 'Pay_Rate_Hourly',
                    'Pay_Tier', 'Shift_Type', 'Daily_Call_Volume', 
                    'Performance_Rating', 'Is_Late', 'Had_Negative_Delta']

# Save the clean file
clean_df.to_csv(r'C:\Users\INC IzzAll\Desktop\HealthCare Problem\ambulance_response_data_CLEAN.csv', index=False)

print("\n=== Cleaning Complete! ===")
print("Clean dataset saved as: ambulance_response_data_CLEAN.csv")
print("Final shape:", clean_df.shape)