#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 11:14:41 2023

@author: zhangsiqi
"""

# -*- coding: utf-8 -*-
#%% 导入模块
from urllib.parse import unquote
from urllib.parse import urlparse
import requests
from os import path
import time
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
import numpy as np
import pandas as pd
import re
import sqlite3 as sqlite
import math
import datetime
import os
#import pyttsx3


os.chdir('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0210补充事件时间')

#%% 读取、创建数据库等
evtable = pd.read_excel('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0210补充事件时间/events+timestamp+evtype+range.xlsx')
evtable1 = evtable
entryall = evtable['entry'].unique().tolist()


# 创建sql数据库
#sqname = 'BaiduWiki['+ datetime.datetime.now().strftime('%m-%d-%H:%M].sqlite')
os.chdir('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0214补充词条数据')
conn= sqlite.connect("/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1.sqlite")
c = conn.cursor()

# #合并新加的history
# dfediadd = pd.read_sql('SELECT * FROM test_add_his', conn)
# dfediadd1 = pd.read_sql('SELECT * FROM test_add_his1', conn)
# dfediadd2 = pd.read_sql('SELECT * FROM test_add_his2', conn)
# dfediadd3 = pd.read_sql('SELECT * FROM test_add_his3', conn)
# dfediadd4 = pd.read_sql('SELECT * FROM test_add_his4', conn)
# dfediadd5 = pd.read_sql('SELECT * FROM test_add_his5', conn)
# dfediadd6 = pd.read_sql('SELECT * FROM test_add_his6', conn)
# dfediadd7 = pd.read_sql('SELECT * FROM test_add_his7', conn)
# dfediadd8 = pd.read_sql('SELECT * FROM test_add_his8', conn)
# dfediadd9 = pd.read_sql('SELECT * FROM test_add_his9', conn)
# dfediadd10 = pd.read_sql('SELECT * FROM test_add_his10', conn)

# dfediadd_all = pd.concat([dfediadd,dfediadd1,dfediadd2,dfediadd3,dfediadd4,dfediadd5,dfediadd6,dfediadd7,dfediadd8,dfediadd9,dfediadd10])

# #14955条 14955+2773=17728
# for index, row in dfediadd_all.iterrows():
#     hist_row_values = (row['entry'], row['edit_entryindex'], row['author_name'], row['update_time'],row['edit_time'])
#     c.execute(''' INSERT INTO edit_time (entry, edit_entryindex, author_name, update_time, edit_time) VALUES (?, ?, ?, ?, ?)''', hist_row_values)
#     conn.commit()


dfedi = pd.read_sql('SELECT * FROM edit_time', conn)
dfedi_ev = dfedi['entry'].unique().tolist()

dfev = pd.read_sql('SELECT * FROM events', conn)
dfev_ev = dfev['entry'].unique().tolist()


#%%% 参考资料表单
# c.execute('''ALTER TABLE ci ADD COLUMN type''') #新增type字段
          
# # #%%% 事件表单
# c.execute('''CREATE TABLE IF NOT EXISTS events 
#           (entryindex, event_id int, event text, year, entry text, baikelink text, viewcount int, votecount int, 
#             topeditor_count int, editcount int, editurl text,
#             toc_level1 text, toclevel1_count int, tocs text, reference_count int,
#             summary text, para_content text, link_count int, sci_paper_count int, 
#             relevant int, collect_time)''')
# #%%% 参考资料表单
# c.execute('''CREATE TABLE IF NOT EXISTS citations
#           (entryindex, event_id int, event text, year, entry text, reference_count int, reference_entryindex, 
#             reference_text text, reference_title text, 
#             reference_url text, reference_site text, source_time, cite_time, redir_url text, original_url text, 
#             status_code text, snapshot_url text, collect_time)''')
# #%%% 编辑历史表单
# c.execute('''CREATE TABLE IF NOT EXISTS edithistory
#           (entryindex, event_id int, event text, year, entry text, edit_count, edit_entryindex, author_name text, 
#             update_time, collect_time)''')
# #%%% 百科内链表单
# c.execute('''CREATE TABLE if NOT EXISTS wikilink 
#           (entryindex, event_id int, event text, year, entry text, link_count int, link_entryindex, link_name text, 
#             link_url text, collect_time)''')
# #%%% 突出贡献表单
# c.execute('''CREATE TABLE if NOT EXISTS topeditor
#           (entryindex, event_id int, event text, year, entry text, editor_name text, editor_id int,
#             contribution text, collect_time)''')
# #%%% 文内引用表单
# c.execute('''CREATE TABLE if NOT EXISTS wikitext
#           (entryindex, event_id int, event text, year, entry text, wiki_text text, cited_count int,
#             cited_item text, collect_time)''')
# #%%% 学术论文表单
# c.execute('''CREATE TABLE if NOT EXISTS science
#           (entryindex, event_id int, event text, year, entry text, sci_count int, sci_entryindex, sci_author text,
#             sci_title text, sci_joural text, sci_year, sci_link text, collect_time)''')
# #%%% 相关知识表单
# c.execute('''CREATE TABLE if NOT EXISTS relevance
#           (entryindex, event_id int, event text, year, entry text, rebox_count int, rebox_entryindex, rebox_name text, 
#             reitem_count int, reitem_entryindex, reitem_name text, reitem_link text, collect_time)''')
          
# 定义一个捕捉元素时出现StaleElementReferenceException异常后重试的装饰器
@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(2))
def get_elements(driver, method, name):
    #print('尝试获取元素',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),name)
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i.text for i in targets]

# 定义一个捕捉元素时出现StaleElementReferenceException异常后重试的装饰器
@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(3))
def click_elements(driver, method, name):
    #print('尝试获取元素',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),name)
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i for i in targets]

#%% 爬虫循环开始
browser = webdriver.Chrome(executable_path = 'chromedriver')

#%%% 事件表单第一部分
#根据词条网址获取网页内容
#for index, row in evtable.iterrows():
for index, row in evtable1.iterrows():
    # print('line',line.strip())
    line = row['baikelink']
    year = row['year']
    eventname = row['event']
    event_id = row['event_id']
    wangzhi = urlparse(line.strip()) #从URL中解析出各个部分
    entryname = unquote(wangzhi[2][6:]) #从解析结果中提取出事件内容部分并且转成中文给html文件命名，
    #命名中的斜杠要删除,否则后面新建html有问题
    if '/' in entryname:
        entryname = entryname.split('/')[0]

    filename = entryname + ".html"  # 保存的文件名
    # if path.exists(filename):  # 检查文件是否存在，若存在就跳过(避免重复文件)
    #     continue
    if entryname in dfev_ev:#如果sqlite的数据出现在eatable中，则跳过
        continue
    if entryname in dfedi_ev: #如果该词条已经收录在sqlite的编辑历史数据表中，则跳过
        continue
    
    print('事件', len(evtable),'-', index + 1, entryname)

    browser.get(line.strip()) #selenium获取网页
    original_window = browser.current_window_handle #记录事件百科的原始标签页
    
    votecount = browser.find_element(By.CLASS_NAME, "vote-count").text #点赞量
    sidebox = browser.find_elements(By.CSS_SELECTOR, 'dl.side-box.lemma-statistics') #右侧表单
    if sidebox:
        viewcount = sidebox[0].find_element(By.ID, "j-lemmaStatistics-pv").text #浏览量
        editurl = sidebox[0].find_element(By.LINK_TEXT, '历史版本').get_attribute('href') #编辑历史的链接
        editcount = sidebox[0].find_element(By.CSS_SELECTOR,'dd:nth-child(2) > ul > li:nth-child(2)').text[5:][:-5]#编辑次数
    else:
        viewcount = -99 #浏览量
        editurl = None #编辑历史的链接
        editcount = -99 #编辑次数
    
    #一级目录 
    toc1s = browser.find_elements(By.CLASS_NAME,"level1") 
    toc1s_li = [toc1.text for toc1 in toc1s if toc1.text]
    toc1text = '\n'.join(toc1s_li)

    #所有目录
    tocs = browser.find_elements(By.XPATH,'//li[contains(@class,"level")]') # table of contents, complete
    tocs_li = [toc.text for toc in tocs if toc.text]
    tocstext = '\n'.join(tocs_li)
    
#%%% 突出贡献表单
    topeditors = browser.find_elements(By.CSS_SELECTOR,'div.side-content > dl > dd.description.excellent-description > ul > li')
    if topeditors:
        for editor in topeditors:
            editor_name = editor.find_element(By.CLASS_NAME, 'usercard').text #用户名
            editor_id = editor.find_element(By.CLASS_NAME, 'usercard').get_attribute('data-uid') #用户id
            contris = editor.find_element(By.CLASS_NAME, 'right').find_elements(By.TAG_NAME, 'img')
            editor_contri = [contri.get_attribute('title') for contri in contris] # 用户贡献的类型
            # 写入sql
            editor_values = (index + 1, event_id, eventname, year, entryname, editor_name, editor_id, str(editor_contri),
                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #最后的列表要转化为字符串
            c.execute(''' INSERT INTO topeditor (entryindex, event_id, event, year, entry, 
                      editor_name, editor_id,
              contribution, collect_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', editor_values)
            conn.commit()
    print('突出贡献表单done')
        
#%%% 文字内容表单
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
    paratext = [para.text for para in paras if para.text]
    contents = '\n'.join(paratext)
    #记录有引用的段落，可是有的表格被单独成段了
    for para in paras:
        if para.text:
            cited = para.find_elements(By.CSS_SELECTOR,'sup.sup--normal') #找到段落中的引用角标
            cited_items = [cite.text for cite in cited]
            # 写入sql
            wikitext_values = (index + 1, event_id, eventname, year, entryname, para.text, len(cited), '; '.join(cited_items), 
                               datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #最后的列表要转化为字符串
            c.execute(''' INSERT INTO wikitext (entryindex, event_id, event, year, entry,
                      wiki_text, cited_count,
              cited_item, collect_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', wikitext_values)
            conn.commit()
    
    print('文字内容表单done')
    
#%%% 百科内链表单
    table_links = browser.find_elements(By.CSS_SELECTOR, 'a[target="_blank"][href^="/item/"][data-log="info"]')
    summ_links = browser.find_elements(By.CSS_SELECTOR, 'a[target="_blank"][href^="/item/"][data-log="summary"]')
    body_links = browser.find_elements(By.CSS_SELECTOR, 'a[target="_blank"][href^="/item/"][data-log="text"]')
    
    lis = [table_links, summ_links, body_links]
    wiki_links = [i for li in lis for i in li]
    
    for linkindex, wiki_link in enumerate(wiki_links, start = 1):
        # 写入sql
        wikilink_values = (index + 1, event_id, eventname, year, entryname, len(wiki_links), linkindex, wiki_link.text, 
                           wiki_link.get_attribute('href'), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        c.execute(''' INSERT INTO wikilink (entryindex, event_id, event, year, entry, 
                  link_count, link_entryindex, link_name, 
          link_url, collect_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', wikilink_values)
        conn.commit()
        
    print('百科内链表单done')
#%%% 参考资料表单    
    read_more_btn = browser.find_elements(By.CSS_SELECTOR,'dd.toggle > span.text.expand-text')#展开更多参考资料
    if read_more_btn:
        read_more_btn[0].click()
        time.sleep(1.5)
    
    references = browser.find_elements(By.CLASS_NAME, 'reference-item') #不能分开抓序号、标题这些，因为有些为空
    
    if references:
        for ref in references:
            ref_index = ref.find_element(By.CLASS_NAME,'index').text #参考资料序号
            reference_text = ref.text[5:] #参考资料所有文字
            
            #参考资料源日期
            ti = re.search(r'(?<!引用日期)．(?P<y>20[0-2][0-9])[-年\.](?P<m>[0-1]?[0-9])[-月\.](?P<d>[0-3]?[0-9])[日\.\[\s]?', reference_text)
            if ti:
                source_time = ti.groupdict()['y']+'-'+ti.groupdict()['m']+'-'+ti.groupdict()['d']
            else:
                source_time = None
            #引用日期
            if '[引用日期' in reference_text:
                cite_time = reference_text[-11:-1] 
            else:
                cite_time = None
            
            ref_title = ref.find_element(By.CLASS_NAME,'text').text.strip('．') #参考资料标题
            ref_url = ref.find_element(By.CLASS_NAME,'text').get_attribute('href')#百科的参考资料页面的链接
            ref_links = ref.find_elements(By.CLASS_NAME,'wiki-lemma-icons_reference-link') #找到百科的参考资料页面的链接
            ref_type = ref.get_attribute('data-type') #参考资料类型
            
            if ref_type=='1':
#            if ref_links: # 判断参考资料为网页，提取网页相关字段
                ref_site = ref.find_elements(By.CLASS_NAME,'site') #参考资料网站名字
                if ref_site:
                    reference_site = ref_site[0].text.strip('．')
                else:
                    reference_site = None
                    
                ref_link = ref_links[0]
                ref_link.click() #点击参考资料链接，打开新标签页
                browser.switch_to.window(browser.window_handles[-1]) #切换到参考资料窗口
                redirlink = browser.find_element(By.CLASS_NAME,'link').get_attribute('href') #得到原始链接的redirect链接
                origins = browser.find_elements(By.TAG_NAME,'strong') #有的原始链接直接记录在页面了
                if origins:
                    origilink = origins[0].text
                else:
                    origilink = None
                snapshot_urls = browser.find_elements(By.CLASS_NAME,'snapshot')#参考资料的快照截图链接列表
                if snapshot_urls:
                    snapshot_url = snapshot_urls[0].get_attribute('src')
                else:
                    snapshot_url = None
                browser.close() #关闭标签页
                browser.switch_to.window(original_window) #回到原初的百科页面
                time.sleep(1)
            else:
                reference_site = None
                snapshot_url = None
                redirlink = None
                origilink = None

            #写入sql参考资料表单
            ref_values = (index + 1, event_id, eventname, year, entryname, len(references), ref_index, reference_text, ref_title, ref_url,
                          reference_site, source_time, cite_time, redirlink, origilink, None, snapshot_url,
                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ref_type)
            c.execute(''' INSERT INTO ci (entryindex, event_id, event, year, entry, reference_count, reference_entryindex, 
              reference_text, reference_title, reference_url, reference_site, source_time, cite_time, redir_url, original_url, 
              status_code, snapshot_url, collect_time, type) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', ref_values)
    
            conn.commit()
    print('参考资料表单done')
    
#%%% 编辑历史表单
    if int(editcount) > 0: #有编辑历史则继续
        editpage_nos = math.ceil(int(editcount)/25) #通过向上取整确定编辑历史的页面数量
        reflist = []
        for num in range(1,editpage_nos+1):
            histo_url = editurl + '#page' + str(num)
            edit_jsscript = '''window.open("'''+ histo_url + '''", 'new_window')''' 
            browser.execute_script(edit_jsscript) #打开新标签页，进入编辑历史的网页
            browser.switch_to.window(browser.window_handles[-1]) #切换窗口
            time.sleep(1.5)
            #一直等待到元素可见
            wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.TAG_NAME, 'td')))
            lst = get_elements(browser, By.TAG_NAME, 'td')
            #lst = [td.text for td in versions]
            browser.close() #关闭当前的编辑历史标签页
            browser.switch_to.window(original_window) #回到原初的百科页面
            for j in range(0,int(len(lst)/4)):
                #编辑历史写入sql
                version_values = (index + 1, event_id, eventname, year, entryname, editcount, 25*(num-1)+j+1, lst[4*j+1], 
                                  lst[4*j], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                c.execute(''' INSERT INTO edithistory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', version_values)
                conn.commit()
        
    # if int(editcount) > 0: #有编辑历史则继续
    #     editpage_nos = math.ceil(int(editcount)/25) #通过向上取整确定编辑历史的页面数量
    #     for num in range(1,editpage_nos+1):
    #         histo_url = editurl + '#page' + str(num)
    #         edit_jsscript = '''window.open("'''+ histo_url + '''", 'new_window')''' 
    #         browser.execute_script(edit_jsscript) #打开新标签页，进入编辑历史的网页
    #         browser.switch_to.window(browser.window_handles[-1]) #切换窗口
    #         time.sleep(2)
    #         #一直等待到元素可见
    #         wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
    #         versions = browser.find_elements(By.TAG_NAME, 'tr')
            
    #         for m, version in enumerate(versions[1:], start = 1):
    #             submit_time = get_elements(version, 'submitTime').text
    #             contri_card = get_elements(version, 'uname')
    #             contributor_name = contri_card.text
    #             contributor_id = contri_card.get_attribute('data-uid')
    #             #编辑历史写入sql
    #             version_values = (index + 46, eventname, year, entryname, editcount, 25*(num-1)+m, contributor_name, contributor_id, 
    #                               submit_time, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))         
    #             c.execute(''' INSERT INTO edithistory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', version_values)
    #             conn.commit()
    #         browser.close() #关闭当前的编辑历史标签页
    #         browser.switch_to.window(original_window) #回到原初的百科页面
    print('编辑历史表单done')
    
#%%% 相关类目表单
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
    
#%%% 学术论文表单
    sciences= browser.find_elements(By.CSS_SELECTOR,'li.sciencePaper-item')
    if sciences:
        for sci_index, sci in enumerate(sciences, start = 1):
            sci_author = sci.find_elements(By.CSS_SELECTOR,'span.interrupt.authors')
            if sci_author:
                sciauthor = sci_author[0].text[:-1]
            else:
                sciauthor = None
            sci_title = sci.find_elements(By.CSS_SELECTOR,'span.interrupt.title')
            if sci_title:
                scititle = sci_title[0].text[:-1]
            else:
                scititle = None
            sci_journal = sci.find_elements(By.CSS_SELECTOR,'span.interrupt.publishedAt')
            if sci_journal:
                scijournal = sci_journal[0].text
            else:
                scijournal = None
            sci_year = sci.find_elements(By.CSS_SELECTOR,'span.interrupt.time')
            if sci_year:
                sciyear = sci_year[0].text
            else:
                sciyear = None
            sci_link = sci.find_element(By.CSS_SELECTOR,'a.text-link').get_attribute('href')
            #写入sql
            sci_values = (index + 1, event_id, eventname, year, entryname, len(sciences), sci_index, sciauthor, scititle, scijournal, 
                      sciyear, sci_link, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            c.execute(''' INSERT INTO science  (entryindex, event_id, event, year, 
                      entry, sci_count, sci_entryindex, sci_author,
              sci_title, sci_joural, sci_year, sci_link, collect_time) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', sci_values)
                      
            conn.commit()
    print('学术论文表单done')
    
#%%% 事件表单2
    event_values = (index + 1, event_id, eventname, year, entryname, line, viewcount, votecount, len(topeditors), editcount, editurl, 
              toc1text, len(toc1s_li), tocstext, len(references), content_sum, contents, len(wiki_links), 
              len(sciences), relevance, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    c.execute(''' INSERT INTO events (entryindex, event_id, event, year, entry, 
              baikelink, viewcount, votecount, 
      topeditor_count, editcount, editurl,
      toc_level1, toclevel1_count, tocs, reference_count,
      summary, para_content, link_count, sci_paper_count, 
      relevant, collect_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', event_values)
              
    conn.commit()      
    print('事件表单done')
    
    # 保存百科事件的html。因为可能会返回空文件，检查响应内容长度，大于800，再保存html文件
    response = requests.get(line.strip()) #不strip网址会带上/n导致无法找到词条
    if len(response.text) > 800 and response.status_code == 200:
        with open(filename, "w", encoding='utf-8') as g: #selenium方式保存的html
            g.write(browser.page_source)
            g.close()
    
    # 等待数秒继续下一个
    time.sleep(4)

browser.quit()

#%%将sqlite表单写入多张csv
# def sql2csv(table_name, sqldb):
#     table = pd.read_sql_query('SELECT * FROM '+ table_name, sqldb)
#     table.index += 1
#     table.to_csv(table_name + datetime.datetime.now().strftime('%m-%d-%H-%M') +'sql.csv', index=True)

# sql2csv('events',conn)
# sql2csv('ci',conn)
# sql2csv('edithistory',conn)
# sql2csv('wikilink',conn)
# sql2csv('topeditor',conn)
# sql2csv('wikitext',conn)
# sql2csv('science',conn)
# #sql2csv('relevance',conn)

c.close()
conn.close() #关闭sql

