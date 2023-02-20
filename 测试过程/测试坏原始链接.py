#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 17:23:29 2023

@author: zhangsiqi
"""

import time
#from bs4 import BeautifulSoup
from seleniumwire import webdriver
import datetime
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome('chromedriver')
driver.get('https://baike.baidu.com/redirect/95e7gn5CNS-JAzJ9-uKH7uSqHQyPveBEmxSb0DAjMT6Gz_zp9B3aXgvBjKd6bCNszmnWegVXkjOATS6w5MLsoRshpYri9WqRwZk')
#print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

driver.get('https://baike.baidu.com/redirect/feefMtx5SBaxhRlLsKRHuVx619ZlQdDNubGQiNkTUgk4dVKiN4SG3gCZPQhtYYs75VwkEIdui5wK64dZPp7wpnA8UuOwGvwnPs3q1Qdfdq9K6Br9zVY2zpzgWuM')
b = driver.requests
print(b)

# Access requests via the `requests` attribute
try:
    a = driver.requests
    #print(a)
    for request in a:
        #if request.response:
        print(
            request.url,
            request.response.status_code)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
except:
    original_url = 'Error'

import requests
url = "https://baike.baidu.com/redirect/95e7gn5CNS-JAzJ9-uKH7uSqHQyPveBEmxSb0DAjMT6Gz_zp9B3aXgvBjKd6bCNszmnWegVXkjOATS6w5MLsoRshpYri9WqRwZk"
response = requests.get(url,allow_redirects=True,headers={"Content-Type":"application/json"})
print(response.status_code)

import requests
url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
response = requests.get(url,allow_redirects=True,headers={"Content-Type":"application/json"})
print(response.status_code)

import requests
url = "http://www.tz8.com/html/2011-7/news-61385.htm"
response = requests.get(url,headers={"Content-Type":"application/json"})
print(response.status_code)

import requests
url = "http://www.bousai.go.jp/2011daishinsai/pdf/torimatome20170308.pdf"
response = requests.get(url,allow_redirects=True,headers={"Content-Type":"application/json"})
print(response.status_code)



import requests
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}
s = requests.session()
# 打开我的随笔
url = "https://baike.baidu.com/redirect/95e7gn5CNS-JAzJ9-uKH7uSqHQyPveBEmxSb0DAjMT6Gz_zp9B3aXgvBjKd6bCNszmnWegVXkjOATS6w5MLsoRshpYri9WqRwZk"
r = s.get(url,headers=headers,allow_redirects=False,verify=False)
# 打印状态码，自动处理重定向请求
print (r.status_code)
new_url = r.headers["Location"]
print (new_url)



import requests
response = requests.get('https://baike.baidu.com/redirect/feefMtx5SBaxhRlLsKRHuVx619ZlQdDNubGQiNkTUgk4dVKiN4SG3gCZPQhtYYs75VwkEIdui5wK64dZPp7wpnA8UuOwGvwnPs3q1Qdfdq9K6Br9zVY2zpzgWuM',allow_redirects=True)
print(response.url)
print(response.history)

response = requests.get('http://news.ifeng.com/gundong/detail_2011_03/13/5125115_0.shtml',allow_redirects=True)

print(response.url)

print(response.history)

response = requests.get('http://news.ifeng.com/gundong/detail_2011_03/13/5125115_0.shtml',allow_redirects=False)

print(response.url)

print(response.history)

from urllib import request
url = 'https://baike.baidu.com/redirect/feefMtx5SBaxhRlLsKRHuVx619ZlQdDNubGQiNkTUgk4dVKiN4SG3gCZPQhtYYs75VwkEIdui5wK64dZPp7wpnA8UuOwGvwnPs3q1Qdfdq9K6Br9zVY2zpzgWuM'
print(response.status)
response = request.urlopen(url)
new_url = response.geturl()
print(new_url)

import requests
response = requests.head('https://www.chinacdc.cn/',allow_redirects=True)
print(response.status_code)
# 疾病预防控制中心的网站没有那么强的反扒机制

 
import requests
response = requests.head('http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml',allow_redirects=True)
print(response.status_code)


from seleniumwire import webdriver
url = 'https://baike.baidu.com/redirect/6f75zUyCd5hAWh6Bkd6nCFYBX9RKVam7U3gBqDcNyAhn7kRtyDFuQ4JoXA5_jcro-Yop9rUNihjGSJ5z3uQO9ETc_rTk482WXEcXZacJ43Wm'
url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
url = 'http://news.ifeng.com/gundong/detail_2011_03/13/5125115_0.shtml'
url = 'https://baike.baidu.com/redirect/e7f2_H6Id7zZLAStOFC7-GWLC_ob7NKjpKE2Bwn-CKhk7skw34H-sZp-IcPkkyARgDOvMxWpjcpqYvuC'
url = 'https://baike.baidu.com/redirect/b653OPXPyywyaRR5rqBumrgWTgGArMEiXyRutK0D2f793616HtbQbW8a2IczfUkRhepR3IUNIqNga-poMc4vX3MQRSTl7JdseBEaEjBLbFoJ'
url = 'https://baike.baidu.com/redirect/f417_fBVcPNiAx_fxFE1c58pjihK57ZbW3GKaLYW7c0jjVBYanpBJZhBboakpBT72wuosfPKTTFPFb3xQMN6PvvssIY5PO8vqve7NajSFD_ZwH3t'
driver = webdriver.Chrome('chromedriver')
driver.get(url)
for request in driver.requests[0:4]:
  print(request.url) # <--------------- Request url
  #print(request.headers) # <----------- Request headers
  #print(request.response.headers) # <-- Response headers
  print(request.response.status_code)
driver.quit()

# 输出结果
# http://news.ifeng.com/gundong/detail_2011_03/13/5125115_0.shtml
# 301
# https://news.ifeng.com/gundong/detail_2011_03/13/5125115_0.shtml
# 301
# https://news.ifeng.com/
# 200
# https://x2.ifengimg.com/fe/shank/list/es-e40109762c.polyfill.modern.min.js
# 200
# https://x2.ifengimg.com/fe/shank/list/errorupload-f348bc846f.min.js
# 200
# https://x2.ifengimg.com/fe/shank/list/shanklist_shanklist~dev_release~.5609f54897b1cfa8aa03.css
# 200
# https://x0.ifengimg.com/feprod/c/m/mobile_inice_v202.js
# 200
# https://x2.ifengimg.com/fe/shank/list/externals.7268b943.js
# 200




import seleniumwire.undetected_chromedriver as uc

chrome_options = uc.ChromeOptions()

driver = uc.Chrome(
    options=chrome_options,
    seleniumwire_options={}
)
url = 'http://www.nhc.gov.cn/xcs/xxgzbd/gzbd_index.shtml'
driver.get(url)


for request in driver.requests[0:5]:
    #if request.response:
    print(
        request.url,
        request.response.status_code)

