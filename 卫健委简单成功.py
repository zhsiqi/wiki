#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 22:46:18 2023

@author: zhangsiqi
"""

import os
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

import nest_asyncio
nest_asyncio.apply()

async def pyppteer_fetchUrl(url):
    browser = await launch({'headless': False,'dumpio':True, 'autoClose':True, 'args':['--window-size={800},{800}']})
    page = await browser.newPage()
    await page.setViewport({'width': 800, 'height': 800})
    await page.goto(url)
    # element = await page.querySelector('div > div.fix-menu > div.date')
    # ele = await (await element.getProperty('YYYY')).jsonValue()
    # print(ele) #获取文本内容

    await asyncio.sleep(60)
    source = await page.content()
    await browser.close()
    return source
    

def fetchUrl(url):
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetchUrl(url))

# fetchUrl('https://world.huanqiu.com/article/9CaKrnKiVec')

#%
#gov.
def getTitleUrl(html):
    bsobj = BeautifulSoup(html,'html.parser')
    title = bsobj.find('div', attrs={"class":"tit"}).text
    date = bsobj.find('div', attrs={"class":"source"}).text
    print('标题是',title)
    print('日期是',date)
    return title

if "__main__" == __name__: 
    s = fetchUrl('http://www.nhc.gov.cn/xcs/fkdt/202212/075a30385dff4672b53dd4bf864e3e38.shtml')
#    s =fetchUrl('http://www.nhc.gov.cn/xcs/yqtb/202109/a24a8dca26c343e0a2a96461539f18b8.shtml')
    getTitleUrl(s)

with open('try.html', "w", encoding='utf-8') as g:
    g.write(s)
    g.close()