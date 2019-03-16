from selenium import webdriver
import requests
import time
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

url = 'https://www.ptt.cc/bbs'
TABLES = str(input('欲選看版 : '))
#html = urlopen(url)
#soup1=soup(html,'html.parser')

#print(soup1)
#print("****************************************************")

driver=webdriver.PhantomJS(executable_path='/home/rex/桌面/GliaCloud/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
#driver = webdriver.Chrome(executable_path='/usr/local/share/chromedriver')
driver.get(url)

driver.find_element_by_xpath("//div/a/div[text()='"+TABLES+"']").click()

#time.sleep(2)


headers = {
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'cookie': '__cfduid=d45c36e6b90991d9c214ae9a7f7542b391523876817; _ga=GA1.2.209739768.1523876819; _gid=GA1.2.480346404.1552660312; _gat=1'
        }


def RE(content):
    TABLEre = re.compile(r"(看板\w*)(標)")
    AUTHORre = re.compile(r"(作者\w*\s)")
    TITLEre = re.compile(r"(標題.*)(時間)")
    DATEre = re.compile(r"(時間.*)")
    CONTENTre = re.compile(r"(時間[\w| |:]*)(.*)(--)",re.DOTALL)
    
    TABLE = TABLEre.search(content)
    AUTHOR = AUTHORre.search(content)
    TITLE = TITLEre.search(content)
    DATE = DATEre.search(content)
    CONTENT = CONTENTre.search(content)
    
    return TABLE, AUTHOR, TITLE, DATE, CONTENT


#html=requests.get(url,headers = headers)
soup1=soup(driver.page_source,'html.parser')

article = soup1.find_all('div', attrs={'class':'title'})
#date = soup1.find_all('div', attrs={'class':'date'})
#author = soup1.find_all('div', attrs={'class':'author'})

for i in range(0, len(article)):
    
    if article[i].find('a') == None:
        pass
    else:
        
        driver.find_element_by_xpath("//div/a[text()='"+article[i].text.replace('\n','')+"']").click()    
        soup1 = soup(driver.page_source,'html.parser')
        content = soup1.find('div', attrs = {'id':'main-content'}).text
        
        time.sleep(1)
        
        driver.back()
        
        time.sleep(1)
        
        TABLE, AUTHOR, TITLE, DATE, CONTENT = RE(content)
        
        print("----------------------------------------------------------------------")
        
        if TITLE.group(1).find("標題[公告]") >= 0:
            print(TABLE.group(1))        
            print(AUTHOR.group())        
            print(TITLE.group(1))
            print(DATE.group())
            print("連結 : ", article[i].find('a').attrs['href'])
        
        else:
            print(TABLE.group(1))        
            print(AUTHOR.group())        
            print(TITLE.group(1))
            print(DATE.group())
            print("*******************************< 內文 >*******************************\n", CONTENT.group(2))
        
        #print("\nDATE : ", date[i].text, ",",
        #      "AUTHOR : ", author[i].text,
        #      "\nTITLE : ", article[i].text.replace('\n',''))
        #print("ARTICLE : ", content)#article[i].find('a').attrs['href'])

driver.quit()

