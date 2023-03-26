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
import numpy as np
import math
import datetime
import os

# 链接sql数据库
#sqname = 'BaiduWiki['+ datetime.datetime.now().strftime('%m-%d-%H:%M].sqlite')
os.chdir('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0214补充词条数据')
conn= sqlite.connect("/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1.sqlite")
c = conn.cursor()

conn1= sqlite.connect("/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1元.sqlite")
c1 = conn1.cursor()

#dfev = pd.read_sql('SELECT * FROM events', conn)
#dfev_ev = dfev['entry'].unique().tolist()
#dfedi_ev = dfedi['entry'].unique().tolist()
#%% 补充漏掉的天价鱼事件
evtable = pd.read_excel('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0210补充事件时间/events+timestamp+evtype+range.xlsx')
entryall = evtable['entry'].unique()

dfev = pd.read_sql('SELECT * FROM events', conn1)

# #去除dfev重复项
# dfevdup = dfev[dfev.duplicated(['entry'])==True]
dfev = dfev[dfev.duplicated(['entry'])==False]

evtableadd = evtable[['event_id','event','year','entry','baikelink','no_entry_merge','nev_entry','uncovertime','start_cl_scale','start_cl','edi_start','docu_start','edi_end','type','pre_event']]
#dfevadd = dfev[['event_id','event','year','entry','baikelink']
dfev.drop(columns=['entryindex','event','index','year','baikelink','event_id','start_time','end_time','uncovertime','once','start_cl','edi_start','edi_end','edi_range','create_range','type','antici'],inplace=True)
#这里一定要 drop年份 eventid

dfm = pd.merge(evtableadd, dfev, how='left', on=['entry'])
dfm.index += 1
dfm.to_sql('event', conn, index=True, if_exists = 'replace')

#=======edit_time表单===========
df1ti = pd.read_sql('SELECT * FROM edit_time', conn1)
fishti = df1ti[df1ti['entry']=='天价鱼']

for index, row in fishti.iterrows():
    hist_row_values = (row['entry'], row['edit_entryindex'], row['author_name'], row['update_time'],row['edit_time'])
    c.execute(''' INSERT INTO edit_time (entry, edit_entryindex, author_name, update_time, edit_time) VALUES (?, ?, ?, ?, ?)''', hist_row_values)
    conn.commit()

#=======cite表单===========
dfci = pd.read_sql('SELECT * FROM ci', conn)
df1ci = pd.read_sql('SELECT * FROM ci', conn1)
fishci = df1ci[df1ci['entry']=='天价鱼']

fishci_all = pd.concat([dfci,fishci])
fishci_all.to_sql('ci', conn, index=False, if_exists = 'replace')

#=======topeditor表单===========
dftop = pd.read_sql('SELECT * FROM topeditor', conn)
df1top = pd.read_sql('SELECT * FROM topeditor', conn1)
fishtop = df1top[df1top['entry']=='天价鱼']

fishtop_all = pd.concat([dftop,fishtop])
fishtop_all.to_sql('topeditor', conn, index=True, if_exists = 'replace')

#=======wikilink表单===========
dfwikilink = pd.read_sql('SELECT * FROM wikilink', conn)
df1wikilink = pd.read_sql('SELECT * FROM wikilink', conn1)
fishwikilink = df1wikilink[df1wikilink['entry']=='天价鱼']

fishwikilink_all = pd.concat([dfwikilink,fishwikilink])
fishwikilink_all.to_sql('wikilink', conn, index=True, if_exists = 'replace')

#=======wikitext表单===========
dfwikitext = pd.read_sql('SELECT * FROM wikitext', conn)
df1wikitext = pd.read_sql('SELECT * FROM wikitext', conn1)
fishwikitext = df1wikitext[df1wikitext['entry']=='天价鱼']

fishwikitext_all = pd.concat([dfwikitext,fishwikitext])
fishwikitext_all.to_sql('wikitext', conn, index=True, if_exists = 'replace')


#%% 将补好的ci给wiki+1

conn2= sqlite.connect("/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1只差mini的editime.sqlite")
c2 = conn2.cursor()


