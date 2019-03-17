from urllib.request import urlopen
from random import randint

def wordListSum(wordList):
    sum=0
    for word,value in wordList.items():
        sum+=value#value的總和也就是各個單詞接續次數的總數
    return sum

def retrieveRandomWord(wordList):
    randIndex=randint(1,wordListSum(wordList))
    for word,value in wordList.items():#依照這個運算會是接續次數最高的單詞回傳機率最大
        randIndex-=value
        if randIndex<=0:
            return word
        
def buildWordDict(text):
    text=text.replace('\n'," ")
    text=text.replace('\"',"")
    punctuation=[',','.',':',';']
    for symbol in punctuation:#使標點符號獨立出來為一元素
        text=text.replace(symbol,''+symbol+'')
    words=text.split(' ')#此時words已是串列型態
    words=[word for word in words if word != '']#使用串列生成式為了利用if功能重製串列
    
    wordDict={}
    for i in range(1,len(words)):
        if words[i-1] not in wordDict:
            wordDict[words[i-1]]={}#建立二維字典
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
            wordDict[words[i-1]][words[i]] += 1
    return wordDict

text=str(urlopen('http://pythonscraping.com/files/inaugurationSpeech.txt').read(),'utf-8')
wordDict=buildWordDict(text)

length=100
chain=''
currentWord='I'
for i in range(0,length):
    chain+=currentWord+' '
    currentWord=retrieveRandomWord(wordDict[currentWord])
print(chain)