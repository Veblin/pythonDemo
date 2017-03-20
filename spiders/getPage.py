import urllib
import urllib.request
import http.cookiejar
import re
import csv
import codecs

from bs4 import BeautifulSoup

from lxml import html

import requests
# get HTML

_url = 'http://www.circ.gov.cn/web/site0/tab5203/info4054427.htm'

def getHtmlDom(url):
    page = requests.get(url)
    return BeautifulSoup(page.text,'lxml')

tableDom = getHtmlDom(_url).find(id='tab_content').table

## open csv

f = open('table.csv', 'w')
csv_writer = csv.writer(f)

## var
companyName = ''  # 公司名
companyType = '' # 公司属性 0 中资 1 外资
PM = '' # 原保费收入
newPM = '' #新增保费收入

# get each tr
trIndex = 0
for row in tableDom.find_all('tr'):

    # TODO get data form td in tr
    _cells = row.find_all('td')


    if len(_cells) == 6 :
        #第一行
            companyType = _cells[0].find(text=True)

    elif len(_cells) == 5 :
        # 其他行
        companyName = _cells[1].find(text=True).string
        PM = _cells[2].find(text=True)
        newPM = _cells[3].find(text=True)
        csv_writer.writerow([x.encode('utf-8') for x in [companyName, companyType, PM, newPM]])
    # print(newPM.string)
    trIndex += 1


print('DONE')
#
# for tr in tableDom:
#
# print(tableDom)
