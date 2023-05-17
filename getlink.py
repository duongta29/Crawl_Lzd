from selenium import webdriver
from time import sleep
import random, time
import pyautogui
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920x1080")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(chrome_options=options,executable_path ='chromedriver.exe')
driver.get('https://www.lazada.vn')

action = ActionChains(driver)
action.send_keys(Keys.PAGE_DOWN).perform()

elem = driver.find_element("xpath", "/html/body/div[6]/section/div[1]/div/div[2]/ul/li[1]/a")
elem.click()
links= []
links_1= []
links_2 = []
elem_1 =  driver.find_elements(By.CSS_SELECTOR, ".multi-col-list")
for elem1 in elem_1:
    elem_link = elem1.find_elements(By.TAG_NAME, 'a')
    for elem in elem_link:
        links.append(elem.get_attribute('href'))
        
for link in links:
    driver.get(link)
    elem_2 =  driver.find_elements(By.CSS_SELECTOR, ".multi-col-list")
    for elem2 in elem_2:
        elem_link1 = elem2.find_elements(By.TAG_NAME, 'a')
        for elem in elem_link1:
            links_1.append(elem.get_attribute('href'))
            
with open('my_file.txt', 'w') as file:
    for item in links_1:
        file.write(str(item) + '\n')
# j = len(links_1) - 1500
j = 203763
links_11 = links_1[-j:]
for link1 in links_11:
    j-=1
    links_2 = list(set(links_2))
    driver.get(link1)
    elem_3 =  driver.find_elements(By.CSS_SELECTOR, ".one-col-list")
    for elem3 in elem_3:
        elem_link2 = elem3.find_elements(By.TAG_NAME, 'a')
        for elem in elem_link2:
            links_2.append(elem.get_attribute('href'))
sleep(60*10)
# link1 đang chạy đến link_1[1187]
with open('my_list.txt', 'w') as file:
    for item in links_2:
        file.write(str(item) + '\n')
        
index = links_1.index('https://www.lazada.vn/directory/categories/portable+speakers+accessories/500')
print(index)
