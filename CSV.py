import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

html=urlopen('https://en.wikipedia.org/wiki/Comparison_of_text_editors')
soup1=soup(html,'html.parser')
#表格在'class':'wikitable'內
table=soup1.find_all('table',{'class':'wikitable'})[0]
rows=table.find_all('tr')
#以下寫入動作都需在with內
with open('C:/Users/Rex/Desktop/Crawler/table.csv','wt',newline='',encoding='utf-8') as csvFile:
    writer=csv.writer(csvFile)
    
    try:
        for row in rows:
            csvRow=[]
            for i in row.find_all(['td','th']):#有'td'或'th'都找
                csvRow.append(i.get_text())
            writer.writerow(csvRow)
    finally:
        csvFile.close()