import pandas as pd
import folium

# Read the csv file into a DataFrame
df = pd.read_csv('merged_tempe_schools_data.csv')

# remove rows without address
df = df.dropna(subset=['Business Address'])

# Create a map centered on Malibu
malibu_map = folium.Map(location=[33.4093, -111.9349], zoom_start=14)

# Iterate through each record and add a marker for the business location
for i, row in df.iterrows():
    folium.Marker([row['lat'], row['lon']], 
                  popup=f"School: {row['schoolName']}<br>Business: {row['Business Name']}<br>Address: {row['Business Address']}").add_to(malibu_map)

# Display the map
malibu_map.save("tempe_schools_map.html")

