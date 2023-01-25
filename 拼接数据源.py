#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 16:11:17 2023

@author: zhangsiqi
拼接csv数据
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pylab as plt



os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0124补充卫健委等时间')

df = pd.read_csv('citation+news-nhc-6.csv',index_col='Unnamed: 0')

#%% status_code 修正
/404




#%%
notici = pd.isna(df['cite_time']).sum()
print('引用时间缺失',notici)

#筛选出引用时间存在，但各种源时间都不存在的行
a = df[(df['cite_time'].notna()) & (df['source_time'].isna()) & \
   (df['url_time'] == "['None', 'None', 'None']") & (df['timestamp'].isna())]

print('有引用时间但各种源时间都没有', len(a))

a.groupby("status_code")["status_code"].count().plot(kind="bar")
plt.show()

tici = df['cite_time']
tiso = df['source_time']
tiurl = df['url_time']
ticraw = df['timestamp']
tihtor = df['htmldate_ori']
tihtup = df['htmldate_upd']
