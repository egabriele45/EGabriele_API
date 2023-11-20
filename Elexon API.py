# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 12:42:58 2023

@author: EGabriele
"""

import os
from typing import Optional
from ElexonDataPortal.dev import orchestrator
from datetime import timedelta
import datetime
import pytz
from pytz import timezone
import pandas as pd

class Client:
    def __init__(
        self, 
        api_key: str = 'i7z8e1hhp8ijllb', 
        n_retry_attempts: int = 3,
        non_local_tz: Optional[str] = None
    ):
        if api_key is None:
            assert 'BMRS_API_KEY' in os.environ.keys(), 'If the `api_key` is not specified during client initialisation then it must be set to as the environment variable `BMRS_API_KEY`'
            api_key = os.environ['BMRS_API_KEY']
            
        self.api_key = api_key
        self.n_retry_attempts = n_retry_attempts
        self.non_local_tz = non_local_tz
        
        #self.set_method_descs()
        
        return
    """    
    def set_method_descs(self):
        get_methods_names = [attr for attr in dir(self) if attr[:4]=='get_']
        get_method_descs = [getattr(self, get_methods_name).__doc__.split('\n')[1].strip() for get_methods_name in get_methods_names]

        self.methods = dict(zip(get_methods_names, get_method_descs))
    """
    #Imbalance Price
    def get_B1770(
        self,
        start_date: str = '2020-01-01 1:00', 
        end_date: str = '2020-01-01 1:30',
    ):

        
        df = orchestrator.query_orchestrator(
            method = 'get_B1770',
            api_key = self.api_key,
            n_attempts = self.n_retry_attempts,
            request_type = 'SP_and_date',
            kwargs_map = {'date': 'SettlementDate', 'SP': 'Period'},
            func_params = ['APIKey', 'date', 'SP', 'ServiceType'],
            start_date = start_date,
            end_date = end_date,
            non_local_tz = self.non_local_tz
        )
        
        return df
    
    #Imbalance Volumes
    def get_B1780(
        self,
        start_date: str = '2020-01-01 1:00', 
        end_date: str = '2020-01-01 1:30',
    ):
        
        df = orchestrator.query_orchestrator(
            method = 'get_B1780',
            api_key = self.api_key,
            n_attempts = self.n_retry_attempts,
            request_type = 'SP_and_date',
            kwargs_map = {'date': 'SettlementDate', 'SP': 'Period'},
            func_params = ['APIKey', 'date', 'SP', 'ServiceType'],
            start_date = start_date,
            end_date = end_date,
            non_local_tz = self.non_local_tz
        )
        
        return df
        
#Imbalance
C = Client()

#dti = pd.date_range(start="2023-11-13 00:00:00+00:00",
                    #freq='D', periods=2).tz_convert('GMT')
#df_Imb = C.get_B1780(start_date = str(datetime.date.today()-timedelta(days=1)), end_date = str(datetime.date.today()-timedelta(days=1)))
df_Imb = C.get_B1780(start_date = "2023-11-13 00:00:00+00:00", end_date= "2023-11-14 00:00:00+00:00")
print(df_Imb)

"""
df_temp = df_temp.set_index('ApplicableFor')
df_temp = df_temp.drop(['ApplicableAt', 'QualityIndicator', 'GeneratedTimeStamp', 'Substituted', 'CreatedDate'], axis=1)
"""