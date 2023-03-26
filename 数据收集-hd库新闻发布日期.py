#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 16:19:51 2023

@author: zhangsiqi
"""

import os
import pandas as pd
import sqlite3 as sqlite
import datetime
import numpy as np
import re
from htmldate import find_date
import time
import datetime

conn= sqlite.connect("/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1.sqlite")
c = conn.cursor()

df = pd.read_sql('SELECT * FROM ci_time', conn)

# os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0209补充发布时间戳')
# #os.chdir('D:\zsq')
# df = pd.read_csv('citation+time-2.csv', index_col=('Unnamed: 0'))

# df['htmltimestamp']=pd.NaT


for index, row in df.iterrows():
    url = row['origin_url_x']
    dmname = row['domain']
    maindo = row['maindo']
    if '环球' in maindo:
        if pd.notna(url) and pd.isna(row['source_time']) and pd.notna(row['cite_time']) and pd.isna(row['timestamp_x']) and pd.isna(row['org']) and pd.isna(row['htmltimestamp']) and pd.isna(row['handtime']):
            try:
                date = find_date(url, outputformat='%Y-%m-%d %H:%M')
                #time.sleep(5)
            except ValueError:
                date = pd.NaT
            df.at[index,'htmltimestamp'] = date
            print(row['entry'],index,date)
        #df.at[index,'timestamp'] = date

#os.chdir('D:\zsq')


df.loc[df['htmltimestamp'] == '2023-03-23 00:00','htmltimestamp'] = pd.NaT
df.loc[(df['htmltimestamp'].str.contains('01-01 00:00')) & (df['htmltimestamp'].notna()),'htmltimestamp'] = pd.NaT
df.loc[pd.to_datetime(df['htmltimestamp']) > datetime.datetime(2023,1,17,00,00,00),'htmltimestamp'] = pd.NaT


#正确的   
# www.jfdaily.com
# www.81.cn
# www.js7tv.cn
# www.cet.com.cn
# ie.bjd.com.cn
# t.ynet.cn
# wsjkw.gd.gov.cn
# www.mofcom.gov.cn
# www.mod.gov.cn
# www.gcs.gov.mo
# www.gov.mo
# 3g.k.sohu.com #同时是应用程序
# k.sina.com.cn
# m.bjnews.com.cn
# slide.sports.sina
# slide.ent.sina.com.cn
# cj.sina.com.cn
# k.sina.cn
# news.hbtv.com.cn
# m.voc.com.cn
# www.thepaper.cn
# m.thepaper.cn
# hqtime.huanqiu.com
# 3w.huanqiu.com
# baijiahao.baidu.com
# static.cdsb.com


# origin_url:
# www.sohu.com/a
# www.xinhuanet.com/world

df.to_csv("ci+htmltimestamp.csv", index=True)


df.to_sql('ci_time_hd', conn, index=False, if_exists = 'replace')
conn.close()
