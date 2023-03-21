#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 15:36:35 2023

@author: zhangsiqi
"""

import pandas as pd
import sqlite3 as sqlite
import datetime
import re

# 链接sql数据库，删除不完整的201412  
conn = sqlite.connect('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1.sqlite')
c = conn.cursor()

#dfev = pd.read_sql('SELECT * FROM events', conn)
#dfev_ev = dfev['entry'].unique().tolist()
#dfedi_ev = dfedi['entry'].unique().tolist()

#%% 删除多余词条与重复词条

evtable = pd.read_excel('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0210补充事件时间/events+timestamp+evtype+range.xlsx')
entryall = evtable['entry'].unique().tolist()

#=================去除其他表单中的重复词条====================
#引用表单原始代码
# dfci = pd.read_sql('SELECT * FROM ci', conn)
# evli = []
# evdic = {}
# base =  'test'
# for index, row in dfci.iterrows():
#     entry = row['entry']
#     if entry != base: #如果词条和上一行不同
#         if entry not in evli: #如果词条不在evli里面
#             evli.append(entry)
#             evindex = []
#             evindex.append(index)
#             base = entry
#             evdic[entry] = evindex
#         else: #如果词条和上一行不同，且词条已经出现在evli中，将这一行删除
#             dfci.drop([index],inplace=True)
#     else: #如果词条和上一行相同
#         evindex.append(index)
#         base = entry
#         evdic[entry] = evindex

# print(len(evli))
# print(len(evdic))

# dfci.reset_index(drop=True)
# dfci.index += 1
# dfci.to_sql('ci', conn, index=True, if_exists = 'replace')

#检验上面的是否错误
# allli = list(evdic.values())
# lenall = 0
# for i in allli:
#     lenall += len(i)
# #lenall  14734 

# ciev = pd.DataFrame(evli).value_counts()

# ciev_di = list(set(dfev_ev).difference(set(evli))) #发现缺失的词条都是没有参考文献的

def del_dup_entry(sheet,conn):
    df = pd.read_sql('SELECT * FROM '+ sheet, conn)
    evli = []
    evdic = {}
    base =  'test'
    for index, row in df.iterrows():
        entry = row['entry']
        if entry != base: #如果词条和上一行不同
            if entry not in evli: #如果词条不在evli里面则加入evli，且更新base词条
                evli.append(entry)
                evindex = [] #该词条对应的参考资料index列表
                evindex.append(index)
                base = entry
                evdic[entry] = evindex
            else: #如果词条和上一行不同，且词条已经出现在evli中，将这一行删除，base词条不变
                df.drop([index],inplace=True)
        else: #如果词条和上一行相同，只扩充index列表，base词条不变
            evindex.append(index)
            evdic[entry] = evindex
    df.reset_index(drop=True)
    df.index += 1
    df.to_sql(sheet, conn, index=True, if_exists = 'replace')


del_dup_entry('ci', conn)

del_dup_entry('edithistory', conn)


#%%更新引用日期中的正则提取错误
dfci = pd.read_sql('SELECT * FROM ci', conn)
#dfev['cite_time'] = 
dfci['cite_time'].replace(regex=['日', '期'], value='',inplace=True)
dfci.to_sql('ci', conn, index=True, if_exists = 'replace')


#%%剔除1月16日以后的日期
def del_overtime(sheet,timefield):
    df = pd.read_sql('SELECT * FROM '+ sheet, conn)
    df[timefield] = pd.to_datetime(df[timefield])
    df = df[pd.to_datetime(df[timefield]) < datetime.datetime(2023,1,17,00,00,00)]
    df.to_sql(sheet, conn, index=True, if_exists = 'replace')
    print(sheet, "Total number of rows updated :", conn.total_changes)


del_overtime('ci', 'cite_time')

del_overtime('cittion_edtime', 'update_time')
del_overtime('edithistory', 'update_time')
conn.close()


#%% 修正百科的引用日期的正则表达式
#引用日期 马英九对美媒称钓鱼岛地理地质上都“属台湾”   ．环球网．2010-10-22[引用日期2014-4-27]
reference_text = ' 马英九对美媒称钓鱼岛地理地质上都“属台湾”   ．环球网．2010-10-22[引用日期2014-4-27]'
reference_text = ' 检察日报：中国司法机关对江歌案嫌犯有追诉权   ．中国新闻网[引用日期2020-6-6]'
reference_text = ' 红色通缉犯郭文贵在美国被捕|   ．界面新闻 · 快讯[引用日期2023-03-16]'
if '[引用日期' in reference_text:
    citi = re.search(r'引用日期.?(?P<y>20[0-2][0-9])-(?P<m>[0-1]?[0-9])-(?P<d>[0-3]?[0-9])\]?', reference_text)
    cite_time = citi.groupdict()['y']+'-'+citi.groupdict()['m']+'-'+citi.groupdict()['d']
    print(cite_time)
else:
    cite_time = None