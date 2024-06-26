from bs4 import BeautifulSoup
import requests
import pandas as pd

url='https://electrify.stiigo.com/'
page=requests.get(url)
soup=BeautifulSoup(page.text, 'html.parser')

soup1=str(soup.find_all('tr')[1:2])
removelist=['<table>', '<tbody>', '<tr>', '</tr>', '</tbody>', '</table>', '</td>', '<td class="label">','<td class="data">', '°', '\n\n', '<td align="right">', '<td><input id="emailaddr" style="width:235px; margin-bottom:3px" type="text"/>, <td><a href="#" id="regemail"><img alt="" src="regemail.png"/></a>]', '<td>', '<td><span style="font-size:11px">', '<b>', '</b>']
for word in removelist:
    soup1=soup1.replace(word, '')

soup1=soup1[-14:-8]
MWh=float(soup1)
KWh=MWh/10
KWh=round(KWh, 3)
print(KWh)

teststartcol=1

from openpyxl import Workbook

cellid=()

filename = "excelKWh.xlsx"
workbook = Workbook()
sheet = workbook.active
sheet["A1"] = KWh
workbook.save(filename=filename)