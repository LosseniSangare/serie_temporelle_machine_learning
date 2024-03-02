# aggreg_by_duration v1.0
# Script to aggregate (average) demand values by a specified duration

# Avoid FutureWarning messages
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Import librairies
import os
import pandas as pd
from utils import aggreg_to_utc_duration

# Set source and destination file paths
wrk_dir = os.getcwd()
src_path = wrk_dir + "/src_files/"
dst_path = wrk_dir + "/dst_files/"

# Build list of source files by scanning the source path
src_file_list = sorted(os.listdir(src_path))

# Ask user for data aggregation duration
duration = input("Enter the duration for data aggregation (10mn, 1h, 1d): ")

# Open destination CSV file
with open(f"{dst_path}REE_data_aggregated_by_{duration}.csv", "w") as dst_file:

	# Write the header row
	dst_file.write('datetime_utc,demanda,programada,prevista\n')

	# Go through the list of source files
	for file in src_file_list:

		# Open one source CSV file
		with open (src_path + file, "r") as src_file:
			
			# Read source file into a dataframe
			df = pd.read_csv(src_file, sep=";")

			# Time interval in source file, for information only
			time_A = int(df.iloc[0,0][14:16])
			time_B = int(df.iloc[1,0][14:16])
			interval = time_B-time_A
			print(f"Time interval in source file is {interval} mn")

			df_duration = aggreg_to_utc_duration(df, duration)

            # Write dataframe with reformatted data to destination CSV file
			df_duration.to_csv(dst_file, header=False, index=False, mode='a', sep=',')