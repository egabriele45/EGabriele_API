# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 08:51:05 2023

@author: EGabriele
"""

from urllib.request import urlopen
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import timedelta
import ast
import numpy as np

MYTOKEN = '1d9f6a4f-c8f3-4de2-aa81-432a9d318430'
in_domain = '10YFR-RTE------C'
out_domain = '10YGB----------A'
start = datetime.date.today() 
start = start.strftime("%Y%m%d%H%M")

end = datetime.date.today() + timedelta(days=1)
end = end.strftime("%Y%m%d%H%M")

start_m1 = datetime.date.today()-timedelta(days=1)
start_m1 = start_m1.strftime("%Y%m%d%H%M")

end_today = datetime.date.today()
end_today = end_today.strftime("%Y%m%d%H%M")

"""
flows_url = f'https://web-api.tp.entsoe.eu/api?securityToken={MYTOKEN}&documentType=A11&in_Domain={in_domain}&out_Domain={out_domain}&periodStart={start}&periodEnd={end}'

response = urlopen(flows_url)

data = response.read().decode('utf-8')
"""

"""

Gen_for_url = f'https://web-api.tp.entsoe.eu/api?securityToken={MYTOKEN}&documentType=A71&processType=A01&in_Domain={in_domain}&periodStart={start}&periodEnd={end}'

response = urlopen(gen_for_url)

data = response.read().decode('utf-8')



url = f'https://web-api.tp.entsoe.eu/api?securityToken={MYTOKEN}&documentType=A75&processType=A16&psrType=B02&in_Domain={in_domain}&periodStart={start_m1}&periodEnd={end_today}'

response = urlopen(url)

data = response.read().decode('utf-8')

print(data)


example:

Physical Flows [12.1.G]
Document type = A11
in_Domain = 10YCZ-CEPS-----N
out_Domain = 10SK-SEPS-----K
periodStart = 201412312300
periodend = 201612312300
(or time interval)

https://web-api.tp.entsoe.eu/api?securityToken=MYTOKEN&documentType=A11&in_Domain=10YCZ-CEPS-----N&out_Domain=10YSK-SEPS-----K&periodStart=201512312300&periodEnd=201612312300



Day-ahaead Aggregated Generation [14.1.C]
Document type = A71
processType=A01
in_Domain = 10YCZ-CEPS-----N
periodStart = 201412312300
periodend = 201612312300
(or time interval)

https://web-api.tp.entsoe.eu/api?securityToken=MYTOKEN&documentType=A71&processType=A01&in_Domain=10YCZ-CEPS-----N&periodStart=201512312300&periodEnd=201612312300



Aggregated Generation per Type [16.1.B&C]

Document type = A75
processType=A16
psrType=A04
in_Domain = 10YCZ-CEPS-----N
periodStart = 201412312300
periodend = 201612312300
(or time interval)

https://web-api.tp.entsoe.eu/api?securityToken=MYTOKEN&documentType=A75&processType=A16&psrType=B02&in_Domain=10YCZ-CEPS-----N&periodStart=201512312300&periodEnd=201612312300

processType
A01 - Day Ahead
A02 - Intra day incremental
A16 - Realised

documentType
A71 - Generation forecast
A75 - Actual generation per type
A80 - Generation unavailability

psrType
A03 - Mixed
A04 - Generation
B14 -  Nuclear
B18/B19 - Onshore/Offshore Wind

Domain
France - 10YFR-RTE------C
UK - 10YGB----------A
Belgium - 10YBE----------2
Eleclink - 11Y0-0000-0265-K
IFA2 - 17Y0000009369493
IFA - 10Y1001C--00098F
North Sea Link - BZN|NO2A

1d9f6a4f-c8f3-4de2-aa81-432a9d318430

"""