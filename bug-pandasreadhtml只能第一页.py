#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:10:34 2023

@author: zhangsiqi
"""

import os
import time
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tenacity import retry, retry_if_exception_type, wait_fixed
#from selenium.webdriver.common.keys import Keys
#import pandas as pd
import re
import sqlite3 as sqlite
import math
import pandas as pd

# 连接sql数据库
os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情')
conn= sqlite.connect('Wiki.sqlite')

dfev = pd.read_sql('SELECT * FROM events', conn, index_col='index')
dfedi = pd.read_sql('SELECT * FROM edithistory', conn)


conn.close()
dfedi['edit_time']=pd.NaT
#dfnew['edit_time']=pd.NaT

# 定义一个捕捉元素时出现StaleElementReferenceException异常后重试的装饰器
@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(3))
def get_elements(driver, method, name):
    #print('尝试获取元素',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),name)
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

browser = webdriver.Chrome(executable_path = 'chromedriver')

dfall_new = pd.DataFrame(columns=['entry','edit_entryindex','提交时间', '贡献者','edit_time'])
for index, row in dfev[0:2].iterrows():
    editurl = row['editurl']
    editcount = row['editcount']
    if editurl:
        editpage_nos = math.ceil(int(editcount)/25) #通过向上取整确定编辑历史的页面数量
        dfev_new = pd.DataFrame(columns=['entry','edit_entryindex','提交时间', '贡献者','edit_time'])
        for num in range(1,editpage_nos+1):
            histo_url = editurl + '#page' + str(num)
            edit_jsscript = '''window.open("'''+ histo_url + '''", 'new_window')''' 
            browser.execute_script(edit_jsscript) #打开新标签页，进入编辑历史的网页
            browser.switch_to.window(browser.window_handles[-1]) #切换窗口
            time.sleep(2.5)
            #一直等待到元素可见
            wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.TAG_NAME, 'td')))
            
            frame = pd.read_html(histo_url)[0][['提交时间','贡献者']] #0表示抓取网页中第一个表格
            dfev_new = pd.concat([dfev_new, frame],ignore_index=True, sort=False)#在合并不保留原索引，启用新的自然索引：
        dfev_new['entry'] = row['entry']
        dfev_new['edit_entryindex'] = dfev_new.index + 1
        dfall_new = pd.concat([dfall_new,dfev_new])

browser.close() #关闭当前的编辑历史标签页
browser.quit()