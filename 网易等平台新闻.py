#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 17:23:19 2023

@author: zhangsiqi
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')
browser.get('https://www.163.com/news/article/EUOOB2G100018AOR.html') #selenium获取网页

@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

info = get_elements(browser, By.CLASS_NAME, 'post_info')[0]
time = info[0:19]
m = re.search(r'来源: (?P<author>\S*)\n', info)
author = m.groupdict()['author']

browser.quit()

print(info)
print(time)
print(author)

#%% jiemian.com
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')
url = 'https://www.jiemian.com/article/7335122.html'
url = 'https://www.jiemian.com/article/6382058.html'
browser.get(url) #selenium获取网页

@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

box = get_elements(browser, By.CLASS_NAME, 'article-info')

ti = get_elements(browser, By.CSS_SELECTOR, 'span[data-article-publish-time]')

browser.quit()

timestamp = ti[0]


print(timestamp)

#%% thepaper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')


url = 'https://www.thepaper.cn/newsDetail_forward_2376192'
url = 'https://www.thepaper.cn/newsDetail_forward_15833621'
url = 'https://www.thepaper.cn/newsDetail_forward_2675586'
url = 'https://www.thepaper.cn/newsDetail_forward_2247702'
url = 'https://www.thepaper.cn/newsDetail_forward_3515915'
browser.get(url) #selenium获取网页


@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

box = get_elements(browser, By.CLASS_NAME, 'index_left__LfzyH')

ti = re.search(r'(?P<time>20[0-9-]{8}\s[0-9:]{5})', box[0],flags=re.MULTILINE)
so = re.search(r'^(?P<source>[\u4e00-\u9fa5].+)\n',box[0])
ly = re.search(r'来源：(?P<laiyuan>.+(\n)?.+)',box[0],flags=re.MULTILINE)

timestamp = ti.groupdict()['time']
if so:
    realsource = so.groupdict()['source']
    
if ly:
    laiyuan = ly.groupdict()['laiyuan']
    laiyuan = re.sub('[>∙\n]','',laiyuan).strip()
    if '澎湃号' in laiyuan:
        pph = get_elements(browser, By.CLASS_NAME, 'index_name__ID4kk')
        print('pengpaihao',pph[0])
        realsource = laiyuan +': ' + pph[0]
    else:
        realsource = laiyuan
    
browser.quit()

print('laiyuan',realsource)
print('time',timestamp)


# print('box',box)
# eles = box[0].split('\n')
# print(eles)

# print(box[0].split('\n')[0])




#%% beijing daily 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')
url = 'https://bj.bjd.com.cn/5b165687a010550e5ddc0e6a/contentShare/5b16573ae4b02a9fe2d558f9/AP625bcde7e4b01d2ae395a4b2.html'
url = 'https://bj.bjd.com.cn/5b165687a010550e5ddc0e6a/contentShare/5b16573ae4b02a9fe2d558f9/AP62b95e8fe4b01c9fa7b210ae.html'
browser.get(url)
#https://bj.bjd.com.cn/5b165687a010550e5ddc0e6a/contentShare/5b16573ae4b02a9fe2d558f9/AP625bcde7e4b01d2ae395a4b2.html

@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

box = get_elements(browser, By.CLASS_NAME, 'infomation')
timestamp = box[0].split('\n')[1]
source = box[0].split('\n')[0]
if '|' in source:
    realsource = source[:source.index('|')].strip()
else:
    realsource = source


print('timestamp', timestamp)
print('timestamp[0]', timestamp[0])
print('realsource',realsource)
eles = timestamp[0].split('\n')

print(timestamp[0].split('\n'))
browser.quit()

#%% baidu baijiahao

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')
url = 'https://mbd.baidu.com/newspage/data/landingsuper?rs=2104165771&ruk=OSAd2TjUWTBDB00v25y09g&isBdboxFrom=1&pageType=1&urlext=%7B%22cuid%22%3A%22Yivzu_uN2a0w8282givg8_iCHal9aSiH_ivcagaIvu0tivirjuHtajf51ul6t3Ojt9FmA%22%7D&context=%7B%22nid%22%3A%22news_6569249065725710457%22%7D'
url = 'https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9326475174755388778%22%7D&n_type=-1&p_from=-1'
browser.get(url)

