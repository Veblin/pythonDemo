from datetime import datetime
from urllib.request import urlretrieve
import sys
import json
import pymongo
from pymongo import MongoClient
import flask 
from flask import request,Flask,jsonify,make_response

_conditions = {
    'start':'2016-01-01',
    'end':'2016-04-01'
}

app = Flask(__name__)

def getData(
    tableName = 'shibor',
    conditions = {}
):
    _client = MongoClient('localhost',27017)
    _db = _client['shibor']
    _arr = []
    #获取时间戳
    _startStamp = int(datetime.timestamp(datetime.strptime(conditions['start'],'%Y-%m-%d')))
    _endStamp = int(datetime.timestamp(datetime.strptime(conditions['end'],'%Y-%m-%d')))
    _table = _db.get_collection(tableName)
    for _date in range(_startStamp,_endStamp+1,3600*24):
        #格式化日期格式
        __date = datetime.fromtimestamp(_date).strftime('%Y-%m-%d')
        # 过滤数据
        __data =  _table.find_one({'Date':__date})
        # 把符合过滤条件的数据添加到数组
        if __data != None:
            _arr.append(__data)
        # print(__data)

    return _arr
    
    
def formatDateTime (str):
    try:
       return datetime.strptime(str)
    finally:
        return

def apiRetData(data):
    # 格式化数据
    # [{
    #     'x': [{
    #         'date': '2016-03-30'
    #     }],
    #     'y': [{
    #         'O/N': 2.004,
    #         '1W': 2.312,
    #        ....
    #     }]
    # },
    # .....
    api = []
    yKey = ['O/N','1W','2W','3M','6M','9M','1Y']
    for i in range(0,len(data)):
        _data = data[i]
        _yData = fillData(_data,yKey)
        _api = {
            'x':[
                {
                    'data':_data['Date']
                }
            ],
            'y':[
                _yData
            ]
        }
        api.append(_api)

    return api

def fillData(data,arr):
    res = {}
    for i in range(0,len(arr)):
        _key = arr[i]
        res[_key] = data[_key]

    return res

#跨域
def modHttp(origin=None):
    def allow_cross_domain(fun):
        def wrapper_fun(*args, **kwargs):
            resp = make_response(*args, **kwargs)
            resp.headers['Access-Control-Allow-Origin'] = origin
            return resp
        fun.provide_automatic_options = False
        return wrapper_fun
    print('modHttp')
    return allow_cross_domain


@app.route('/api/shibor',methods = ['POST','GET'])
# TODO 解决跨域问题
@modHttp(origin='localhost')
def apiShibor():
    print('apiShibor')
    # show the post with the given id, the id is an integer
    start = request.values['start_time']
    end =  request.values['end_time']
    
    if start is None or end is None:
        _message = 'POST data is wrong'
    
    _conditions={
        'start':start,
        'end':end
    }
    _data = apiRetData(getData('shibor',_conditions))
    _message = ''
    _code = 200
    if len(_data) == 0:
        _message = 'No Data'
    else:
        _message = 'Success'
        
    # 
    # print(getBaseReturnValue(_data,_message,_code))
    return getBaseReturnValue(_data,_message,_code)

def getBaseReturnValue(data,msg,code):
    _json_data = jsonify({'datas':data,'msg':msg,'success':code})
    return _json_data


if __name__ == "__main__":
    # 返回数据
    app.run(debug=True)
    