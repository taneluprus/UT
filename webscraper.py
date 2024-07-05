from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
import datetime
import time
import re
#requierments - bs4, requests, openpyxl, datetime, time, schedule
#file requierments (current) - startcolrecord.txt, Ilmjahind.xlsx


f1=open(r'D:\UT\git\UT\startcolrecord.txt', 'r+')
startingcolumn=int(f1.readlines()[-1])

url='https://hipikuut.com/weewx/'
page=requests.get(url, timeout=5)
#print(page)
weathersoup=BeautifulSoup(page.text, 'html.parser')

weatherstr=str(weathersoup.find('table'))

removelist=['<table>', '<tbody>', '<tr>', '</tr>', '</tbody>', '</table>', '</td>', '<td class="label">','<td class="data">', '°', '\n\n']
for word in removelist:
    weatherstr=weatherstr.replace(word, '')

weatherstr=weatherstr.replace('²','2')
weatherstr=weatherstr.strip()
print(weatherstr)

andmed={}

andmedlines = weatherstr.splitlines()
print(andmedlines)

#andmedlines=['Outside Temperature', '16.5C', 'Heat Index', '16.6C', 'Wind Chill', '16.5C', 'Dew Point', '15.2C', 'Humidity', '92%', 'Barometer', '1003.2 mbar (0.7)', 'Wind', '0.3 m/s ESE (123)', 'Rain Rate', '0.0 mm/h', 'Rain Today', '1.0 mm', 'UV Index', '3.8', 'ET', '0.0 mm', 'Radiation', '432 W/m2', 'Inside Temperature', '22.9C', 'Inside Humidity', '52%']

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

andmed=Convert(andmedlines)
#print(andmed)



#       ELEKTRIHIND
#--------------------------------------------------------------------------------------------
url='https://electrify.stiigo.com/'
page=requests.get(url)
soup=BeautifulSoup(page.text, 'html.parser')

soup1=str(soup.find_all('tr')[1:2])
removelist=['<table>', '<tbody>', '<tr>', '</tr>', '</tbody>', '</table>', '</td>', '<td class="label">','<td class="data">', '°', '\n\n', '<td align="right">', '<td><input id="emailaddr" style="width:235px; margin-bottom:3px" type="text"/>, <td><a href="#" id="regemail"><img alt="" src="regemail.png"/></a>]', '<td>', '<td><span style="font-size:11px">', '<b>', '</b>']
for word in removelist:
    soup1=soup1.replace(word, '')

non_decimal = re.compile(r'[^\d.-]+')
soup1=non_decimal.sub('', soup1)
print(soup1)

soup1=soup1[0:6]
print(soup1)
MWh=float(soup1)
KWh=MWh/10
KWh=round(KWh, 3)
KWh=str(KWh)

andmed['Elektrhind']=KWh


#--------------------------------------------------------------------------------------------


currenttime=datetime.datetime.now().strftime('%H:%M')
andmed['Time']=currenttime
currentdate=datetime.datetime.now().strftime('%d-%m')
andmed['Date']=currentdate


andmedvalues=andmed.values()
#print(andmedvalues)


df=pd.DataFrame([andmedvalues])


with pd.ExcelWriter(r'D:\UT\git\UT\ilm.xlsx', mode='a', if_sheet_exists='overlay') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=startingcolumn, columns=None, header=None)
    startingcolumn+=1
    

f1.write('\n') 
f1.write(str(startingcolumn))
f1.close()
