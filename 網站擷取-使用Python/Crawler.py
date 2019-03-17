import os
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup as soup

downloadDirectory='downloaded'#用以決定資料夾名稱
baseUrl='http://pythonscraping.com'
#以下函式用以正規化所有連結
def getAbsoluteURL(baseUrl,source):
    if source.startswith('http://www.'):
        url='http://'+source[11:]
    elif source.startswith('http://'):
        url=source
    elif source.startswith('www.'):
        url=source[4:]
        url='http://'+source
    else:
        url=baseUrl+'/'+source
    if baseUrl not in url:#排除外部連結
        return None
    return url 
#以下函式用以制定建立資料夾及操作檔案路徑
def getDownloadPath(baseUrl,absoluteUrl,downloadDirectory):
    path=absoluteUrl.replace('www.','')
    path=path.replace(baseUrl,'')
    path=downloadDirectory+path
    directory=os.path.dirname(path)#回傳路徑名稱用以建立資料夾
    if not os.path.exists(directory):#False=not True
        os.makedirs(directory)#建立所指定資料夾且料夾原先需不存在
    return path
html=urlopen('http://www.pythonscraping.com')
soup1=soup(html,'html.parser')
downloadList=soup1.find_all(src=True)


for i in downloadList:
    fileUrl=getAbsoluteURL(baseUrl,i['src'])
#    fileUrl=fileUrl.replace('?','')
    if fileUrl is not None:
        print(fileUrl)
        urlretrieve(fileUrl,getDownloadPath(baseUrl,fileUrl,downloadDirectory))
        #聯結有亂碼(?)不能run