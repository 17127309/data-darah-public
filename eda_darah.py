import pandas as pd

# Read the CSV files into DataFrames
facility_df = pd.read_csv('donations_facility.csv')
state_df = pd.read_csv('donations_state.csv')

# Display the first few rows of each DataFrame
print("Facility Donations:")
print(facility_df.head())

print("\nState Donations:")
print(state_df.head())
