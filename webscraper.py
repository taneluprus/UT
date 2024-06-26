from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
import datetime
import time
import schedule
#requierments - bs4, requests, openpyxl, datetime, time, schedule
#file requierments (current) - startcolrecord.txt, Ilmjahind.xlsx

f1=open(r'D:\UT\git\startcolrecord.txt', 'r+')
startingcolumn=int(f1.readlines()[-1])

url='https://hipikuut.com/weewx/'
page=requests.get(url, timeout=5)
print(page)
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



def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

andmed=Convert(andmedlines)
print(andmed)

currenttime=datetime.datetime.now().strftime('%H:%M')
timelist=[]
timelist.append(currenttime)


andmedvalues=andmed.values()

df=pd.DataFrame(andmedvalues, columns=timelist)

with pd.ExcelWriter(r'D:\UT\git\UT\ilm.xlsx', mode='a',engine='openpyxl', if_sheet_exists='overlay') as writer:
    df.to_excel(writer, sheet_name='Sheet1', startcol=startingcolumn, index=False)
    startingcolumn+=1
    

f1.write('\n') 
f1.write(str(startingcolumn))
f1.close()

