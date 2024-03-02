# monthly_data_import_w.API_batch v1.0

'''
This script collects REE data starting from a user specified year and month until the last day of last month.

REE's public API used: https://www.ree.es/en/apidatos

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
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import csv, time
from utils import API_request


# Define the URL for the targeted data (electricity demand in real time)
URL = 'https://apidatos.ree.es/es/datos/demanda/demanda-tiempo-real?'


# Get user input for year and month of data to be collected
year = input("Year as a 4-digit number : ")
month = input("Month as a 2-digit number : ")

# Set start date and time for specified year and month
start_date  = f"{year}-{month}-01T00:00"
month_start = dt.strptime(start_date, "%Y-%m-%dT%H:%M")

this_month = dt.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

while month_start < this_month:
    # Set end date and time (23h59 on last day of month) for 'start_date' above
    month_end = month_start + relativedelta(months=1) - relativedelta(days=1)
    start_date = month_start.strftime("%Y-%m-%d")+"T00:00"
    end_date = month_end.strftime("%Y-%m-%d")+"T23:59"

    # Display computed start and end date and time to be used by the API request
    print("\nStart date for API request :", start_date)
    print("End date for API request   :", end_date)

    # Send GET request and collect returned data into 'response'
    print("Please wait while data is being downloaded...")
    response = API_request(URL, start_date, end_date)

    # Extract values of 'Demanda real' (actual demand) from JSON structure returned in API response
    demanda_real = response.json()["included"][0]["attributes"]["values"]
    demanda_programada = response.json()["included"][1]["attributes"]["values"]
    demanda_prevista = response.json()["included"][2]["attributes"]["values"]

    # Define full path to save data in dedicated CSV file
    csv_file_dir = "../Data/csv_output/"
    month_mm = "{:02d}".format(month_start.month)
    csv_file_path = f"REE_data_{month_start.year}-{month_mm}.csv"

    # Open CSV file for writing data
    with open(csv_file_dir+csv_file_path, "w", newline="") as csv_file:
        # Instantiate CSV writer with non-default delimiter
        csv_writer = csv.writer(csv_file, delimiter=";")
        # Write header row
        csv_writer.writerow(["datetime", "demanda", "programada", "prevista"])
        # Get and write datetime and demand values only (other fields discarded)
        for real, programada, prevista in zip(demanda_real, demanda_programada, demanda_prevista):
            date_time = real["datetime"]
            demand = real["value"]
            planned = programada["value"]
            forecast = prevista["value"]
            csv_writer.writerow([date_time, demand, planned, forecast])
    month_start += relativedelta(months=1)
    # Wait 10 seconds before next API request
    time.sleep(10)