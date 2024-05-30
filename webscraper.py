from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
import datetime
import time
#requierments - bs4, requests, openpyxl, datetime, time, Jinja2
#file requierments (current) - startcolrecord.txt, testexcel1.xlsx
#[TODO] CHANGE FILENAMES at some point

teststartcol=1

while True:
    url='https://hipikuut.com/weewx/'
    page=requests.get(url)
    weathersoup=BeautifulSoup(page.text, 'html.parser')

    #print(soup.find('table'))
    teststr=str(weathersoup.find('table'))

    removelist=['<table>', '<tbody>', '<tr>', '</tr>', '</tbody>', '</table>', '</td>', '<td class="label">','<td class="data">', '°', '\n\n']
    for word in removelist:
        teststr=teststr.replace(word, '')

    teststr=teststr.replace('²','2')
    teststr=teststr.strip()

    andmed={}

    andmedlines = teststr.splitlines()

    def convert(lst):
       res_dict = {}
       for i in range(0, len(lst), 2):
           res_dict[lst[i]] = lst[i + 1]
       return res_dict

    andmed=convert(andmedlines)



    url='https://electrify.stiigo.com/'
    page=requests.get(url)
    hindsoup=BeautifulSoup(page.text, 'html.parser')

    hindsoup=str(hindsoup.find_all('tr')[1:2])
    removelist=['<table>', '<tbody>', '<tr>', '</tr>', '</tbody>', '</table>', '</td>', '<td class="label">','<td class="data">', '°', '\n\n', '<td align="right">', '<td><input id="emailaddr" style="width:235px; margin-bottom:3px" type="text"/>, <td><a href="#" id="regemail"><img alt="" src="regemail.png"/></a>]', '<td>', '<td><span style="font-size:11px">', '<b>', '</b>']
    for word in removelist:
        hindsoup=hindsoup.replace(word, '')

    hindsoup=hindsoup[-14:-8]
    MWh=float(hindsoup)
    KWh=MWh/10
    KWh=round(KWh, 3)
    #KWh=str(KWh)
    #KWh=(KWh,'s/KWh')
    andmed['Hind']=KWh


    currenttime=datetime.datetime.now().strftime('%H:%M')
    #print(time)
    timelist=[]
    timelist.append(currenttime)

    

    andmedvalues=andmed.values()

    df=pd.DataFrame(andmedvalues, columns=timelist)
    #df=(df.T)
    #print(df)

    with pd.ExcelWriter('C:\\Users\\Tanel\\Desktop\\testexcel1.xlsx', mode='a',engine='openpyxl', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, sheet_name='Sheet1', startcol=teststartcol, index=False)
        teststartcol+=1
    
    f1=open(r'C:\Users\Tanel\Desktop\startcolrecord.txt', 'a')
    f1.write(str(teststartcol))
    f1.write('\n')  
    f1.close()

    time.sleep(1)
    