from selenium import webdriver 
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException
import time

def waitForLoad(driver):
    elem=driver.find_element_by_tag_name('div')
    count=0
    while True:
        count+=1
        print(count)
        if count>10:#若tag是前後頁面都有的標籤則由此return
            print('Timeing out after 10 seconds and returning')
            return
        
        time.sleep(.5)#每半秒try一次
        try:#若tag是只有前頁面有則由此return
            elem==driver.find_element_by_tag_name('div')
            
        except NoSuchElementException:#書上用StaleElementReferenceException但無法
            return
    
driver=webdriver.PhantomJS(executable_path='/Users/user/Desktop/Crawler/phantomjs-2.1.1-windows/bin/phantomjs')
driver.get('http://pythonscraping.com/pages/javascript/redirectDemo1.html')

waitForLoad(driver)
print(driver.page_source)    

driver.close()