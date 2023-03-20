import csv
import json
import requests

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
