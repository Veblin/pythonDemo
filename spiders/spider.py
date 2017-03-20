from urllib.request import urlopen
from bs4 import BeautifulSoup
from lxml import html
import re
import datetime
import random

#var 
pages = set ()
random.seed(datetime.datetime.now())
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
# get all internal links in the page
def getInternalLinks (bsObj,includeUrl):
    internalLinks = []
    for link in bsObj.find_all('a',href=re.compile('^(/|.*' + includeUrl + ')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

# get all external links in the page
def getExternalLinks(bsObj,excludeUrl):
    externalLinks = []
    # find http or www
    for link in bsObj.find_all('a',href=re.compile('^(http|https|www)((?!'+excludeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def splitAddress(address):
    addressParts = address.replace('http://','').split('/')
    return addressParts

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html,"html.parser")
    externalLinks = getExternalLinks(bsObj,splitAddress(startingPage)[0])

    if len(externalLinks) == 0:
        print('没有外链，继续查找ing')
        internalLinks = getInternalLinks(startingPage)
        return getNextExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0,len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print('随机外链是：'+ externalLink)
    followExternalOnly(externalLink)

# get all externalLink in internet
allExtLinks = set()
allIntLinks = set()
excludeLinks = ["http://www.circ.gov.cn/dig/advsearch.action?advrp=0","javascript:window.external.AddFavorite('http://www.circ.gov.cn', '中国保险监督管理委员会')"]

def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html,"html.parser")
    internalLinks = getInternalLinks(bsObj,splitAddress(siteUrl)[0])
    externalLinks = getExternalLinks(bsObj,splitAddress(siteUrl)[0])
    #获取不重复的外链
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print('外链新增：'+link)
    #获取不重复的内链
    for link in internalLinks:
        if link in excludeLinks:
            continue
        elif link not in allIntLinks:
            __link = formatLinks(link)
            allIntLinks.add(__link)
            print('内链新增：'+__link)
            # getAllExternalLinks(__link)


def formatLinks (link):
    _link = ''
    if link[0] == '/':
        _domain = 'http://www.circ.gov.cn'
        _link = _domain + link
    else:
        _link = linkscrapy

    return _link

if __name__ == "__main__":
    # _url = 'http://bdp.yiche.com'
    _url = 'http://www.circ.gov.cn/web/site0/tab5179/'
    # followExternalOnly('http://www.circ.gov.cn/web/site0/tab5179/')
    # followExternalOnly(_url)
    getAllExternalLinks(_url)
    print('allIntLinks:'+allIntLinks)
