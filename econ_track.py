
import csv
import requests
import json
import os
import pandas as pd
import plotly

from dotenv import load_dotenv
load_dotenv()


#SAMPLE 3
#from plotly.subplots import make_subplots
#fig = make_subplots(rows=1, cols=2)
#fig.add_scatter(y=[4, 2, 1], mode="lines", row=1, col=1)
#fig.add_bar(y=[2, 1, 3], row=1, col=2)
##fig.show()
#plotly.offline.plot(fig)

#SAMPLE 2 
#import plotly.graph_objects as go
#fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
##fig.show()
#plotly.offline.plot(fig) 

#SAMPLE 1
#import plotly.express as px
#df = px.data.iris()
#fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", title="A Plotly Express Figure")
# print(fig)
#fig.show() if it is not working use this one -----   plotly.offline.plot(fig) 


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
    index += 1
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

# Data Visualization 
#SELECTED STATE 
##{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","observation_start":"1600-01-01",
##"observation_end":"9999-12-31","units":"lin","output_type":1,"file_type":"json","order_by":"observation_date",
##"sort_order":"asc","count":533,"offset":0,"limit":100000,"observations":
##
##[{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"1976-01-01","value":"10.3"},
##{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"1976-02-01","value":"10.300"},
##{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"1976-03-01","value":"10.200"},
##{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"1976-04-01","value":"10.200"}
##{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"2020-05-01","value":"14.5"}]}
##{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"2020-02-01","value":"3.7"},
# {"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"2020-03-01","value":"4.1"},
# {"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"2020-04-01","value":"15.3"},
# {"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"2020-05-01","value":"14.5"}]}


#US NATIONAL
#{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","observation_start":"1600-01-01",
#"observation_end":"9999-12-31","units":"lin","output_type":1,"file_type":"json","order_by":"observation_date",
#"sort_order":"asc","count":869,"offset":0,"limit":100000,"observations":
#[{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"1948-01-01","value":"3.4"},
#{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"1948-02-01","value":"3.8"},
#{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"1948-03-01","value":"4.0"}
#{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"2020-03-01","value":"4.4"},
#{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"2020-04-01","value":"14.7"},
#{"realtime_start":"2020-06-25","realtime_end":"2020-06-25","date":"2020-05-01","value":"13.3"}]}


import plotly.graph_objects as go

all_val = []
a = -1
for w in parsed_response["observations"]:
    a = a + 1
    valuec = float(parsed_response["observations"][a]["value"])
    all_val.append(valuec)
values = all_val

all_val_us = []
b = -1
for x in parsed_response["observations"]:
    b += 1
    valuec_us = float(parsed_response_us["observations"][b]["value"])
    all_val_us.append(valuec_us)
values_us = all_val_us


all_date = []
c = -1
for y in parsed_response["observations"]:
    c += 1
    val_date = parsed_response["observations"][c]["date"]
    all_date.append(val_date)
#dates = all_date    

all_us_date = []
d = -1
for z in parsed_response_us["observations"]:
    d += 1
    us_date = parsed_response_us["observations"][d]["date"]
    all_us_date.append(us_date)
#us_dates = all_us_date  

fig = go.Figure()
# Create and style traces
fig.add_trace(go.Scatter(x=all_date, y=values, name='selected state',line = dict(color='firebrick', width=4)))
fig.add_trace(go.Scatter(x=all_us_date, y=values_us, name='national',line = dict(color='royalblue', width=4, dash='dash')))

# Alternative style traces
#fig.add_trace(go.Scatter(x=month, y=low_2014, name = 'Low 2014',line=dict(color='royalblue', width=4)))
#fig.add_trace(go.Scatter(x=month, y=high_2007, name='High 2007',line=dict(color='firebrick', width=4,dash='dash') # dash options include 'dash', 'dot', and 'dashdot'))
#fig.add_trace(go.Scatter(x=month, y=high_2000, name='High 2000',line = dict(color='firebrick', width=4, dash='dot')))
#fig.add_trace(go.Scatter(x=month, y=low_2000, name='Low 2000',line=dict(color='royalblue', width=4, dash='dot')))

# Edit the layout
fig.update_layout(title='Unemployment Rates for Selected State & National',
                   xaxis_title='Date',
                   yaxis_title='Value')
plotly.offline.plot(fig)