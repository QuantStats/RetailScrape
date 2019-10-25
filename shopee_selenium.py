import os
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(executable_path=r'(your_path_here)\geckodriver.exe')
wait_sec = 30
en_button_xpath = '/html/body/div[2]/div[1]/div[1]/div/div[3]/button[1]'
price_class = '_341bF0'

url_front = 'https://shopee.com.my/Watches-cat.159?page='
url_back = '&sortBy=pop'

for i in range(0,6):

    url = url_front+str(i)+url_back
    driver.get(url)

    #click the english button if it is the home page of the subsection
    if i == 0:   
        WebDriverWait(driver, wait_sec).until(
            EC.element_to_be_clickable((By.XPATH, en_button_xpath))
           )
        driver.find_element_by_xpath(en_button_xpath).click()

    #implement two waits to be safe
    WebDriverWait(driver, wait_sec).until(
        EC.presence_of_element_located((By.CLASS_NAME, price_class))
        )
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    WebDriverWait(driver, wait_sec).until(
        EC.presence_of_element_located((By.CLASS_NAME, price_class))
        )


    #main scrape
    bs = BeautifulSoup(driver.page_source, 'lxml')

    temp = bs.find_all(type='application/ld+json')

    le = len(temp)

    it = iter(range(le))

    ls = {str(next(it)):json.loads(temp[_].text) for _ in range(le) if 'offers' in temp[_].text}


    #write to json
    with open('page'+str(i)+'.json', 'w', encoding='utf-8') as outfile:
        json.dump(ls, outfile)
        outfile.write('\n')

#terminate the browser
os.system('tskill plugin-container')
driver.close()
driver.quit()
