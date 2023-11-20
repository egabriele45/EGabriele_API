# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:33:48 2023

@author: EGabriele
"""

import requests
import re
import json
import pandas as pd
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import seaborn as sns

api_key = 'i7z8e1hhp8ijllb'

yesterday = datetime.date.today()-timedelta(days=1)
date_range = pd.date_range(yesterday,periods=48,freq="30min")

SP = []
Imb = []
Surplus = []

for i in range(1,49):
    Imb_Vol = requests.get(f'https://api.bmreports.com/BMRS/B1780/v1?APIKey={api_key}&SettlementDate={yesterday}&Period={i}&ServiceType=csv')
    Imb_Vol = Imb_Vol.text
    Imb_Vol_lst = re.split(':|,|\*|\n',Imb_Vol)
    #Imb_Vol = json.loads(Imb_Vol_lst)
    df=pd.DataFrame(Imb_Vol_lst)
    #Set_date = df[0][27]
    #Dates.append(Set_date)
    Set_Per = df[0][28]
    SP.append(Set_Per)
    ImbVol = df[0][29]
    Imb.append(ImbVol)
    Surpl = df[0][38]
    Surplus.append(Surpl)

df_Imb = pd.DataFrame({'Settlement_Period':SP,'Imbalance Volumes':Imb,'Surplus':Surplus})
yesterday = datetime.date.today()-timedelta(days=1)
df_Imb['Settlement_Date'] = date_range
df_Imb.index = df_Imb['Settlement_Date'] 
df_Imb['Imbalance Volumes'] = df_Imb['Imbalance Volumes'].astype(float)
del df_Imb['Settlement_Date']


SP2 = []
Imb_Pr = []

for i in range(1,49):
    Imb_Price = requests.get(f'https://api.bmreports.com/BMRS/B1770/v1?APIKey={api_key}&SettlementDate={yesterday}&Period={i}&ServiceType=csv')
    Imb_Price = Imb_Price.text
    Imb_Price = re.split(':|,|\*|\n',Imb_Price)
    #Imb_Vol = json.loads(Imb_Vol_lst)
    df=pd.DataFrame(Imb_Price)
    Set_Per = df[0][48]
    SP2.append(Set_Per)
    ImbPri = df[0][47]
    Imb_Pr.append(ImbPri)

df_Imb_Price = pd.DataFrame({'Settlement_Period':SP2,'Imbalance Price':Imb_Pr})
date_range = pd.date_range(yesterday,periods=48,freq="30min")
df_Imb_Price['Settlement_Date'] = date_range
df_Imb_Price.index = df_Imb_Price['Settlement_Date'] 
df_Imb_Price['Imbalance Price'] = df_Imb_Price['Imbalance Price'].astype(float)
del df_Imb_Price['Settlement_Date']


SP = []
APX = []

for i in range(1,49):
    APX_Prices = requests.get(f'https://api.bmreports.com/BMRS/MID/v1?APIKey={api_key}&FromSettlementDate={yesterday}&ToSettlementDate={yesterday}&Period='+str(i)+'&ServiceType=csv')
    APX_Prices = APX_Prices.text
    APX_lst = re.split(':|,|\*|\n',APX_Prices)
    #Imb_Vol = json.loads(Imb_Vol_lst)
    df2 = pd.DataFrame(APX_lst)
    Set_Per = df2[0][5]
    SP.append(Set_Per)
    Price = df2[0][6]
    APX.append(Price)

df_APX = pd.DataFrame({'Settlement_Period':SP,'APX_Price':APX})
date_range = pd.date_range(yesterday,periods=48,freq="30min")
df_APX['Settlement_Date'] = date_range
df_APX.index = df_APX['Settlement_Date']
df_APX['APX_Price'] = df_APX['APX_Price'].astype(float)
del df_APX['Settlement_Date']

print(df_Imb)
print(df_Imb_Price)
print(df_APX)

ax = plt.figure(figsize=(10,6))
sns.lineplot(x=df_Imb.index, y=df_Imb['Imbalance Volumes'])
plt.xlabel(f"{yesterday}")
plt.ylabel("Imbalance Volumes MWh")
plt.title("Imbalance Volumes D-1(MWh)")
plt.xlim(df_Imb.index[0],df_Imb.index[-1])
plt.show()

ax = plt.figure(figsize=(10,6))
sns.lineplot(x=df_Imb_Price.index, y=df_Imb_Price['Imbalance Price'])
plt.xlabel(f"{yesterday}")
plt.ylabel("Imbalance Price £/MWh")
plt.title("Imbalance Price D-1(£/MWh)")
plt.xlim(df_Imb_Price.index[0],df_Imb_Price.index[-1])
plt.show()

ax = plt.figure(figsize=(10,6))
sns.lineplot(x=df_APX.index, y=df_APX['APX_Price'])
plt.xlabel(f"{yesterday}")
plt.ylabel("APX Price £/MWh")
plt.title("APX Price D-1(£/MWh)")
plt.xlim(df_APX.index[0],df_APX.index[-1])
plt.show()