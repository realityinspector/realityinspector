import requests
import csv
import geocoder 

# replace YOUR_API_KEY with your actual API key
api_key = "aec3bc0b5f101ac4c9dfc1134f0b20df"

# make a GET request to the Crunchbase API
response = requests.get(f"https://api.crunchbase.com/api/v4/searches/organizations?query=education+edtech+schools&field=short_description&user_key={api_key}")

# parse the JSON response
data = response.json()["data"]["items"]

# write the data to a CSV file
with open("edtech_organizations.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Type", "Location", "Short Description"])
    for item in data:
        if "education" in item["short_description"] or "edtech" in item["short_description"] or "schools" in item["short_description"]:
            writer.writerow([item["name"], item["entity_def_id"], item["location_identifiers"], item["short_description"]])
