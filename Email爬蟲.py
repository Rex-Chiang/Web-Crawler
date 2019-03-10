import smtplib
from email.mime.text import MIMEText
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import time

def sendMail(subject,body):
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']='m41045@gmai.com'
    msg['To']='m41045@gmai.com'
    
    s=smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
    
soup1=soup(urlopen('https://isitchristmas.com/'),'html.parser')
while(soup1.find('a',{'id':'answer'}).attrs['title']=='不是'):
    print('It is not Christmas yet.')
    time.sleep(3600)
    soup1=soup(urlopen('https://isitchristmas.com/'),'html.parser')
sendMail('It is Chrismas!','Accordind to https://isitchristmas.com/')
#沒有SMTP SERVER