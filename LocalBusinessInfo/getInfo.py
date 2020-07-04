# Illustrates an API call to Datafiniti's Product Database for hotels.
import requests
import urllib.parse
import urllib.request
import json
import time

# Set your API parameters here.
API_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjZm8ya3h6M29nM3FxY3AyaXdtYzNoeTZ3aDI5MzA5cSIsImlzcyI6ImRhdGFmaW5pdGkuY28ifQ.f5S9MwfwuRZWuq_XNyyTJlnEDwLKhzglz7siB61sXGpcLUj8CEBhUALECvJIM-m6eAGWpxe0DFqpKmPYrUpGYfmTYo6Myd4BW9BcAyctAp975OrAZvXIuR7ea-WdaIN5TY4pRzcU-Uy9TspdtA3KgdIreytpACTa0CBTlKsvN6wkeNLEUANDRLbX5T2WdizIBov3FiI9zk0E2ZKl_fjkfCx_in371rUG14a19NrEcYlmFDDzO0A2RLhxXG1M0rIbBLFq6qUuPbHYAlC65W9mAuPsjCoghR8m-lpZJ8lxEc2TtkxIxKKqpgxdDLpp35hQgprMWOBQuZ1BBUnIgWi4vjBDPEWTzKISYxeqCZ7hnGhPM3vFpdTuIVamOh2bO615w7ZqsVY4J4j53jRRl07OLs60jkYyyTyuWVrHgcYuX35MUiS6CURErxDp3-_XWlc9YjnxJ3SqhaL7Pvyge64KM6imoEZDptUQE_wqbZk9I1RQg7mtbZPft_JhY9D3bFB-e6qwUVfJmzClh28gvwgAdvvMeF6g1DYl8dKB7G5Wv7mV3K8_0KBCgcO5R_BrkHGG6FtlBzsT5AfV2FAto45RL8FGjbolKgIHF97aSe-FJgBAa-CbItOOPFjOIHQlgwdGjGjixC3QNEg5zo35qDA-xbTnI7oAWAbiZ-4MTnTmzik'
view_name = 'business_all_nested'
format = 'csv'
query = 'city:(chicago) AND province:(IL) AND postalCode:(60603 OR 60604 OR 60621 OR 60623 OR 60624 OR 60643) AND country:(US)'
num_records = 24995
download = True

request_headers = {
    'Authorization': 'Bearer ' + API_token,
    'Content-Type': 'application/json',
}
request_data = {
    'query': query,
    'view': view_name,
    'format': format,
    'num_records': num_records,
    'download': download
}

# Make the API call.
r = requests.post('https://api.datafiniti.co/v4/businesses/search', json=request_data, headers=request_headers)

# Do something with the response.
if r.status_code == 200:
    request_response = r.json()
    print(request_response)

    # Keep checking the request status until the download has completed
    download_id = request_response['id']
    download_status = request_response['status']

    download_response = {}

    while download_status != 'completed':
        time.sleep(5)
        download_r = requests.get('https://api.datafiniti.co/v4/downloads/' + str(download_id), headers=request_headers)
        download_response = download_r.json()
        download_status = download_response['status']
        print('Records downloaded: ' + str(download_response['num_downloaded']))

    # Once the download has completed, get the list of links to the result files and download each file
    if download_status == 'completed':
        result_list = download_response['results']
        i = 1
        for result in result_list:
            filename = "LocalBusinessInfo" + '.' + format
            urllib.request.urlretrieve(result, filename)
            print('File: ' + str(i) + ' out of ' + str(len(result_list)) + ' saved: ' + filename)
            i += 1

else:
    print('Request failed')
    print(r)
