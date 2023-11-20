# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:23:28 2023

@author: EGabriele
"""

import datetime
import requests
from datetime import timedelta
import json
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import dates


MYTOKEN = '1d9f6a4f-c8f3-4de2-aa81-432a9d318430'


#Day-ahaead Aggregated Generation [14.1.C]
def generation_forecast(MYTOKEN, doc_type, processType, in_domain, fr):
    
    periodStart = datetime.date.today() - timedelta(days=1)
    periodStart_str = periodStart.strftime("%Y%m%d")+str("2300")

    periodEnd = datetime.date.today()
    periodEnd_str = periodEnd.strftime("%Y%m%d")+str("2300")
        
    filepath = f"https://web-api.tp.entsoe.eu/api?securityToken={MYTOKEN}&documentType={doc_type}&processType={processType}&in_Domain={in_domain}&periodStart={periodStart_str}&periodEnd={periodEnd_str}"
    response = requests.get(filepath)
    response = response.text
    
    gen_for_lst = re.split('<|,|>',response)
    gen_for_lst = gen_for_lst[104:]
    forecast = []
    for x in gen_for_lst[::12]:
        forecast.append(x)
    
    period = np.arange(1,len(forecast)+1,1)
    date_range = pd.date_range(periodStart + timedelta(days=1),periods=len(forecast), freq=fr)
    set_time = date_range.strftime('%H:%M')
    name = 'Generation_Forecast_'+in_domain[3:5]
    
    df = pd.DataFrame({'Settlement_Date':date_range, 'Periods':period,'Time': set_time, name: forecast})
    df.index = df['Time']
    df[name] = df[name].astype(float)
    del df['Time']
    
    ax = plt.figure(figsize=(12,6))
    sns.lineplot(df[name])
    plt.xlabel(datetime.date.today())
    plt.ylabel("Generation Forecast (MW)")
    plt.title("Generation Forecast " + in_domain[3:5]+" (MW)")
    plt.xlim(df.index[0],df.index[-1])
    xticks = (pd.date_range(datetime.date.today(),periods=12,freq='2H')).strftime('%H:%M')
    plt.xticks(xticks)
    plt.show()

generation_forecast(MYTOKEN, 'A71','A01','10YFR-RTE------C','H')
generation_forecast(MYTOKEN, 'A71','A01','10YBE----------2','H')
generation_forecast(MYTOKEN, 'A71','A01','10YNO-0--------C','H')
generation_forecast(MYTOKEN, 'A71','A01','10YNL----------L','15min')

#################################################################################################

#Actual Physical Flows [12.1.G]
def interconnector_flows(MYTOKEN, doc_type, in_domain, out_domain, fr):
    
    periodStart = datetime.date.today()-timedelta(days=7)
    periodStart_str = periodStart.strftime("%Y%m%d")+str("2300")

    periodEnd = datetime.date.today()
    periodEnd_str = periodEnd.strftime("%Y%m%d")+str("2300")
        
    filepath = f"https://web-api.tp.entsoe.eu/api?securityToken={MYTOKEN}&documentType={doc_type}&in_Domain={in_domain}&out_Domain={out_domain}&periodStart={periodStart_str}&periodEnd={periodEnd_str}"
    
    response = requests.get(filepath)
    response = response.text
    flows_lst = re.split('<|,|>',response)
    flows_lst = flows_lst[100:]
    
    flows = []
    for x in flows_lst[::12]:
        flows.append(x)
    
    period = np.arange(1,len(flows)+1,1)
    
    date_range = pd.date_range(periodStart + timedelta(days=1),periods=len(flows), freq=fr)
        
    name = 'Int_flow '+out_domain[3:5]+' to '+in_domain[3:5]
    df = pd.DataFrame({'Settlement_Date':date_range, 'Periods':period, name:flows})
    df.index = df['Settlement_Date']
    df[name] = df[name].astype(float)
    del df['Settlement_Date']
        
    ax = plt.figure(figsize=(12,6))
    sns.lineplot(df[name], label=name)
    
    filepath = f"https://web-api.tp.entsoe.eu/api?securityToken={MYTOKEN}&documentType={doc_type}&in_Domain={out_domain}&out_Domain={in_domain}&periodStart={periodStart_str}&periodEnd={periodEnd_str}"
    
    response = requests.get(filepath)
    response = response.text
    flows_lst = re.split('<|,|>',response)
    flows_lst = flows_lst[100:]
    
    flows = []
    for x in flows_lst[::12]:
        flows.append(x)
    
    period = np.arange(1,len(flows)+1,1)
    
    date_range = pd.date_range(periodStart + timedelta(days=1),periods=len(flows), freq=fr)
        
    name = 'Int_flow '+in_domain[3:5]+' to '+out_domain[3:5]
    df = pd.DataFrame({'Settlement_Date':date_range, 'Periods':period, name:flows})
    df.index = df['Settlement_Date']
    df[name] = df[name].astype(float)
    del df['Settlement_Date']
        
    sns.lineplot(df[name], label = name, color = 'r')
    plt.ylabel("Interconnector_Flows (MW)", fontsize=15)
    plt.title("Interconnector Flows " + out_domain[3:5] + " (MW)", fontsize=20)
    plt.xlim(df.index[0],df.index[-1])
    plt.legend(bbox_to_anchor=(0.7,-0.1), ncol=len(df.columns), fontsize=12)
    plt.show()

interconnector_flows(MYTOKEN, 'A11', '10YGB----------A','10YFR-RTE------C', 'H')
interconnector_flows(MYTOKEN, 'A11', '10YGB----------A','10YBE----------2', '15min')
interconnector_flows(MYTOKEN, 'A11', '10YGB----------A','10YNO-0--------C', 'H')
interconnector_flows(MYTOKEN, 'A11', '10YGB----------A','10YNL----------L', '15min')

#############################################################################################

#Scheduled Interconnector flows

def scheduled_flows(MYTOKEN,doc_type, in_domain, out_domain):
    
    periodStart = datetime.date.today() - timedelta(days=1)
    periodStart_str = periodStart.strftime("%Y%m%d")+str("2300")

    periodEnd = datetime.date.today()
    periodEnd_str = periodEnd.strftime("%Y%m%d")+str("2300")  
    
    filepath = f"https://web-api.tp.entsoe.eu/api?securityToken={MYTOKEN}&documentType={doc_type}&in_Domain={in_domain}&out_Domain={out_domain}&periodStart={periodStart_str}&periodEnd={periodEnd_str}"
    response = requests.get(filepath)
    response = response.text
    flows_lst = re.split('<|,|>',response)
    flows_lst = flows_lst[104:]
    flows = []
    for x in flows_lst[::12]:
        flows.append(x)
    flows = flows[0:24]
    period = np.arange(1,len(flows)+1,1)
    date_range = pd.date_range(periodStart+timedelta(days=1),periods=len(flows), freq='H')
    
    name = 'Scheduled_Flows_'+out_domain[3:5]+'to'+in_domain[3:5]
    
    set_time = pd.date_range(datetime.date.today(),periods=24,freq='H')
    set_time = set_time.strftime('%H:%M')
    
    df = pd.DataFrame({'Settlement_Date':date_range, 'Periods':period, 'Time':set_time, name:flows})
    df.index = df['Time']
    df[name] = df[name].astype(float)
    del df['Settlement_Date']
    
    ax = plt.figure(figsize=(12,6))
    sns.lineplot(df[name], label= 'Import from '+ out_domain[3:5])
    
    filepath = f"https://web-api.tp.entsoe.eu/api?securityToken={MYTOKEN}&documentType={doc_type}&in_Domain={out_domain}&out_Domain={in_domain}&periodStart={periodStart_str}&periodEnd={periodEnd_str}"
    response = requests.get(filepath)
    response = response.text
    flows_lst = re.split('<|,|>',response)
    flows_lst = flows_lst[104:]
    flows = []
    for x in flows_lst[::12]:
        flows.append(x)
    flows = flows[0:24]
    period = np.arange(1,len(flows)+1,1)
    date_range = pd.date_range(periodStart+timedelta(days=1),periods=len(flows), freq='H')
    
    name = 'Scheduled_Flows_'+in_domain[3:5]+'to'+out_domain[3:5]

    df = pd.DataFrame({'Settlement_Date':date_range, 'Periods':period, 'Time':set_time, name:flows})
    df.index = df['Time']
    df[name] = df[name].astype(float)
    del df['Settlement_Date']
    
    sns.lineplot(df[name], label='Export to '+ in_domain[3:5], color='r')
    plt.xlabel(f"{periodEnd}", fontsize=15)
    plt.ylabel("Scheduled_Flows (MW)", fontsize=15)
    plt.title("Scheduled Interconnector Flows " + out_domain[3:5] + " (MW)",fontsize=20)
    plt.xlim(df.index[0],df.index[-1])
    plt.legend(bbox_to_anchor=(0.7,-0.1), ncol=len(df.columns), fontsize=12)
    xticks = (pd.date_range(datetime.date.today(),periods=24,freq='2H')).strftime('%H:%M')
    plt.xticks(xticks)
    plt.show()

scheduled_flows(MYTOKEN, 'A09','10YGB----------A','10YFR-RTE------C')
scheduled_flows(MYTOKEN, 'A09','10YGB----------A','10YBE----------2')
scheduled_flows(MYTOKEN, 'A09','10YGB----------A','10YNO-0--------C')
scheduled_flows(MYTOKEN, 'A09','10YGB----------A','10YNL----------L')