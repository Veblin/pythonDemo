import requests
from bs4 import BeautifulSoup
import codecs
import json
import re



_dict = {
    '社团名称':'association',
    '类型':'type',
    '变更前':'before',
    '变更后':'after',
    '批准时间':'modTime',
    '法定代表人':'leader',
    '地址':'address',
    '业务主管单位':'director',
    '法人':'legal',
    '批准日期':'modTime',
    #
    '发证时间':'',
    '英文名称':'',
    '业务主管部门':'director',
    '注册资金':'',
    '网址':'',
    '登记证号':'',
    '组织机构代码':'',
    '业务范围':'',
    '宗旨':'',
    '办公地址':'',
    '法定代表人姓名':'leader',
    '单位负责人数':'',
    '女性人数':'',
    '会员总数':'',
    '个人会员':'',
    '分支机构代表机构数':''
}


def getHtmlDom(url):
    # 从 url中获取当前页面所有数据
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

def fixTdData (arr):
    # 清洗数据
    _arr = []
    for i in range(0,len(arr)):
        _arr.insert(i,_dict[arr[i]])
    return _arr

def getDataFromPages (urls):
    # 从 url组中挑选数据并格式化
    _arr = []
    
    for i in range(0,len(urls)):
        __mess = '暂无数据'
        __url = urls[i]
        _page = getHtmlDom(__url)
        # 从url获取id
        _ids = __url.split('?')[1].split('=')
        _dataTable = _page.select('td.bk > table table')
        if (len(_dataTable)>0):
            __mess = '获取数据...'
            _data = _dataTable[0].find_all('tr')
            # 返回格式{
            #     id:id, 来源ArticleID
            #     name: 'xx'
            #     lists:[{
            #         'type':'',
            #         'td1':'xxx',
            #         'td2':'xxx'
            #         'td3':'xxx'
            #     },]
            # }
            _res = {
                'id':_ids[1],
                'name':_data[1].td.text,
                'lists':[]
            }
            
            _th = fixTdData(makeStr2Arr(_data[0].text))[1:]
            for index in range(1,len(_data)):
                __list = makeStr2Arr(_data[index].text)
                if index == 1:
                    __list = __list[1:]
                
                __jsonData = json.loads(json.dumps(dict(zip(_th,__list))))
                _res['lists'].append(__jsonData)
                
            _arr.append(_res)
        print(__url+':'+__mess)
    return _arr
        
def makeUrlList (s,e):
    _url = []
    _json = {}
    for i in range(s,e):
        _url.append('http://www.hnmjzz.org.cn/shows.asp?ArticleID='+str(i))
    
    _json = getDataFromPages(_url)
    with open('hn.json', 'w',encoding='utf-8') as f:  
        f.write(json.dumps(_json,ensure_ascii=False))

def getDataFrom_jbqk_show(urls):
    _arr = []
    
    for i in range(0,len(urls)):
        __mess = '获取数据...'
        __url = urls[i]
        _page = getHtmlDom(__url)
        # 从url获取id
        _ids = __url.split('?')[1].split('=')
        _dataTable = _page.select('table table table')[0]
        _data = _dataTable.find_all('tr')
            # 返回格式{
            #     id:id, 来源ArticleID
            #     name:'xxx'
            # }
        _res = {
            'id':_ids[1]
        }
        
        for index in range(0,len(_data)):
            __row = _data[index]
            for row in range (0,len(__row)):
                # TODO 页面解析
                if row%2 == 0:
                    


        _arr.append(_res)
        print(__url+':'+__mess)

    return _arr

def make_jbqk_show(s,e):
    _url = []
    _json = {}
    for i in range(s,e):
        _url.append('http://www.hnmjzz.org.cn/jbqk_show.asp?ArticleID='+str(i))
    
    _json = getDataFrom_jbqk_show(_url)
    # with open('jbqk_show.json', 'w',encoding='utf-8') as f:  
    #     f.write(json.dumps(_json,ensure_ascii=False))


if __name__ == '__main__':
    # makeUrlList(2060,2070)
    make_jbqk_show(1,5)