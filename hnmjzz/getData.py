import requests
from bs4 import BeautifulSoup
import codecs
import json
import re

_url = ['http://www.hnmjzz.org.cn/shows.asp?ArticleID=1060']



def getHtmlDom(url):
    _headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    page = requests.get(url,headers=_headers)
    # 声明页面编码，默认是 'utf-8'
    page.encoding = 'gb2312'
    return BeautifulSoup(page.text,'lxml')

def makeStr2Arr (str):
    return re.split('^\n',str)[1].split('\n')

def getDataFromPages (urls):
    
    for i in range(0,len(urls)):
        __url = urls[i]
        _page = getHtmlDom(__url)
        # 从url获取id
        _ids = __url.split('?')[1].split('=')
        _dataTable = _page.select('td.bk > table table')
        if (len(_dataTable)>0):
            _data = _dataTable[0].find_all('tr')
            _th = makeStr2Arr(_data[0].text)
            _td = makeStr2Arr(_data[1].text)
            _jsonData = json.loads(json.dumps(dict(zip(_th,_td))))
            return {
                _ids[0]:_ids[1]
                data:_jsonData
            }



if __name__ == '__main__':
    getDataFromPages(_url);