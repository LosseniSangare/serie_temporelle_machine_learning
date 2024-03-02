# utils v1.0
# Common functions for processing REE data


# Import librairies
from datetime import datetime as dt
from dateutil import tz
import pandas as pd
import pytz
import requests


# Define a function building an API request based on user defined start and end dates
def API_request(url, start, end):

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

    response = requests.get(url=url, params=request_params, headers=headers)

    # Display response code and url returned by the API
    print("API request completed.")
    print("API Response code :", response.status_code)
    print("API Response URL :", response.url)

    # Return the API response
    return response


# Define a function to convert REE datetime to UTC special format
def datetime_to_utc_str(date):
    '''
    Input: date string in REE format
    Output: date string in UTC format

    Example:
    REE datetime format: "2024-02-19T03:00:00.000+01:00", string length: 29
    Target UTC datetime format: "2024-02-18 23:00:00", string length: 19
    '''
    date_time = dt.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z')
    datetime_utc = date_time.astimezone(pytz.UTC)
    datetime_utc = datetime_utc.strftime("%Y-%m-%d %H:%M:%S%z")
    return datetime_utc


# Define a function to convert REE datetime to UTC special format and aggregate values by duration
def aggreg_to_utc_duration(df, duration):
    '''
    Input: dataframe with datetime in REE format
    Output: dataframe with datetime in special UTC format and values aggregated by duration
    '''
    durations = {
        "10mn": 15,
        "1h": 13,
        "1d": 10
    }
    # Set the time string to complete the truncated timestamp to the duration format
    time_string = " 00:00:00"

    # Change string to/from datetime object to convert the timestamp to UTC
    df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%dT%H:%M:%S.%f%z")
    df['datetime'] = df['datetime'].apply(lambda x: x.tz_convert(tz.tzutc()))
    df['datetime'] = df['datetime'].dt.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    # Truncate the timestamp to the specified duration and store it as a new column 'datatime_UTC'
    df['datetime_UTC']=df['datetime'].str[:durations[duration]]

    # Create a dataframe with UTC timestamps where a data value is the mean of values for the specified duration
    df_duration = df.groupby('datetime_UTC')['demanda'].mean().reset_index()
    df_duration['programada'] = df.groupby('datetime_UTC')['prevista'].mean().reset_index()['prevista']
    df_duration['prevista'] = df.groupby('datetime_UTC')['prevista'].mean().reset_index()['prevista']

    # Complete the truncated timestamp according to the specified duration
    df_duration['datetime_UTC'] += time_string[durations[duration]-19:]
    
    return df_duration