
import csv
import requests
import json
import os
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px

from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("FRED_API_KEY")

# User Input and API Pull

while True: 
    try:
        state = input("Please input a state abbreviation: ")
        FRED_series_id = (state) + "UR"
        request_url = f"https://api.stlouisfed.org/fred/series/observations?series_id={FRED_series_id}&api_key={api_key}&file_type=json"
        response = requests.get(request_url)

        parsed_response = json.loads(response.text)

        total_observations = parsed_response["count"]
        break

    except KeyError:
        print("Hey, didn't find that state. Please try again with a state abbreviation.")
        

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

matching_dates_low = [v for v in parsed_response["observations"] if float(v["value"]) == all_time_low]
matching_date_low = matching_dates_low[0]
all_time_low_date = matching_date_low["date"]

matching_dates_high = [v for v in parsed_response["observations"] if float(v["value"]) == all_time_high]
matching_date_high = matching_dates_high[0]
all_time_high_date = matching_date_high["date"]

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
print(f"The {str.upper(state)} Labor Market During COVID-19 Pandemic")
print("----------------------------------------------------------------------")
print(f"Current Unemployment Rate: {str(last_value)}%")
print(f"February 2020 Unemployment Rate {str(pre_covid_level)}%")
print(f"All-Time High Unemployment Rate ({all_time_high_date}): {str(all_time_high)}%")
print(f"All-Time Low Unemployment Rate ({all_time_low_date}): {str(all_time_low)}%")
print(f"Current Unemployment Rate for the United States: {str(last_value_us)}%")
print(f"Difference between {str.upper(state)} and the US: {str(UR_difference)}ppts")
print("----------------------------------------------------------------------")
if last_value > last_value_us:
    print("THIS STATE'S LABOR MARKET IS AT HIGHER RISK OF NEEDING ECONOMIC POLICY ASSISTANCE")
else:
    print("THIS STATE'S LABOR MARKET IS AT LOWER RISK OF NEEDING ECONOMIC POLICY ASSISTANCE")
print("----------------------------------------------------------------------")

# Data Visualization 1 REFERENCE: https://plotly.com/python/time-series/

all_val = []
k = -1
for t in parsed_response["observations"]:
    k += 1
    valuec = float(parsed_response["observations"][k]["value"])
    all_val.append(valuec) 
values = all_val 


all_date = []
m = -1
for r in parsed_response["observations"]:
    m += 1
    val_date = parsed_response["observations"][m]["date"]
    all_date.append(val_date)
dates = all_date 


fig = px.line(x=dates, y=values, title=str.upper(state) + " State Unemployment Rate")
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")])))
fig.update_yaxes(ticksuffix="%") #reference : https://plotly.com/python/axes/
fig.update_layout(xaxis_title='Date',yaxis_title='Value %')

plotly.offline.plot(fig)

# Data Visualization 2 REFERENCE: https://plotly.com/python/line-charts/

all_val2 = []
a = -1
for w in parsed_response["observations"]:
    a += 1
    valuec2 = float(parsed_response["observations"][a]["value"])
    all_val2.append(valuec2)
values2 = all_val2

all_val_us2 = []
b = -1
for x in parsed_response_us["observations"]:
    b += 1
    valuec_us2 = float(parsed_response_us["observations"][b]["value"])
    all_val_us2.append(valuec_us2)
values_us2 = all_val_us2


all_date2 = []
c = -1
for y in parsed_response["observations"]:
    c += 1
    val_date2 = parsed_response["observations"][c]["date"]
    all_date2.append(val_date2)
dates2 = all_date2   

all_us_date2 = []
d = -1
for z in parsed_response_us["observations"]:
    d += 1
    us_date2 = parsed_response_us["observations"][d]["date"]
    all_us_date2.append(us_date2)
us_dates2 = all_us_date2  

fig2 = go.Figure()

# Create and style traces

fig2.add_trace(go.Scatter(x=all_date2, y=values2, name='state', line = dict(color='firebrick', width=4)))
fig2.add_trace(go.Scatter(x=all_us_date2, y=values_us2, name='national', line = dict(color='royalblue', width=4, dash='dash')))
fig2.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")])))
# Edit the layout

fig2.update_yaxes(ticksuffix="%")
fig2.update_layout(title="The National & " + str.upper(state) + " Unemployment Rates", xaxis_title='Date', yaxis_title='Value %')
plotly.offline.plot(fig2)