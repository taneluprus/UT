#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
import datetime
import re
import os
#requierments - bs4, requests, pandas, openpyxl, datetime, re, os

directory=os.path.dirname(os.path.realpath(__file__))

#     ILMAANDMED
#--------------------------------------------------------------------------------------------
url='https://hipikuut.com/weewx/'
page=requests.get(url, timeout=5)

weathersoup=BeautifulSoup(page.text, 'html.parser')
weatherstr=str(weathersoup.find('table'))

#Eemaldab mittevajalikud elemendid
removelist=['<table>', '<tbody>', '<tr>', '</tr>', '</tbody>', '</table>', '</td>', '<td class="label">','<td class="data">', '\n\n', '°']
for word in removelist:
    weatherstr=weatherstr.replace(word, '')
weatherstr=weatherstr.replace('²','2')
weatherstr=weatherstr.strip()
andmedlines = weatherstr.splitlines()

#Muudab andmete listi dictiks
def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

andmed={}
andmed=Convert(andmedlines)


#--------------------------------------------------------------------------------------------

#       ELEKTRIHIND
#--------------------------------------------------------------------------------------------
url='https://electrify.stiigo.com/'
page=requests.get(url)
soup=BeautifulSoup(page.text, 'html.parser')

#Eemaldab mittevajalikud elemendid
soup1=str(soup.find_all('tr')[1:2])
removelist=['<table>', '<tbody>', '<tr>', '</tr>', '</tbody>', '</table>', '</td>', '<td class="label">','<td class="data">', '°', '\n\n', '<td align="right">', '<td><input id="emailaddr" style="width:235px; margin-bottom:3px" type="text"/>, <td><a href="#" id="regemail"><img alt="" src="regemail.png"/></a>]', '<td>', '<td><span style="font-size:11px">', '<b>', '</b>']
for word in removelist:
    soup1=soup1.replace(word, '')

#Eemaldab kõik mittenumbrid
non_decimal = re.compile(r'[^\d.-]+')
soup1=non_decimal.sub('', soup1)
print(soup1)

#Muudab hinna s/KWh
soup1=soup1[0:6]
print(soup1)
MWh=float(soup1)
KWh=MWh/10
KWh=round(KWh, 3)
KWh=str(KWh)

andmed['Elektrhind']=KWh


#--------------------------------------------------------------------------------------------

#    KELLAAEG JA KUUPÄEV
#--------------------------------------------------------------------------------------------
currenttime=datetime.datetime.now().strftime('%H:%M')
andmed['Time']=currenttime
currentdate=datetime.datetime.now().strftime('%d-%m')
andmed['Date']=currentdate
#--------------------------------------------------------------------------------------------

#     EXCEL
#--------------------------------------------------------------------------------------------
andmedvalues=andmed.values()

df=pd.DataFrame([andmedvalues])

#Leiab mitmendasse ritta peab andmed kirjutama
f1=open((directory+r'/startcolrecord.txt'), 'r+')
startingcolumn=int(f1.readlines()[-1])

#Kirjutab andmed tabelisse
with pd.ExcelWriter((directory+r'/ilm.xlsx'), mode='a', if_sheet_exists='overlay') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=startingcolumn, columns=None, header=None)
    startingcolumn+=1

#Kirjutab faili järgmise kirjutattava rea numbri
f1.write('\n') 
f1.write(str(startingcolumn))
f1.close()
#--------------------------------------------------------------------------------------------
