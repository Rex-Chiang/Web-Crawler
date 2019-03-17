from selenium import webdriver
from bs4 import BeautifulSoup as soup
import time
import re
import os

url = 'https://www.ptt.cc/bbs'
TABLES = str(input('欲選看版 : '))

####################################只設置userAgent#################################
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#dcap = dict(DesiredCapabilities.PHANTOMJS)
#dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
#driver=webdriver.PhantomJS(executable_path='/home/rex/桌面/GliaCloud/phantomjs-2.1.1-linux-x86_64/bin/phantomjs', desired_capabilities = dcap)
####################################################################################

#####################################設置完整headers################################
headers ={
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'cookie':'__cfduid=d45c36e6b90991d9c214ae9a7f7542b391523876817; _ga=GA1.2.209739768.1523876819; _gid=GA1.2.480346404.1552660312; _gat=1'
        }

for key in headers:
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
    
driver = webdriver.PhantomJS(executable_path='/home/rex/桌面/GliaCloud/phantomjs-2.1.1-linux-x86_64/bin/phantomjs', service_log_path = os.path.devnull)
####################################################################################

#driver = webdriver.Chrome(executable_path='/usr/local/share/chromedriver')
#cookie = ';'.join(['{}={}'.format(item.get('name'),item.get('value')) for item in driver.get_cookies()])

driver.get(url)
# 依照所輸入看板名稱進入該看板
driver.find_element_by_xpath("//div/a/div[text()='"+TABLES+"']").click()


def RE(content):
    # " . "能匹配除了換行符號以外的所有字元，若想包含換行字元，使用 re.DOTALL進入單行模式
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
    # 若文章已被刪除或是內容不存在則跳過
    if article[i].find('a') == None:
        pass
    else:
        
        driver.find_element_by_xpath("//div/a[text()='"+article[i].text.replace('\n','')+"']").click()    
        soup1 = soup(driver.page_source,'html.parser')
        # content 包含標題、內文、回覆，需使用正則表達式取出主要文章
        content = soup1.find('div', attrs = {'id':'main-content'}).text
        
        time.sleep(1)
        # 返回上一頁（文章選擇頁）
        driver.back()
        
        time.sleep(1)
        
        TABLE, AUTHOR, TITLE, DATE, CONTENT = RE(content)
        
        print("----------------------------------------------------------------------")
        # 若文章為公告類型，僅列出連結
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


