#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 20:13:20 2023

@author: zhangsiqi
"""

import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.by import By

chrome_options = uc.ChromeOptions()

driver = uc.Chrome(
    options=chrome_options,
    seleniumwire_options={}
)

url = 'http://www.nhc.gov.cn/xcs/yqtb/202109/a24a8dca26c343e0a2a96461539f18b8.shtml'
driver.get(url)

with open('test1.html', "w", encoding='utf-8') as g: #selenium方式保存的html
    g.write(driver.page_source)
    g.close()
# 定义一个捕捉元素时出现StaleElementReferenceException异常后重试的装饰器

def get_elements(driver, method, name):
    targets = driver.find_elements(method, name)
    #print('获取元素成功')
    return [i.text for i in targets]

a = get_elements(driver, By.CSS_SELECTOR, 'body > div.w1024.mb50 > div.list > div.source > span')
print(a)

#%%

import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import time

driver = uc.Chrome()
driver.get('http://www.nhc.gov.cn/xcs/yqtb/202109/a24a8dca26c343e0a2a96461539f18b8.shtml')
wait = WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'source')))
time.sleep(10)
targets = driver.find_elements(By.CLASS_NAME, 'source')

for i in targets:
    print(i.text)

driver.quit()


from htmldate import find_date
find_date('http://paper.people.com.cn/rmrb/html/2022-06/09/nw.D110000renmrb_20220609_3-09.htm')
#find_date('https://world.huanqiu.com/article/9CaKrnKiVec')
# find_date('http://www.nhc.gov.cn/xcs/yqtb/202109/a24a8dca26c343e0a2a96461539f18b8.shtml')