dfci_200s = pd.read_sql("SELECT * FROM 'ci+200s'", conn2)

dfci_200s.loc[pd.isna(dfci_200s['origin_url']) & pd.notna(dfci_200s['redir_url']),'origin_url']=dfci_200s['original_url']

dfci_200s.to_sql('ci+200s', conn, index=False, if_exists = 'replace')


#%%合并新加的history
dfediadd = pd.read_sql('SELECT * FROM test_add_his_final', conn)
dfediadd1 = pd.read_sql('SELECT * FROM test_add_his_2022covidpart', conn)
dfediadd2 = pd.read_sql('SELECT * FROM test_add_his_2022covid2', conn)
dfediadd3 = pd.read_sql('SELECT * FROM test_add_his_2', conn)

dfediadd_all = pd.concat([dfediadd,dfediadd1,dfediadd2,dfediadd3]) 

for index, row in dfediadd_all.iterrows():
    hist_row_values = (row['entry'], row['edit_entryindex'], row['author_name'], row['update_time'],row['edit_time'])
    c.execute(''' INSERT INTO edit_time (entry, edit_entryindex, author_name, update_time, edit_time) VALUES (?, ?, ?, ?, ?)''', hist_row_values)
    conn.commit()

dfediadd = pd.read_sql('SELECT * FROM test_add_his_final', conn)

for index, row in dfediadd.iterrows():
    hist_row_values = (row['entry'], row['edit_entryindex'], row['author_name'], row['update_time'],row['edit_time'])
    c.execute(''' INSERT INTO edit_time (entry, edit_entryindex, author_name, update_time, edit_time) VALUES (?, ?, ?, ?, ?)''', hist_row_values)
    conn.commit()


#%% 删除多余词条与重复词条
evtable = pd.read_excel('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0210补充事件时间/events+timestamp+evtype+range.xlsx')
entryall = evtable['entry'].unique().tolist()

dfev = pd.read_sql('SELECT * FROM events', conn)
dfev_ev = dfev['entry'].unique().tolist()

#events表去除重复
c.execute('DELETE FROM events WHERE events.rowid NOT IN (SELECT min(events.rowid) FROM events GROUP BY entry);')
#=================去除其他表单中的重复词条====================
#未制作函数之前的原始代码
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
    #df.drop(columns=['index'])
    #df.reset_index(drop=True)
    #df.index += 1
    df.to_sql(sheet, conn, index=False, if_exists = 'replace')

del_dup_entry('edit_time', conn)
del_dup_entry('ci', conn)
del_dup_entry('topeditor', conn)

del_dup_entry('science', conn)
del_dup_entry('wikilink', conn)
del_dup_entry('wikitext', conn) #原来是55258

#============删除多余词条的数据================
#取出 多余的词条名
ev_di = list(set(dfev_ev).difference(set(entryall)))

def del_sql(sheet, conn, entryall):
    df_ev = pd.read_sql('SELECT * FROM '+ sheet, conn)
    dfev_ev = df_ev['entry'].unique().tolist()
    entry_di = list(set(dfev_ev).difference(set(entryall)))
    for i in entry_di:
        sql_script = '''DELETE FROM ''' + sheet + ''' WHERE entry = "''' + i + '''";'''
        c.execute(sql_script)
        conn.commit()

del_sql('edit_time', conn, entryall)
del_sql('ci', conn, entryall)
del_sql('science', conn, entryall)
del_sql('topeditor', conn, entryall)
del_sql('wikilink', conn, entryall)
del_sql('wikitext', conn, entryall)


dfedi = pd.read_sql('SELECT * FROM edit_time', conn)
dfedi_ev = pd.DataFrame(dfedi['entry'].value_counts())

dfci = pd.read_sql('SELECT * FROM ci', conn)
dfci_ev = pd.DataFrame(dfci['entry'].value_counts())

# test = del_sql("ci", "脱贫攻坚")
# print(del_sql("ci", "脱贫攻坚"))

#检查出top editor还是有重复
df1top = pd.read_sql('SELECT * FROM topeditor', conn1)
df1top.to_sql('topeditor', conn, index=False, if_exists = 'replace')

