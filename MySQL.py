from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
import datetime
import random
import pymysql

conn=pymysql.connect(host='127.0.0.1',port=3306,user='Rex',passwd='Rex3893090',db='mysql',charset='utf8')
cur=conn.cursor()#建立游標物件
cur.execute('USE scraping')#'.execute'等同在MySQL中鍵入

random.seed(datetime.datetime.now())


#以下定義函式代入title,content用以INSERT進MySQL
def store(title,content):
    cur.execute('INSERT INTO pages (title,content)'+' VALUES(%s,%s)',(title,content))
    cur.connection.commit()#連線將資訊傳給資料庫
    
def getLinks(url):
    html=urlopen('https://en.wikipedia.org'+url)
    soup1=soup(html.read(),'html.parser')
    title=soup1.find('h1').get_text()
    content=soup1.find('div',{'id':'mw-content-text'}).find('p').get_text()
    store(title,content)
    return soup1.find('div',{'id':'bodyContent'}).find_all('a',href=re.compile('^(/wiki/)((?!:).)*$'))
    
links= getLinks('/wiki/Kevin_Bacon')#設定起始網頁
    
try:
    while(len(links)>0):
        newArticle=links[random.randint(0,len(links)-1)].attrs['href']
        print(newArticle)
        links=getLinks(newArticle)
finally:
    cur.close()
    conn.close()