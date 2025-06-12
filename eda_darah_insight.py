"""
Exploratory Data Analysis (EDA) for Blood Donation Datasets
- donations_facility.csv
- donations_state.csv

This script provides a detailed EDA, including:
- Data loading and inspection
- Data cleaning
- Descriptive statistics
- Time series and trend analysis
- Analysis by hospital/facility and by state
- Blood type and donation type analysis
- Social group and donor type analysis
- Visualizations

Author: Azrul Syaffiq
Date: 12-06-2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set plot style
sns.set(style="whitegrid")

# 1. Load Data
facility_df = pd.read_csv('donations_facility.csv')
state_df = pd.read_csv('donations_state.csv')

# Exclude rows where state is 'Malaysia' (case-insensitive) in state_df
if 'state' in state_df.columns:
    state_df = state_df[~state_df['state'].str.lower().eq('malaysia')].copy()

# 2. Initial Inspection
print("\n--- Facility Data Overview ---")
print(facility_df.info())
print(facility_df.head())

print("\n--- State Data Overview ---")
print(state_df.info())
print(state_df.head())

# 3. Data Cleaning
# Convert 'date' to datetime
facility_df['date'] = pd.to_datetime(facility_df['date'], errors='coerce')
state_df['date'] = pd.to_datetime(state_df['date'], errors='coerce')

# Check for missing values
print("\nFacility missing values:\n", facility_df.isnull().sum())
print("\nState missing values:\n", state_df.isnull().sum())

# Fill missing hospital/state names with 'Unknown'
facility_df['hospital'] = facility_df['hospital'].fillna('Unknown')
if 'state' in state_df.columns:
    state_df['state'] = state_df['state'].fillna('Unknown')

# 4. Verification: Compare Daily Totals by Date Between Facility and State Files
# -----------------------------------------------------------------------------
# EXPLANATION:
# The 'daily' column in both files represents the total number of donations for each date.
# In the facility file, this is the sum across all hospitals for a given date.
# In the state file, this is the reported total for the entire country (or state) for that date.
# To verify data consistency, we sum the 'daily' values by date in the facility file and compare
# them to the corresponding 'daily' value in the state file. Any difference may indicate missing
# data, reporting errors, or aggregation issues. We print summary statistics, count mismatches,
# and show a few examples. A plot visualizes the difference over time.

# Sum daily donations by date for both datasets
facility_daily_sum = facility_df.groupby('date')['daily'].sum().sort_index()
state_daily_sum = state_df.groupby('date')['daily'].sum().sort_index()

# Merge for comparison
verification_df = pd.DataFrame({
    'facility_total': facility_daily_sum,
    'state_total': state_daily_sum
})
verification_df['difference'] = verification_df['facility_total'] - verification_df['state_total']

# Show summary statistics and mismatches
print("\n--- Verification of Daily Totals (Facility vs State) ---")
print("This section checks if the sum of daily donations from all facilities matches the reported total in the state file for each date. Ideally, the difference should be zero for all dates. Any nonzero difference may indicate data inconsistencies or missing records.")
print(verification_df.describe())

# Show dates where the difference is not zero
mismatches = verification_df[verification_df['difference'] != 0]
print(f"\nNumber of mismatched days: {len(mismatches)}")
if not mismatches.empty:
    print("Sample of mismatched days (first 10):")
    print(mismatches.head(10))
else:
    print("All daily totals match between facility and state files.")

# Visualize the difference over time
plt.figure(figsize=(12,5))
plt.plot(verification_df.index, verification_df['difference'], label='Facility - State Daily Total')
plt.axhline(0, color='red', linestyle='--', linewidth=1)
plt.title('Difference in Daily Donations: Facility vs State')
plt.xlabel('Date')
plt.ylabel('Difference in Daily Total')
plt.legend()
plt.tight_layout()
plt.show()

# 5. Descriptive Statistics
print("\n--- Facility Data Description ---")
print(facility_df.describe())

print("\n--- State Data Description ---")
print(state_df.describe())

# 6. Time Series Analysis: Total Donations Over Time
plt.figure(figsize=(12,5))
facility_daily = facility_df.groupby('date')['daily'].sum()
state_daily = state_df.groupby('date')['daily'].sum()
plt.plot(facility_daily.index, facility_daily.values, label='Facility Total')
plt.plot(state_daily.index, state_daily.values, label='State Total')
plt.title('Total Daily Donations Over Time')
plt.xlabel('Date')
plt.ylabel('Donations')
plt.legend()
plt.tight_layout()
plt.show()

# 7. Analysis by Hospital/Facility
facility_totals = facility_df.groupby('hospital')['daily'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,6))
facility_totals.head(15).plot(kind='bar')
plt.title('Top 15 Hospitals by Total Donations')
plt.ylabel('Total Donations')
plt.xlabel('Hospital')
plt.tight_layout()
plt.show()

# 8. Yearly Time Series Analysis for Facility and State
yearly_facility = facility_df.groupby(facility_df['date'].dt.year)['daily'].sum()
yearly_state = state_df.groupby(state_df['date'].dt.year)['daily'].sum()

plt.figure(figsize=(10,6))
yearly_facility.plot(label='Facility', marker='o')
yearly_state.plot(label='State', marker='o')
plt.title('Yearly Total Donations: Facility vs State')
plt.xlabel('Year')
plt.ylabel('Total Donations')
plt.legend()
plt.tight_layout()
plt.show()

# Yearly donation trends by individual facility
facility_yearly_pivot = facility_df.pivot_table(index=facility_df['date'].dt.year, columns='hospital', values='daily', aggfunc='sum')
plt.figure(figsize=(14,8))
for col in facility_yearly_pivot.columns:
    plt.plot(facility_yearly_pivot.index, facility_yearly_pivot[col], marker='o', label=col, alpha=0.5)
plt.title('Yearly Donation Trends by Facility')
plt.xlabel('Year')
plt.ylabel('Total Donations')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', ncol=2, frameon=False)
plt.tight_layout()
plt.show()

# 9. Blood Type Distribution
blood_types = ['blood_a', 'blood_b', 'blood_o', 'blood_ab']
plt.figure(figsize=(8,5))
facility_blood = facility_df[blood_types].sum()
state_blood = state_df[blood_types].sum()
width = 0.35
x = np.arange(len(blood_types))
plt.bar(x - width/2, facility_blood, width, label='Facility')
plt.bar(x + width/2, state_blood, width, label='State')
plt.xticks(x, ['A', 'B', 'O', 'AB'])
plt.ylabel('Total Donations')
plt.title('Blood Type Distribution')
plt.legend()
plt.tight_layout()
plt.show()

# 10. Donation Type Analysis
# Whole blood, apheresis platelet, apheresis plasma, other
donation_types = ['type_wholeblood', 'type_apheresis_platelet', 'type_apheresis_plasma', 'type_other']
plt.figure(figsize=(8,5))
facility_types = facility_df[donation_types].sum()
state_types = state_df[donation_types].sum()
plt.bar(x - width/2, facility_types, width, label='Facility')
plt.bar(x + width/2, state_types, width, label='State')
plt.xticks(x, ['Whole Blood', 'Apheresis Platelet', 'Apheresis Plasma', 'Other'])
plt.ylabel('Total Donations')
plt.title('Donation Type Distribution')
plt.legend()
plt.tight_layout()
plt.show()

# 11. Social Group Analysis
social_groups = ['social_civilian', 'social_student', 'social_policearmy']
plt.figure(figsize=(8,5))
facility_social = facility_df[social_groups].sum()
state_social = state_df[social_groups].sum()
plt.bar(x - width/2, facility_social, width, label='Facility')
plt.bar(x + width/2, state_social, width, label='State')
plt.xticks(x, ['Civilian', 'Student', 'Police/Army'])
plt.ylabel('Total Donations')
plt.title('Social Group Distribution')
plt.legend()
plt.tight_layout()
plt.show()

# 12. Donor Type Analysis (New, Regular, Irregular)
donor_types = ['donations_new', 'donations_regular', 'donations_irregular']
plt.figure(figsize=(8,5))
facility_donors = facility_df[donor_types].sum()
state_donors = state_df[donor_types].sum()
plt.bar(x - width/2, facility_donors, width, label='Facility')
plt.bar(x + width/2, state_donors, width, label='State')
plt.xticks(x, ['New', 'Regular', 'Irregular'])
plt.ylabel('Total Donations')
plt.title('Donor Type Distribution')
plt.legend()
plt.tight_layout()
plt.show()

# 13. Correlation Analysis
plt.figure(figsize=(10,8))
sns.heatmap(facility_df.corr(numeric_only=True), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Facility Data Correlation Matrix')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,8))
sns.heatmap(state_df.corr(numeric_only=True), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('State Data Correlation Matrix')
plt.tight_layout()
plt.show()

# 14. Seasonality/Monthly Trends
facility_monthly = facility_df.groupby(facility_df['date'].dt.to_period('M'))['daily'].sum()
state_monthly = state_df.groupby(state_df['date'].dt.to_period('M'))['daily'].sum()
plt.figure(figsize=(12,5))
facility_monthly.plot(label='Facility')
state_monthly.plot(label='State')
plt.title('Monthly Donations Trend')
plt.xlabel('Month')
plt.ylabel('Total Donations')
plt.legend()
plt.tight_layout()
plt.show()

print("\nEDA complete. See plots and outputs above for insights.")
