from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
import pymysql

conn=pymysql.connect(host='127.0.0.1',port=3306,user='Rex',passwd='Rex3893090',db='mysql',charset='utf8')
cur=conn.cursor()#建立游標物件
cur.execute('USE wikipedia')#'.execute'等同在MySQL中鍵入
#以下定義函式用以確認頁面連結及頁面連結id是否已經存在
def pageScraped(url):
    cur.execute('SELECT * FROM pages WHERE url = %s',(url))
    if cur.rowcount==0:
        return False
    page=cur.fetchone()#將資料取進python，一次取出一筆：fetchone()
    
    cur.execute('SELECT * FROM links WHERE fromPageId = %s',(int(page[0])))
    if cur.rowcount==0:
        return False
    return True
#以下定義函式用以確認頁面連結是否已經存在，若是則回傳該頁面連結id，反之則立即插入(新增)該頁面連結並回傳其頁面連結id
def insertPageIfNotExists(url):
    cur.execute('SELECT * FROM pages WHERE url = %s',(url))
    if cur.rowcount==0:
        cur.execute('INSERT INTO pages (url) VALUES (%s)',(url))
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0]
#以下定義函式用以確認頁面連結id是否已經存在，若否則立即插入(新增)代入函式的頁面連結id
def insertLink(fromPageId,toPageId):
    cur.execute('SELECT * FROM links WHERE fromPageId = %s AND toPageId = %s',(int(fromPageId),int(toPageId)))
    if cur.rowcount==0:
        cur.execute('INSERT INTO links (fromPageId,toPageId) VALUES (%s,%s)',(int(fromPageId),int(toPageId)))
        conn.commit()

def getLinks(pageUrl,recursionLevel):
#    global pages
    if recursionLevel>4:
        return
    pageId=insertPageIfNotExists(pageUrl)
    html=urlopen('https://en.wikipedia.org'+pageUrl)
    soup1=soup(html,'html.parser')
    for link in soup1.find_all('a',href=re.compile('^(/wiki/)((?!:).)*$')):
        insertLink(pageId,insertPageIfNotExists(link.attrs['href']))#插入(新增)頁面連結id
        if not pageScraped(link.attrs['href']):#not False = True
            newPage=link.attrs['href']#再以newPage連往下一個頁面
            print(newPage)
            getLinks(newPage,recursionLevel+1)#有未記錄過的連結就取它繼續連結下去
        else:
            print('Skipping:',link.attrs['href'],'found on',pageUrl)
getLinks('/wiki/Kevin_Bacon',0)
cur.close()
conn.close()