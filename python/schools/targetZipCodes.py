import csv
import json
import requests
import geocoder

# Yelp API credentials
api_key = "7foPR1cQp_82rYiBREpTS3l_8gAmJYoLWwGnwjyk24X4-q5IsJ1erCTaHl69ZKAj-Gh-1oUz0osd7a0w7BEConY74k1E_P6pHwGMUk1jJK6oH4GkFjLW4xPmyQHDY3Yx"
headers = {
    "Authorization": "Bearer " + api_key,
    "accept": "application/json"
}

# GreatSchools API Key
gs_api_key = "bEcQLIy6927yXQJUB4MZ72QF2ySxXijEaZlukTkB"

# Open targetLocations.csv file
with open('targetLocations.csv', 'r') as f:
    reader = csv.reader(f)
    cities = list(reader)

# Create a new CSV file to store the results
with open('schools_and_nearby_family_activities.csv', 'w') as f:
    writer = csv.writer(f)
    # Write the header row
    writer.writerow(['School Name', 'School City', 'Business Name', 'Business Address', 'Business Phone', 'Business Rating', 'Distance from School'])

    # Iterate through the cities
    for city in cities[1:]:
        city_name = city[0]

        # Get the latitude and longitude of the city
        g = geocoder.google(city_name)
        lat = g.latlng[0]
        lon = g.latlng[1]

               # construct the GreatSchools API URL
        gs_url = f"https://gs-api.greatschools.org/nearby-schools?lat={lat}&lon={lon}&limit=200&distance=100&level_codes=e"

        # create the API request
        gs_req = Request(gs_url)

        # set the API key
        gs_req.add_header('X-API-Key', gs_api_key)  

        # send the request and read the response
        try:
            gs_content = urlopen(gs_req).read()
        except Exception as e:
            print("Error: Failed to fetch data from GreatSchools API")
            print(e)
        else:
            # parse the json
            gs_data = json.loads(gs_content)
            gs_schools = gs_data['schools']

            for school in gs_schools:
                # Get the latitude and longitude of the school
                lat = school['lat']
                lon = school['lon']

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

               