dftop = pd.read_sql('SELECT * FROM topeditor', conn)
dftop = dftop[dftop.duplicated(['entry','editor_name'])==False]
dftop.to_sql('topeditor', conn, index=False, if_exists = 'replace')

#检查出wikilink还是有重复 毕福剑词条
dfwikilink = pd.read_sql('SELECT * FROM wikilink', conn)
dfwikilink = dfwikilink[dfwikilink.duplicated(['entry','link_entryindex'])==False]
dfwikilink.to_sql('wikilink', conn, index=False, if_exists = 'replace')

#检查出wikitext还是有重复 毕福剑词条
dfwikitext = pd.read_sql('SELECT * FROM wikitext', conn)
dfwikitext = dfwikitext[dfwikitext.duplicated(['entry','wiki_text'])==False]
dfwikitext.to_sql('wikitext', conn, index=False, if_exists = 'replace')

b=pd.DataFrame(dfwikitext['entry'].value_counts())

dupwikitext = dfwikitext[dfwikitext.duplicated(['entry','wiki_text','cited_item'])==True]
dupwikitext.to_sql('dupwikitext', conn, index=False, if_exists = 'replace')

#%%更新引用日期中的正则提取错误
dfci = pd.read_sql('SELECT * FROM ci', conn)
#dfev['cite_time'] = 
dfci['cite_time'].replace(regex=['日', '期'], value='',inplace=True)
dfci.to_sql('ci', conn, index=False, if_exists = 'replace')


#%%剔除1月16日以后的参考资料和编辑记录
def del_overtime(sheet,timefield):
    df = pd.read_sql('SELECT * FROM '+ sheet, conn)
    df[timefield] = pd.to_datetime(df[timefield])
    df = df[(pd.to_datetime(df[timefield]) < datetime.datetime(2023,1,17,00,00,00)) | (pd.isna(df[timefield]))]
    #df.drop(columns=['index'],inplace=True)
    #df.index+=1
    df.to_sql(sheet+'0116', conn, index=False, if_exists = 'replace')
    print(sheet, "Total number of rows updated :", conn.total_changes)

del_overtime('ci', 'cite_time')
del_overtime('edit_time', 'update_time')
del_overtime('ci0116', 'source_time')

#%% 特殊词条仅保留在事件发生后的参考资料和编辑记录


#===================2023-03-22
#1 将range表更新到sql
dfev = pd.read_sql('SELECT * FROM eventf', conn)
evtable = pd.read_excel('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0210补充事件时间/events+timestamp+evtype+range.xlsx')

evtableadd = evtable[['event_id','event','year','entry','baikelink','only_createrange','del_before','nev_entry','uncovertime','start_cl_scale','start_cl','edi_start','docu_start','edi_end','type','pre_event']]
#dfevadd = dfev[['event_id','event','year','entry','baikelink']
dfev.drop(columns=['index','year','event','baikelink','event_id','nev_entry','pre_event','start_cl_scale','docu_start','start_cl','uncovertime','edi_start','edi_end','type'],inplace=True)
#这里一定要 drop年份 eventid

dfm = pd.merge(evtableadd, dfev, how='left', on=['entry'])
dfm.to_sql('eventf', conn, index=True, if_exists = 'replace')

#1.1 特别不相干的词条剔除参考资料的考察，采取截断的做法
dfev = pd.read_sql('SELECT * FROM eventf', conn)
dfti = pd.read_sql('SELECT * FROM edit_time0116', conn)
dfci = pd.read_sql('SELECT * FROM ci01160116', conn)

for index, row in dfev.iterrows():#删除引用日期在事件发生之前的
    i = row['entry']
    #j = row['editcount']
    filt = row['del_before']
    if filt == 1:
        #one = dfci[dfci['entry']==i]
        start = datetime.datetime.strptime(row['start_cl_scale'],'%Y-%m-%d %H:%M:%S')
        for index1, row1 in dfci.iterrows():
            if pd.notna(row1['cite_time']):
                if (row1['entry']==i) & (datetime.datetime.strptime(row1['cite_time'],'%Y-%m-%d %H:%M:%S') < start):
                    dfci.drop(index1,inplace=True)
        
    
