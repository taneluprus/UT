from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import datetime


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

KWhlist=[]
KWhlist.append(KWh)

currenttime=datetime.datetime.now().strftime('%m-%d %H:%M')
timelist=[]
timelist.append(currenttime)

f1=open(r'D:\UT\git\UT\Elektrihind.txt', 'a')
f1.write(currenttime)
f1.write(' - ')
f1.write(KWh)
f1.write('\n')
f1.close
