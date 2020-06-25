
import csv
import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("FRED_API_KEY")

# User Input and API Pull

try:
    state = input("Please input a state abbreviation: ")
    FRED_series_id = (state) + "UR"
    request_url = f"https://api.stlouisfed.org/fred/series/observations?series_id={FRED_series_id}&api_key={api_key}&file_type=json"
    response = requests.get(request_url)

    parsed_response = json.loads(response.text)

    total_observations = parsed_response["count"]

except KeyError:
    print("Hey, didn't find that location. Try again please.")
    exit()

# Getting the state's most recent UR

last_value = float(parsed_response["observations"][total_observations-1]["value"]) # assumes oldest data point comes first, as is FRED standard

# Getting the state's all-time high/all-time low UR

all_values = []
index = -1

for v in parsed_response["observations"]:
    index = index + 1
    value = float(parsed_response["observations"][index]["value"])
    all_values.append(value)

all_time_high = max(all_values)
all_time_low = min(all_values)

# Getting the state's pre-COVID-19 unemployment rate

pre_covid_date = "2020-02-01"

matching_observations = [v for v in parsed_response["observations"] if v["date"] == pre_covid_date] 
matching_observation = matching_observations[0]
pre_covid_level = float(matching_observation["value"])

# Getting the current national UR

request_url_us = f"https://api.stlouisfed.org/fred/series/observations?series_id=UNRATE&api_key={api_key}&file_type=json"
response_us = requests.get(request_url_us)
parsed_response_us = json.loads(response_us.text)

total_observations_us = parsed_response_us["count"]
last_value_us = float(parsed_response_us["observations"][total_observations_us-1]["value"])

# Calculate and the difference between the state and national URs

UR_difference = round(last_value - last_value_us, 1)

# Information Output

print("----------------------------------------------------------------------")
print("The " + str.upper(state) + " Labor Market During COVID-19 Pandemic")
print("----------------------------------------------------------------------")
print("Current Unemployment Rate: " + str(last_value) + "%")
print("February 2020 Unemployment Rate " + str(pre_covid_level) + "%")
print("All-Time High Unemployment Rate: " + str(all_time_high) + "%")
print("All-Time Low Unemployment Rate: " + str(all_time_low) + "%")
print("Current Unemployment Rate for the United States: " + str(last_value_us) + "%")
print("Difference between " + str.upper(state) + " and the US: " + str(UR_difference) + "ppts")
print("----------------------------------------------------------------------")
if last_value > last_value_us:
    print("THIS STATE'S LABOR MARKET IS AT HIGHER RISK OF NEEDING ECONOMIC POLICY ASSISTANCE")
else:
    print("THIS STATE'S LABOR MARKET IS AT LOWER RISK OF NEEDING ECONOMIC POLICY ASSISTANCE")
print("----------------------------------------------------------------------")