dfci.to_sql('ci_delb', conn, if_exists = 'replace')


dfci = pd.read_sql('SELECT * FROM ci_delb', conn)
for index, row in dfev.iterrows():#删除资料发布日期在事件发生之前的
    i = row['entry']
    #j = row['editcount']
    filt = row['del_before']
    if filt == 1:
        #one = dfci[dfci['entry']==i]
        start = datetime.datetime.strptime(row['start_cl_scale'],'%Y-%m-%d %H:%M:%S')
        for index1, row1 in dfci.iterrows():
            if pd.notna(row1['source_time']):
                if (row1['entry']==i) & (datetime.datetime.strptime(row1['source_time'],'%Y-%m-%d %H:%M:%S') < start):
                    dfci.drop(index1,inplace=True)

for index2, row2 in dfci.iterrows():
    if row2['entry']=='马龙':
        if '退赛' not in row2['reference_text']:
            dfci.drop(index2,inplace=True)
    if row2['entry']=='马英九':
        dfci.drop(index2,inplace=True)
    
dfci.to_sql('ci_delb', conn, index=False, if_exists = 'replace')
    
#dfci.drop(dfci[(dfci['entry']==i) & (pd.notna(dfci['cite_time'])) &(datetime.datetime.strptime(dfci['cite_time'],'%Y-%m-%d %I-%M-%S') < datetime.datetime(start))].index,inplace=True)

dftp = pd.read_sql('SELECT * FROM topeditor', conn)
dfwl = pd.read_sql('SELECT * FROM wikilink', conn)
dfwt = pd.read_sql('SELECT * FROM wikitext', conn)

#检查缺不缺事件
dftp['entry'].value_counts()
dfev['topeditor_count'].sum()
dfev['link_count'].sum()

#===========todolist===========
#% 根据截止日期前的结果更新event字段；以及ci和edit_time的索引

# a = pd.DataFrame(dfti['entry'].value_counts())
# a.entry.sum() #30668
# a.to_csv('a.csv')

dfev = pd.read_sql('SELECT * FROM eventf', conn)
dfti = pd.read_sql('SELECT * FROM edit_time0116', conn)
dfci = pd.read_sql('SELECT * FROM ci_delb_fish', conn)

for index, row in dfev.iterrows():
    i = row['entry']
    j = row['editcount']
    length = len(dfti[dfti['entry']==i])
    if length != j:
        print(i, j, '新采集的',length, '编辑次数变了')
    dfti.loc[dfti['entry']==i,'edit_entryindex'] = range(length,0,-1) #记录一个词条内部的索引,因时间新的编辑记录在前面，使用倒序
    dfti.loc[dfti['entry']==i,'edit_count'] = length #记录一个词条的总编辑次数
    dfti.loc[dfti['entry']==i,'year'] = row['year'] #记录一个词条的年份
    dfti.loc[dfti['entry']==i,'event'] = row['event'] #记录一个词条的事件    
    dfti.loc[dfti['entry']==i,'event_id'] = row['event_id'] #记录一个词条的事件id
    dfti.loc[dfti['entry']==i,'entryindex'] = index+1
    dfti.sort_values(by=['entryindex', 'edit_entryindex'], ascending=[True, False],inplace=True)
    dfev.at[index,'editcount'] = length

dfti.reset_index(inplace=True) #重置索引
dfti.drop(columns=['index'],inplace=True)
dfti.index+=1
dfti.to_sql('edit_time_reindex', conn, index=True, if_exists = 'replace')

dfev.to_sql('eventf', conn, index=False, if_exists = 'replace')

