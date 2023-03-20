import pandas as pd
from geopy.geocoders import Nominatim

# Read the csv file into a DataFrame
df = pd.read_csv('merged_tempe_schools_data.csv')

# remove rows without address
df = df.dropna(subset=['Business Address'])

# Create a geolocator object
geolocator = Nominatim(user_agent="geoapiExercises")

# Iterate through each record and update the latitude and longitude columns
for i, row in df.iterrows():
    location = geolocator.geocode(row['Business Address'])
    if location:
        df.at[i, 'Latitude'] = location.latitude
        df.at[i, 'Longitude'] = location.longitude

# Save the updated DataFrame to a new csv file
df.to_csv('cleaned_tempe_schools_data.csv', index=False)
