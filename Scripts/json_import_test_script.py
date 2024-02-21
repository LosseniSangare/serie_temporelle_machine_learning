# REE_data_import v1.0

'''
This a test version importing data from a file downloaded manually with HTTP GET using
REE's public API documented at https://www.ree.es/en/apidatos
'''

import csv, json

# Path to JSON file to be imported
json_file_path = "../Data/json_input/REE_data_2022-04-30.json"
# Path to save data into CSV file
csv_file_path = "../Data/csv_output/REE_data_2022-04-30.csv"

try:
    # Read JSON data from file
    with open(json_file_path, "r") as json_file:
        parsed_data = json.load(json_file)

        # Extract datetime and demand values from JSON structure
        demand_datetime_values = parsed_data["included"][0]["attributes"]["values"]

        # Write to CSV file
        with open(csv_file_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=";")
            csv_writer.writerow(["datetime", "demand"])  # Write header row

            for values in demand_datetime_values:
                datetime = values["datetime"]
                demand = values["value"]
                csv_writer.writerow([datetime, demand])
        print(f"Data written to {csv_file_path}")

except FileNotFoundError:
    print(f"Error: File '{json_file_path}' not found.")
except KeyError:
    print("Error: Invalid JSON structure or missing fields.")