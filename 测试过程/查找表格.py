#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 13:06:34 2023

@author: zhangsiqi
"""
#如果只用查找一个表格的话

import pandas as pd
url="https://baike.baidu.com/historylist/2004%E5%B9%B4%E9%9B%85%E5%85%B8%E5%A5%A5%E8%BF%90%E4%BC%9A/5373487#page1"
url1='https://baike.baidu.com/historylist/2004%E5%B9%B4%E9%9B%85%E5%85%B8%E5%A5%A5%E8%BF%90%E4%BC%9A/5373487#page3'

tables = pd.read_html(url)
tables1 = pd.read_html(url1)

print(tables)
print(tables1)


df = tables[0]
df1 = tables1[0]

df3 = pd.concat([df,df1],ignore_index=True, sort=False)
all_table = df3[['提交时间','贡献者']] 
# print(tables)
# print(tables1)
print(all_table)
print(all_table.dtypes)
print(all_table.iloc[20]['提交时间'])