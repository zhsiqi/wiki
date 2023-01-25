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
import sqlite3 as sqlite



os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0125补充htmldate时间')

df = pd.read_csv('citation+html2date.csv', index_col='Unnamed: 0')

#查看每列的缺失值
print(df.isnull().sum())


#第一次直接复制sourcetime
df['pub_time'] = df['source_time']

#第二次将urltime不为空的值重叠到pubtime一列
df['pub_time'] = df['pub_time'].where(df['url_time'].notna(), df['url_time'])

conn3= sqlite.connect('test移动.sqlite')
df.to_sql('citation', conn3, index=True, if_exists = 'replace')
conn3.close()

#%% status_code 修正，后面有空再说



#%% cnOCR
from cnocr import CnOcr

img_fp = '/Users/zhangsiqi/Desktop/毕业论文代码mini/testrm.png'
ocr = CnOcr(det_model_name='naive_det')  # 所有参数都使用默认值
out = ocr.ocr(img_fp)

print(out)


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
