import csv
import requests

# Set the URL for the Guardian API
guardian_url = "https://content.guardianapis.com/search"

# Set the parameters for the API request
guardian_params = {
    "api-key": "498629fb-6420-460f-bf99-a925db65ff06",
    "q": "unschool, virtual schools"
}

# Make the API request
try:
    guardian_response = requests.get(guardian_url, params=guardian_params)
    guardian_response.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Failed to retrieve data from Guardian API:", e)
    guardian_data = None

# Check if the API request failed
if guardian_response.status_code != 200:
    raise Exception("Failed to retrieve data from Guardian API")

# Parse the response as JSON
guardian_data = guardian_response.json()

# Open a CSV file for writing
with open("results.csv", "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Headline", "Publisher", "URL"])

    # Write the data rows from the Guardian API
    for article in guardian_data["response"]["results"]:
        writer.writerow([
            article["webTitle"],
            "The Guardian",
            article["webUrl"]
        ])
