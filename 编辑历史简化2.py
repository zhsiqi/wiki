#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 11:14:53 2023

@author: zhangsiqi
"""


# from urllib.parse import quote
from urllib.parse import unquote
from urllib.parse import urlparse
import requests
from os import path
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
#from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import sqlite3 as sqlite
import math
import datetime
from tenacity import retry, retry_if_exception_type, wait_fixed

#========第一步：事件名称汉字转URL编码=============

# create a dataframe to store target data
#df = pd.DataFrame(columns=['event','viewcount','votecount','topeditorcount','editcount','editurl','toc'])

evtable = pd.read_excel('events的副本.xlsx')


# 创建sql数据库
conn= sqlite.connect('test-simpleedit-v2.sqlite')
c = conn.cursor()

# 创建表单，保存各个事件
c.execute('''CREATE TABLE IF NOT EXISTS events 
          (event_id int, event text, year, entry text, baikelink text, viewcount int, votecount int, 
           topeditor_count int, editcount int, editurl text,
           toc_level1 text, toclevel1_count int, tocs text, reference_count int,
           summary text, para_content text, link_count int, science_paper int, 
           all_reitem_count int, collect_time)''')
# 创建表单，保存事件下面的参考资料
c.execute('''CREATE TABLE IF NOT EXISTS citations 
          (event_id int, event text, year, entry text, reference_count int, reference_index int, 
           reference_text text, reference_title text, 
           reference_url text, reference_site text, source_time, cite_time, redir_url text, original_url text, 
           status_code text, snapshot_url text, collect_time)''')
# 创建表单，保存事件下面的编辑历史
c.execute('''CREATE TABLE IF NOT EXISTS edithistory 
          (event_id int, event text, year, entry text, edit_count, edit_index int, author_name text, author_id text,  
           update_time, collect_time)''') #unique最后改一下
# 创建表单，保存事件下面的百科内部链接
c.execute('''CREATE TABLE if NOT EXISTS link 
          (event_id int, event text, year, entry text, link_count int, link_index int, link_name text, link_url text, collect_time)''')
# 创建表单，保存事件下面的突出贡献榜
c.execute('''CREATE TABLE if NOT EXISTS topeditor
          (event_id int, event text, year, entry text, editor_name text, editor_id int,
           contribution text, collect_time)''')
# 创建表单，保存事件的文字段落和段落内的引用情况
c.execute('''CREATE TABLE if NOT EXISTS wikitext
          (event_id int, event text, year, entry text, wiki_text text, cited_count int,
           cited_item text, collect_time)''')
# 创建表单，保存事件的学术论文的引用情况
c.execute('''CREATE TABLE if NOT EXISTS science
          (event_id int, event text, year, entry text, sci_count int, sci_index int, sci_author text,
           sci_title text, sci_joural text, sci_year, sci_link text,
           collect_time)''')
# 创建表单，保存事件底部的相关栏目
c.execute('''CREATE TABLE if NOT EXISTS relevance
          (event_id int, event text, year, entry text, rebox_count int, rebox_index int, rebox_name text, reitem_count int, 
           reitem_index int, reitem_name text, reitem_link text, collect_time)''')
          
#========第一步：根据词条网址获取网页内容============
#browser = webdriver.Chrome(executable_path = 'D:\python\chromedriver_win32\chromedriver')
browser = webdriver.Chrome(executable_path = 'chromedriver')

# 定义一个捕捉元素时出现StaleElementReferenceException异常后重试的装饰器
@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, name):
    print('尝试获取元素',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),name)
    targets = driver.find_element(By.CLASS_NAME, name)
    print('获取元素成功')
    return targets


for index, row in evtable.iterrows():
    # print('line',line.strip())
    line = row['url']
    year = row['year']
    eventname = row['event']
    event_id = row['event_id']
    wangzhi = urlparse(line.strip()) #从URL中解析出各个部分
    # print('wangzhi', wangzhi[2])
    entryname = unquote(wangzhi[2][6:]) #从解析结果中提取出事件内容部分并且转成中文给html文件命名，
    #命名中的斜杠要删除,否则后面新建html有问题
    if '/' in entryname:
        entryname = entryname.split('/')[0]
    
    filename = entryname + "requests" + ".html"  # 保存的文件名
    filename1 = entryname + ".html"  # 保存的文件名
    
    if path.exists(filename):  # 检查文件是否存在，若存在就跳过(避免重复文件)
        continue

    print('事件', len(evtable),'-', index + 1, entryname)
    
    response = requests.get(line.strip()) #不strip网址会带上/n导致无法找到词条

    browser.get(line.strip()) #selenium获取网页
    original_window = browser.current_window_handle #记录事件百科的原始标签页
    
    # 打印文本行，去除前后空格换行，http状态码，响应内容长度. 200 means sucessful requests
    #print(entryname, response.status_code, len(response.text))
    
    

# ==============定位元素并提取数据
    
#events表单
    votecount = browser.find_element(By.CLASS_NAME, "vote-count").text #点赞量
    sidebox = browser.find_elements(By.CSS_SELECTOR, 'dl.side-box.lemma-statistics') #右侧表单
    if sidebox:
        viewcount = sidebox[0].find_element(By.ID, "j-lemmaStatistics-pv").text #浏览量
        editurl = sidebox[0].find_element(By.LINK_TEXT, '历史版本').get_attribute('href') #编辑历史的链接
        editcount = sidebox[0].find_element(By.CSS_SELECTOR,'dd:nth-child(2) > ul > li:nth-child(2)').text[5:][:-5]#编辑次数
    else:
        viewcount = -99 #浏览量
        editurl = 'NA' #编辑历史的链接
        editcount = -99 #编辑次数
    #print('历史编辑次数',editcount,'次')

#编辑历史表单
    if int(editcount) > 0: #有编辑历史则继续
        editpage_nos = math.ceil(int(editcount)/25) #通过向上取整确定编辑历史的页面数量
        for num in range(1,editpage_nos+1):
            histo_url = editurl + '#page' + str(num)
            edit_jsscript = '''window.open("'''+ histo_url + '''", 'new_window')''' 
            browser.execute_script(edit_jsscript) #打开新标签页，进入编辑历史的网页
            browser.switch_to.window(browser.window_handles[-1]) #切换窗口
            time.sleep(1)
            #一直等待到元素可见
            wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.TAG_NAME, 'td')))
            versions = browser.find_elements(By.TAG_NAME, 'td')
            lst = [td.text for td in versions]
            #print(lst)
            browser.close() #关闭当前的编辑历史标签页
            browser.switch_to.window(original_window) #回到原初的百科页面
            for j in range(0,int(len(lst)/4)):
                #update_time = lst[4*j]
                #author_name = lst[4*j+1]
                #编辑历史写入sql
                version_values = (event_id, eventname, year, entryname, editcount, 25*(num-1)+j+1, lst[4*j+1], 'contributor_id', 
                                  lst[4*j], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))         
                c.execute(''' INSERT INTO edithistory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', version_values)
                conn.commit()
      
    
    print('编辑历史表单done')
conn.close()
browser.quit()