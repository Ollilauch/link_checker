from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
import requests
import os
from datetime import date
from time import sleep
from threading import Thread
import sys
import json

start_url = 'https://eye-tracking-education.com/mehr-als-50-verschiedene-eye-tracking-anwendungen-auf-einen-blick' # URL where link_checker starts
finished = False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_link(link):
    r = requests.get(link)

    if (("Video nicht verfügbar" in r.text or "Video unavailable" in r.text or "Video ist privat" in r.text) or (r.status_code != 200)) == False:
        return f"{bcolors.OKGREEN}200{bcolors.ENDC}"
    elif (("Video nicht verfügbar" in r.text or "Video unavailable" in r.text or "Video ist privat" in r.text) or (r.status_code != 200)) == True:
        return f"{bcolors.FAIL}404{bcolors.ENDC}"
    else:
        return "Unknown"

#convert embedded to videocd 
def embedded_to_video(link):
    #https://www.youtube.com/watch?v=[id]
    #https://www.youtube-nocookie.com/embed/[id]?feature=oembed
    #https://www.youtube-nocookie.com/embed/[id]?start=[seconds]&feature=oembed

    if link.find("start=") == -1:
        video_id = (link.split("embed/")[1]).split("?feature=oembed")[0]
    elif link.find("start=") != -1:
        video_id = ((link.split("embed/")[1]).split("&feature=oembed")[0]).replace("?", "&")
    
    video_link = 'https://www.youtube.com/watch?v=[id]'.replace("[id]", video_id)

    return video_link

#def send_webhook(content: str):
    webhook_url = 'https://discord.com/api/webhooks/1130560129394298992/Vmh5fo-Ej9A98HUvFl9H62aYb5sGmbT7gnMAuDFBsTJDwGa4Ju-Y4JML07FlETh3ldsH'
    data = {    'content' : content
            }
    r = requests.post(webhook_url, data=json.dumps(data), headers={ 'content-type' : 'application/json'})

def check_youtube_videos():
    global finished
    content = ' '

    #START FIREFOX SESSION
    os.environ['MOZ_HEADLESS'] = '1'
    driver = webdriver.Firefox()
    if not driver:
        return 1
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

    if elems != None:
        finished = True
        sleep(2)

    max_len_titles = max(len(str(titles[l].get_attribute('innerHTML'))) for l in range(len(titles))) + 1
    max_len_elems = max(len(str(elems[l].get_attribute('src'))) for l in range(len(elems))) + 1

    for i in range(len(titles)):
        print('{}{}{}{}{}{}'.format("title: ", str(titles[i].get_attribute('innerHTML')).ljust(max_len_titles), " | ",
                                    embedded_to_video(str(elems[i].get_attribute('src'))).ljust(max_len_elems), " | status: ",
                                    check_link(embedded_to_video(elems[i].get_attribute('src')))))
        #print("-" * (len("title: ") + (max_len_titles) + len(" | ") + (max_len_elems) + len("status: Unknown")))
        content.join(f'"title: " {str(titles[i].get_attribute("innerHTML")).ljust(max_len_titles)} " | " {embedded_to_video(str(elems[i].get_attribute("src"))).ljust(max_len_elems)} " | status: " {check_link(embedded_to_video(elems[i].get_attribute("src")))} "\n"')

#    send_webhook(content)
    #for elem in elems:
    #    print(elem.get_attribute('src'))

    #links = [elem.get_attribute('href') for elem in elems]
    #links = driver.find_elements(By.CSS_SELECTOR, '[href]')
    #print(links)

    driver.close()
    driver.quit()

def print_loading():
    print("\nchecking links", end=' ')

    loading = True
    loading_string = '.' * 6
    i = 0

    while loading:
        for index, char in enumerate(loading_string):
            sys.stdout.write(char)
            sys.stdout.flush()
            sleep(1.0)
        
        index+=1
        sys.stdout.write("\b" * index + " " * index + "\b" * index)
        sys.stdout.flush()
        
        i+=1

        if i == 5 or finished == True:
            loading = False
        
    os.system('cls')

def start_thread(function, daemon):
    t = Thread(target=function, daemon=daemon)
    if t:
        t.start()
        return t
    else:
        return None

def main():
    os.system('cls')
    p1 = start_thread(print_loading, False)
    p2 = start_thread(check_youtube_videos, False)
    p2.join()

    print("\ndate of checking: ", date.today().strftime("%d/%m/%Y"), "\n")

if __name__ == '__main__':
    main()