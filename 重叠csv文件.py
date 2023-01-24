#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 13:53:10 2023

@author: zhangsiqi
"""

#%% 重叠15s文件
import pandas as pd
import sqlite3 as sqlite

df1 = pd.read_csv('citation+原始链接补15s.csv')
df2 = pd.read_csv('citation+原始链接补15s-1.csv')
df3 = pd.read_csv('citation+原始链接补15s-3.csv')

df = df1.combine_first(df2).combine_first(df3) #将3个csv重叠
df = df.drop(columns=df.columns[0], axis=1)

df.index += 1


conn= sqlite.connect('citation+原始链接15s-完整.sqlite')
# 将数据写入
df.to_csv('citation+原始链接15s-完整.csv') #把两张相同大小的表堆叠在一起用以互相补充
df.to_sql('com-citation', conn, index=True)
conn.close()

over_count = ((df['original_url'] == '15s超时')|(df['original_url'] == '弹窗错误')|(df['original_url'] == 'driver错误')).sum()
print('后面需要处理的超时等链接个数为', over_count)


#%% 重叠100s文件
import pandas as pd
import sqlite3 as sqlite
import numpy as np

df1 = pd.read_csv('citation+原始链接补100s(1-400).csv')
df1.replace({'original_url': {'15s超时': np.nan, '弹窗错误': np.nan, 'driver错误': np.nan}},inplace=True) #15s必须替换为空值，否则重叠失效

df2 = pd.read_csv('citation+原始链接补100s(401-800).csv')
df2.replace({'original_url': {'15s超时': np.nan, '弹窗错误': np.nan, 'driver错误': np.nan}},inplace=True) #15s必须替换为空值，否则重叠失效

df3 = pd.read_csv('citation+原始链接补100s(801-936).csv')
df3.replace({'original_url': {'15s超时': np.nan, '弹窗错误': np.nan, 'driver错误': np.nan}},inplace=True) #15s必须替换为空值，否则重叠失效

df = df1.combine_first(df2).combine_first(df3) #将3个csv重叠

df.index += 1


conn= sqlite.connect('citation+原始链接100s-完整.sqlite')
# 将数据写入
df.to_csv('citation+原始链接100s-完整.csv') #把两张相同大小的表堆叠在一起用以互相补充
df.to_sql('com-citation', conn, index=True)
conn.close()

over_count = ((df['original_url'] == '100s超时')|(df['original_url'] == '弹窗错误')|(df['original_url'] == 'driver错误')).sum()
print('后面需要处理的超时等链接个数为', over_count)

over_count = ((df['original_url'] == '弹窗错误')|(df['original_url'] == 'driver错误')).sum()
print('后面需要处理的超时等链接个数为', over_count)