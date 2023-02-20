#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 01:22:24 2023

@author: zhangsiqi

对原始数据进行格式、解析等处理
1.
2.对URL的处理：提取出其中的参考资料发布时间和域名
3. 使用htmldate库补充参考资料发布时间
"""
#%% 从URL中提取日期和域名
#修正URL时间解析错误 20230126，之前为了容错/20190829af20结果引入了/20190836af67的噪音
import re
from urllib.parse import urlparse
import requests
import pandas as pd
import numpy as np
import sqlite3 as sqlite
import os

def get_pubtime_by_url(url):    
    m0 = re.search(r'/t(?P<all>20\d{6})_', url) #如/t20150324_
    m1 = re.search(r'[/_](?P<year>20[0-2][0-9])[-/_]?(?P<month>[0-1][0-9])[-/_]?(?P<date>[0-3][0-9])[/_]', url) #如/2018/0324/
    m2 = re.search(r'view\.inews\.qq\.com/\S+(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url) #如https://view.inews.qq.com/a/NEW2019082900295010?uid=
    m3 = re.search(r'/(?P<year>[0-2][0-9])[/-](?P<month>[0-1]?[0-9])[/-]?(?P<date>[0-3]?[0-9])/', url) #如/12/11-22/
    m4 = re.search(r'xinhuanet\.com/\S+(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url)
    m5 = re.search(r'/(?P<year>20[0-2][0-9])[/-](?P<month>[0-1]?[0-9])[/-](?P<date>[0-3]?[0-9])/', url) #/art/2021/5/26/art
    
    if m1:
        date = m1.groupdict()['year']+'-'+ m1.groupdict()['month']+'-'+ m1.groupdict()['date']
        return date
    if m0:
        #print(m0.group())
        date = m0.groupdict()['all'][:4] +'-'+ m0.groupdict()['all'][4:6] +'-'+ m0.groupdict()['all'][6:8]
        return date
    if m2:
        date = m2.groupdict()['year']+'-'+ m2.groupdict()['month']+'-'+ m2.groupdict()['date']
        return date
    if m3:
        date = '20'+m3.groupdict()['year']+'-'+ m3.groupdict()['month']+'-'+ m3.groupdict()['date']
        return date
    if m4:
        date = m4.groupdict()['year']+'-'+ m4.groupdict()['month']+'-'+ m4.groupdict()['date']
        return date
    if m5:
        date = m5.groupdict()['year']+'-'+ m5.groupdict()['month']+'-'+ m5.groupdict()['date']
        print(url, date)
        return date
    if m0 == None and m1 == None and m2 == None and m3 == None and m4 == None and m5 == None:
        return None

#print(get_pubtime_by_url('http://www.haishu.gov.cn/art/2021/5/26/art_1229100495_58940958.html'))

os.chdir('/Volumes/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0125修正百科source时间提取错误')

df = pd.read_csv('citation+html2date-修正soti.csv',index_col=('Unnamed: 0'))

for index, row in df.iterrows():
    url = row['origin_url']
    if pd.isna(url) == False:
        
        date = get_pubtime_by_url(url) #不能用urlpath因为得到的urlpath并不完整
        df.at[index, 'url_time'] = date
        
        print(index, url, date)

os.chdir('/Volumes/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0216修正regex解析URL时间错误')

df.to_csv("citation+ht2t+updateurlti.csv",index=True)

conn3= sqlite.connect('citation+ht2t+updateurlti.sqlite')
df.to_sql('citation', conn3, index=True, if_exists = 'replace')
conn3.close()    




