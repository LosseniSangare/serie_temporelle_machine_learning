# monthly_data_import_w.API v1.1
#   Updates from v1.0:
#   - Fix %M:%S to %H:%M in month_start definition

'''
This script uses the REE's public API to download and save electricity demand for a user specified year and month.
API reference: https://www.ree.es/en/apidatos

A relevant extract of the JSON structure returned by the API is shown below. Note that "peninsular" is the default
and intended area for 'demanda-tiempo-real' API requests.

{
    "data": {
        "type": "Demanda peninsular en tiempo real",
        "id": "dem15",
        "attributes": {
            "title": "Demanda peninsular en tiempo real",
            "last-update": "2024-02-20T04:03:58.000+01:00",
            "description": null
        }
    },
    "included": [
        {
            "type": "Demanda real",
            "id": "1293",
            "groupId": null,
            "attributes": {
                "title": "Demanda real",
                "description": "Demanda real",
                "color": "#ffea00",
                "type": null,
                "magnitude": null,
                "composite": false,
                "last-update": "2024-02-20T04:03:58.000+01:00",
                "values": [
                    {
                        "value": 20015,
                        "percentage": 0.33296180463135483,
                        "datetime": "2024-02-19T03:00:00.000+01:00"
                    },
(...)

Script output when the user selects '2023' as year and '01' as month:
    Year as a 4-digit number : 2023
    Month as a 2-digit number : 02
    Start date for API request : 2023-02-01T00:00
    End date for API request : 2023-02-28T23:59
    Please wait while data is being downloaded...

    API request completed.
    API Response code : 200
    API Response URL : https://apidatos.ree.es/es/datos/demanda/demanda-tiempo-real?start_date=2023-02-01T00%3A00&end_date=2023-02-28T23%3A59&time_trunc=hour
'''

# Import librairies
from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv, requests


# Define the base URL for the targeted data (actual demand in real time)
BASE_URL = 'https://apidatos.ree.es/es/datos/demanda/demanda-tiempo-real?'

# Define a function building an API request based on user defined year and month
def API_request(start, end):

    # Set request parameters
    request_params = {
        "start_date" : start,
        "end_date"   : end,
        "time_trunc" : "hour",
    }
    
    # Set user agent
    user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0')

    # Set request headers
    headers = {
        "User-Agent": user_agent,
        # "Accept": "application/json",
    }

    # Return the API request based on elements above
    return requests.get(url=BASE_URL, params=request_params, headers=headers)


# Get user input for year and month of data to be collected
year = input("Year as a 4-digit number : ")
month = input("Month as a 2-digit number : ")

# Set start date and time for specified year and month
start_date  = f"{year}-{month}-01T00:00"

# Compute and set end date and time (23h59 on last day of month) for 'start_date' above
month_start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
month_end = month_start.replace(day=1) + relativedelta(months=1) - relativedelta(days=1)
end_date = month_end.strftime("%Y-%m-%d")+"T23:59"

# Display computed start and end date and time to be used by the API request
print("Start date for API request :", start_date)
print("End date for API request :", end_date)

# Send GET request and collect returned data into 'response'
print("Please wait while data is being downloaded...\n")
response = API_request(start_date, end_date)

# Display response code and url returned by the API
print("API request completed.")
print("API Response code :", response.status_code)
print("API Response URL :", response.url)

# Extract values of 'Demanda real' (actual demand) from JSON structure returned in API response
demanda_real_values = response.json()["included"][0]["attributes"]["values"]

# Define full path to save data in dedicated CSV file
csv_file_dir = "../Data/csv_output/"
csv_file_path = f"REE_data_{year}-{month}.csv"

# Open CSV file for writing data
with open(csv_file_dir+csv_file_path, "w", newline="") as csv_file:
    
    # Instantiate CSV writer with non-default delimiter
    csv_writer = csv.writer(csv_file, delimiter=";")
    # Write header row
    csv_writer.writerow(["datetime", "demand"])
    # Get and write datetime and demand values only (other fields discarded)
    for values in demanda_real_values:
        datetime = values["datetime"]
        demand = values["value"]
        csv_writer.writerow([datetime, demand])