@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

timestamp = get_elements(browser, By.CLASS_NAME, '_10s4U')
source = get_elements(browser, By.CLASS_NAME, '_7y5nA')
source1 = get_elements(browser, By.CLASS_NAME, '_2JgKg')
if source:
    realsource = source[0]
if source1:
    realsource = source1[0]

print('timestamp是', timestamp)
print('timestamp[0]是', timestamp[0])
print('realsource是',realsource)
# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))
browser.quit()

#%% wechat 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')
url = 'https://mp.weixin.qq.com/s?__biz=MzA4OTIyMjUyOQ==&mid=2654663686&idx=1&sn=ebdb3b3d88d1ef41013706b8fad601a0&chksm=8bd068e8bca7e1feb84a7c3981974bf0aeba25cceb18fb7c115444aa1ad35d69cd915b4dfb62&mpshare=1&scene=23&srcid=0513h3t7Iu3THdVba8Mphw0T&sharer_sharetime=1620877002211&sharer_shareid=020acbd4476ea8c93c995b49451b3186#rd'
browser.get(url)

@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

timestamp = get_elements(browser, By.ID, 'publish_time')
source = get_elements(browser, By.CLASS_NAME, 'rich_media_meta_nickname')

print('timestamp是', timestamp)
#print('timestamp[0]是', timestamp[0])
print('source是',source)
# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))
browser.quit()
#%% people's daily app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')
url = 'https://wap.peopleapp.com/article/5272803/5178438?utm_source=weibo&utm_medium=social&utm_oi=845761683086532608'
url = 'https://wap.peopleapp.com/article/4778549/4664953'
browser.get(url)

@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]
wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.head-info.normal-info')))

source = get_elements(browser, By.CSS_SELECTOR, 'span.pr10.head-info-copyfrom')
#timetest = get_elements(browser, By.CSS_SELECTOR, 'span.head-info.normal-info')
box = get_elements(browser, By.CSS_SELECTOR, 'div.head-info.normal-info')

ti = re.search(r'\n(?P<time>20.+)\n', box[0])

# timest = get_elements(browser, By.ID, 'publish_time')

# timestamp = timest[0]
print('box 是',box)

print('timestamp是', ti.groupdict()['time'])
#print('timestamp[0]是', timestamp[0])
print('source是',source[0])
# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))
browser.quit()



#%% huanqiu website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re
import time


@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

browser = webdriver.Chrome('chromedriver')
url = 'https://world.huanqiu.com/article/9CaKrnKiVec'
url = 'https://world.huanqiu.com/article/9CaKrnJFnwJ'
browser.get(url)


#wait = WebDriverWait(browser, 100, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'source')))
time.sleep(10) #这个网站老是有问题,感觉是抓得太快了

timestamp = get_elements(browser, By.CSS_SELECTOR, 'div.date')
source = get_elements(browser, By.CLASS_NAME, 'source')
paras = get_elements(browser, By.TAG_NAME, 'p')


print(i for i in paras)
# print('timestamp是', timestamp[0].replace('-',''))
# #print('timestamp[0]是', timestamp[0])
# print('source是',source[0].strip('来源：'))
# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))
browser.quit()

#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')

url = 'https://m.thepaper.cn/baijiahao_15616291'
url = 'https://m.thepaper.cn/baijiahao_20093108'
url = 'https://m.thepaper.cn/baijiahao_15594094'
browser.get(url)

@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.info.link')))
box = get_elements(browser, By.CSS_SELECTOR,'div.info.link')

ti = re.search(r'(?P<time>20.+)$', box[0])
so = re.search(r'(?P<source>[：\u4e00-\u9fa5]+)\s', box[0])
source = '澎湃号·'+ so.groupdict()['source'].strip()
# timest = get_elements(browser, By.ID, 'publish_time')

