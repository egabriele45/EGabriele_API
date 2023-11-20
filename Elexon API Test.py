# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 10:40:44 2023

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
from matplotlib.dates import DateFormatter

api_key = 'i7z8e1hhp8ijllb'

Dates2 = []
SP2 = []
Imb_Pr = []

yesterday = datetime.date.today()-timedelta(days=1)

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

ax = plt.figure(figsize=(10,6))
sns.lineplot(x=df_Imb_Price.index, y=df_Imb_Price['Imbalance Price'])
plt.xlabel(f"{yesterday}")
plt.ylabel("Imbalance Price £/MWh")
plt.title("Imbalance Price D-1(£/MWh)")
plt.xlim(df_Imb_Price.index[0],df_Imb_Price.index[-1])
plt.show()


