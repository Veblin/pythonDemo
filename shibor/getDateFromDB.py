from datetime import datetime
from urllib.request import urlretrieve
import sys
import json
import pymongo
from pymongo import MongoClient
import flask 
from flask import request,Flask

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




@app.route('/api/shibor',methods = ['POST'])
def apiShibor():
    # show the post with the given id, the id is an integer
    start = request.values['start_time']
    end =  request.values['end_time']
    if start is None or end is None:
        abort(400)
    
    
    _conditions={
        'start':start,
        'end':end
    }
    # TODO 返回数据json格式化
    # 
    print(apiRetData(getData('shibor',_conditions)))
        # return 'Post %d' % post_id



if __name__ == "__main__":
    # 返回数据
    app.run()
    