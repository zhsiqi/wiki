#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 20:05:47 2023

@author: zhangsiqi
"""

# =======
import pandas as pd
from selenium.common.exceptions import TimeoutException
from seleniumwire import webdriver
import datetime
import sqlite3 as sqlite
# =========================================================
# （1）找到链接是空的行
# （2）使用wire-webdriver 定位原始链接和状态码，这个状态码可能有错
df = pd.read_csv('citation+strong.csv',index_col=0)
df = df.drop(['Unnamed: 0.1.1','Unnamed: 0.1.1.1'], axis=1) #删除之前的多余索引
df['status_collect_time'] = 'NA' #添加列记录时间
df['status_code'] = df['status_code'].astype(str) #把变量变为字符串类型,或者 df['A'] = df['A'].astype(str)
print(df.dtypes)


for index, row in df.iterrows():
    oriurl = row['original_url']
    line = row['redir_url']
    
    if pd.isna(oriurl) and pd.isna(line)==False: #需要补充原始链接的行：判断原始链接为空的行，且redirlink不为空
        driver = webdriver.Chrome('chromedriver')
        try:
            driver.set_page_load_timeout(30)
            driver.set_script_timeout(30)#这两种设置都进行才有效
            # jssc = '''window.open("'''+ line.strip() + '''", 'new_window')'''
            # driver.execute_script(jssc)
            # driver.switch_to.window(driver.window_handles[-1])
            driver.get(line)
            print('当前url',driver.current_url)
        except TimeoutException:
            df.at[index, 'original_url'] = '30s超时'
            df.at[index, 'status_code'] = '30s超时'
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '30s超时')
        else:
            #driver.switch_to.window(driver.window_handles[-1])
            b = driver.requests[1] #
            if b.response:
                df.at[index, 'original_url'] = b.url
                df.at[index, 'status_code'] = b.response.status_code     
                df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(index, '原始链接', b.url[0:20],'原始链接状态码',b.response.status_code)
                
            if len(driver.requests) >= 3:
                if driver.requests[2].response:
                    c = driver.requests[2] #这个https请求有时候存在
                    print(index, '原始链接2', c.url[0:20],'原始链接状态码2',c.response.status_code)
        driver.close()
    

#if df['ir'].notnull().sum()

driver.quit()
df.to_csv('citation+原始链接补全完成.csv')

conn = sqlite.connect('citation+原始链接补全完成-test.sqlite')
df.to_sql('citation+origi', conn, index=False)
conn.close()
