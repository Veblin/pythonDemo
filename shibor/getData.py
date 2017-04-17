import requests
import sys
from datetime import datetime
from urllib.request import urlretrieve
import re
# lib for excel & mongo
import xlrd
import sys
import json
import pymongo
from pymongo import MongoClient

# get Data from URL 
# DEMO 
#Shibor URL
# http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_Shibor_Data_2016.xls&nameOld=Shibor%CA%FD%BE%DD2016.xls&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data

#Report URL
#http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_Quote_Data_2016.xls&nameOld=%B1%A8%BC%DB%CA%FD%BE%DD2016.xls&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data

#Shibor Ava URL
#http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_Shibor_Tendency_Data_2016.xls&nameOld=Shibor%BE%F9%D6%B5%CA%FD%BE%DD2016.xls&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data


# Headers 
# GET /shibor/web/html/downLoad.html?nameNew=Historical_Shibor_Data_2017.xls&nameOld=Shibor%CA%FD%BE%DD2017.xls&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data HTTP/1.1
# Host: www.shibor.org
# Connection: keep-alive
# Pragma: no-cache
# Cache-Control: no-cache
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
# Referer: http://www.shibor.org/shibor/web/downLoad.jsp
# Accept-Encoding: gzip, deflate, sdch
# Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6
# Cookie: JSESSIONID=2hl2YPjMn1H4mPB3sQDyzbVQTWVDTwYLY53xQTh2Q9QYSpfNhzrK!-957207357; _gscu_67677853=899794585tquw176; _gscs_67677853=t89986570ltvzan15|pv:1; _gscbrs_67677853=1

fileDic = {
    'shibor':('Historical_Shibor_Data_','Shibor%CA%FD%BE%DD'),
    'report':('Historical_Quote_Data_','%B1%A8%BC%DB%CA%FD%BE%DD'),
    'shiborAva':('Historical_Shibor_Tendency_Data_','Shibor%BE%F9%D6%B5%CA%FD%BE%DD')
}
filePath = sys.path[0] +'/files/'

startYear = 2006
thisYear = datetime.now().year
typeList = ('shibor','report','shiborAva')

def getFile(year,type):
    # date's format like Year YYYY
    _date = str(year)
    
    _url = 'http://www.shibor.org/shibor/web/html/downLoad.html?nameNew='+ fileDic[type][0] +_date+'.xls&nameOld='+fileDic[type][1]+_date+'.xls&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data'

    _headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch'
    }
    _fileName = filePath + fileDic[type][0] + _date + '.xls'
    print ('Download file to' + _fileName)
    return urlretrieve (_url, _fileName)
    # _req = requests.get(_url,headers = _headers)
    # if (_req.status_code == 200) : 
    #     return _req.content

def getFileList():
    
    # TODO 完善循环体
    for type in typeList:
        __nowYear = startYear
        while __nowYear <= thisYear:
            getFile(__nowYear,type)
            __nowYear += + 1


def toDB (
    type = 'shibor',
    year = startYear
    ):
    _DBName = 'shibor'
    #连接数据库
    _client = MongoClient('localhost',27017)
    # 删除数据库
    # _client.drop_database(_DBName)
    # 新建数据库
    _db = _client[_DBName]
    _dbTable = _db[type] #变量
    _data = xlrd.open_workbook(filePath + fileDic[type][0] + str(year) +'.xls')
    _table = _data.sheets()[0]
    _th = _table.row_values(0)
    _trs = _table.nrows
    _row = {}
    # th添加timestamp 为ID
    _th[0] = 'Date'
    _th.insert(0,'timestamp')
    
    # 添加数据到数据库
    for i in range(1,_trs):
        __tr = formatTr(_table.row_values(i))
        _row[i] = json.dumps(dict(zip(_th,__tr)))
        _row[i] = json.loads(_row[i])
        _dbTable.insert(_row[i])

# 返回 原行数据，并在第一位插入时间戳作为唯一识别id
def formatTr(
    tr= [] #行数据
    ):
    _arr = tr
    #时间转换
    _dateCell = xlrd.xldate.xldate_as_datetime(tr[0],0)
    _arr[0] = _dateCell.strftime('%Y-%m-%d')
    # 添加时间戳为ID 单位毫秒
    _arr.insert(0,int(int(datetime.timestamp(_dateCell))))
    return _arr

def fillDB():
    for type in typeList:
        for year in range(startYear,thisYear):
            toDB(type,year)
            print('Filling Date:Year|'+str(year) +',type|'+type )


if __name__ == "__main__":
    getFileList()

    # 灌入数据
    # fillDB()

    # cleanData()
    
