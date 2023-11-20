# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 13:11:53 2023

@author: EGabriele
"""

import requests
import json
import pandas as pd

filepath = 'https://opendata.edf.fr/api/explore/v2.1/catalog/datasets/indisponibilites-des-moyens-de-production-edf-sa/records?limit=100&refine=filiere%3A%22Nucl%C3%A9aire%22'
response = requests.get(filepath)
response = response.text
response = json.loads(response)

df = pd.json_normalize(response['results'])
df = df[['identifiant','status','filiere','nom','date_de_publication','date_de_debut','date_de_fin','puissance_maximale_mw','puissance_disponible_mw','information_complementaire']]
df.columns = ['Plant_ID','Status','Tech','Name','Publication_Date','Start_Date','End_Date','Capacity_Max','Available_Capacity','Extra_Info']
df['Extra_Info'] = df['Extra_Info']
df['Extra_Info'] = df['Extra_Info'].str[5:]
print(df)

