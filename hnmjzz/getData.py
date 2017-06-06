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
jsonArr = []

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
                'id':_ids[1]
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

def clearCellText (string,reg):
    _string = ''
    if type(string) == str:
        _string = string
    else:
        _string = str(string)
    
    _string = _string.strip()
    
    return _string.replace(reg,'')
def clearBSCellText (bsObj):
    _string = ''
    for string in bsObj.stripped_strings:
        _string = string
    
    return _string

def getDataFrom_jbqk_show(urls):
    
    for i in range(0,len(urls)):
        __mess = '获取数据...'
        __url = urls[i]
        _page = getHtmlDom(__url)
        # 从url获取id
        _ids = __url.split('?')[1].split('=')
        _tables = _page.select('table table table')
        if len(_tables) < 1 :
            # 页面无数据
            __mess = '无数据，下一个'
            continue
        
        _dataTable = _tables[0]
        _data = _dataTable.find_all('tr')
            # 返回格式{
            #     id:id, 来源ArticleID
            #     data:'xxx'
            # }
        _res = {
            'id':_ids[1]
        }
        __obj = {}
        __child1Obj = {} # 
        __child2Obj = {}
        __parentKey = []
        __parentVal = []    
        __child2Keys = []
        __child2Vals = []
        print(__url+':'+__mess)
        # 遍历表格
        for index in range(1,len(_data)):
            __row = _data[index].find_all('td')
            if index == 10 :
                #  __child1Obj 社团刊物 子数据结构
                __childKeys = []
                __childVals = []
                for row in range (2,len(__row)):
                    __text = clearBSCellText(__row[row])
                    if row%2 == 0:
                        __childKeys.append(__text)
                    else:
                        # 过滤空格
                        __text = re.findall('(\d+|[\u4e00-\u9fa5]+)[^\s]',__text)
                        if len(__text)>0 : 
                            __text = __text[0]
                        else:
                            __text = '0'

                        __childVals.append(__text)

                __child1Obj = dict(zip(__childKeys,__childVals))
            elif index == 13 :
                    #  __child2Obj 社团刊物 子数据结构
                for row in range (1,len(__row)):
                    __text = clearBSCellText(__row[row])
                    if row%2 != 0:
                        __child2Keys.append(__text)
                    else:
                        __child2Vals.append(__text)
                        
                
            elif index == 14:
                for row in range (0,len(__row)):
                    __text = clearBSCellText(__row[row])
                    if row%2 == 0:
                        __child2Keys.append(__text)
                    else:
                        __child2Vals.append(__text)

                __child2Obj = dict(zip(__child2Keys,__child2Vals))
            else:
                __cell = __row
                for row in range (0,len(__row)):
                    __text = clearBSCellText(__row[row])
                    # print('index:'+str(index) + ',text:'+__text)
                    #页面解析
                    # key
                
                    if row%2 == 0 and row < len(__row) - 1:
                        if __text != '' and clearBSCellText(__row[row+1]) != '':
                            __parentKey.append(__text)
                    else:
                        if __text != '' and clearBSCellText(__row[row-1]) != '':
                            __parentVal.append(__text)

                __obj = dict(zip(__parentKey,__parentVal))
            
                # 手动添加 会费标准和社团刊物
                __obj['会费标准'] = __child1Obj
                __obj['社团刊物'] = __child2Obj
                _res['data'] = __obj

        jsonArr.append(_res)

def make_jbqk_show(s,e):
    _url = []
    for i in range(s,e):
        _url.append('http://www.hnmjzz.org.cn/jbqk_show.asp?ArticleID='+str(i))
    
    getDataFrom_jbqk_show(_url)
    with open('jbqk_show.json', 'w',encoding='utf-8') as f:  
        f.write(json.dumps(jsonArr,ensure_ascii=False))
    print(jsonArr)

if __name__ == '__main__':
    # makeUrlList(2060,2070)
    make_jbqk_show(1,500)