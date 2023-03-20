import csv
import json
import geocoder
import requests

try:
    from urllib.request import Request, urlopen  # Python 3
except ImportError:
    from urllib2 import Request, urlopen  # Python 2

# set the API endpoint URL
url = 'https://gs-api.greatschools.org/nearby-schools?lat=30.238008573491275&lon=-97.74995907982841&limit=200&distance=100&level_codes=e'

# create the API request
req = Request(url)

# set the API key
req.add_header('X-API-Key', 'bEcQLIy6927yXQJUB4MZ72QF2ySxXijEaZlukTkB')  

# send the request and read the response
try:
    content = urlopen(req).read()
except Exception as e:
    print("Error: Failed to fetch data from API")
    print(e)
else:
    # parse the json
    data = json.loads(content)
    schools = data['schools']
    
    # create a csv file
    with open('schools.csv', 'w') as csv_file:
        # write the header row
        writer = csv.writer(csv_file)
        writer.writerow(['universal-id', 'nces-id', 'state-id', 'name', 'school-summary', 'type', 'level', 'street', 'city', 'state', 'zip', 'fipscounty', 'phone', 'fax', 'county', 'lat', 'lon', 'district-name', 'district-id', 'web-site', 'overview-url', 'rating', 'year', 'distance'])

        # loop through the schools
        for school in schools:
            # write the school data to the csv file
            writer.writerow([school['universal-id'], school['nces-id'], school['state-id'], school['name'], school['school-summary'], school['type'], school['level'], school['street'], school['city'], school['state'], school['zip'], school['fipscounty'], school['phone'], school['fax'], school['county'], school['lat'], school['lon'], school['district-name'], school['district-id'], school['web-site'], school['overview-url'], school['rating'], school['year'], school['distance']])

    # open schools.csv file again to add lat, lon
    with open('schools.csv', 'r') as f:
        reader = csv.reader(f)
        schools = list(reader)

  # add lat, lon
    for school in schools[1:]:
        address = school[7] + ', ' + school[8] + ', ' + school[9] + ' ' + school[10]
        g = geocoder.google(address)
        if g.latlng:
            school.append(g.latlng[0])
            school.append(g.latlng[1])

# write the schools with lat, lon to a new csv file
    with open('schools_with_lat_lon.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(schools)

# Yelp API credentials
api_key = "7foPR1cQp_82rYiBREpTS3l_8gAmJYoLWwGnwjyk24X4-q5IsJ1erCTaHl69ZKAj-Gh-1oUz0osd7a0w7BEConY74k1E_P6pHwGMUk1jJK6oH4GkFjLW4xPmyQHDY3Yx"

# Open schools_with_lat_lon.csv file
with open('schools_with_lat_lon.csv', 'r') as f:
    reader = csv.reader(f)
    schools = list(reader)

# Create a new csv file to store the Yelp results
with open('yelp_results.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['school_name', 'city', 'business_name', 'business_address', 'business_rating', 'business_review_count'])
    
    # Iterate through each school
    for school in schools[1:]:
        school_name = school[3]
        city = school[8]
        lat = school[-2]
        lon = school[-1]
        location = f"{lat},{lon}"
        radius = 1609 # 1 mile in meters
        category = "kids-and-families-activities"
        
        # Send a GET request to the Yelp API
        url = f"https://api.yelp.com/v3/businesses/search?term=kids-and-families-activities&location={location}&radius={radius}"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'businesses' in data:
            businesses = data['businesses']
            for business in businesses:
                business_name = business['name']
                business_address = business['location']['address1']
                business_rating = business['rating']
                business_review_count = business['review_count']
                writer.writerow([school_name, city, business_name, business_address, business_rating, business_review_count])
        else:
            print(f'No businesses found for {school_name}')
    else:
        print(f'Error {response.status_code}: {response.text}')
