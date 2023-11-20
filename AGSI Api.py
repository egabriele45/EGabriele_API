# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:40:03 2023

@author: EGabriele
"""

from gie import GiePandasClient
import datetime
from datetime import timedelta

"""
Possible options below

query_gas_storage
query_gas_company
query_gas_country
query_lng_terminal
query_lng_lso
query_lng_country
"""

api_key = '5488103ec3476485ae912ccbc2992ca9'

client = GiePandasClient(api_key=api_key)

today = datetime.date.today()

df_storage = client.query_gas_country('GB', start=today-timedelta(days=21), end=today)
df_GB_full = df_storage['full']
print(df_GB_full)