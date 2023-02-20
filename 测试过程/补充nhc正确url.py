#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 14:38:07 2023

@author: zhangsiqi
修正代码，可废弃，已整合至主干代码
"""

from os import path
import os
import pandas as pd
import sqlite3 as sqlite
import datetime
import numpy as np
import re

# chrome_options = uc.ChromeOptions()

# driver = uc.Chrome(
#     options=chrome_options,
#     seleniumwire_options={}
# )

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0124补充卫健委等时间')
df = pd.read_csv('citation+news-nhc-4.csv',index_col=('Unnamed: 0'))

#手动替换错误URL值
df = df.replace({'origin_url':'http://d6181c548b615eb9441.shtmlwww.nhc.gov.cn/xcs/yqfkdt/202204/311452e077aa4'},\
                'http://www.nhc.gov.cn/jkj/s7915/202204/311452e077aa4d6181c548b615eb9441.shtml')
df = df.replace({'origin_url':'http://www.nhc.gov.cn/xcs/yqfkdt/202204/0a1ca5213df34b4aa6fa65001f15906b.shtml'},\
                'http://www.nhc.gov.cn/xcs/yqtb/202204/de4ae15047034dbdb3b183165679cca6.shtml')
    
for index, row in df.iterrows():
    url = row['origin_url']
    dmname = row['domain']
    title = row['reference_title']
    if pd.isna(url) == False and "nhc.gov" in dmname:#修正错误20230125
        #用标题确定正确的URL
        qks = ['最新', '截至']
        if any(qk in title for qk in qks) and '/xcs/yqfkdt/' in url:
            url = re.sub('/xcs/yqfkdt/', '/xcs/yqtb/', url)
            df.at[index,'origin_url'] = url #替换原始url为正确的
        elif '疫苗接种情' in title and '/xcs/yqfkdt/' in url:
            if index < 5917: #卫健委的URL规则在20221109号又变了，在表中的索引是5917
                url = re.sub('/xcs/yqfkdt/', '/jkj/s7915/', url)
                df.at[index,'origin_url'] = url #替换原始url为正确的
            else:
                url = re.sub('/xcs/yqfkdt/', '/xcs/yqjzqk/', url)
                df.at[index,'origin_url'] = url #替换原始url为正确的
        
        filepath = '/Users/zhangsiqi/Desktop/毕业论文代码mini/卫健委网站'
       
        print(index, row['reference_title'], url)

#写入csv & sql
os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0124补充卫健委等时间')

df.to_csv("citation+news-nhc-5.csv", index=True)

conn3= sqlite.connect('citation+news-nhc-5.sqlite')
df.to_sql('citation+news', conn3, index=True, if_exists = 'replace')
conn3.close()

#语音播报结束
import pyttsx3
engine = pyttsx3.init()  # 创建engine并初始化
engine.say("本程序运行结束")
engine.runAndWait()  # 等待语音播报完毕
#%%
from os import path
import os
import pandas as pd
import sqlite3 as sqlite
import datetime
import numpy as np
import re


os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0124补充卫健委等时间')
df = pd.read_csv('citation+news-nhc-5.csv',index_col=('Unnamed: 0'))

df = df.replace({'domain':'d6181c548b615eb9441.shtmlwww.nhc.gov.cn'},\
                'www.nhc.gov.cn')
df.at[3504,'source'] = '卫健委官网' #替换原始url为正确的

df.to_csv("citation+news-nhc-6.csv", index=True)

conn3= sqlite.connect('citation+news-nhc-6.sqlite')
df.to_sql('citation+news', conn3, index=True, if_exists = 'replace')
conn3.close()
