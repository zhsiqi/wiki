#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 01:29:52 2023

@author: zhangsiqi

test代码，可废弃
"""

#%% 【百家号】时间、保存html、作者、
from urllib.parse import unquote
from urllib.parse import urlparse
from os import path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
import selenium.common.exceptions
from tenacity import retry, retry_if_exception_type, wait_fixed
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.keys import Keys
import pandas as pd
import sqlite3 as sqlite
import datetime
import numpy as np


# conn= sqlite.connect('citation+code+resolve.sqlite')
# c = conn.cursor()

# 定义一个捕捉元素时出现StaleElementReferenceException异常后重试的装饰器
@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    #print('尝试获取元素',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),name)
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]


#% 爬虫循环开始
browser = webdriver.Chrome(executable_path = 'chromedriver')

#写成一个函数

# df = pd.read_csv('citation+code+resolve.csv')

# df['timestamp'] = 'NA'
# df['source'] = 'NA'

df = pd.read_csv('citation+baijiahao2.csv',index_col=('Unnamed: 0'))

x = 0
for index, row in df[7019:].iterrows():
    url = row['origin_url']
    if pd.isna(url) == False and '200' in row['status_code'] and row['domain'] == 'baijiahao.baidu.com':
        x += 1
        filename = (row['reference_title']+'-'+row['entry'] + str(row['reference_entryindex'])).replace('/', '_')+'.html'
        # 这个一定要把斜杠替换掉，否则后面识别成文件路径了
        browser.get(url.strip()) #selenium获取网页
        
        #一直等待到元素可见
        wait = WebDriverWait(browser, 50, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'V6XfG')))
        try:
            source = get_elements(browser, By.CLASS_NAME, '_7y5nA')
            timestamp = get_elements(browser, By.CLASS_NAME, '_10s4U')
        except NoSuchElementException:
            print('元素不存在',url)
            continue
        else:
            df.at[index,'source'] = source
            df.at[index,'timestamp'] = timestamp
        # with open(filename, "w", encoding='utf-8') as g: #selenium方式保存的html
        #     g.write(browser.page_source)
        #     g.close()
        print(index, row['reference_title'], url)
        
        time.sleep(2)

browser.quit()

df.to_csv("citation+baijiahao3.csv",index=False)


#写入sql
df = pd.read_csv('citation+baijiahao3.csv')

conn3= sqlite.connect('citation+baijia3.sqlite')
df.to_sql('citation+baijia3', conn3, index=True, if_exists = 'replace')
conn3.close()

#语音播报结束ß
import pyttsx3
engine = pyttsx3.init()  # 创建engine并初始化
engine.say("本程序运行结束")
engine.runAndWait()  # 等待语音播报完毕
        

# def get_news_elements(url, domain):

#     if row['domain'] = 'paper 乱七八糟':
#         time_element = 
#         source_element = 
#         save html
#     if row['domain'] = 'statis 乱七八糟':
#         elementmethod = 




        