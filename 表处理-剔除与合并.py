#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 22:19:24 2023

@author: zhangsiqi
"""

import requests
import pandas as pd
import numpy as np
import sqlite3 as sqlite

#%% 拼接原始链接和新的表
#%%将sqlite表单写入多张csv
# 链接sql数据库，删除不完整的201412  
conn = sqlite.connect('BaiduWiki[01-16-00:33].sqlite')
c = conn.cursor()

c.execute(''' DELETE FROM events where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM citations where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM edithistory where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM wikilink where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM topeditor where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM wikitext where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM science where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

conn.close()



def sql2csv(table_name, sqldb):
    table = pd.read_sql_query('SELECT * FROM '+ table_name, sqldb)
    table.index += 1
    table.to_csv(table_name + '[01-16-00:33]' +'sql.csv', index=True)

sql2csv('events',conn)
sql2csv('citations',conn)
sql2csv('edithistory',conn)
sql2csv('wikilink',conn)
sql2csv('topeditor',conn)
sql2csv('wikitext',conn)
sql2csv('science',conn)

c.close()
conn.close() #关闭sql

# %% 合并csv
def mergecsv(a,b):
    dfa = pd.read_csv(a,index_col=('Unnamed: 0'))
    dfb = pd.read_csv(b,index_col=('Unnamed: 0'))
    df = pd.concat([dfa,dfb], ignore_index=True, sort=False)
    df.index += 1
    df.to_csv(a[:-20]+'.csv',index=True)

mergecsv('topeditor[01-16-00:33]sql.csv', 'topeditor[01-16-23:00]sql.csv')
mergecsv('events[01-16-00:33]sql.csv', 'events[01-16-23:00]sql.csv')
mergecsv('edithistory[01-16-00:33]sql.csv', 'edithistory[01-16-23:00]sql.csv')
mergecsv('citations[01-16-00:33]sql.csv', 'citations[01-16-23:00]sql.csv')
mergecsv('science[01-16-00:33]sql.csv', 'science[01-16-23:00]sql.csv')
mergecsv('wikilink[01-16-00:33]sql.csv', 'wikilink[01-16-23:00]sql.csv')
mergecsv('wikitext[01-16-00:33]sql.csv', 'wikitext[01-16-23:00]sql.csv')

#%% 补全csv中的原始链接
df_new = pd.read_csv('citations.csv') ##等待补全链接的数据

df_ori = pd.read_csv('citation+原始链接全.csv')[['event','reference_index','reference_text','original_url']] #补充的原始链接
df_ori = df_ori.rename(columns={'event':'entry'})
df_ori = df_ori.rename(columns={'original_url':'origin_url'})
df_ori = df_ori.rename(columns={'reference_index':'reference_entryindex'})
df_ori['reference_entryindex'] = df_ori['reference_entryindex'].astype('int')
print(df_ori.dtypes)
print(df_new.dtypes)

df = pd.merge(df_new, df_ori, on=['entry','reference_text','reference_entryindex'], how='left')
print(df.dtypes)

#手动修改错误的原始链接
df.at[6080,'origin_url'] = 'https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_11809/202301/t20230101_263164.html'
df.at[6081,'origin_url'] = 'https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_12208/202301/t20230101_263165.html'

conn1= sqlite.connect('com_citations.sqlite')
df.to_sql('com_citations', conn1, index=False)
conn1.close()

df.to_csv("citation.csv",index=False)

















