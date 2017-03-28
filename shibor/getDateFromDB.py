from datetime import datetime
from urllib.request import urlretrieve
import sys
import json
import pymongo
from pymongo import MongoClient

_conditions = {
    'start':'2016-01-01',
    'end':'2016-04-01'
}

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
        _arr.append(__data)
        print(__data)

    return _arr
    
    
def formatDateTime (str):
    try:
       return datetime.strptime(str)
    finally:
        return

if __name__ == "__main__":
    getData('shibor',_conditions)