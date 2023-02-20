#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 01:28:44 2023

@author: zhangsiqi

当时提取了两次编辑历史中的区块链信息，结果发现还有一两条数据有变，找了半天硬是不知道为啥链接两张表对不上

"""

#%% 区块链窗口获取时间 2023-02-06
import os
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
import re
import sqlite3 as sqlite
import math
import pandas as pd
import datetime
import numpy as np

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

# 定义一个捕捉元素时出现StaleElementReferenceException异常后重试的装饰器
@retry(retry = retry_if_exception_type(StaleElementReferenceException), wait = wait_fixed(3))
def click_elements(driver, method, name):
    #print('尝试获取元素',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),name)
    targets = driver.find_elements(method, name) #method =By.CLASS_NAME
    #print('获取元素成功')
    return [i for i in targets]

browser = webdriver.Chrome(executable_path = 'chromedriver')
original_window = browser.current_window_handle

dfall_new = pd.DataFrame(columns=['entry','edit_entryindex','author_name', 'update_time','edit_time'])

for index, row in dfev.iterrows():
#for index, row in dfev[1:2].iterrows():
    editurl = row['editurl']
    editcount = row['editcount']
    if editurl:#有编辑历史则继续
        editpage_nos = math.ceil(int(editcount)/25) #通过向上取整确定编辑历史的页面数量
        #dfev_new = pd.DataFrame(columns=['entry','edit_entryindex','author_name','update_time','edit_time'])
        
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
            #update_time = lst[4*j]
            #author_name = lst[4*j+1]
            dfli = pd.DataFrame(dflist) #列表转化为数据框
            dfli.rename(columns={0:'edit_entryindex',1:'author_name',2:'update_time'},inplace=True)
            #print(dfli)
            #----------打开区块链信息窗口抓取时间--------------
            blockchains = click_elements(browser, By.LINK_TEXT, '查看') #寻找可点击的区块链查看窗口
            for blockchain in blockchains:
                blockchain.click()
                time.sleep(3.5) #这个停顿一定需要，否则页面没有更新，定位元素会找不到
                # wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'ul.hash-info > li:nth-child(3)')))
                real_timeli = get_elements(browser, By.CSS_SELECTOR, 'ul.hash-info > li:nth-child(3)')
                if real_timeli:
                    real_time = real_timeli[0][5:]
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
        # dfev_new['entry'] = row['entry']
        # dfev_new['edit_time'] = time_new
        #-------合并不同词条下的所有编辑历史数据框------
        #dfall_new = pd.concat([dfall_new,dfev_new],ignore_index=True, sort=False)#合并时不保留原索引，启用新的自然索引
    time.sleep(2)

browser.close() #关闭当前的编辑历史标签页
browser.quit()

dfall_new['update_time'] = pd.to_datetime(dfall_new['update_time'])

dfall_new['edit_time'] = dfall_new['edit_time'].replace('待补全',value=pd.NaT)
dfall_new['edit_time'] = pd.to_datetime(dfall_new['edit_time'])
#dfall_new['time_di'] = dfall_new['update_time'] - dfall_new['edit_time']
#dfall_new['di_sec'] = df['time_di'].total_seconds()

# df['a'] = df['a'].astype(str)
# df['asplit'] = df['a'].str.split(':')
#df['amins'] = df['asplit'].apply(lambda x: int(x[0])*60 + int(x[1]))

# 创建sql数据库
sqname = 'BaiduWiki['+ datetime.datetime.now().strftime('%m-%d-%H:%M].sqlite')
conn= sqlite.connect(sqname)
dfall_new.index += 1
dfall_new.to_sql('edithis', conn, index=True, if_exists = 'replace')
conn.close()

dfall_new.to_csv('dfall_new.csv',index=True)
dfall_new.to_excel('dfall_new.xlsx',index=True)

#把分csv拼接

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0208补全编辑时间戳')

dfti0 = pd.read_csv('dfall_new.csv', index_col='Unnamed: 0')
dfti1 = pd.read_csv('dfall_new-1.csv', index_col='Unnamed: 0')
dfti2 = pd.read_csv('dfall_new-2.csv', index_col='Unnamed: 0')
dfti3 = pd.read_csv('dfall_new-3.csv', index_col='Unnamed: 0')
dfti4 = pd.read_csv('dfall_new-4.csv', index_col='Unnamed: 0')
dfti5 = pd.read_csv('dfall_new-5.csv', index_col='Unnamed: 0')
dfti6 = pd.read_csv('dfall_new-6.csv', index_col='Unnamed: 0')
dfti7 = pd.read_csv('dfall_new-6-1.csv', index_col='Unnamed: 0')
dfti8 = pd.read_csv('dfall_new-7.csv', index_col='Unnamed: 0')

frames = [dfti0,dfti1,dfti2,dfti3,dfti4,dfti5,dfti6,dfti7,dfti8]
df = pd.concat(frames,ignore_index=True, sort=False)#合并不保留原索引，启用新的自然索引：

conn= sqlite.connect('alledittime.sqlite')
df.index += 1
df.to_sql('edittime', conn, index=True, if_exists = 'replace')
conn.close()

df.to_csv('alleditime.csv',index=True)
#发现结果多了几十条编辑历史，再匹配到原表就行，下面是痛苦的查找不匹配原因的过程

#%% csv连接数据：补充编辑历史的实际编辑时间 2023-02-08
import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re
import datetime

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0208补全编辑时间戳')

dfev = pd.read_csv('eventssql.csv', index_col='Unnamed: 0')
dfti = pd.read_csv('alleditime.csv', index_col='Unnamed: 0')

#dfev['update_time'] = pd.to_datetime(dfev['update_time'])

#屠呦呦 bug 因为爬取中断后直接从中间页面开始导致新抓取时实际抓取到的还是第一页的，所以25条编辑历史重复了 6292-6316
dftu = pd.read_csv('tuyou.csv', index_col='Unnamed: 0')
dftu['edit_entryindex']=range(126,151)
dfti = dfti.drop(index=range(6292,6317))

#替换掉重复的屠呦呦编辑历史
df0 = dfti[:6292]
df1 = dfti[6292:]
dfti = pd.concat([df0,dftu,df1],ignore_index=True, sort=False)#合并不保留原索引，启用新的自然索引：
#剔除2023.1.18及以后的编辑历史
dfti['update_time'] = pd.to_datetime(dfti['update_time'])
dfti['date'] = dfti['update_time'].dt.date
dfti['baseline'] = datetime.datetime(2023,1,18)
dfti = dfti[dfti['date']< dfti['baseline']]

#把每个事件的编辑历史索引更正
namelist = dfti['entry'].unique()

#namelist = dfti['entry'].unique().tolist()
dfti['edit_entryindex']=np.nan
dfti['edit_count']=np.nan
dfti['year']=None
dfti['event']=None
dfti['event_id']=None
dfti['entryindex']=None

for index, row in dfev.iterrows():
    i = row['entry']
    j = row['editcount']
    length = len(dfti[dfti['entry']==i])
    if length != j:
        print(i, j, '新采集的',length, '编辑次数变了')
    dfti.loc[dfti['entry']==i,'edit_entryindex'] = range(1,length+1)
    dfti.loc[dfti['entry']==i,'edit_count'] = length
    
    dfti.loc[dfti['entry']==i,'year'] = row['year']
    dfti.loc[dfti['entry']==i,'event'] = row['event']    
    dfti.loc[dfti['entry']==i,'event_id'] = row['event_id']
    dfti.loc[dfti['entry']==i,'entryindex'] = row['entryindex']
    
    # dfti.loc[dfti['entry']==i,'edit_entryindex'] = range(1,length+1) 死活想不明白为啥改成series就只能赋值第一个事件

# conn= sqlite.connect('置换.sqlite')
# dfti.to_sql('edit', conn, index=True, if_exists = 'replace')
# conn.close()

# dfti = dfti[['entry','edit_entryindex', 'update_time','author_name','edit_time']]
# dfti['edit_entryindex']=dfti['edit_entryindex'].astype(np.int64)
# dfap = pd.merge(df, dfti, how='left',on=['entry','update_time','author_name','edit_entryindex'])
dfti.drop(['baseline','date','time_di'],inplace=True,axis=1)

dfed = pd.read_csv('edithistorysql.csv', index_col='Unnamed: 0')
dfed['update_time'] = pd.to_datetime(dfed['update_time'])
dfed.year = dfed.year.astype('str')
dfed.event_id = dfed.event_id.astype('str')
dfed.edit_entryindex = dfed.edit_entryindex.astype('str')


dfmis = dfed[4448:4449]
dfmis['edit_time']=pd.NaT
dfmis.loc[:,'edit_time'] = pd.to_datetime('2014-03-08 08:59:00') 

#dfmis['edit_time']=pd.to_datetime('2014-03-08 08:59')

#插入缺失值
dfti.edit_count = dfti.edit_count.astype(int)
dfti1 = dfti[:4448]
dfti2 = dfti[4448:]
dfti = pd.concat([dfti1,dfmis,dfti2],ignore_index=True, sort=False)#合并不保留原索引，启用新的自然索引：
dfti.loc[dfti['entry']=='3·8马来西亚航班失踪事件','edit_count'] = 175

#下面导出数据很无语，因为老是parameter不对，最后直接导出csv再导入csv为sql了
os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0208补全编辑时间戳')
dfti.to_csv('edittimeall.csv',index=True)

df = pd.read_csv('edittimeall.csv',index_col='Unnamed: 0')
df.index += 1
# conn= sqlite.connect('edi+time.sqlite')
# df.to_sql('edit+time', conn, index=True, if_exists = 'replace')
# conn.close()
os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情')

conn= sqlite.connect('Wiki.sqlite')
df.to_sql('edit_time', conn, index=True, if_exists = 'replace')
conn.close()

