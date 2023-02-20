#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 02:20:04 2023

@author: zhangsiqi
导出sql表单
"""
#%% 导出各表单
import os
import sqlite3 as sqlite
import pandas as pd

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情')
conn= sqlite.connect('Wiki.sqlite')


#将sqlite表单写入多张csv
def sql2csv(table_name, sqldb):
    table = pd.read_sql_query('SELECT * FROM '+ table_name, sqldb)
    table.index += 1
    table.to_csv(table_name+'sql.csv', index=True)
    
sql2csv('events',conn)
sql2csv('citation',conn)
sql2csv('edithistory',conn)
sql2csv('wikilink',conn)
sql2csv('topeditor',conn)
sql2csv('wikitext',conn)
sql2csv('science',conn)

def sql2excel(table_name, sqldb):
    table = pd.read_sql_query('SELECT * FROM '+ table_name, sqldb)
    table.index += 1
    table.to_excel(table_name+'.xlsx',index=True)
    
sql2excel('events',conn)
sql2excel('citation',conn)
sql2excel('edithistory',conn)
sql2excel('wikilink',conn)
sql2excel('topeditor',conn)
sql2excel('wikitext',conn)
sql2excel('science',conn)        

conn.close() #关闭sql

