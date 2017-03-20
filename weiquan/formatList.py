from bs4 import BeautifulSoup
from urllib.parse import urlparse
from lxml import html
import re
import urllib
import string

# 数据文件路径
import os
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR,'weiquan.html') 

import jieba
dict_path = os.path.join(BASE_DIR,'userdict.txt') 
jieba.load_userdict(dict_path)


html = open(file_path,'r')

bsObj = BeautifulSoup(html,'html.parser')
# bsObj = BeautifulSoup(html)

list = bsObj.find_all('div',attrs={'class':'member ng-scope'})


nameList = []
index = 0
for link in list:
    print(link.attrs['title'])
    if link.attrs['title'] is not None:
        index = index + 1
        _info = link.p.get_text()
        # 初步去杂质
        _info = _info.strip(string.punctuation)

        _userInfoObj = urllib.parse.parse_qs(link.img.attrs['src'])
        if len(_info) > 0:
            __info = jieba.cut(_info,cut_all=False)
            nameList.append({
                'id':index,
                'username':_userInfoObj['username'][0],
                'name':'/'.join(__info)
            })
#清洗字符串
# def cleanInput (input):
    # input.strip(string.punctuation)


print (nameList)
