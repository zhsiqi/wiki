#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 15:05:54 2023

@author: zhangsiqi
"""

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

#============2023-03-09=============

#os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0210补充事件时间')

#%% 读取、创建数据库等
evtable = pd.read_excel('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0210补充事件时间/events+timestamp+evtype+range.xlsx')
entryall = evtable['entry'].unique()

# 创建sql数据库
#sqname = 'BaiduWiki['+ datetime.datetime.now().strftime('%m-%d-%H:%M].sqlite')
os.chdir('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0214补充词条数据')
conn= sqlite.connect("/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1.sqlite")
c = conn.cursor()


dfev = pd.read_sql('SELECT * FROM events', conn)

# #去除dfev重复项
# dfevdup = dfev[dfev.duplicated(['entry'])==True]
# dfev = dfev[dfev.duplicated(['entry'])==False]

dfedi = pd.read_sql('SELECT * FROM edit_time', conn)
dfedi_ev = dfedi['entry'].unique().tolist()

dfediadd11 = pd.read_sql('SELECT * FROM test_add_his1', conn)
dfediadd11_ev = dfediadd11['entry'].unique().tolist()

dfediadd1 = pd.read_sql('SELECT * FROM test_add_his_2022covidpart', conn)
dfediadd1_ev = dfediadd1['entry'].unique().tolist()

# dfediadd2 = pd.read_sql('SELECT * FROM test_add_his2', conn)
# dfediadd2_ev = dfediadd2['entry'].unique().tolist()

# dfediadd3 = pd.read_sql('SELECT * FROM test_add_his3', conn)
# dfediadd3_ev = dfediadd3['entry'].unique().tolist()

# dfediadd4 = pd.read_sql('SELECT * FROM test_add_his4', conn)
# dfediadd4_ev = dfediadd4['entry'].unique().tolist()

# dfediadd5 = pd.read_sql('SELECT * FROM test_add_his5', conn)
# dfediadd5_ev = dfediadd5['entry'].unique().tolist()

# dfediadd6 = pd.read_sql('SELECT * FROM test_add_his6', conn)
# dfediadd6_ev = dfediadd6['entry'].unique().tolist()

# dfediadd7 = pd.read_sql('SELECT * FROM test_add_his7', conn)
# dfediadd7_ev = dfediadd7['entry'].unique().tolist()

# dfediadd8 = pd.read_sql('SELECT * FROM test_add_his8', conn)
# dfediadd8_ev = dfediadd8['entry'].unique().tolist()

# dfediadd9 = pd.read_sql('SELECT * FROM test_add_his9', conn)
# dfediadd9_ev = dfediadd9['entry'].unique().tolist()

# dfediadd10 = pd.read_sql('SELECT * FROM test_add_his10', conn)
# dfediadd10_ev = dfediadd10['entry'].unique().tolist()

#evtableadd = evtable[['event_id','event','year','entry','baikelink','start_cl_scale','start_cl','edi_start','docu_start','edi_end','type','pre_event']]
#evtableadd = evtable[['event_id','event','year','entry','baikelink','no_entry_merge','nev_entry','uncovertime','start_cl_scale','start_cl','edi_start','docu_start','edi_end','type','pre_event']]

evtableadd = evtable[['event_id','event','year','entry','baikelink','no_entry_merge','nev_entry','uncovertime','start_cl_scale','start_cl','edi_start','docu_start','edi_end','type','pre_event']]
#dfevadd = dfev[['event_id','event','year','entry','baikelink']
dfev.drop(columns=['entryindex','index','year','baikelink','event_id','start_time','end_time','uncovertime','once','start_cl','edi_start','edi_end','edi_range','create_range','type','antici'],inplace=True)
#这里一定要 drop年份

dfm = pd.merge(evtableadd, dfev, how='left', on=['entry'])

dfm.to_sql('final_events_0320_1', conn, index=True, if_exists = 'replace')



#%%% 参考资料表单       
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
original_window = browser.current_window_handle #记录事件百科的原始标签页

#%% 事件表单第一部分

dfall_new = pd.DataFrame(columns=['entry','edit_entryindex','author_name', 'update_time','edit_time'])

#根据词条网址获取网页内容
#for index, row in evtable.iterrows():
for index, row in dfm.iterrows():
    line = row['baikelink']
    # print('line',line.strip())
    year = row['year']
    eventname = row['event_x']
    event_id = row['event_id']
    entryname = row['entry']
    editcount = row['editcount']
    editurl = row['editurl']
    evstart = row['start_cl_scale']

    if entryname in dfedi_ev: #如果该词条已经收录在sqlite的编辑历史数据表中，则跳过
        continue
    if entryname in dfediadd11_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
        continue
    if entryname in dfediadd1_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
        continue
    # if entryname in dfediadd2_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
    #     continue
    # if entryname in dfediadd3_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
    #     continue
    # if entryname in dfediadd4_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
    #     continue
    # if entryname in dfediadd5_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
    #     continue
    # if entryname in dfediadd6_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
    #     continue
    # if entryname in dfediadd7_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
    #     continue
    # if entryname in dfediadd8_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
    #     continue
    # if entryname in dfediadd9_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
    #     continue
    # if entryname in dfediadd10_ev: #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
    #     continue
    # if entryname =='马龙': #如果该词条已经收录在sqlite的补充编辑历史数据表中，则跳过
    #     continue
    

    #browser.get(line.strip()) #selenium获取网页

    
#%%编辑历史表单
    if editurl: #有编辑历史则继续
        print('事件', len(evtable),'-', index + 1, entryname)
        editpage_nos = math.ceil(int(editcount)/25) #通过向上取整确定编辑历史的页面数量
        for num in range(1,editpage_nos+1):
            time_new = []
            histo_url = editurl + '#page' + str(num)
            edit_jsscript = '''window.open("'''+ histo_url + '''", 'new_window')''' 
            browser.execute_script(edit_jsscript) #打开新标签页，进入编辑历史的网页
            browser.switch_to.window(browser.window_handles[-1]) #切换窗口
            time.sleep(3)
            #一直等待到元素可见
            wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.TAG_NAME, 'td')))
            lst = get_elements(browser, By.TAG_NAME, 'td')
            #print(lst)
            dflist = [[25*(num-1)+j+1, lst[4*j+1],lst[4*j]] for j in range(0,int(len(lst)/4))]
            dfli = pd.DataFrame(dflist) #列表转化为数据框
            dfli.rename(columns={0:'edit_entryindex',1:'author_name',2:'update_time'},inplace=True)
            #print(dfli)
            #----------打开区块链信息窗口抓取时间--------------
            blockchains = click_elements(browser, By.LINK_TEXT, '查看') #寻找可点击的区块链查看窗口
            for blockchain in blockchains:
                blockchain.click()
                time.sleep(3.5) #这个停顿一定需要，否则页面没有更新，定位元素会找不到
                wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > dl.wgt_dialog.modal.blockChain-dialog > dd.con.no-icon.no-sub-msg > div:nth-child(1) > ul > li:nth-child(3)')))
                real_timeli = get_elements(browser, By.CSS_SELECTOR, 'body > dl.wgt_dialog.modal.blockChain-dialog > dd.con.no-icon.no-sub-msg > div:nth-child(1) > ul > li:nth-child(3)')
                
                if real_timeli:
                    real_time = real_timeli[0][5:]
                    time_new.append(real_time)
                    closewindow = click_elements(browser, By.CSS_SELECTOR, 'dl.wgt_dialog.modal.blockChain-dialog > dd.close.dialog-btn > em')[0]
                else:
                    time.sleep(2)
                    real_timeli1 = get_elements(browser, By.CSS_SELECTOR, 'body > dl.wgt_dialog.modal.blockChain-dialog > dd.con.no-icon.no-sub-msg > div:nth-child(1) > ul > li:nth-child(3)')
                    if real_timeli1:
                        real_time = real_timeli1[0][5:]
                        time_new.append(real_time)
                        closewindow = click_elements(browser, By.CSS_SELECTOR, 'dl.wgt_dialog.modal.blockChain-dialog > dd.close.dialog-btn > em')[0]
                    else:
                        time_new.append(pd.NaT)
                        closewindow = click_elements(browser, By.CSS_SELECTOR, 'dl.wgt_dialog.no-title.modal.width-fixed > dd.close.dialog-btn > em')[0]
                #------关闭打开的区块链窗口------ 
                
                browser.execute_script('arguments[0].click();', closewindow)
            browser.close() #关闭当前的编辑历史标签页
            browser.switch_to.window(original_window) #回到原初的百科页面
            dfli['entry'] = row['entry']
            dfli['edit_time'] = time_new
            #-------合并同一词条下的所有编辑历史数据框------
            #dfev_new = pd.concat([dfev_new, dfli],ignore_index=True, sort=False)#合并不保留原索引，启用新的自然索引：
            dfall_new = pd.concat([dfall_new, dfli],ignore_index=True, sort=False)#合并不保留原索引，启用新的自然索引：

    # 等待数秒继续下一个
    time.sleep(2)
    
    print('编辑历史表单done')

browser.quit()

dfall_new.index += 1
dfall_new.to_sql('test_add_his_2', conn, index=True, if_exists = 'replace')
conn.close()

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

# c.close()
# conn.close() #关闭sql

