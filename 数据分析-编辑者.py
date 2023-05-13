#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 12:55:27 2023

@author: zhangsiqi
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

df = pd.read_excel('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0512补充作者/events.xlsx',index_col=0)


dfac = df['author_count_1']

manygr = pd.cut(dfac, bins=[1,10,20,50,100,500])
manygr_des = dfac.groupby(manygr).describe()
manygr_des.to_excel('author_count_multi_des.xlsx', index=True)

dfac.describe()

# count    272.000000
# mean      39.573529
# std       54.804400
# min        2.000000
# 25%       12.000000
# 50%       21.000000
# 75%       46.000000
# max      466.000000
# Name: author_count_1, dtype: float64

dfac.hist()


# 每个编辑者的次数分布
df1 = pd.read_excel('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0512补充作者/作者编辑次数分布.xlsx',index_col=0)

dfedic = df1['author_name']

manygr1 = pd.cut(dfedic, bins=[0,1,3,10,50,3500])
manygr1_des = dfedic.groupby(manygr1).describe()
manygr1_des.to_excel('author_edit_count_multi_des.xlsx', index=True)

dfedic.describe()

# count    272.000000
# mean      39.573529
# std       54.804400
# min        2.000000
# 25%       12.000000
# 50%       21.000000
# 75%       46.000000
# max      466.000000
# Name: author_count_1, dtype: float64

dfedic.hist()


#%% 找到每个词条的创建者，也即author_name序列的第一个

dfev = pd.read_excel('events_ac.xlsx', index_col=0)
dfev['firstauthor'] = None

dfedi = pd.read_excel('edit_time_reindex.xlsx', index_col=0)

for index, row in dfev.iterrows():
#for index, row in dfev[141:142].iterrows():
    dfau = dfedi.loc[dfedi['entry'] == row['entry'],'author_name']
    if not dfau.empty:
        author_first = dfau[dfau.index.max()] #取出最大的序列号的对应作者，也即创建者
        
    else:
        author_first = None
        
    dfev.at[index, 'firstauthor'] = author_first


dfev.to_excel('event.xlsx')

















