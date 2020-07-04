# Python program to convert
# JSON file to CSV
import json
import csv
import requests

url = "https://api.crimeometer.com/v1/incidents/raw-data?lat=41.843975&lon=-87.754021&distance=17mi&datetime_ini=2010-06-15T00:00:00.000Z&datetime_end=2020-06-16T00:00:00.000Z&page_size=900"

payload = {}
headers = {
    'x-api-key': 'U2fXoSQ6AV9CZcgFBA0y48wWEBkOujMfsl4DZJMf'
}

response = requests.request("GET", url, headers=headers, data=payload)

assign = response.json()
# print(response.text.encode('utf8'))

# Serializing json
json_object = json.dumps(assign, indent=4)

# Writing to sample.json
with open("CrimeData.json", "w") as outfile:
    outfile.write(json_object)

# Opening JSON file and loading the data
# into the variable data
# Python program to convert
# JSON file to CSV
with open("CrimeData.json") as json_file:
    data = json.load(json_file)

crime_data = data['incidents']

# now we will open a file for writing
data_file = open('CrimeData.csv', 'w')

# create the csv writer object
csv_writer = csv.writer(data_file)

# Counter variable used for writing
# headers to the CSV file
count = 0

for temp in crime_data:
    if count == 0:
        # Writing headers of CSV file
        header = temp.keys()
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow(temp.values())

data_file.close()
