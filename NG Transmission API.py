# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 09:29:14 2023

@author: EGabriele
"""

from zeep import Client
from zeep.helpers import serialize_object
import pandas as pd
import datetime
from datetime import timedelta
from matplotlib import pyplot as plt



class Mipi:

    def __init__(self):
        self.client = Client('http://marketinformation.natgrid.co.uk/MIPIws-public/public/publicwebservice.asmx?wsdl')
        self.error = "No data retrieved. If you're expecting something try reducing the length of the from-to interval"

    def get_data_item(self, data_item, from_date, to_date, latest=False):

        fromDate = from_date.strftime('%Y-%m-%d')
        toDate = to_date.strftime('%Y-%m-%d')
        if latest:
            LatestFlag = 'Y'
        else:
            LatestFlag = 'N'

        dateType = 'GASDAY'
        ApplicableForFlag = 'Y'  # the query is by GAS DAY

        body = {'LatestFlag': f'{LatestFlag}',
                'ApplicableForFlag': f'{ApplicableForFlag}',
                'FromDate': f'{fromDate}',
                'ToDate': f"{toDate}",
                'DateType': f'{dateType}',
                'PublicationObjectNameList': {'string': f'{data_item}'}}

        r = self.client.service.GetPublicationDataWM(body)

        
        if r is not None:
                data = r[0].PublicationObjectData['CLSPublicationObjectDataBE']
                data_dic = [serialize_object(d) for d in data]
                df = pd.DataFrame(data=data_dic, columns=data_dic[0].keys())
                df['Value'] = pd.to_numeric(df['Value'])
                #print("DEBUG", f"{data_item} gathering complete")
                return df
        else:
            print("WARNING", f'No Data for: {data_item}')
        

    
    def get_sap(self, from_date, to_date, latest=True):
        
        report = 'SAP, Actual Day'
        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df

    
    def get_demand(self, from_date, to_date, report = 'DP1', latest=True):

        if report == 'DP6':
            report = 'Demand Actual, NTS, D+6'

        elif report == 'DP1':
            report = 'Demand Actual, NTS, D+1'

        elif report == 'PS':
            report = 'NTS Volume Offtaken, Powerstations Total'

        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df

    
    def get_forecast_demand(self, from_date, to_date, report='DF', latest=True):

        if report == 'DF':
            report = 'Demand Forecast, NTS'

        elif report == 'DF2':
            report = 'Demand Forecast, NTS, D-2'

        elif report == 'DF3':
            report = 'Demand Forecast, NTS, D-3'
            
        elif report == 'DF4':
            report = 'Demand Forecast, NTS, D-4'  
        
        elif report == 'DF5':
            report = 'Demand Forecast, NTS, D-5'
        
        elif report == 'DF6':
            report = 'Demand Forecast, NTS, D-6'
        
        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df
        
    def get_supply(self, from_date, to_date, latest=True):
        
        report = 'System Entry Flows, National, Physical'
        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df
    
    def get_forecast_temp(self, from_date, to_date, latest=True):
        
        report = 'Temperature, Forecast, D-1'
        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df
    
    def get_actual_temp(self, from_date, to_date, latest=True):
        
        report = 'Temperature, Actual, D+1'
        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df
    
    def get_forecast_supply(self, from_date, to_date, latest=True):
        
        report = 'System Entry Flows, National, Physical'
        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df
    
    def get_open_linepack(self, from_date, to_date, latest=True):
        
        report = 'Opening Linepack, actual'
        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df
    
    def get_close_linepack(self, from_date, to_date, latest=True):
        
        report = 'Closing Linepack, actual'
        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df
    
    

M = Mipi()
start = datetime.date.today()-timedelta(days=365)
stop = datetime.date.today()

#Daily Temperature
df_temp = M.get_actual_temp(start, stop)
df_temp = df_temp.set_index('ApplicableFor')
df_temp = df_temp.drop(['ApplicableAt', 'QualityIndicator', 'GeneratedTimeStamp', 'Substituted', 'CreatedDate'], axis=1)

#Forecast Temperature
df_Ftemp = M.get_forecast_temp(start, stop+timedelta(days=1))
df_Ftemp = df_Ftemp.set_index('ApplicableFor')
df_Ftemp = df_Ftemp.drop(['ApplicableAt', 'QualityIndicator', 'GeneratedTimeStamp', 'Substituted', 'CreatedDate'], axis=1)

#Gas Supply
start1 = datetime.datetime.today()-timedelta(days=365)
start1 = start1.replace(hour=0, minute=0, second=0, microsecond=0)
stop1 = datetime.datetime.today()
stop1 = stop1.replace(hour=0, minute=0, second=0, microsecond=0)
df_Supply = M.get_supply(start1, stop1)
df_Supply = df_Supply.set_index('ApplicableFor')
df_Supply = df_Supply.drop(['ApplicableAt', 'QualityIndicator', 'GeneratedTimeStamp', 'Substituted', 'CreatedDate'], axis=1)

#Forecast Temperature
df_dem = M.get_demand(start, stop+timedelta(days=1))
df_dem = df_dem.set_index('ApplicableFor')
df_dem = df_dem.drop(['ApplicableAt', 'QualityIndicator', 'GeneratedTimeStamp', 'Substituted', 'CreatedDate'], axis=1)

#Forecast Gas Supply
today = datetime.date.today()
df_Fsupply = M.get_forecast_supply(today, today+timedelta(days=1))
df_Fsupply = df_Fsupply.set_index('ApplicableFor')
df_Fsupply = df_Fsupply.drop(['ApplicableAt', 'QualityIndicator', 'GeneratedTimeStamp', 'Substituted', 'CreatedDate'], axis=1)

#Gas Demand
df_dem = M.get_demand(start, stop)
df_dem = df_dem.set_index('ApplicableFor')
df_dem = df_dem.drop(['ApplicableAt', 'QualityIndicator', 'GeneratedTimeStamp', 'Substituted', 'CreatedDate'], axis=1)

#Forecast Gas Demand
today = datetime.date.today()
df_Fdem = M.get_forecast_demand(today, today+timedelta(days=1))
df_Fdem = df_Fdem.set_index('ApplicableFor')
df_Fdem = df_Fdem.drop(['ApplicableAt', 'QualityIndicator', 'GeneratedTimeStamp', 'Substituted', 'CreatedDate'], axis=1)

#Opening Linepack
today = datetime.date.today()
df_Olin = M.get_open_linepack(today - timedelta(days=1), today)
df_Olin = df_Olin.set_index('ApplicableFor')
df_Olin = df_Olin.drop(['ApplicableAt', 'QualityIndicator', 'GeneratedTimeStamp', 'Substituted', 'CreatedDate'], axis=1)

#Closing Linepack
today = datetime.date.today()
df_Clin = M.get_close_linepack(today - timedelta(days=1), today)
df_Clin = df_Clin.set_index('ApplicableFor')
df_Clin = df_Clin.drop(['ApplicableAt', 'QualityIndicator', 'GeneratedTimeStamp', 'Substituted', 'CreatedDate'], axis=1)


"""

M = Mipi()
start = datetime.date.today()-timedelta(days=7)
stop = datetime.date.today()
df2 = M.get_actual_temp(start, stop)

df2 = df2.set_index('ApplicableFor')
df2['Value'].plot()
plt.ylabel('Supply (mcm)')
plt.title('Hourly Gas Supply UK')
plt.show()
"""