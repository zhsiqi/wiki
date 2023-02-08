#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:59:40 2023

@author: zhangsiqi
"""


import re
import pandas as pd
import numpy as np
import os
import datefinder
import sqlite3 as sqlite
import datetime
import time

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情')
df = pd.read_csv('wikitextsql.csv')
dfev = pd.read_csv('eventssql.csv', index_col='Unnamed: 0')

df['date_strict'] = pd.NaT
df['withmon'] = pd.NaT
df['date_more'] = pd.NaT

df['text_copy'] = df['wiki_text'].replace(regex =['-','小时','0—24时','0时—24时'], value = 'interval ')
#df['text_copy'] = df['text_copy'].replace(to_replace =r'\d+(\.\d+)万|亿|公|千|米', value = 'interval ', regex=True)

df['text_copy'] = df['text_copy'].replace(to_replace =r'次年\d+月', value = 'interval ', regex=True)
df['text_copy'] = df['text_copy'].replace(to_replace =r'\d+年\d+个多?月', value = 'interval ', regex=True)

df['text_copy'] = df['text_copy'].replace(to_replace =r'\d+(\.\d+)([\u4e00-\u9fa5]|\u3002|\uff1b|\uff0c|\uff1a|\u201c|\u201d|\uff08|\uff09|\u3001|\uff1f|\u300a|\u300b)', value = 'interval ', regex=True)
df['text_copy'] = df['text_copy'].replace(to_replace =r'\d+月(底|上旬|中旬|下旬|末|初|\u3002|\uff1b|\uff0c|\uff1a|\u201c|\u201d|\uff08|\uff09|\u3001|\uff1f|\u300a|\u300b)', value = 'interval ', regex=True)
df['text_copy'] = df['text_copy'].replace(regex =['年','月'], value = '-')

df['text_copy'] = df['text_copy'].replace(to_replace =r'(上午|早上|早|凌晨)(\d+)(点|时)[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]', value = r'\2:00am ', regex=True)
df['text_copy'] = df['text_copy'].replace(to_replace =r'(下午|中午|晚上|晚)(\d+)(点|时)[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]', value = r'\2:00pm ', regex=True)

df['text_copy'] = df['text_copy'].replace(to_replace = r'(下午|晚上|晚|夜)(\d+)(点|时)(\d+)分?', value = r'\2:\4pm', regex=True)
df['text_copy'] = df['text_copy'].replace(to_replace = r'(上午|早上|早|凌晨)(\d+)(点|时)(\d+)分?', value = r'\2:\4am', regex=True)

df['text_copy'] = df['text_copy'].replace(regex =['点','时','分'], value = ':')
df['text_copy'] = df['text_copy'].replace(regex =['秒','日'], value = ' ')

for index, row in dfev.iterrows():
#for index, row in df[0:50].iterrows():
    year = row['year']
    #base_time = datetime.datetime(year,1,1)
    df_wev = df[df['entry'] == row['entry']]
    for windex, wrow in df_wev.iterrows(): 
        if pd.notna(wrow['text_copy']):
            text = wrow['text_copy']
            matches = datefinder.find_dates(text, strict=True)
            timeli = []
            for match in matches:
                if match.year < 2024 and match.year > 2000:
                    timeli.append(str(match))
                    #base_time = match
            df_wev.at[windex,'date_strict'] = str(timeli)
            
            matches_blur = datefinder.find_dates(text, source=True)
            origin_timeli = []
            for match in matches_blur:
                b = match[1]
                origin_timeli.append(b)
            withm = [i for i in origin_timeli if '-' in i]
            df_wev.at[windex,'withmon'] = str(withm)
            
    df.loc[df['entry'] == row['entry'],'date_strict'] = df_wev['date_strict']
    df.loc[df['entry'] == row['entry'],'withmon'] = df_wev['withmon']


conn3= sqlite.connect('wikitexttime-base.sqlite')
df.to_sql('wikitexttime', conn3, index=True, if_exists = 'replace')
conn3.close()




#if match.year > 1999

#%%
import datefinder
import re
from zhon.hanzi import punctuation


text = '2011-8-8 20:30:05 thus gygsYu gysd  gcdysg 9-9 '
text = '钱云会（1957年10月13日-2010年12月25日)男，汉族，浙江省温州市乐清市蒲岐镇寨桥村人，2005年当选村主任后，因土地纠纷问题带领村民上访。在5年的上访过程中，先后3次被投入看守所。2010年12月25日上午9时，被工程车撞死。有网友爆料，钱云会是被“有些人故意害死的”，乐清市公安局在随后的发布会上称，这是一起交通肇事事故，钱云会当时撑一把雨伞从右侧向左侧横穿马路，工程车紧急刹车但仍与死者发生碰撞，造成钱云会当场死亡。2011年1月29日，据报道公安机关已查获了钱云会出事当天所戴的附有微录设备的手表。'
#text = '《铁路旅客意外伤害强制保险条例》规定每个人赔付两万元保险金额；发生死亡的情况下，《铁路交通事故应急救援和调查处理条例》规定，旅客人身伤亡赔偿限额为，行李损失赔偿限额为。三项相加的上限应该是。事故给出的赔偿91.5万突破了这样的数额。中国人民大学等机构召开了研讨会，探讨事故赔偿的法律问题，也有学者撰文对赔偿问题提出意见。'
text = '2011年10月13日下午5点30分'

#df['text_copy'] = df['text_copy'].replace(to_replace =r'(上午|早上|早|凌晨)\d(点|时)[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]', value = ':', regex=True)

text = re.sub(r'\d+(\.?\d+)万|亿|元|美元|%', 'interval ', text)
text = re.sub(r'-', 'interval ', text)
text = re.sub(r'(上午|早上|早|凌晨)(\d)(点|时)[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]',r'\2:00am ',text)

text = re.sub(r'(下午|晚上|晚|夜)(\d)(点|时)[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]',r'\2:00pm ',text)

text = re.sub(r'(下午|晚上|晚|夜)(\d+)(点|时)(\d+)',r'\2:\4 pm',text)
text = re.sub(r'小时', 'interval', text)
text = re.sub(r'年|月', '-', text)
text = re.sub(r'点|时|分', ':', text)
text = re.sub(r'秒|日', ' ', text)


matches = datefinder.find_dates(text,source=True)

for match in matches:
    print(match)

#%%
import datetime
import time

timestr = '1991-02-07 00:00:00'

date_time = datetime.datetime.strptime(timestr,'%Y-%m-%d %H:%M:%S')
time_time = time.mktime(date_time.timetuple())




