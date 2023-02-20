#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:15:51 2023

@author: zhangsiqi
"""

"""
根据域名筛选出卫健委网站
判断网址政务
如果网址错误，生成正确网址
加载正确网址，获取时间
"""

from os import path
import os
import time
from tenacity import retry, retry_if_exception_type, wait_fixed
#from selenium.webdriver.common.keys import Keys
import pandas as pd
import sqlite3 as sqlite
import datetime
import numpy as np
import re
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

import nest_asyncio
nest_asyncio.apply()

def get_html(filepath, html, title, entry, entryindex):
    os.chdir(filepath)
    filename = (title+'-'+ entry + str(entryindex)).replace('/', '_') +'.html'
    # remember to replace '/' since it will be recognized as file path instead of file name
    if not path.exists(filename):
        with open(filename, "w", encoding='utf-8') as g:
            g.write(html)
            g.close()
            
async def pyppteer_fetchUrl(url):
    browser = await launch({'headless': False,'dumpio':True, 'autoClose':True, 'args':['--window-size={600},{600}']})
    page = await browser.newPage()
    await page.setViewport({'width': 600, 'height': 600})
    await page.evaluateOnNewDocument('Object.defineProperty(navigator,"webdriver",{get:()=>undefined})')
    await page.goto(url)
    await asyncio.sleep(30)
    source = await page.content()
    await browser.close()
    return source

def fetchUrl(url):
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetchUrl(url))

#gov.
def getdate(html):
    bsobj = BeautifulSoup(html,'html.parser')
    date = bsobj.find('div', attrs={"class":"source"})
    if date:
        date = date.text
        print('日期是',date)
        return date

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0117补充各渠道的时间等')
df = pd.read_csv('citation+news-9-3.csv')

for index, row in df[3504:3600].iterrows():
    url = row['origin_url']
    dmname = row['domain']
    title = row['reference_title']
    if pd.isna(url) == False and "nhc.gov" in dmname:
        #用标题确定类别
        if ('最新' or '截至' in title) and ('/xcs/yqfkdt/' in url):
            url = re.sub('/xcs/yqfkdt/', '/xcs/yqtb/', url)
        elif '疫苗接种情' in title and '/jkj/s7915/' not in url:
            url = re.sub('/xcs/yqfkdt/', '/jkj/s7915/', url)
            
        s = fetchUrl(url)
        urldate = getdate(s)
        if urldate:
            ti = re.search(r'(?P<time>20\S+)', urldate, flags=re.MULTILINE)
            df.at[index,'timestamp'] = ti.groupdict()['time']
            
        filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/卫健委网站'
        get_html(filepath, s, title, row['entry'], row['reference_entryindex'])
        print(index, row['reference_title'], url)
        time.sleep(1.5)
        