# timestamp = timest[0]
print('box 是',box)
print('box[0]',box[0])
print('source是',source)
print('timestamp是', ti.groupdict()['time'])
#print('timestamp[0]是', timestamp[0])
# print('source是',source[0])
# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))
browser.quit()


# (By.CSS_SELECTOR,'div.info.link')
#%% beijing daily app


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')
url = 'https://ie.bjd.com.cn/5b165687a010550e5ddc0e6a/contentApp/5b16573ae4b02a9fe2d558f9/AP5ee8d88ee4b01e723d187a66?isshare=1&app=f51e65a4363b2402&contentType=0&isBjh=0'
url = 'https://ie.bjd.com.cn/5b165687a010550e5ddc0e6a/contentApp/5b16573ae4b02a9fe2d558f9/AP5ee8d88ee4b01e723d187a66?isshare=1&app=f51e65a4363b2402&contentType=0&isBjh=0'
url = 'https://ie.bjd.com.cn/5b165687a010550e5ddc0e6a/contentApp/5b16573ae4b02a9fe2d558f9/AP610563c5e4b02a0d8b0aed0d?isshare=1&app=F65B1909-7589-4563-A91F-0D49EB319643&contentType=0&isBjh=0'
url = 'https://bj.bjd.com.cn/5b165687a010550e5ddc0e6a/contentShare/5b16573ae4b02a9fe2d558f9/AP625c1fe6e4b0c727d7a612c0.html'
url = 'https://bj.bjd.com.cn/5b165687a010550e5ddc0e6a/contentShare/5b16573ae4b02a9fe2d558f9/AP6256a12fe4b09a81e0103b67.html'
browser.get(url)
#https://bj.bjd.com.cn/5b165687a010550e5ddc0e6a/contentShare/5b16573ae4b02a9fe2d558f9/AP625bcde7e4b01d2ae395a4b2.html

@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

box = get_elements(browser, By.CLASS_NAME, 'infomation')

print('box[0]',box[0])

# timestamp = re.search(r'^(?P<time>20.+)$',box[0],flags=re.MULTILINE)
# source = re.search(r'^(?P<source>[\u4e00-\u9fa5].+?)\s',box[0])
# print(source.groupdict()['source'])
# print(timestamp.groupdict()['time'])

ti = re.search(r'(?P<time>20.+)$', box[0])
so = re.search(r'^(?P<source>.+?)\s', box[0])
#so = re.search(r'^(?P<source>[\u4e00-\u9fa5].+?)\s',box[0]) #这个正则不对，以中文开头会排除掉@开头的账号
source = so.groupdict()['source'].strip()

browser.quit()

print('timestamp', ti.groupdict()['time'])
print('realsource',source)


# # print('timestamp[0]', timestamp[0])

# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))



#%% guanchawang website
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')


url = 'https://www.guancha.cn/society/2018_04_18_454174.shtml'
url = 'https://www.guancha.cn/politics/2020_02_22_537736.shtml'
browser.get(url)

@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.time.fix')))
box = get_elements(browser, By.CSS_SELECTOR,'div.time.fix')

ti = re.search(r'(?P<time>20.+)\s', box[0])
so = re.search(r'来源：(?P<source>.+)$', box[0])
# timest = get_elements(browser, By.ID, 'publish_time')

# timestamp = timest[0]
browser.quit()

print('box 是',box)
print('box[0]',box[0])
print('source是',so.groupdict()['source'])
print('timestamp是', ti.groupdict()['time'])

#%% fenghuang finance

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re
import time


@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

browser = webdriver.Chrome('chromedriver')
url = 'https://world.huanqiu.com/article/9CaKrnKiVec'
url = 'https://finance.ifeng.com/c/7nZt6gyaCUi'
browser.get(url)

time.sleep(2) #这个网站老是有问题,感觉是抓得太快了

timestamp = get_elements(browser, By.CLASS_NAME, 'timeBref-2lHnksft')
source = get_elements(browser, By.CLASS_NAME, 'sourceTitleText-3cWSuiol')

