import csv
import json
import requests
import pandas as pd
import folium
import geocoder

# Yelp API credentials
api_key = "7foPR1cQp_82rYiBREpTS3l_8gAmJYoLWwGnwjyk24X4-q5IsJ1erCTaHl69ZKAj-Gh-1oUz0osd7a0w7BEConY74k1E_P6pHwGMUk1jJK6oH4GkFjLW4xPmyQHDY3Yx"
headers = {
    "Authorization": "Bearer " + api_key,
    "accept": "application/json"
}

# Read the schools.csv file
with open('malibu-schools.csv', 'r') as f:
    reader = csv.reader(f)
    schools = list(reader)

# Create a new CSV file to store the results
with open('schools_and_nearby_family_activities.csv', 'w') as f:
    writer = csv.writer(f)
    # Write the header row
    writer.writerow(['School Name', 'School City', 'Business Name', 'Business Address', 'Business Phone', 'Business Rating', 'Distance from School'])

    # Iterate through the schools
    for school in schools[1:]:
        # Get the latitude and longitude of the school
        lat = school[15]
        lon = school[16]

        # Construct the Yelp API URL
        url = f"https://api.yelp.com/v3/businesses/search?term=family-activities&latitude={lat}&longitude={lon}&radius=1609"

        # Send the GET request to the Yelp API
        response = requests.get(url, headers=headers)

        # Parse the JSON response
        data = json.loads(response.text)

        # Get the businesses from the response
        businesses = data["businesses"]

        # Iterate through the businesses
        for business in businesses:
            # Get the business name, address, phone, rating, and distance from school
            name = business["name"]
            address = business["location"]["address1"]
            phone = business["phone"]
            rating = business["rating"]
            distance = business["distance"]

            # Write the results to the new CSV file
            writer.writerow([school[3], school[8], name, address, phone, rating, distance])

            # Read the csv files into DataFrames
            family_activities_df = pd.read_csv('schools_and_nearby_family_activities.csv')
            schools_df = pd.read_csv('malibu-schools.csv')

            # Left join the two DataFrames on the "School Name" column
            merged_df = pd.merge(family_activities_df, schools_df, on='School Name', how='left')

            # Get the latitude and longitude of the school from the address
            merged_df["lat"] = merged_df["School Address"].apply(lambda x: geocoder.arcgis(x).latlng[0])
            merged_df["lon"] = merged_df["School Address"].apply(lambda x: geocoder.arcgis(x).latlng[1])

            # Write the merged DataFrame to a new csv file
            merged_df.to_csv('merged_malibu_schools_data.csv', index=False)

            # Create a map centered on Malibu
            malibu_map = folium.Map(location=[34.03, -118.69], zoom_start=12)
                
            # Iterate through each record and add a marker for the school location
            for i, row in df.iterrows():
                # Use geocoder to get the latitude and longitude of the address
                g = geocoder.osm(row['Business Address'])
                lat, lon = g.latlng

                # Add the marker to the map
                folium.Marker([lat, lon], 
                              popup=f"School: {row['schoolName']}<br>Business: {row['Business Name']}<br>Address: {row['Business Address']}").add_to(malibu_map)

            # Save the map as an HTML file
            malibu_map.save("tempe_schools_map.html")

