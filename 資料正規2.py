from urllib.request import urlopen
import re
import string
from operator import itemgetter#用以排序 速度比lambda快

def cleanInput(input):
    cleanInput=[]
    input=re.sub('\n+',' ',input).lower()#lower()是為了大小寫不同但其實等同的元素所設置
    input=re.sub(' +',' ',input)
    input=re.sub('[[0-9]*\]','',input)
    input=bytes(input,'utf-8')
    input=input.decode('ascii','ignore').lower()
    input=input.split(' ')
    for item in input:
        item=item.strip(string.punctuation)#string.punctuation為標點符號
        if len(item)>1 or (item.lower()=='a' or item.lower()=='i'):
            cleanInput.append(item)
    return cleanInput
    
def getNgrams(input,n):
    output={}
    input=cleanInput(input)
    for i in range(len(input)-n+1):
        ngramTemp=' '.join(input[i:i+n])
        if ngramTemp not in output:
            output[ngramTemp]=0
        output[ngramTemp]+=1
    return output

content=str(urlopen('http://pythonscraping.com/files/inaugurationSpeech.txt').read(),'utf-8')

ngrams=getNgrams(content,2)
sortedNgrams=sorted(ngrams.items(),key=itemgetter(1),reverse=True)
print(sortedNgrams)