from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
url='https://tw.yahoo.com/'
html=urlopen(url)
soup=soup(html.read(),'html.parser')
tag=soup.head.title
def test():
    try:
        html=urlopen(url)
    except HTTPError as e:#未知
        return 0
    try:
        tag=soup.head.title
    except AttributeError as e:#當head不存在時
        return 1
    else:
        if tag==None:#當title不存在時
            return 2
        else:
            pass
    return tag
if test()==0:
    print('httpwrong')
elif test()==1:
    print('wrong')
elif test()==3:
    print('錯誤')
else:
    print(test())