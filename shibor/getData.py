import requests


# get Data from URL 
# DEMO 

# http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_Shibor_Data_2016.xls&nameOld=Shibor%CA%FD%BE%DD2016.xls&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data

# http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_Shibor_Data_2017.xls&nameOld=Shibor%CA%FD%BE%DD2017.xls&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data

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

def makeUrl(date):
    # date's format like Year YYYY
    _url = 'http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_Shibor_Data_'+date+'.xls&nameOld=Shibor%CA%FD%BE%DD'+date+'.xls&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data'

    _headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch'
    }

    return requests.get(_url,headers = _headers)


print(makeUrl('2017'))