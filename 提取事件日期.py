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

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情')
df = pd.read_csv('wikitextsql.csv')

df['finddate'] = pd.NaT


df['text_copy'] = df['wiki_text'].replace(regex =['小时'], value = 'interval')
df['text_copy'] = df['text_copy'].replace(regex =['年','月'], value = '-')
df['text_copy'] = df['text_copy'].replace(regex =['点','时','分'], value = ':')
df['text_copy'] = df['text_copy'].replace(regex =['秒','日'], value = ' ')


for index, row in df[0:50].iterrows():
    text = row['text_copy']
    matches = datefinder.find_dates(text)
    for match in matches:
        print(index,match)





#%%
import datefinder

text = '2011-8-8 20:30:05 thus gygsYu gysd  gcdysg 9-9 '

matches = datefinder.find_dates(text)

for match in matches:
    print(match)