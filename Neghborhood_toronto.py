# Neighborhood in Torronto

!pip install bs4
!pip install lxml

from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import requests
import lxml 

# download url data from internet
url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
source = requests.get(url).text
canada_data = BeautifulSoup(source, 'lxml')

# creat a new Dataframe
column_names = ['Postalcode','Borough','Neighborhood']
toronto = pd.DataFrame(columns = column_names)

# loop through to find postcode, borough, neighborhood 
content = canada_data.find('div', class_='mw-parser-output')
table = content.table.tbody
postcode = 0
borough = 0
neighborhood = 0

for tr in table.find_all('tr'):
    i = 0
    for td in tr.find_all('td'):
        if i == 0:
            postcode = td.text.replace('\n','')
            i = i + 1
        elif i == 1:
            borough = td.text.replace('\n','')
            i = i + 1
        elif i == 2: 
            neighborhood = td.text.replace('\n', '')
    toronto = toronto.append({'Postalcode': postcode,'Borough': borough,'Neighborhood': neighborhood},ignore_index=True)

# clean dataframe 
toronto = toronto[toronto.Borough!='Not assigned']
toronto = toronto[toronto.Borough!= 0]
toronto.reset_index(drop = True, inplace = True)
i = 0
for i in range(0,toronto.shape[0]):
    if toronto.iloc[i][2] == 'Not assigned':
        toronto.iloc[i][2] = toronto.iloc[i][1]
        i = i+1
                                 
df = toronto.groupby(['Postalcode','Borough'])['Neighborhood'].apply(', '.join).reset_index()
df.head()

# Data Cleaning

df = df.dropna()
empty = 'Not assigned'
df = df[(df.Postalcode != empty ) & (df.Borough != empty) & (df.Neighborhood != empty)]
df.head()

def neighborhood_list(grouped):    
    return ', '.join(sorted(grouped['Neighborhood'].tolist()))
                    
grp = df.groupby(['Postalcode', 'Borough'])
df2 = grp.apply(neighborhood_list).reset_index(name='Neighborhood')
print(df2.shape)
df2.head()

# Adding geolocation

geolocation =  pd.read_csv('http://cocl.us/Geospatial_data')
geolocation.head()

geolocation.reset_index()
geolocation.columns = ['Postalcode', 'Latitude', 'Longitude']
geolocation.head()

toronto = pd.merge(toronto,geolocation,on = 'Postalcode')
toronto.head(10)

toronto.groupby('Neighborhood').count().head()
