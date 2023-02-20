#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 20:13:20 2023

@author: zhangsiqi
抓取卫健委网站文章的时间和html
"""
from os import path
import os
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import selenium.common.exceptions
import time
import pandas as pd
import sqlite3 as sqlite
import datetime
import numpy as np
import re

# chrome_options = uc.ChromeOptions()

# driver = uc.Chrome(
#     options=chrome_options,
#     seleniumwire_options={}
# )

# 定义一个捕捉元素时出现StaleElementReferenceException异常后重试的装饰器
@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]


def get_html(filepath, browser, title, entry, entryindex):
    os.chdir(filepath)
    filename = (title+'-'+ entry + str(entryindex)).replace('/', '_') +'.html'
    # remember to replace '/' since it will be recognized as file path instead of file name
    if not path.exists(filename):
        with open(filename, "w", encoding='utf-8') as g: #selenium方式保存的html
            g.write(browser.page_source)
            g.close()


driver = uc.Chrome()
os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0124补充卫健委等时间')
df = pd.read_csv('citation+news-nhc-4.csv',index_col=('Unnamed: 0'))

#手动替换错误URL值
df = df.replace({'origin_url':'http://d6181c548b615eb9441.shtmlwww.nhc.gov.cn/xcs/yqfkdt/202204/311452e077aa4'},\
                'http://www.nhc.gov.cn/jkj/s7915/202204/311452e077aa4d6181c548b615eb9441.shtml')
df = df.replace({'origin_url':'http://www.nhc.gov.cn/xcs/yqfkdt/202204/0a1ca5213df34b4aa6fa65001f15906b.shtml'},\
                'http://www.nhc.gov.cn/xcs/yqtb/202204/de4ae15047034dbdb3b183165679cca6.shtml')   
    
for index, row in df.iterrows():
    url = row['origin_url']
    dmname = row['domain']
    title = row['reference_title']
    #if pd.isna(url) == False and "nhc.gov" in dmname and row['timestamp'] == '超时错误':#修正错误20230125
    if pd.isna(url) == False and "nhc.gov" in dmname and pd.isna(row['timestamp']) == True:#卫健委
        df.at[index,'source'] = '卫健委官网'
        qks = ['最新', '截至'] #用标题确定正确的URL
        if any(qk in title for qk in qks) and '/xcs/yqfkdt/' in url:
            url = re.sub('/xcs/yqfkdt/', '/xcs/yqtb/', url)
            df.at[index,'origin_url'] = url #替换原始url为正确的
        elif '疫苗接种情' in title and '/xcs/yqfkdt/' in url:
            if index < 5917: #卫健委的URL规则在20221109号又变了，在表中的索引是5917
                url = re.sub('/xcs/yqfkdt/', '/jkj/s7915/', url)
                df.at[index,'origin_url'] = url #替换原始url为正确的
            else:
                url = re.sub('/xcs/yqfkdt/', '/xcs/yqjzqk/', url)
                df.at[index,'origin_url'] = url #替换原始url为正确的
        try:
            driver.get(url.strip())
            wait = WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'source')))
            time.sleep(10) #感觉这个等待和停顿的时间是不是短了
            timestamp = get_elements(driver, By.CLASS_NAME, 'source')
        except TimeoutException:
            df.at[index,'timestamp'] = '超时错误'
            print(index, '超时',url)
            continue
        except NoSuchElementException:
            df.at[index,'timestamp'] = '元素不存在错误'
            print(index, '元素不存在',url)
            continue
        else:
            ti = re.search(r'(?P<time>20\S+)',timestamp[0])
            df.at[index,'timestamp'] = ti.groupdict()['time']
        
        filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/卫健委网站'
        get_html(filepath, driver, row['reference_title'], row['entry'], row['reference_entryindex'])
        print(index, row['reference_title'], url)
        time.sleep(1.5)


driver.quit()

#写入csv & sql
os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0124补充卫健委等时间')

df.to_csv("citation+news-nhc-5.csv", index=True)

conn3= sqlite.connect('citation+news-nhc-5.sqlite')
df.to_sql('citation+news', conn3, index=True, if_exists = 'replace')
conn3.close()

#语音播报结束
import pyttsx3
engine = pyttsx3.init()  # 创建engine并初始化
engine.say("本程序运行结束")
engine.runAndWait()  # 等待语音播报完毕

#%%

import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import time

driver = uc.Chrome()
# url = 'http://www.nhc.gov.cn/xcs/yqtb/202109/a24a8dca26c343e0a2a96461539f18b8.shtml'
# driver.get(url)
# wait = WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'source')))
# time.sleep(10)
# targets = driver.find_elements(By.CLASS_NAME, 'source')

# huanqiu 
# url = 'https://world.huanqiu.com/article/9CaKrnKiVec'
# driver.get(url)
# #wait = WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'date')))
# time.sleep(30)
# targets = driver.find_elements(By.CLASS_NAME, 'date')

# 163
url = 'https://news.163.com/photoview/00AP0001/2300573.html?baike#p=EAS7DK1T00AP0001NOS'
driver.get(url)
wait = WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.gallery > div.top.cf > div.headline > span')))
time.sleep(30)
targets = driver.find_elements(By.CSS_SELECTOR, 'body > div.gallery > div.top.cf > div.headline > span')

for i in targets:
    print('时间', i.text)

with open('filename2.html', "w", encoding='utf-8') as g: #selenium方式保存的html
    g.write(driver.page_source)
    g.close()

driver.quit()

#%%

from htmldate import find_date
url = 'https://news.163.com/photoview/00AP0001/2300573.html?baike#p=EAS7DK1T00AP0001NOS'
url = 'https://news.163.com/photoview/00AO0001/2290927.html#p=DBO0DIBQ00AO0001NOS'
find_date(url)
# 'http://paper.people.com.cn/rmrb/html/2022-06/09/nw.D110000renmrb_20220609_3-09.htm' 不准确
#find_date('https://world.huanqiu.com/article/9CaKrnKiVec')
# find_date('http://www.nhc.gov.cn/xcs/yqtb/202109/a24a8dca26c343e0a2a96461539f18b8.shtml')
