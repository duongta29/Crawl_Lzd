### FINAL CODE   ###

from selenium  import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import threading
from queue import Queue
import queue
import csv
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
import json
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920x1080")
options.add_argument("--incognito")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#### GLOBAL INIT #####

n = 11
threads = []
link_O = []
# with open('data_2.csv', mode='w', newline='', encoding='utf-8-sig' ) as file:
#     writer = csv.writer(file)
    
#     # Viết tiêu đề của các cột vào file CSV
#     writer.writerow(['link' , 'title' , 'price' , 'discount','sale_rating','ship_on_time','chat_respone', 'score' , 'star', 'count'])
results = []

#### DEFINE LOGIC #####

def openMultiBrowsers(n):
    drivers = []
    for i in range(n):
        driver = webdriver.Chrome(executable_path ='chromedriver.exe')
        drivers.append(driver)
    return drivers


def getData(driver, link_que):
    c = 0
    while c < 50:
        try:
            link = link_que.get(block=False) 
        except queue.Empty: 
            break
    # driver.maximize_window()
        driver.get(link)
        sleep(3)
        try:
            elem = driver.find_element('xpath' , "/html/body/div[7]/div/div[2]/div/span/i")
            elem.click()
        except :
            pass
        try:
            elem = driver.find_element('xpath' , "/html/body/div[2]/div/h3")
            print("Sorry! This product is no longer available ")
            with open("data_del.txt", "a") as file:
                file.write(link + "\n")
            continue
        except :
            pass
        try:
            elem = driver.find_element("xpath", "/html/body/div[7]/div[2]/div")
            elem.click()
            print("Error ! Please wait in 15 minutes")
            driver.close()
            sleep(15*60)
            driver = webdriver.Chrome(executable_path ='chromedriver.exe')
            continue
        except:
            pass
        try:
            elem = driver.find_element(By.LINK_TEXT, '关闭')
            elem.click()
            print("Error ! Please wait in 15 minutes")
            driver.close()
            sleep(15*60)
            driver = webdriver.Chrome(executable_path ='chromedriver.exe')
            continue
        except:
            pass
        
        elem_body = driver.find_element(By.TAG_NAME ,"body")
        elem_body.send_keys(Keys.PAGE_DOWN)
        sleep(6)
        try:
            elems_count = driver.find_element('xpath' , "/html/body/div[4]/div/div[3]/div[2]/div/div[1]/div[5]/div[1]/div/div/a")
            count = elems_count.text
            if (count == 'Không có đánh giá') or (count == '1 đánh giá'):
                with open("data_del.txt", "a") as file:
                    file.write(link + "\n")
                    continue
            elems_title = driver.find_element(By.CSS_SELECTOR , ".pdp-mod-product-badge-title")
            title = elems_title.text 
                    
            elems_price = driver.find_element(By.CSS_SELECTOR , ".pdp-product-price ")
            price = elems_price.text.split('\n')[0]
            try:
                elems_discount = driver.find_element(By.CSS_SELECTOR , ".pdp-product-price__discount ")
                discount = elems_discount.text 
            except:
                discount = 0
                
            elems_salerating = driver.find_element("xpath" , "/html/body/div[4]/div/div[3]/div[2]/div/div[2]/div[6]/div/div[2]/div[1]/div[2]")
            sale_rating = elems_salerating.text
                       
            elems_ship_on_time = driver.find_elements(By.CSS_SELECTOR , ".seller-info-value ")
            ship_on_time = elems_ship_on_time[0].text
            chat_respone = elems_ship_on_time[1].text
                
            try:
                elems_score = driver.find_element(By.CSS_SELECTOR , ".summary .score")
                score = elems_score.text
            except:
                with open("data_del.txt", "a") as file:
                    file.write(link + "\n")
                continue
            elems_star = driver.find_element(By.CSS_SELECTOR , ".detail")
            star = elems_star.text.split('\n')
                       
            elems_count = driver.find_element('xpath' , "/html/body/div[4]/div/div[3]/div[2]/div/div[1]/div[5]/div[1]/div/div/a")
            count = elems_count.text
        except:
            continue
        
        result = { 'link': link,'title': title,'price': price,'discount': discount,'sale_rating': sale_rating ,'ship_on_time': ship_on_time,'chat_respone': chat_respone ,'score': score,'star': star,'count': count }
        results.append(result)
        
        print(result)
        
        with open('data_2.csv', 'a', newline='', encoding='utf-8-sig' ) as f:
            writer = csv.DictWriter(f, fieldnames=['link', 'title','price', 'discount','sale_rating', 'ship_on_time', 'chat_respone', 'score', 'star', 'count'])
            writer.writerow(result) 
        with open("data.txt", "a") as file:
            file.write(link + "\n")
            print("Done ADD")
    c =+ 1
    if c == 50:
        driver.quit()
        sleep(300)
        driver = webdriver.Chrome(executable_path ='chromedriver.exe')
    

    
          
    driver.close()
 
    
def new_list(link1, link2):
    for item1 in link1:
        for item2 in link2:
            if item1 == item2 :
                link2.remove(item2)
    return link2
        


def runInParallel(drivers_rx, link_que):
    for driver in drivers_rx:  
        print("-------Running parallel---------")
        t1 = threading.Thread(target=getData, args=(driver, link_que))
        t1.start()
    

def main():
    link_que = queue.Queue()
    with open('my_list_shuffled.txt', 'r') as file:
        link_li = [line.strip() for line in file.readlines()]
    with open('data.txt', 'r') as file:
        link_done = [line.strip() for line in file.readlines()]
    with open('data_del.txt', 'r') as file:
        link_del = [line.strip() for line in file.readlines()]
    
    for link in link_li:
        if link in link_done:
            continue
        elif link in link_del:
            continue
        else:
            link_que.put(link)
    # Thêm url vào hàng đợi
    # for link in link_li:
    #     link_que.put(link)

    drivers_r1 = openMultiBrowsers(n)
    sleep(5)
    runInParallel(drivers_r1, link_que) 
    sleep(10)
    
# ===========================Run/Execute=======================================


if __name__ == '__main__':
    main()

import json
with open("datalist0.txt", "w") as file:
    json.dump(link_O, file)    
    
    
    
    
    

