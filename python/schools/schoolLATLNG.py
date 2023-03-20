import pandas as pd

# Read the csv files into DataFrames
family_activities_df = pd.read_csv('atx-schools_and_nearby_family_activities.csv')
schools_df = pd.read_csv('austin-schools.csv')

# Left join the two DataFrames on the "School Name" column
merged_df = pd.merge(family_activities_df, schools_df, on='schoolName', how='left')

# Write the merged DataFrame to a new csv file
merged_df.to_csv('merged_atx_schools_data.csv', index=False)
