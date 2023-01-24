#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 01:29:52 2023

@author: zhangsiqi
"""

#%% 100条以上的渠道的新闻的时间、作者、html
from os import path
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
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
import re

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

#% 爬虫循环开始
browser = webdriver.Chrome(executable_path = 'chromedriver')

df = pd.read_csv('citation+code+resolve.csv')

df['timestamp'] = 'NA'
df['source'] = 'NA'


for index, row in df.iterrows():
    url = row['origin_url']
    dmname = row['domain']
    if pd.isna(url) == False and row['url_time'] == "['None', 'None', 'None']" :
        #百度百家号
        if dmname == 'baijiahao.baidu.com' and '200' in row['status_code']:
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'V6XfG')))
                source = get_elements(browser, By.CLASS_NAME, '_7y5nA')
                timestamp = get_elements(browser, By.CLASS_NAME, '_10s4U')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                df.at[index,'source'] = source[0]
                df.at[index,'timestamp'] = timestamp[0]
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/百度百家号新闻'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        #网易163    
        elif dmname == 'www.163.com' and '200' in row['status_code']:
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'post_info')))
                info = get_elements(browser, By.CLASS_NAME, 'post_info')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                df.at[index,'timestamp'] = info[0][0:19]
                m = re.search(r'来源: (?P<author>\S*)\n', info[0])
                df.at[index,'source'] = m.groupdict()['author']
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/网易新闻'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        #央视新闻客户端
        elif dmname == 'content-static.cctvnews.cctv.com' and '200' in row['status_code']:
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'media-publish-time')))
                timestamp = get_elements(browser, By.CLASS_NAME, 'media-publish-time')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                df.at[index,'source'] = '央视新闻客户端'
                df.at[index,'timestamp'] = timestamp[0]
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/央视新闻客户端'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        #界面新闻
        elif dmname == 'www.jiemian.com' and '200' in row['status_code']:
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-article-publish-time]')))
                ti = get_elements(browser, By.CSS_SELECTOR, 'span[data-article-publish-time]')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                df.at[index,'source'] = '界面新闻' #界面在文章信息栏目没有准确标注信源，只标注了“界面新闻”
                df.at[index,'timestamp'] = ti[0]
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/界面新闻'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        #凤凰网
        elif dmname == 'news.ifeng.com' and '200' in row['status_code']:
            if not url == 'https://news.ifeng.com/' and 'https://news.ifeng.com/c/404' not in url:
                try:
                    browser.get(url.strip())
                    wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'ss01')))
                    timestamp = get_elements(browser, By.CLASS_NAME, 'ss01')
                    source = get_elements(browser, By.CLASS_NAME, 'ss03')
                except TimeoutException:
                    print(index, '超时',url)
                    continue
                except NoSuchElementException:
                    print(index, '元素不存在',url)
                    continue
                else:
                    df.at[index,'timestamp'] = timestamp[0]
                    df.at[index,'source'] = source[0]
                filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/凤凰网'
                get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
                print(index, row['reference_title'], url)
                time.sleep(1.5)
        #澎湃网       
        elif dmname == 'www.thepaper.cn' and '200' in row['status_code']:
            if not url == 'https://www.thepaper.cn/':
                try:
                    browser.get(url.strip())
                    wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'index_left__LfzyH')))
                    box = get_elements(browser, By.CLASS_NAME, 'index_left__LfzyH')
                except TimeoutException:
                    print(index, '超时',url)
                    continue
                except NoSuchElementException:
                    print(index, '元素不存在',url)
                    continue
                else:
                    ti = re.search(r'(?P<time>20[0-9-]{8}\s[0-9:]{5})', box[0],flags=re.MULTILINE)
                    #so = re.search(r'^(?P<source>[\u4e00-\u9fa5].+)\n',box[0]) 感觉这个有问题，只能提取中文
                    so = re.search(r'^(?P<source>\S+)\n',box[0]) 
                    ly = re.search(r'来源：(?P<laiyuan>.+(\n)?.+)',box[0],flags=re.MULTILINE)

                    df.at[index,'timestamp'] = ti.groupdict()['time']
                    
                    if so:
                        ppsource = so.groupdict()['source']
                    if ly:
                        laiyuan = ly.groupdict()['laiyuan']
                        laiyuan = re.sub('[>∙\n]','',laiyuan).strip()
                        if '澎湃号' in laiyuan:
                            pph = get_elements(browser, By.CLASS_NAME, 'index_name__ID4kk')
                            print('pengpaihao',pph[0])
                            ppsource = laiyuan +': ' + pph[0]
                        else:
                            ppsource = laiyuan
                    df.at[index,'source'] = ppsource
                    
                filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/澎湃网'
                get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
                print(index, row['reference_title'], url)
                time.sleep(1.5)
        else:
            continue
                    
browser.quit()

#写入csv & sql
df.index += 1
df.to_csv("citation+news-100.csv", index=True)

conn3= sqlite.connect('citation+news-100.sqlite')
df.to_sql('citation+news', conn3, index=True, if_exists = 'replace')
conn3.close()

#语音播报结束
import pyttsx3
engine = pyttsx3.init()  # 创建engine并初始化
engine.say("本程序运行结束")
engine.runAndWait()  # 等待语音播报完毕
        
#%% 45-100
from os import path
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
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
import re

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

browser = webdriver.Chrome(executable_path = 'chromedriver')

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表')

df = pd.read_csv('citation+news-100.csv', index_col=('Unnamed: 0'))

for index, row in df.iterrows():
    url = row['origin_url']
    dmname = row['domain']
    if pd.isna(url) == False and row['url_time'] == "['None', 'None', 'None']" :
        #北京日报客户端
        if dmname == 'bj.bjd.com.cn' and '200' in row['status_code']:
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'infomation')))
                time.sleep(2)
                box = get_elements(browser, By.CLASS_NAME, 'infomation')
                
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                ti = re.search(r'(?P<time>20.+)$',box[0])
                so = re.search(r'^(?P<source>.+?)\s',box[0])
                df.at[index,'timestamp'] = ti.groupdict()['time']
                df.at[index,'source'] = so.groupdict()['source']
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/北京日报客户端'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        #百度百家号pc新闻    
        elif dmname == 'mbd.baidu.com' and '200' in row['status_code'] and 'newspage/data/error?' not in url:
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, '_10s4U')))
                time.sleep(2)
                timestamp = get_elements(browser, By.CLASS_NAME, '_10s4U')
                source = get_elements(browser, By.CLASS_NAME, '_7y5nA')
                source1 = get_elements(browser, By.CLASS_NAME, '_2JgKg')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                df.at[index,'timestamp'] = timestamp[0]
                if source:
                    df.at[index,'source'] = source[0]
                if source1:
                    df.at[index,'source'] = source1[0]
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/百度百家号pc新闻'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        #微信公众号平台
        elif dmname == 'mp.weixin.qq.com' and '200' in row['status_code']:
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'rich_media_meta_nickname')))
                time.sleep(2)
                timestamp = get_elements(browser, By.ID, 'publish_time')
                source = get_elements(browser, By.CLASS_NAME, 'rich_media_meta_nickname')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                df.at[index,'source'] = source[0]
                df.at[index,'timestamp'] = timestamp[0]
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/微信公众号平台'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        #人民日报客户端
        elif dmname == 'wap.peopleapp.com' and '200' in row['status_code']:
            try:
                browser.get(url.strip())
                
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.head-info.normal-info')))
                time.sleep(10) #这个网站老是有问题,感觉是抓得太快了
                box = get_elements(browser, By.CSS_SELECTOR, 'div.head-info.normal-info')
                source = get_elements(browser, By.CSS_SELECTOR, 'span.pr10.head-info-copyfrom')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                # ti = re.search(r'\n(?P<time>20.+)\n', box[0])
                ti = re.search(r'\n(?P<time>20.+)$', box[0],flags=re.MULTILINE)
                df.at[index,'source'] = source[0]
                df.at[index,'timestamp'] = ti.groupdict()['time']
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/人民日报客户端'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        else:
            continue
                    
       
    
browser.quit()

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表')

#写入csv & sql

df.to_csv("citation+news-45.csv", index=True)

conn3= sqlite.connect('citation+news-45.sqlite')
df.to_sql('citation+news', conn3, index=True, if_exists = 'replace')
conn3.close()

#语音播报结束
import pyttsx3
engine = pyttsx3.init()  # 创建engine并初始化
engine.say("本程序运行结束")
engine.runAndWait()  # 等待语音播报完毕

#%% < 45
from os import path
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
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
import re

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

browser = webdriver.Chrome(executable_path = 'chromedriver')

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表')

df = pd.read_csv('citation+news-45-3.csv', index_col=('Unnamed: 0'))
    
for index, row in df.iterrows():
    url = row['origin_url']
    dmname = row['domain']
    if pd.isna(url) == False and row['url_time'] == "['None', 'None', 'None']" :
        #澎湃网元素修正 
        if dmname == 'www.thepaper.cn' and '200' in row['status_code']:
            if not url == 'https://www.thepaper.cn/' and pd.isna(row['timestamp']) == False and not '20' in row['timestamp']:
                try:
                    browser.get(url.strip())
                    wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'index_left__LfzyH')))
                    box = get_elements(browser, By.CLASS_NAME, 'index_left__LfzyH')
                except TimeoutException:
                    print(index, '超时',url)
                    continue
                except NoSuchElementException:
                    print(index, '元素不存在',url)
                    continue
                else:
                    ti = re.search(r'(?P<time>20[0-9-]{8}\s[0-9:]{5})', box[0],flags=re.MULTILINE)
                    so = re.search(r'^(?P<source>[\u4e00-\u9fa5].+)\n',box[0])
                    ly = re.search(r'来源：(?P<laiyuan>.+(\n)?.+)',box[0],flags=re.MULTILINE)

                    df.at[index,'timestamp'] = ti.groupdict()['time']
                    
                    if so:
                        ppsource = so.groupdict()['source']
                    if ly:
                        laiyuan = ly.groupdict()['laiyuan']
                        laiyuan = re.sub('[>∙\n]','',laiyuan).strip()
                        if '澎湃号' in laiyuan:
                            pph = get_elements(browser, By.CLASS_NAME, 'index_name__ID4kk')
                            print('pengpaihao',pph[0])
                            ppsource = laiyuan +': ' + pph[0]
                        else:
                            ppsource = laiyuan
                    df.at[index,'source'] = ppsource   
                filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/澎湃网'
                get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
                print(index, row['reference_title'], url)
                time.sleep(1.5)
        #澎湃网移动端
        elif dmname == 'm.thepaper.cn' and '200' in row['status_code']:
            browser.get(url.strip())
            if '/newsDetail' in url:
                try:
                    wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'index_left__LfzyH')))
                    time.sleep(2)
                    box = get_elements(browser, By.CLASS_NAME, 'index_left__LfzyH')
                except TimeoutException:
                    print(index, '超时',url)
                    continue
                except NoSuchElementException:
                    print(index, '元素不存在',url)
                    continue
                else:
                    ti = re.search(r'(?P<time>20[0-9-]{8}\s[0-9:]{5})', box[0],flags=re.MULTILINE)
                    so = re.search(r'^(?P<source>[\u4e00-\u9fa5].+)\n',box[0])
                    ly = re.search(r'来源：(?P<laiyuan>.+(\n)?.+)',box[0],flags=re.MULTILINE)
                    df.at[index,'timestamp'] = ti.groupdict()['time']
                    if so:
                        ppsource = so.groupdict()['source']
                    if ly:
                        laiyuan = ly.groupdict()['laiyuan']
                        laiyuan = re.sub('[>∙\n]','',laiyuan).strip()
                        if '澎湃号' in laiyuan:
                            pph = get_elements(browser, By.CLASS_NAME, 'index_name__ID4kk')
                            print('pengpaihao',pph[0])
                            ppsource = laiyuan +': ' + pph[0]
                        else:
                            ppsource = laiyuan
                    df.at[index,'source'] = ppsource
                filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/澎湃网移动端'
                get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
                print(index, row['reference_title'], url)
                time.sleep(1.5)
            if '/baijiahao' in url:
                try:
                    wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.info.link')))
                    time.sleep(2)
                    box = get_elements(browser, By.CSS_SELECTOR,'div.info.link')
                except TimeoutException:
                    print(index, '超时',url)
                    continue
                except NoSuchElementException:
                    print(index, '元素不存在',url)
                    continue
                else:
                    ti = re.search(r'(?P<time>20.+)$', box[0])
                    so = re.search(r'(?P<source>\S+)\s', box[0])
                    source = '澎湃号·'+ so.groupdict()['source'].strip()
                    print(source)
                    df.at[index,'timestamp'] = ti.groupdict()['time']
                    df.at[index,'source'] = source
                filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/澎湃网移动端'
                get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
                print(index, row['reference_title'], url)
                time.sleep(1.5)
        #界面新闻元素修正
        elif dmname == 'www.jiemian.com' and '200' in row['status_code']:
            if pd.isna(row['timestamp']) == False and not '20' in row['timestamp']:
                try:
                    browser.get(url.strip())
                    wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-article-publish-time]')))
                    ti = get_elements(browser, By.CSS_SELECTOR, 'span[data-article-publish-time]')
                except TimeoutException:
                    print(index, '超时',url)
                    continue
                except NoSuchElementException:
                    print(index, '元素不存在',url)
                    continue
                else:
                    df.at[index,'source'] = '界面新闻' #界面在文章信息栏目没有准确标注信源，只标注了“界面新闻”
                    df.at[index,'timestamp'] = ti[0]
                filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/界面新闻'
                get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
                print(index, row['reference_title'], url)
                time.sleep(1.5)
        #beijing daily app
        elif dmname == 'ie.bjd.com.cn' and '200' in row['status_code']:
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'infomation')))
                time.sleep(2)
                box = get_elements(browser, By.CLASS_NAME, 'infomation')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                ti = re.search(r'(?P<time>20.+)$',box[0])
                so = re.search(r'^(?P<source>.+?)\s',box[0])
                df.at[index,'timestamp'] = ti.groupdict()['time']
                df.at[index,'source'] = so.groupdict()['source']
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/北京日报客户端'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        #guanchawang    
        elif dmname == 'www.guancha.cn' and '200' in row['status_code']:
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.time.fix')))
                box = get_elements(browser, By.CSS_SELECTOR,'div.time.fix')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                ti = re.search(r'(?P<time>20.+)\s', box[0])
                so = re.search(r'来源：(?P<source>.+)$', box[0])
                df.at[index,'timestamp'] = ti.groupdict()['time']
                df.at[index,'source'] = so.groupdict()['source']
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/观察者网'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        #fenghuang finance
        elif dmname == 'finance.ifeng.com' and '200' in row['status_code']:
            if not url == 'https://finance.ifeng.com/' and not url == 'https://finance.ifeng.com/c/404':
                try:
                    browser.get(url.strip())
                    wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'timeBref-2lHnksft')))
                    time.sleep(6)
                    timestamp = get_elements(browser, By.CLASS_NAME, 'timeBref-2lHnksft')
                    source = get_elements(browser, By.CLASS_NAME, 'sourceTitleText-3cWSuiol')
                except TimeoutException:
                    print(index, '超时',url)
                    continue
                except NoSuchElementException:
                    print(index, '元素不存在',url)
                    continue
                else:
                    df.at[index,'source'] = source[0]
                    df.at[index,'timestamp'] = timestamp[0]
                filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/凤凰网财经'
                get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
                print(index, row['reference_title'], url)
                time.sleep(1.5)
        #FIFA
        elif dmname == 'www.fifa.com':
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 60, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'capitalize-transform-text')))
                time.sleep(10)
                timestamp = get_elements(browser, By.CLASS_NAME, 'capitalize-transform-text')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                df.at[index,'timestamp'] = timestamp[0]
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/国际足联官网'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        #fenghuang app
        elif dmname == 'ishare.ifeng.com':
            if not url == 'https://ishare.ifeng.com/hotNewsShare404':
                try:
                    browser.get(url.strip())
                    wait = WebDriverWait(browser, 60, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'time-M6w87NaQ')))
                    time.sleep(5)
                    timestamp = get_elements(browser, By.CLASS_NAME, 'time-M6w87NaQ')
                    source = get_elements(browser, By.CLASS_NAME, 'source-3cecBclA')
                except TimeoutException:
                    print(index, '超时',url)
                    continue
                except NoSuchElementException:
                    print(index, '元素不存在',url)
                    continue
                else:
                    df.at[index,'timestamp'] = timestamp[0]
                    df.at[index,'source'] = source[0]
                filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/凤凰网客户端'
                get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
                print(index, row['reference_title'], url)
                time.sleep(1.5)
        elif dmname == '3w.huanqiu.com':
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 60, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'time')))
                time.sleep(5)
                timestamp = get_elements(browser, By.CSS_SELECTOR, 'span.time')
                source = get_elements(browser, By.CSS_SELECTOR, 'span.source')
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                df.at[index,'timestamp'] = timestamp[0]
                df.at[index,'source'] = source[0]
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/环球网'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
        elif dmname == 'slide.news.sina.com.cn':
            try:
                browser.get(url.strip())
                wait = WebDriverWait(browser, 60, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'swpt-time')))
                time.sleep(5)
                timestamp = get_elements(browser, By.CLASS_NAME, 'swpt-time')
                
            except TimeoutException:
                print(index, '超时',url)
                continue
            except NoSuchElementException:
                print(index, '元素不存在',url)
                continue
            else:
                df.at[index,'timestamp'] = timestamp[0]
               
            filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/新浪新闻'
            get_html(filepath, browser, row['reference_title'], row['entry'], row['reference_entryindex'])
            print(index, row['reference_title'], url)
            time.sleep(1.5)
    else:
            continue
                    
       
browser.quit()

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表')

#写入csv & sql

df.to_csv("citation+news-9次.csv", index=True)

conn3= sqlite.connect('citation+news-9次.sqlite')
df.to_sql('citation+news', conn3, index=True, if_exists = 'replace')
conn3.close()

#语音播报结束
# import pyttsx3
# engine = pyttsx3.init()  # 创建engine并初始化
# engine.say("本程序运行结束")
# engine.runAndWait()  # 等待语音播报完毕



        