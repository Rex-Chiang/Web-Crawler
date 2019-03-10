from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
#from collections import OrderedDict
import re
import string

def cleanInput(input):
    cleanInput=[]
    input=re.sub('\n+',' ',input)
    input=re.sub(' +',' ',input)
    input=re.sub('[[0-9]*\]','',input)
    input=bytes(input,'utf-8')
    input=input.decode('ascii','ignore')
    input=input.strip(' ')#為了消除空白單獨一項的情況
    input=input.split(' ')
    for item in input:
        item=item.strip(string.punctuation)#string.punctuation為標點符號
        if len(item)>1 or (item.lower()=='a' or item.lower()=='i'):
            cleanInput.append(item)
    return cleanInput
    
def getNgrams(input,n):
    output=[]
    input=cleanInput(input)
    
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

html=urlopen('https://en.wikipedia.org/wiki/Python_(programming_language)')
soup1=soup(html.read(),'html.parser')
content=soup1.find('div',{'id':'mw-content-text'}).get_text()

ngrams=getNgrams(content,2)

a=set()
b=[]
for i in ngrams:#元素須為同一資料型態才能比較
    a.add(str(i))
    b.append(str(i))
s={w:b.count(w) for w in a}#製作以元素出現次數為值的字典
s1=sorted(s.items(),key=lambda x:x[1],reverse=True)#按照出現次數大小排列其中items()以tuple呼叫字典中的鍵值
print(ngrams)
print('2-grams count is:',str(len(ngrams)))