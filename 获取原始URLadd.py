#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 16:01:02 2023

@author: zhangsiqi
"""

import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException
from seleniumwire import webdriver
import datetime
import sqlite3 as sqlite
# %%15s为限获取链接
# （1）找到链接是空的行
# （2）使用webdriver获取原始链接和状态码，这个状态码可能有错

df = pd.read_csv('ci02-14-14-25.csv')
#df['status_collect_time'] = 'NA' #添加列记录时间
df['status_code'] = df['status_code'].astype(str) #把变量变为字符串类型
print(df.dtypes)

driver = webdriver.Chrome('chromedriver')

for index, row in df.iterrows():
    oriurl = row['original_url']
    line = row['redir_url']
    
    if pd.isna(oriurl) and pd.isna(line)==False: #需要补充原始链接的行：判断原始链接为空的行，且redirlink不为空
        
        try:
            driver.set_page_load_timeout(15)
            driver.set_script_timeout(15)#这两种设置都进行才有效
            jssc = '''window.open("'''+ line.strip() + '''", 'new_window')'''
            driver.execute_script(jssc)
            driver.switch_to.window(driver.window_handles[-1])
            link = driver.current_url
        except TimeoutException:
            df.at[index, 'original_url'] = '15s超时'
            #df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '15s超时')
        except UnexpectedAlertPresentException:
            driver.switch_to.alert.accept()
            df.at[index, 'original_url'] = link
            #df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '弹窗错误', link)
        except WebDriverException:
            df.at[index, 'original_url'] = 'driver错误'
            #df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, 'driver错误')
        else:
            df.at[index, 'original_url'] = link
            #df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '原始链接', driver.current_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    
driver.quit()
df.to_csv('ci+原始链接补15s.csv',index=True)

conn = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0214补充词条数据/Wiki+1.sqlite.sqlite')
df.to_sql('ci+15s', conn, index=True)
conn.close()

over_count = ((df['original_url'] == '15s超时')|(df['original_url'] == 'driver错误')).sum()
print('后面需要处理的超时等链接个数为', over_count)

#%%100s为限获取链接
df = pd.read_csv('citation+原始链接补15s.csv',index_col=0)

driver = webdriver.Chrome('chromedriver')

for index, row in df.iterrows():
    oriurl = row['original_url']
    line = row['redir_url']
    if ((oriurl == '15s超时')|(oriurl == 'driver错误')|(oriurl == '弹窗错误')) and pd.isna(line)==False: #需要补充原始链接的行：判断原始链接为空的行，且redirlink不为空
        try:
            driver.set_page_load_timeout(100)
            driver.set_script_timeout(100)#这两种设置都进行才有效
            jssc = '''window.open("'''+ line.strip() + '''", 'new_window')'''
            driver.execute_script(jssc)
            driver.switch_to.window(driver.window_handles[-1])
            link = driver.current_url
        except TimeoutException:
            df.at[index, 'original_url'] = '100s超时'
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '100s超时')
        except UnexpectedAlertPresentException:
            driver.switch_to.alert.accept()
            df.at[index, 'original_url'] = link
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '弹窗错误')
        except WebDriverException:
            df.at[index, 'original_url'] = 'driver错误'
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, 'driver错误')
        else:
            df.at[index, 'original_url'] = link
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '原始链接', driver.current_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    
driver.quit()

df.to_csv('citation+原始链接补100s.csv',index=False)

conn = sqlite.connect('citation+原始链接补100s.sqlite')
df.to_sql('citation+origi100s', conn, index=False)
conn.close()

over_count = ((df['original_url'] == '100s超时')|(df['original_url'] == 'driver错误')).sum()
print('后面需要处理的超时链接个数为', over_count)

#%%300s为限获取链接

df = pd.read_csv('citation+原始链接100s-完整.csv',index_col=0)

driver = webdriver.Chrome('chromedriver')

for index, row in df.iterrows():
    oriurl = row['original_url']
    line = row['redir_url']
    if ((oriurl == '100s超时')|(oriurl == 'driver错误')) and pd.isna(line)==False: #需要补充原始链接的行：判断原始链接为空的行，且redirlink不为空
        try:
            driver.set_page_load_timeout(300)
            driver.set_script_timeout(300)#这两种设置都进行才有效
            jssc = '''window.open("'''+ line.strip() + '''", 'new_window')'''
            driver.execute_script(jssc)
            driver.switch_to.window(driver.window_handles[-1])
            link = driver.current_url
        except TimeoutException:
            df.at[index, 'original_url'] = '300s超时'
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '300s超时')
        except UnexpectedAlertPresentException:
            driver.switch_to.alert.accept()
            df.at[index, 'original_url'] = link
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '弹窗错误')
        except WebDriverException:
            df.at[index, 'original_url'] = 'driver错误'
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, 'driver错误')
        else:
            df.at[index, 'original_url'] = link
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '原始链接', driver.current_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    
driver.quit()

df.to_csv('citation+原始链接补300s.csv',index=False)

conn = sqlite.connect('citation+原始链接补300s.sqlite')
df.to_sql('citation+origi300s', conn, index=False)
conn.close()

over_count = ((df['original_url'] == '300s超时')|(df['original_url'] == 'driver错误')).sum()
print('后面需要处理的超时链接个数为', over_count)

#%%1000s为限获取链接
df = pd.read_csv('citation+原始链接补300s.csv')
df.index += 1

driver = webdriver.Chrome('chromedriver')

for index, row in df.iterrows():
    oriurl = row['original_url']
    line = row['redir_url']
    if ((oriurl == '300s超时')|(oriurl == 'driver错误')) and pd.isna(line)==False: #需要补充原始链接的行：判断原始链接为空的行，且redirlink不为空
        try:
            driver.set_page_load_timeout(1000)
            driver.set_script_timeout(1000)#这两种设置都进行才有效
            jssc = '''window.open("'''+ line.strip() + '''", 'new_window')'''
            driver.execute_script(jssc)
            driver.switch_to.window(driver.window_handles[-1])
            link = driver.current_url
        except TimeoutException:
            df.at[index, 'original_url'] = '1000s超时'
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '1000s超时')
        except UnexpectedAlertPresentException:
            driver.switch_to.alert.accept()
            df.at[index, 'original_url'] = link
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '弹窗错误')
        except WebDriverException:
            df.at[index, 'original_url'] = 'driver错误'
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, 'driver错误')
        else:
            df.at[index, 'original_url'] = link
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '原始链接', driver.current_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    
driver.quit()

df.to_csv('citation+原始链接补1000s.csv',index=True)

conn = sqlite.connect('citation+原始链接补1000s.sqlite')
df.to_sql('citation+origi600s', conn, index=True)
conn.close()

over_count = ((df['original_url'] == '1000s超时')|(df['original_url'] == 'driver错误')).sum()
print('后面需要处理的超时链接个数为', over_count)





