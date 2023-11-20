# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 14:27:49 2023

@author: EGabriele
"""

import requests

filepath = 'https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_production_type'
response = requests.get(filepath)
response = response.text
print(response)

