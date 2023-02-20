#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 01:41:44 2023

@author: zhangsiqi
没啥用
"""

#%% 获取状态码
import requests
import pandas as pd
import numpy as np
import sqlite3 as sqlite


df = pd.read_csv('citation.csv')

for index, row in df.iterrows():
    # print('line',line.strip())
    url = row['origin_url']
    if pd.isna(url) == False:
        try:
            html = requests.head(url,timeout=60) # 用head方法去请求资源头部
        except requests.ConnectionError:
            # print("OOPS!! Connection error")
            status_code = 'Connection Error'
        except requests.Timeout:
            # print("OOPS!! Timeout Error")
            status_code = 'Timeout error'
        except requests.RequestException:
            # print("OOPS!! General Error")
            status_code = 'General error'
        else:
            status_code = html.status_code
        finally:
            print('7214 -',index, url[:20],'http状态码', status_code) #参考资料的状态码
            df.at[index, 'status_code'] = status_code
        

df.to_csv("citation+code.csv",index=False)

conn2= sqlite.connect('citation+code.sqlite')
df.to_sql('citation+code', conn2, index=True)
conn2.close()

#语音播报结束
import pyttsx3
engine = pyttsx3.init()  # 创建engine并初始化
engine.say("本程序运行结束")
engine.runAndWait()  # 等待语音播报完毕


over_count = (df['status_code'] == 200).sum()
print('后面需要处理的超时等链接个数为', 7414-over_count) #后面需要处理的超时等链接个数为 2838
