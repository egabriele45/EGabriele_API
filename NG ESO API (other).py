# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 13:59:07 2023

@author: EGabriele
"""


import requests
from urllib import parse

sql_query = '''SELECT 2023-11-10 FROM  "0eede912-8820-4c66-a58a-f7436d36b95f" ORDER BY "_id" ASC LIMIT 100'''

params = {
'sql'
: sql_query}

response = requests.get('https://api.nationalgrideso.com/api/3/action/datastore_search_sql',params = parse.urlencode(params))
    
print(response)

"""  
    
    data = resposne.json()[
"result"
]
    print(data) # Printing data
except requests.exceptions.RequestException as e:
    print(e.response.text)
    
"""