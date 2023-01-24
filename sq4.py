#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 20:12:35 2023

@author: zhangsiqi
"""


# -*- coding: utf-8 -*-
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

evtable = pd.read_excel('events.xlsx')


# 创建sql数据库
conn= sqlite.connect('wikitest.sqlite')
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
actions = ActionChains(browser)

# 定义一个捕捉元素时出现StaleElementReferenceException异常后重试的装饰器
@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, name):
    print('尝试获取元素',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),name)
    targets = driver.find_element(By.CLASS_NAME, name)
    print('获取元素成功')
    return targets
    

#x = 1 #dataframe行序号

cookies = {
    'zhishiTopicRequestTime': '1661827301845',
    'BIDUPSID': '3C3CB214132757685D3A8221F479E496',
    'PSTM': '1537443294',
    '__yjs_duid': '1_bc4c7ccdc417b0e5aa90b36df028fef81620385718241',
    'ZFY': 'uPTMDrpQRQHF:AEN5a:ASY6P6wQI3Zi0w8cn:BKlLBBynY:C',
    'BAIDUID': '01F1FC0AFD7C78051DA2019A1CCE5CDB:SL=0:NR=10:FG=1',
    'BAIDUID_BFESS': '01F1FC0AFD7C78051DA2019A1CCE5CDB:SL=0:NR=10:FG=1',
    'BDUSS': 'VBTWpONWttLXloRWYwNlZSbVhoczZOVy1ZWnlxNDVkMjV3TmtUa3piWER-eFZqRVFBQUFBJCQAAAAAAAAAAAEAAADwRVAb1Ma25Of3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMNy7mLDcu5iY1',
    'BDUSS_BFESS': 'VBTWpONWttLXloRWYwNlZSbVhoczZOVy1ZWnlxNDVkMjV3TmtUa3piWER-eFZqRVFBQUFBJCQAAAAAAAAAAAEAAADwRVAb1Ma25Of3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMNy7mLDcu5iY1',
    'Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a': '1661251662',
    'H_WISE_SIDS': '110085_179347_180636_188745_194529_196428_197471_204427_204906_209568_210321_211435_212296_212867_212967_213028_213357_215727_216374_216715_216841_216941_217084_217167_218315_218567_218620_219404_219558_219942_219946_220639_221121_221479_221502_221697_221734_221874_221915_221920_222299_222335_222397_222466_222522_222539_222605_222617_222620_222625_222780_222845_222862_223064_223144_223192_223218_223238_223343_223374_223474_223769_223844_223898_223906_223917_224055_224080_224086_224099_224116_224159_224196_224261_224267_224429_224438_224754_224801_224980_225332_225373_225436_225515_225736_225917_226049',
    'BK_SEARCHLOG': '%7B%22key%22%3A%5B%22%E9%A6%99%E6%B8%AF%E5%8D%A0%E9%A2%86%E4%B8%AD%E7%8E%AF%22%2C%22%E9%A6%99%E6%B8%AF%20%E5%8D%A0%E9%A2%86%20%E4%B8%AD%E7%8E%AF%22%2C%22%E9%A6%99%E6%B8%AF%20%E4%B8%AD%E7%8E%AF%22%2C%22MH370%22%2C%223%C2%B78%E9%A9%AC%E6%9D%A5%E8%A5%BF%E4%BA%9A%E8%88%AA%E7%8F%AD%E5%A4%B1%E8%B8%AA%E4%BA%8B%E4%BB%B6%22%2C%22%E9%A6%99%E6%B8%AF%E5%A5%B6%E7%B2%89%E9%99%90%E8%B4%AD%22%2C%22%E5%A5%B6%E7%B2%89%E9%99%90%E8%B4%AD%E4%BB%A4%22%2C%22%E5%88%98%E9%93%81%E7%94%B7%E6%A1%88%22%2C%229%C2%B718%E7%94%98%E8%82%83%E5%88%9D%E4%B8%AD%E7%94%9F%E5%8F%91%E5%B8%96%E8%A2%AB%E5%88%91%E6%8B%98%22%2C%229%C2%B717%E7%94%98%E8%82%83%E5%88%9D%E4%B8%AD%E7%94%9F%E5%8F%91%E5%B8%96%E8%A2%AB%E5%88%91%E6%8B%98%E4%BA%8B%E4%BB%B6%22%2C%223%C2%B74%E9%95%BF%E6%98%A5%E7%9B%97%E8%BD%A6%E6%9D%80%E5%A9%B4%E6%A1%88%22%2C%22%E6%B5%B7%E5%8D%97%E5%B9%BC%E5%A5%B3%E5%BC%80%E6%88%BF%E6%A1%88%22%2C%22%E6%A0%A1%E9%95%BF%E5%B8%A6%E5%A5%B3%E7%94%9F%E5%BC%80%E6%88%BF%E6%A1%88%22%2C%22%E9%BE%9A%E7%88%B1%E7%88%B1%E6%A1%88%22%2C%22%E9%BE%9A%E7%88%B1%E7%88%B1%22%2C%22%E9%99%95%E8%A5%BF%20%E6%88%BF%E5%A7%90%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%E6%A1%88%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%20%E6%AD%BB%E5%88%91%22%2C%22%E9%BB%84%E6%B5%A6%E6%B1%9F%E6%AD%BB%E7%8C%AA%E4%BA%8B%E4%BB%B6%22%5D%7D',
    'H_WISE_SIDS_BFESS': '110085_179347_180636_188745_194529_196428_197471_204427_204906_209568_210321_211435_212296_212867_212967_213028_213357_215727_216374_216715_216841_216941_217084_217167_218315_218567_218620_219404_219558_219942_219946_220639_221121_221479_221502_221697_221734_221874_221915_221920_222299_222335_222397_222466_222522_222539_222605_222617_222620_222625_222780_222845_222862_223064_223144_223192_223218_223238_223343_223374_223474_223769_223844_223898_223906_223917_224055_224080_224086_224099_224116_224159_224196_224261_224267_224429_224438_224754_224801_224980_225332_225373_225436_225515_225736_225917_226049',
    'ZD_ENTRY': 'google',
    'baikeVisitId': 'f76e8aba-797e-47b9-9a6f-d857e5bf79e9',
    'RT': '"z=1&dm=baidu.com&si=lmtcvn6ru09&ss=l7fl2fhf&sl=2&tt=22k&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=2k5&ul=13ofl"',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'zhishiTopicRequestTime=1661827301845; BIDUPSID=3C3CB214132757685D3A8221F479E496; PSTM=1537443294; __yjs_duid=1_bc4c7ccdc417b0e5aa90b36df028fef81620385718241; ZFY=uPTMDrpQRQHF:AEN5a:ASY6P6wQI3Zi0w8cn:BKlLBBynY:C; BAIDUID=01F1FC0AFD7C78051DA2019A1CCE5CDB:SL=0:NR=10:FG=1; BAIDUID_BFESS=01F1FC0AFD7C78051DA2019A1CCE5CDB:SL=0:NR=10:FG=1; BDUSS=VBTWpONWttLXloRWYwNlZSbVhoczZOVy1ZWnlxNDVkMjV3TmtUa3piWER-eFZqRVFBQUFBJCQAAAAAAAAAAAEAAADwRVAb1Ma25Of3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMNy7mLDcu5iY1; BDUSS_BFESS=VBTWpONWttLXloRWYwNlZSbVhoczZOVy1ZWnlxNDVkMjV3TmtUa3piWER-eFZqRVFBQUFBJCQAAAAAAAAAAAEAAADwRVAb1Ma25Of3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMNy7mLDcu5iY1; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1661251662; H_WISE_SIDS=110085_179347_180636_188745_194529_196428_197471_204427_204906_209568_210321_211435_212296_212867_212967_213028_213357_215727_216374_216715_216841_216941_217084_217167_218315_218567_218620_219404_219558_219942_219946_220639_221121_221479_221502_221697_221734_221874_221915_221920_222299_222335_222397_222466_222522_222539_222605_222617_222620_222625_222780_222845_222862_223064_223144_223192_223218_223238_223343_223374_223474_223769_223844_223898_223906_223917_224055_224080_224086_224099_224116_224159_224196_224261_224267_224429_224438_224754_224801_224980_225332_225373_225436_225515_225736_225917_226049; BK_SEARCHLOG=%7B%22key%22%3A%5B%22%E9%A6%99%E6%B8%AF%E5%8D%A0%E9%A2%86%E4%B8%AD%E7%8E%AF%22%2C%22%E9%A6%99%E6%B8%AF%20%E5%8D%A0%E9%A2%86%20%E4%B8%AD%E7%8E%AF%22%2C%22%E9%A6%99%E6%B8%AF%20%E4%B8%AD%E7%8E%AF%22%2C%22MH370%22%2C%223%C2%B78%E9%A9%AC%E6%9D%A5%E8%A5%BF%E4%BA%9A%E8%88%AA%E7%8F%AD%E5%A4%B1%E8%B8%AA%E4%BA%8B%E4%BB%B6%22%2C%22%E9%A6%99%E6%B8%AF%E5%A5%B6%E7%B2%89%E9%99%90%E8%B4%AD%22%2C%22%E5%A5%B6%E7%B2%89%E9%99%90%E8%B4%AD%E4%BB%A4%22%2C%22%E5%88%98%E9%93%81%E7%94%B7%E6%A1%88%22%2C%229%C2%B718%E7%94%98%E8%82%83%E5%88%9D%E4%B8%AD%E7%94%9F%E5%8F%91%E5%B8%96%E8%A2%AB%E5%88%91%E6%8B%98%22%2C%229%C2%B717%E7%94%98%E8%82%83%E5%88%9D%E4%B8%AD%E7%94%9F%E5%8F%91%E5%B8%96%E8%A2%AB%E5%88%91%E6%8B%98%E4%BA%8B%E4%BB%B6%22%2C%223%C2%B74%E9%95%BF%E6%98%A5%E7%9B%97%E8%BD%A6%E6%9D%80%E5%A9%B4%E6%A1%88%22%2C%22%E6%B5%B7%E5%8D%97%E5%B9%BC%E5%A5%B3%E5%BC%80%E6%88%BF%E6%A1%88%22%2C%22%E6%A0%A1%E9%95%BF%E5%B8%A6%E5%A5%B3%E7%94%9F%E5%BC%80%E6%88%BF%E6%A1%88%22%2C%22%E9%BE%9A%E7%88%B1%E7%88%B1%E6%A1%88%22%2C%22%E9%BE%9A%E7%88%B1%E7%88%B1%22%2C%22%E9%99%95%E8%A5%BF%20%E6%88%BF%E5%A7%90%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%E6%A1%88%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%20%E6%AD%BB%E5%88%91%22%2C%22%E9%BB%84%E6%B5%A6%E6%B1%9F%E6%AD%BB%E7%8C%AA%E4%BA%8B%E4%BB%B6%22%5D%7D; H_WISE_SIDS_BFESS=110085_179347_180636_188745_194529_196428_197471_204427_204906_209568_210321_211435_212296_212867_212967_213028_213357_215727_216374_216715_216841_216941_217084_217167_218315_218567_218620_219404_219558_219942_219946_220639_221121_221479_221502_221697_221734_221874_221915_221920_222299_222335_222397_222466_222522_222539_222605_222617_222620_222625_222780_222845_222862_223064_223144_223192_223218_223238_223343_223374_223474_223769_223844_223898_223906_223917_224055_224080_224086_224099_224116_224159_224196_224261_224267_224429_224438_224754_224801_224980_225332_225373_225436_225515_225736_225917_226049; ZD_ENTRY=google; baikeVisitId=f76e8aba-797e-47b9-9a6f-d857e5bf79e9; RT="z=1&dm=baidu.com&si=lmtcvn6ru09&ss=l7fl2fhf&sl=2&tt=22k&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=2k5&ul=13ofl"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

# q = open("addresstest.txt")
# qcount = len(q.readlines())
# q.close()

#for line in open("addresstest.txt"):
for index, row in evtable.iterrows():
    # print('line',line.strip())
    line = row['url']
    year = row['year']
    eventname = row['event']
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
    
    response = requests.get(line.strip(), cookies=cookies, headers=headers) #不strip网址会带上/n导致无法找到词条

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
    
    # 一级目录 
    toc1s = browser.find_elements(By.CLASS_NAME,"level1") 
    toc1s_li = [toc1.text for toc1 in toc1s if toc1.text]
    toc1text = '\n'.join(toc1s_li)
    #print(toc1text)
    # 所有目录
    tocs = browser.find_elements(By.XPATH,'//li[contains(@class,"level")]') # table of contents, complete
    tocs_li = [toc.text for toc in tocs if toc.text]
    tocstext = '\n'.join(tocs_li)
    #print(tocstext)
    #print('目录拼接完成')
    
    
#突出贡献用户表单
# div.side-content > dl > dd.description.excellent-description > ul > li
# div.side-content > dl > dd.description.excellent-description > ul > li:nth-child(2)
# div.side-content > dl > dd.description.excellent-description > ul > li:nth-child(1)


    topeditors = browser.find_elements(By.CSS_SELECTOR,'div.side-content > dl > dd.description.excellent-description > ul > li')
    if topeditors:
        for editor in topeditors:
            editor_name = editor.find_element(By.CLASS_NAME, 'usercard').text #用户名
            editor_id = editor.find_element(By.CLASS_NAME, 'usercard').get_attribute('data-uid') #用户id
            contris = editor.find_element(By.CLASS_NAME, 'right').find_elements(By.TAG_NAME, 'img')
            editor_contri = [contri.get_attribute('title') for contri in contris] # 用户贡献的类型
            #print(editor_contri)
            # 写入sql
            editor_values = (index + 46, eventname, year, entryname, editor_name, editor_id, str(editor_contri),
                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #最后的列表要转化为字符串
            c.execute(''' INSERT INTO topeditor VALUES (?, ?, ?, ?, ?, ?, ?, ?) ''', editor_values)
            conn.commit()
    print('突出贡献表单done')
        

    # excelluser = browser.find_elements(By.CLASS_NAME, "excellent-description")
    # if excelluser:
    #     topeditors = excelluser[0].find_elements(By.TAG_NAME,'li')
    #     for editor in topeditors:
    #         editor_name = editor.find_element(By.CLASS_NAME, 'usercard').text #用户名
    #         editor_id = editor.find_element(By.CLASS_NAME, 'usercard').get_attribute('data-uid') #用户id
    #         contris = editor.find_element(By.CLASS_NAME, 'right').find_elements(By.TAG_NAME, 'img')
    #         editor_contri = [contri.get_attribute('title') for contri in contris] # 用户贡献的类型
    #         #print(editor_contri)
        
    #         # 写入sql
    #         editor_values = (entryname, editor_name, editor_id, str(editor_contri),
    #                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #最后的列表要转化为字符串
    #         c.execute(''' INSERT INTO topeditor VALUES (?, ?, ?, ?, ?) ''', editor_values)
    #         conn.commit()
    # else:
    #     topeditors = []
    #print('突出贡献用户表单done')
#文字内容表单
    #paras = browser.find_elements(By.CSS_SELECTOR,'div.para')
    # titles = browser.find_elements(By.XPATH,'//*[@class="title-text"]') #这个是所有的次级标题，但是多了两个【分享你的世界】
    # for title in titles:
    #     print(title.text)
    # para1 = browser.find_elements(By.XPATH,'//*[@class="para"]')
    # for para1s in para1:
    #     print(para1s.text)
    # paratests = browser.find_elements(By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/div') #这个是为了剔除表格单独成段
    # paratexts = [paratest.text for paratest in paratests if paratest.text]
    #content_sum = browser.find_element(By.XPATH,'//div[@class="lemma-summary"]').text #事件简介文字,成功版本
    #paras = browser.find_elements(By.XPATH,'//div[@class="para"]') #success
    content_sum = browser.find_element(By.CSS_SELECTOR,'div.lemma-summary').text #事件简介文字
    paras = browser.find_elements(By.CSS_SELECTOR,'div.para')
    #paratest = browser.find_elements(By.CSS_SELECTOR,'div.main-content.J-content.main-content-margin > div:nth-child')
    paratext = [para.text for para in paras if para.text]
    contents = '\n'.join(paratext)
    #print('正文拼接完成')
    #记录有引用的段落，可是有的表格被单独成段了
    for para in paras:
        if para.text:
            cited = para.find_elements(By.CSS_SELECTOR,'sup.sup--normal') #找到段落中的引用角标
            cited_items = [cite.text for cite in cited]
            # 写入sql
            wikitext_values = (index + 46, eventname, year, entryname, para.text, len(cited), '; '.join(cited_items), 
                               datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #最后的列表要转化为字符串
            c.execute(''' INSERT INTO wikitext VALUES (?, ?, ?, ?, ?, ?, ?, ?) ''', wikitext_values)
            conn.commit()
    print('文字内容表单done')
#百科正文中的内链表单
    table_links = browser.find_elements(By.CSS_SELECTOR, 'a[target="_blank"][href^="/item/"][data-log="info"]')
    summ_links = browser.find_elements(By.CSS_SELECTOR, 'a[target="_blank"][href^="/item/"][data-log="summary"]')
    body_links = browser.find_elements(By.CSS_SELECTOR, 'a[target="_blank"][href^="/item/"][data-log="text"]')
    
    lis = [table_links, summ_links, body_links]
    wiki_links = [i for li in lis for i in li]
    
    for linkindex, wiki_link in enumerate(wiki_links, start = 1):
        # 写入sql
        wikilink_values = (index + 46, eventname, year, entryname, len(wiki_links), linkindex, wiki_link.text, wiki_link.get_attribute('href'), 
                           datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        c.execute(''' INSERT INTO link VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ''', wikilink_values)
        conn.commit()
    #print('wikialllink查找完毕')

    print('百科内链表单done')
#参考资料表单    
    #extract references 不能分开抓序号、标题这些，因为有些为空 
    references = browser.find_elements(By.CLASS_NAME, 'reference-item')
    #read_more_btn = browser.find_elements(By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/dl/dd[2]/span[1]') #success
    read_more_btn = browser.find_elements(By.CSS_SELECTOR,'dd.toggle > span.text.expand-text')
    if read_more_btn:
        read_more_btn[0].click()
        time.sleep(1.5)
    
    if references:
        for ref in references:
            ref_index = ref.find_element(By.CLASS_NAME,'index').text #参考资料序号
            # if ref_index:
            #     print(ref_index)
            reference_text = ref.text[5:] #参考资料所有文字
            
            if '．20' in reference_text:
                source_timeli = re.findall(r'．20[0-9-]{8}', reference_text)
                if source_timeli:
                    source_time = source_timeli[0][1:] #参考资料日期
                else:
                    source_timeli1 = re.findall(r'．20[0-9-]{7}', reference_text)
                    if source_timeli1:
                        source_time = source_timeli1[0][1:]
                    else:
                        source_time = 'Error'
            else:
                source_time = 'NA'
            #print(source_time)
            
            if '[引用日期' in reference_text:
                cite_time = reference_text[-11:-1] #引用日期
            else:
                cite_time = 'NA'
            #print(cite_time)
            #cite_time = ref.find_element(By.CL)
            
            ref_title = ref.find_element(By.CLASS_NAME,'text').text.strip('．') #参考资料标题
            ref_url = ref.find_element(By.CLASS_NAME,'text').get_attribute('href')#百科的参考资料页面的链接
            ref_links = ref.find_elements(By.CLASS_NAME,'wiki-lemma-icons_reference-link') #找到百科的参考资料页面的链接
            
            if ref_links: # 判断参考资料为网页，提取网页相关字段
                
                ref_site = ref.find_elements(By.CLASS_NAME,'site') #参考资料网站名字
                if ref_site:
                    reference_site = ref_site[0].text.strip('．')
                else:
                    reference_site = 'NA'
                    
                ref_link = ref_links[0]
                ref_link.click() #点击参考资料链接，打开新标签页
                browser.switch_to.window(browser.window_handles[-1]) #切换到参考资料窗口
                snapshot_urls = browser.find_elements(By.CLASS_NAME,'snapshot')#参考资料的快照截图
                if snapshot_urls:
                    snapshot_url = snapshot_urls[0].get_attribute('src')
                else:
                    snapshot_url = 'NA'
                redirlink = browser.find_element(By.CLASS_NAME,'link').get_attribute('href') #得到链接的redirect链接 
                #print(redirlink) # 参考资料的redirect链接
                # jsscript = '''window.open("'''+ redirlink + '''", 'new_window')''' 
                # browser.execute_script(jsscript) #打开新标签页，进入参考资料的原始网页
                # #time.sleep(0.5)
                # browser.close() #关闭标签页
                # browser.switch_to.window(browser.window_handles[-1]) #切换窗口
                # browser.set_page_load_timeout(50)
                # try:
                #     origilink = browser.current_url #得到原始参考资料的链接
                #     browser.close() #关闭标签页
                # except UnexpectedAlertPresentException:
                #     #origilink = 'Error'
                #     browser.switch_to_alert().accept()
                #     print('原始网页错误', redirlink)
                # except selenium.common.exceptions:
                #     print('原始网页错误', redirlink, '错误为',selenium.common.exceptions)
                #     browser.execute_script('window.stop()')
  
                # #print('origilink', origilink)
                #time.sleep(0.5)
                browser.close() #关闭标签页
                browser.switch_to.window(original_window) #回到原初的百科页面
                time.sleep(1)
                
                # try:
                #     response = requests.get(origilink, cookies=cookies, headers=headers, timeout=40)
                # except requests.ConnectionError:
                #     print("OOPS!! Connection Error")
                #     status_code = 'Connection Error'
                # except requests.Timeout:
                #     print("OOPS!! Timeout Error")
                #     status_code = 'Timeout Error'
                # except requests.RequestException:
                #     print("OOPS!! General Error")
                #     status_code = 'General Error'
                # else:
                #     status_code = response.status_code #参考资料的状态码
                # # finally:
                # #     print('http状态码', status_code) 
            else:
                reference_site = 'NA'
                snapshot_url = 'NA'
                redirlink = 'NA'
        # 如果这个页面是有效的，继续抓文字，如果无效的，返回左边的标签页保存下图片
            origilink = '' #先空着吧
            status_code = '' #先空着吧
            #写入参考资料表单
            ref_values = (index + 46, eventname, year, entryname, len(references), ref_index, reference_text, ref_title, ref_url,
                          reference_site, source_time, cite_time, redirlink, origilink, status_code, snapshot_url,
                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            #print('准备写入sql')
            c.execute(''' INSERT INTO citations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', ref_values)
            conn.commit()
            #print('写入完毕')
    print('参考资料表单done')   
#编辑历史表单
    if int(editcount) > 0:
        editpage_nos = math.ceil(int(editcount)/25) #通过向上取整确定编辑历史的页面数量
     
        for num in range(1,editpage_nos+1):
            #print(num)
            histo_url = editurl + '#page' + str(num)
            #histo_url = editurl
            #print(histo_url)
            edit_jsscript = '''window.open("'''+ histo_url + '''", 'new_window')''' 
            browser.execute_script(edit_jsscript) #打开新标签页，进入编辑历史的网页
            browser.switch_to.window(browser.window_handles[-1]) #切换窗口
            time.sleep(1.5)
            #一直等待到元素可见
            wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
            versions = browser.find_elements(By.TAG_NAME, 'tr')
            
            for m, version in enumerate(versions[1:], start = 1):
                
                submit_time = get_elements(version, 'submitTime').text
                contri_card = get_elements(version, 'uname')
                contributor_name = contri_card.text
                contributor_id = contri_card.get_attribute('data-uid')
               
                # submit_time = version.find_element(By.CLASS_NAME, 'submitTime').text
                # contributor_name = version.find_element(By.CLASS_NAME, 'uname').text
                # contributor_id = version.find_element(By.CLASS_NAME, 'uname').get_attribute('data-uid')
       
                version_values = (index + 46, eventname, year, entryname, editcount, 25*(num-1)+m, contributor_name, contributor_id, 
                                  submit_time, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                #print('本次编辑历史准备写入sql')
                c.execute(''' INSERT INTO edithistory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', version_values)
                conn.commit()
                #print('本次编辑历史写入完毕')
            browser.close() #关闭当前的编辑历史标签页
            browser.switch_to.window(original_window) #回到原初的百科页面
    
    
    # finalpage = browser.find_element(By.XPATH,'//a[contains(@class,"pTag") and contains(@class,"last")]').get_attribute('p-index')
    # print('尾页页码',finalpage)
    print('编辑历史表单done')      
#写入相关类目表单
    reboxes= browser.find_elements(By.CSS_SELECTOR,'div.rslazy.rs-container')
    if reboxes:
        relevance = 1
    #     rele_more_btn = browser.find_elements(By.CSS_SELECTOR,'a.title-folder.title-folder-close')
    #     if rele_more_btn:
    #         #rele_more_btn[0].click() #这个点击会报错
    #         browser.execute_script("arguments[0].click();", rele_more_btn[0])
    #         time.sleep(1.5)
    #     allitemcount = []
    #     for box_index, rebox in enumerate(reboxes, start = 1):
    #         boxname = rebox.find_element(By.CLASS_NAME,'relation-table-title').text
    #         boxitems = rebox.find_elements(By.CSS_SELECTOR,'a.link-inner')
    #         if boxitems:
    #             allitemcount.append(len(boxitems))
    #             for item_index, item in enumerate(boxitems, start = 1):
    #                 rele_values = (index + 46, eventname, year, entryname, len(reboxes), box_index, boxname, len(boxitems), 
    #                                item_index, item.text, item.get_attribute('href'), 
    #                                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #                 c.execute(''' INSERT INTO relevance VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', rele_values)
    #                 conn.commit()
    #     releitem_count = sum(allitemcount)
    else:
          relevance = 0
    print('相关类目表单done')
    
#写入学术论文表单
    sciences= browser.find_elements(By.CSS_SELECTOR,'li.sciencePaper-item')
    if sciences:
        for sci_index, sci in enumerate(sciences, start = 1):
            sci_author = sci.find_element(By.CSS_SELECTOR,'span.interrupt.authors').text[:-1]
            sci_title = sci.find_element(By.CSS_SELECTOR,'span.interrupt.title').text[:-1]
            sci_journal = sci.find_element(By.CSS_SELECTOR,'span.interrupt.publishedAt').text
            sci_year = sci.find_element(By.CSS_SELECTOR,'span.interrupt.time').text
            sci_link = sci.find_element(By.CSS_SELECTOR,'a.text-link').get_attribute('href')
            #写入sql
            sci_values = (index + 46, eventname, year, entryname, len(sciences), sci_index, sci_author, sci_title, sci_journal, 
                      sci_year, sci_link, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            c.execute(''' INSERT INTO science VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', sci_values)
            conn.commit()      
    print('学术论文表单done')
    
#写入事件表单
    event_values = (index + 46, eventname, year, entryname, line, viewcount, votecount, len(topeditors), editcount, editurl, 
              toc1text, len(toc1s_li), tocstext, len(references), content_sum, contents, len(wiki_links), 
              len(sciences), relevance, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    c.execute(''' INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', event_values)
    conn.commit()      
    print('事件表单done')
    
    # 写入数据框
    #df.loc[x] = [entryname, viewcount, votecount, len(topeditors), editcount, editurl, toctext]
    
    #x += 1 #序号+1
    
    # 保存百科事件的html。因为可能会返回空文件，检查响应内容长度，大于800，再保存html文件
    if len(response.text) > 800 and response.status_code == 200:
        with open(filename1, "w", encoding='utf-8') as g: #selenium方式保存的html
            g.write(browser.page_source)
    
            #f.close()
            g.close()
    
    # 等待数秒继续下一个
    time.sleep(4)

browser.quit()

#将sqlite的表单写入到多张csv
def sql2csv(table_name, sqldb):
    table = pd.read_sql_query('SELECT * FROM '+ table_name, sqldb)
    table.index += 1
    table.to_csv(table_name+'sql.csv', index=True)

sql2csv('events',conn)
sql2csv('citations',conn)
sql2csv('edithistory',conn)
sql2csv('link',conn)
sql2csv('topeditor',conn)
sql2csv('wikitext',conn)
sql2csv('science',conn)
#sql2csv('relevance',conn)

#df.to_csv('3event.csv')

conn.close()
