import os
import re


info = ''
testNum = 10000
testPerSec = 2000
_url_ = 'http://navara.zznissan.com.cn/'
# _url_ = input('Input Test URL:')

def getTestData(url):
    _cmd = 'ab -n '+str(testNum)+' -c '+str(testPerSec)+' -k '+url
    return os.popen(_cmd).read()

def clearData(string):
    # 根据回车遍历字符串数据为数组
    _res = []
    _data = re.split('\n',string)
    for i in range(len(_data)):
        __data = _data[i]
        if len(__data) > 0:
            _res.append(__data)
    
    return _res

def clearStr(data):
    # 清除数据空格
    return str(data).strip()


def makeData (arr):
    _dic = dict(
        level=1500,
        faild=0,
        req=1500,
        time=200,
        p90=200
    )
    for i in range(len(arr)):
        _str = arr[i]
        if i>3 and i<20:
            _val = re.split('\s',clearStr(re.split(':',_str)[1]))[0]
        # 并发数    
        if i == 9 :
            _dic['level'] = _val
        # 失败数
        elif i == 12 :
            _dic['faild'] = _val
        # 每秒请求
        elif i == 16 :
            _dic['req'] = _val
        # 平均相应 TODO 还需单独处理
        elif i == 17 :
            _dic['time'] = _val
        # 90%事务响应
        elif i == 31 :
            _dic['p90'] = re.split('\s',_str)[-1]
    
    return _dic

if __name__ == '__main__':
    try
        info = clearData(getTestData(_url_))
    ≤
    data = {}
    if len(info) > 10:
        #successed
        data = makeData(info)
    else:
        data = 'error'

    print('Testing:'+ str(data))