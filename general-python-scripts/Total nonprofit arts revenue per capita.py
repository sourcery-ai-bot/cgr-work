# -*- coding: utf-8 -*-
"""
Created on Thursday Sep 22 11:07:40 2016

@author: Michael Silva
"""

from bs4 import BeautifulSoup
import requests as re
import pandas as pd

base_url = 'http://www.artsindexusa.org/where-i-live?c4='
data_url = 'http://www.artsindexusa.org/fetchCounty.php?selectedCounty='
data = []
states = ['AK','AL','AR','AZ','CA','CO','CT','DC','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY']
states=['DE']
for st in states:
    # Get the list of counties
    url = 'http://www.artsindexusa.org/fetchCounties.php?state='+st
    county_fips = re.get(url).json()
    for fips in county_fips:
        fips = fips.split(':')
        print('Getting data for: '+fips[1]+', '+st)
        # Get the headers and identify which rows we want in the data
        page = re.get(base_url + fips[0])
        soup = BeautifulSoup(page.content, 'lxml')
        headers = {}
        i = 0
        for div in soup.find_all('div',{'class':'sub'}):
            text = div.text
            text = text.replace('\xa0','')
            if 'Total nonprofit arts revenue per capita' in text:
                headers[i] = text
            i += 1
        # Pull the data for the rows identified above
        response = re.get(data_url + fips[0])
        i = 0
        for val in response.json():
            if i in headers:
                soup = BeautifulSoup(val, 'lxml')
                value = soup.get_text()
                if value != 'N/D':
                    data.append({'county fips':fips[0], 'county name':fips[1], 'state':st, 'measure':headers[i], 'value':soup.get_text(),'year':int(headers[32][-4:])})
            i += 1

# Build a data frame from the list of dicts
df = pd.DataFrame(data)

# Save it as an Excel file
print('Writing Data')
writer = pd.ExcelWriter('Nonprofit Revenue.xlsx', engine='xlsxwriter')
df.to_excel(writer,'AFA_Nonprofit_Revenue', index=False)
writer.save()