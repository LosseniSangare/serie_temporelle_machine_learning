# csv_mn_to_hour_test_script v1.0

'''
This a test script to convert 5 or 10mn demand values to hourly values as available in older REE data.
Hour demand is simply the mean of sub-hour values as seen on periods where REE provides both hour and sub-hour values.
'''

import pandas as pd

# Get user input for year and month of data to be reformatted
year = input("Year as a 4-digit number : ")
month = input("Month as a 2-digit number : ")

# File path of source CSV file
src_file_path = f"../Data/csv_output/REE_data_{year}-{month}.csv"
# File path of destination CSV file with reformated data
dst_file_path = f"../Data/csv_output/REE_data_{year}-{month}_h.csv"

# Read source file into a dataframe
df = pd.read_csv(src_file_path, sep=";")

# Time interval provided for user information, not required by csv file handling below
time_A = int(df.iloc[0,0][14:16])
time_B = int(df.iloc[1,0][14:16])
interval = time_B-time_A
print(f"Time interval in source file is {interval} mn")

# Create a 'date_hour' column which is 'datetime' truncated after the two digits of the hour
df['date_hour'] = df['datetime'].str[:13]
# Create a new dataframe of which 1st column is truncated 'datetime' and 2nd column is the mean of 'demand' values for an hour
df_hour = df.groupby('date_hour')['demand'].mean().reset_index()
# Add ':00:00.000+02:00' to 'date_hour' string to be consistant with standard REE file format
df_hour['date_hour']=df_hour['date_hour'] + ":00:00.000+00:00"
# Rename 'date_hour' column to be consistant with standard REE data columns
df_hour.rename(columns={'date_hour': 'datetime'}, inplace=True)

# Write reformatted data to destination CSV file
df_hour.to_csv(dst_file_path, index=False, sep=";")
print(f"Reformatted data written to {dst_file_path}.")