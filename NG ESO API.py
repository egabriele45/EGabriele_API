# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 09:52:01 2023

@author: EGabriele
"""


from urllib.request import urlopen
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


wind_for_url = 'https://api.nationalgrideso.com/api/3/action/datastore_search?&resource_id=93c3048e-1dab-4057-a2a9-417540583929&limit=1000'

response = urlopen(wind_for_url)

data = response.read().decode('utf-8')

dictionary = json.loads(data)

w_forecast = []
date = []
SP = []
for i in range(0,(len(dictionary['result']['records']))):
    w_forecast.append(dictionary['result']['records'][i]['Wind_Forecast'])
    date.append((dictionary['result']['records'][i]['Datetime']))
    SP.append((dictionary['result']['records'][i]['Settlement_period']))

df_wind_for = pd.DataFrame({'Date':date, 'Settlement_Period':SP, 'Forecast':w_forecast})
df_wind_for.index = pd.to_datetime(df_wind_for['Date'])

fig, ax = plt.subplots(figsize=(10,6))
sns.lineplot(x=df_wind_for.index, y=df_wind_for['Forecast'], ax=ax)

ax.set_ylabel("Wind Forecast (MW)")
plt.title("Wind Forecast 2-14 Days Ahead")
plt.xlim(df_wind_for.index[0],df_wind_for.index[-1])
plt.show()


dem_for_url = 'https://api.nationalgrideso.com/api/3/action/datastore_search?resource_id=7c0411cd-2714-4bb5-a408-adb065edf34d&limit=1000'

response = urlopen(dem_for_url)

data = response.read().decode('utf-8')

dictionary = json.loads(data)

dem_forecast = []
date = []

for i in range(0,(len(dictionary['result']['records']))):
    dem_forecast.append(dictionary['result']['records'][i]['NATIONALDEMAND'])
    date.append((dictionary['result']['records'][i]['GDATETIME']))
    
    
df_dem_for = pd.DataFrame({'Date':date, 'Forecast': dem_forecast})
df_dem_for.index = pd.to_datetime(df_dem_for['Date'])

fig, ax = plt.subplots(figsize=(10,6))
sns.lineplot(x=df_dem_for.index, y=df_dem_for['Forecast'], ax=ax)

ax.set_ylabel("Demand Forecast (MW)")
plt.title("Demand Forecast 2-14 days ahead (MW)")
plt.xlim(df_dem_for.index[0],df_dem_for.index[-1])
plt.show()