for index, row in dfev.iterrows():
    i = row['entry']
    j = row['reference_count']
    length = len(dfci[dfci['entry']==i])
    if length != j:
        print(i, j, '新采集的',length, '参考资料数量变了')
    dfci.loc[dfci['entry']==i,'reference_entryindex'] = range(1,length+1) #记录一个词条内部的索引,因时间新的编辑记录在前面，使用倒序
    dfci.loc[dfci['entry']==i,'edit_count'] = length #记录一个词条的总编辑次数
    dfci.loc[dfci['entry']==i,'year'] = row['year'] #记录一个词条的年份
    dfci.loc[dfci['entry']==i,'event'] = row['event'] #记录一个词条的事件
    dfci.loc[dfci['entry']==i,'event_id'] = row['event_id'] #记录一个词条的事件id
    dfci.loc[dfci['entry']==i,'entryindex'] = index+1
    dfci.sort_values(by=['entryindex', 'reference_entryindex'], ascending=[True, True],inplace=True)
    dfev.at[index,'reference_count'] = length



dfci.drop(columns=['index','level_0'],inplace=True)
dfci.reset_index(inplace=True) #重置索引
dfci.index+=1
dfci.to_sql('ci_reindex', conn, index=False, if_exists = 'replace')

dfev.to_sql('eventf', conn, index=False, if_exists = 'replace')

#发现马龙参考资料前面操作错了，修正一下
dfciold = pd.read_sql('SELECT * FROM ciold', conn)
cimalong = dfciold[(dfciold['entry']=='马龙') & (dfciold['reference_text'].str.contains('退赛'))]

malong_all = pd.concat([dfci,cimalong])

dfci = malong_all

for index, row in dfev.iterrows():
    i = row['entry']
    j = row['reference_count']
    length = len(dfci[dfci['entry']==i])
    if length != j:
        print(i, j, '新采集的',length, '参考资料数量变了')
    dfci.loc[dfci['entry']==i,'reference_entryindex'] = range(1,length+1) #记录一个词条内部的索引,因时间新的编辑记录在前面，使用倒序
    dfci.loc[dfci['entry']==i,'edit_count'] = length #记录一个词条的总编辑次数
    dfci.loc[dfci['entry']==i,'year'] = row['year'] #记录一个词条的年份
    dfci.loc[dfci['entry']==i,'event'] = row['event'] #记录一个词条的事件
    dfci.loc[dfci['entry']==i,'event_id'] = row['event_id'] #记录一个词条的事件id
    dfci.loc[dfci['entry']==i,'entryindex'] = index+1
    dfci.sort_values(by=['entryindex', 'reference_entryindex'], ascending=[True, True],inplace=True)
    dfev.at[index,'reference_count'] = length


dfci.drop(columns=['index','level_0'],inplace=True)
dfci.reset_index(inplace=True) #重置索引
dfci.index+=1
dfci.to_sql('ci_reindex', conn, index=False, if_exists = 'replace')

dfev.to_sql('eventf', conn, index=False, if_exists = 'replace')

#3 ========原始链接处理

#2 整理两张白名单


#3 取欠缺的参考资料发布日期

# #%% 剔除wikitext中不在ci表中的引用记录
# dfwt = pd.read_sql('SELECT * FROM wikitext', conn)
# dfci0116 = pd.read_sql('SELECT * FROM ci0116', conn)

# for index, row in dfev.iterrows():
# #for index, row in dfev[141:142].iterrows():   
#     dfci = dfwt.loc[dfwt['entry'] == row['entry'],'cited_item']
#     if not dfci.empty:
#         cilist = [ele for ele in dfci if ele == ele]
#         ci_str = '; '.join(cilist)
#         ci_li = ci_str.split('; ')
#         dash_li = [el.strip('[]') for el in ci_li if '-' in el] #[94-95]
#         if not dash_li: #如果没有出现 ‘【1-3】’的情况
#             cite_count = len(ci_li)
#             #print(ci_li)
#         else:
#             nodash_li = [int(el.strip('[]')) for el in ci_li if '-' not in el]
#             for j in dash_li:
#                 start = re.search(r'(?P<start>\d+)\-',j)
#                 end = re.search(r'\-(?P<end>\d+)',j)
#                 real_li = range(int(start.groupdict()['start']),int(end.groupdict()['end'])+1)
#                 nodash_li.extend(real_li)
#             cite_count = len(nodash_li)
#     else:
#         cite_count = np.nan
#     dfev.at[index, 'cite_count'] = cite_count




#%% 






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