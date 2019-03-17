from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import requests
import json
import datetime
import random
import re

random.seed(datetime.datetime.now())
#以下定義函式用以開啟wiki網頁並回傳其中所有文章頁面連結(list)
def getlinks(url):
    html=urlopen('https://en.wikipedia.org'+url)
    soup1=soup(html,'html.parser')
    return soup1.find('div',{'id':'bodyContent'}).find_all('a',href=re.compile('^(/wiki)((?!:).)*$'))
#以下定義函式用以找出文章頁面歷史編輯紀錄中用ip位置登入的用戶並回傳他們的ip(list)
def getHistoryIP(url):
    url=url.replace('/wiki/','')
    historyurl='https://zh.wikipedia.org/w/index.php?title='+url+'&action=history'
    print('history url is',historyurl)
    html=requests.get(historyurl)
    soup1=soup(html.text,'html.parser')
    #發現用ip位置登入的都在'class':'mw-userlink mw-anonuserlink'中
    ipaddresses=soup1.find_all('a',{'class':'mw-userlink mw-anonuserlink'})
    addresslist=set()
    for i in ipaddresses:
        addresslist.add(i.get_text())
    return addresslist
#以下定義函式用以透過API請求得到一json格式回傳並取出國家位置(country_code)
def getcountry(ipaddress):
    try:
        response=urlopen('https://freegeoip.net/json/'+ipaddress).read().decode('utf-8')
    except HTTPError:
        return None
    responsejson=json.loads(response)
    return responsejson.get('country_code')
#以下指定起始頁面
links=getlinks('/wiki/Python_(programming_language)')

while(len(links)>0):
    for link in links:
        print('----------------------')
        historyips=getHistoryIP(link.attrs['href'])
        for historyip in historyips:
            country=getcountry(historyip)
            if country is not None:
                print(historyip,'is from',country)
    #以下隨機指定下一個頁面
    newlink=links[random.randint(0,len(links)-1)].attrs['href']
    links=getlinks(newlink)