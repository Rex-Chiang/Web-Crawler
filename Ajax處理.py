from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import time
#driver=webdriver.Chrome('chromedriver.exe')#以Chrome開啟
driver=webdriver.PhantomJS(executable_path='/Users/user/Desktop/Crawler/phantomjs-2.1.1-windows/bin/phantomjs')
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')

try:
    element=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'loadedButton')))#暗示等待，等10秒直到EC發生
finally:
    print(driver.find_element_by_id('content').text)
#time.sleep(3)#明確等待，暫停3秒
#print(driver.find_element_by_css_selector('#content').text)

driver.close()