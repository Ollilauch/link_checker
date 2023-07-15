from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
import requests
import os

os.environ['MOZ_HEADLESS'] = '1'
driver = webdriver.Firefox()
start_url = [URL]
driver.get(start_url)

#FIND AND CLICK BORLAND PRIVACY COOKIES
element_xpath = '/html/body/div[1]/div[4]/article/div/div/div[1]/div/div[1]/div/div/p[2]/a'
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
wait = WebDriverWait(driver, 30, ignored_exceptions=ignored_exceptions)

button = wait.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
driver.execute_script("arguments[0].click()", button)

#FIND ALL lINKS
videos_flex_wrapper_xpath = '/html/body/div[1]/div[4]/article/div/div'
title_xpath = '//a/p'

titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, title_xpath)))

elems = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//iframe')))
#elems = driver.find_elements(By.XPATH, "//a[@href]")

for i in range(len(titles)):
    r = requests.get(elems[i].get_attribute('src'))
    if "Video nicht verfügbar" in r.text or "Video unavailable" in r.text or "privat" in r.text == False:
        print(titles[i].get_attribute('innerHTML'), "+", elems[i].get_attribute('src'), ": 200")
    else:
        print(titles[i].get_attribute('innerHTML'), "+", elems[i].get_attribute('src'), ": 404")

#for elem in elems:
#    print(elem.get_attribute('src'))

#links = [elem.get_attribute('href') for elem in elems]
#links = driver.find_elements(By.CSS_SELECTOR, '[href]')
#print(links)

driver.close