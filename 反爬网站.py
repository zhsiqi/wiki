#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 16:47:00 2023

@author: zhangsiqi
"""

import os
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

import nest_asyncio
nest_asyncio.apply()

import logging
pyppeteer_level = logging.WARNING
logging.getLogger('pyppeteer').setLevel(pyppeteer_level)
logging.getLogger('websockets.protocol').setLevel(pyppeteer_level)
pyppeteer_logger = logging.getLogger('pyppeteer')
pyppeteer_logger.setLevel(logging.WARNING)

async def pyppteer_fetchUrl(url):
    browser = await launch({'headless': False,'dumpio':True, 'autoClose':True, 'args':['--window-size={600},{600}']})
    page = await browser.newPage()
    await page.setViewport({'width': 600, 'height': 600})
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
    await page.goto(url)


    await asyncio.sleep(60)
    str = await page.content()
    await browser.close()
    return str
    

def fetchUrl(url):
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetchUrl(url))

# fetchUrl('https://world.huanqiu.com/article/9CaKrnKiVec')

#%
#gov.
def getdate(html):
    bsobj = BeautifulSoup(html,'html.parser')
    title = bsobj.find('div', attrs={"class":"tit"}).text
    date = bsobj.find('div', attrs={"class":"source"}).text
    print('标题是',title)
    print('日期是',date)
    return title

if "__main__" == __name__: 
    s =fetchUrl('http://www.nhc.gov.cn/xcs/yqtb/202109/a24a8dca26c343e0a2a96461539f18b8.shtml')
    getdate(s)


#%%

#huanqiu
# def getTitleUrl(html):
#     bsobj = BeautifulSoup(html,'html.parser')
#     #title = bsobj.find('div', attrs={"class":"head"}).text
#     date = bsobj.find('div', attrs={"class":"date"}).text
#     #print('标题是',title)
#     print('日期是',date)
#     #return title


# def getTitleUrl(html):
#     bsobj = BeautifulSoup(html,'html.parser')
#     titleList = bsobj.find('div', attrs={"class":"list"}).ul.find_all("li")
#     for item in titleList:
#         link = "http://www.nhc.gov.cn" + item.a["href"];
#         title = item.a["title"]
#         date = item.span.text
#         yield title, link, date

    