# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 16:39:06 2023

@author: EGabriele
"""

import requests
import datetime
from datetime import timedelta
import json
import pandas as pd



start='2023-11-16'
end='2023-11-17'

filepath = f"https://api.nationalgrideso.com/api/3/action/datastore_search_sql?sql=SELECT%20COUNT(*)%20OVER%20()%20AS%20_count,%20*%20FROM%20%22f93d1835-75bc-43e5-84ad-12472b180a98%22%20WHERE%20%22DATETIME%22%20%3C=%20'{end}'%20AND%20%22DATETIME%22%20%3E=%20'{start}'%20ORDER%20BY%20%22_id%22%20ASC%20LIMIT%20100"
response = requests.get(filepath)
response = response.text
response = json.loads(response)


#response = pd.read_json()
"""
# Get data and convert into dataframe
import pandas as pd
import requests
from urllib import parse
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import seaborn as sns

start = datetime.date.today() - timedelta(days=7)

sql_query = f'''SELECT COUNT(*) OVER () AS _count, * FROM "f93d1835-75bc-43e5-84ad-12472b180a98" WHERE "DATETIME" >= '{start}' ORDER BY "_id" ASC'''

params = {'sql': sql_query}

try:
    response = requests.get('https://api.nationalgrideso.com/api/3/action/datastore_search_sql', params = parse.urlencode(params))
    data = response.json()["result"]
    df = pd.DataFrame(data["records"])
except requests.exceptions.RequestException as e:
    print(e.response.text)


df_Tot_Gen = df[['DATETIME','GENERATION']]
df_Tot_Gen.index = pd.to_datetime(df_Tot_Gen['DATETIME'])
del df_Tot_Gen['DATETIME']
df_Tot_Gen = df_Tot_Gen.astype(float)

ax = plt.figure(figsize=(10,6))
sns.lineplot(df_Tot_Gen)
plt.xlabel("")
plt.ylabel("Generation (MW)")

plt.title("Total UK Generation (MW)")
plt.show()


df = df[['NUCLEAR','STORAGE','HYDRO','IMPORTS','DATETIME','GAS','COAL','WIND','BIOMASS','OTHER','SOLAR']]
df.index = df['DATETIME']
df.index = pd.to_datetime(df.index)
del df['DATETIME']
df = df.astype(float)

ax = plt.figure(figsize=(14,6))
sns.lineplot(df[['NUCLEAR','IMPORTS','GAS','WIND','SOLAR']])
plt.xlabel("")
plt.ylabel("Generation (MW)")
plt.legend(bbox_to_anchor=(0.7,-0.05), ncol=len(df.columns), fontsize=8)
plt.title("Generation by Technology (MW)")
plt.show()

"""