# print('timestamp是', timestamp[0].replace('-',''))
print('timestamp[0]是', timestamp[0])
print('source是',source[0])
# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))
browser.quit()

#%% FIFA
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re
import time


@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

browser = webdriver.Chrome('chromedriver')

url = 'https://www.fifa.com/tournaments/mens/worldcup/2018russia/media-releases/russia-and-qatar-awarded-2018-and-2022-fifa-world-cups-1344698'
browser.get(url)

time.sleep(2) #这个网站老是有问题,感觉是抓得太快了

timestamp = get_elements(browser, By.CLASS_NAME, 'capitalize-transform-text')

# print('timestamp是', timestamp[0].replace('-',''))
print('timestamp[0]是', timestamp[0])
# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))
browser.quit()

#%% fenghuang app

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re
import time


@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

browser = webdriver.Chrome('chromedriver')

url = 'https://ishare.ifeng.com/c/s/7lFECPLOS4e'
url = 'https://ishare.ifeng.com/c/s/v006t0eFovq2WvqShU3rTCROTwNSSSGLeXUD--2QnOP5WXB1bPKS4ZzQXDih8bd0z9Ii2?spss=np&channelId=&aman=6b104D18ba862P59522f3&gud=10D646t055'
browser.get(url)

time.sleep(2) #这个网站老是有问题,感觉是抓得太快了

timestamp = get_elements(browser, By.CLASS_NAME, 'time-M6w87NaQ')
source = get_elements(browser, By.CLASS_NAME, 'source-3cecBclA')

# print('timestamp是', timestamp[0].replace('-',''))
print('timestamp[0]是', timestamp[0])
print('source是',source[0])
# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))
browser.quit()

#%% huanqiu website

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re
import time


@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

browser = webdriver.Chrome('chromedriver')

url = 'https://3w.huanqiu.com/a/c36dc8/3xNnJ32tVTb'
url = 'https://3w.huanqiu.com/a/8472b6/43470eRDfIG?baike'

browser.get(url)

time.sleep(2) #这个网站老是有问题,感觉是抓得太快了

timestamp = get_elements(browser, By.CSS_SELECTOR, 'span.time')
source = get_elements(browser, By.CSS_SELECTOR, 'span.source')

# print('timestamp是', timestamp[0].replace('-',''))
print('timestamp[0]是', timestamp[0])
print('source是',source[0])
# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))
browser.quit()


#%% wangyi xinwen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tenacity import retry, retry_if_exception_type, wait_fixed
import re

browser = webdriver.Chrome('chromedriver')


url = 'https://www.guancha.cn/society/2018_04_18_454174.shtml'
url = 'https://news.163.com/photoview/00AP0001/2300573.html?baike#p=EAS7DK1T00AP0001NOS'
browser.get(url)

time.sleep(5) 

@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.top.cf > div.headline > span')))
box = get_elements(browser, By.CSS_SELECTOR,'div.top.cf > div.headline > span')

ti = re.search(r'(?P<time>20.+)\s', box[0])
# timest = get_elements(browser, By.ID, 'publish_time')

# timestamp = timest[0]
browser.quit()

print('box 是',box)
print('box[0]',box[0])
#print('source是',so.groupdict()['source'])
print('timestamp是', ti.groupdict()['time'])



#%% 新浪网站
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed
import re
import time


@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

browser = webdriver.Chrome('chromedriver')

url = 'http://slide.news.sina.com.cn/slide_1_2841_136703.html?cre=newspagepc&mod=f&loc=2&r=9&doct=0&rfunc=64#p=1'

browser.get(url)

time.sleep(2) #这个网站老是有问题,感觉是抓得太快了
wait = WebDriverWait(browser, 60, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'swpt-time')))
timestamp = get_elements(browser, By.CLASS_NAME, 'swpt-time')

# print('timestamp是', timestamp[0].replace('-',''))
print('timestamp是', timestamp[0])
# eles = timestamp[0].split('\n')

# print(timestamp[0].split('\n'))
browser.quit()










