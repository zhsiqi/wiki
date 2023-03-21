#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 16:01:02 2023

@author: zhangsiqi
"""
"""
新增加了词条，在redirect链接基础上得到参考资料原始UR
"""

import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException
from seleniumwire import webdriver
import datetime
import sqlite3 as sqlite
# 15s为限获取链接
# （1）找到链接是空的行
# （2）使用webdriver获取原始链接和状态码，这个状态码可能有错

conn = sqlite.connect('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1.sqlite')
c = conn.cursor()
df = pd.read_sql('SELECT * FROM ci', conn)

#df = pd.read_csv('ci02-14-14-25sql.csv')
#df['status_collect_time'] = 'NA' #添加列记录时间
#df['status_code'] = df['status_code'].astype(str) #把变量变为字符串类型
print(df.dtypes)

driver = webdriver.Chrome('chromedriver')

for index, row in df.iterrows():
    oriurl = row['origin_url']
    badurl = row['original_url']
    line = row['redir_url']
    if pd.isna(oriurl) and pd.isna(badurl) and pd.isna(line)==False: #需要补充原始链接的行：判断原始链接为空的行，且redirlink不为空
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

# conn = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0214补充词条数据/Wiki+1.sqlite')
df.to_sql('ci+15s', conn, index=False, if_exists = 'replace')
conn.close()

over_count = ((df['original_url'] == '15s超时')|(df['original_url'] == 'driver错误')).sum()
print('后面需要处理的超时等链接个数为', over_count)

#%%200s为限获取链接
import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException
from seleniumwire import webdriver
import datetime
import sqlite3 as sqlite

conn = sqlite.connect('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1.sqlite')
c = conn.cursor()
df = pd.read_sql("""SELECT * FROM 'ci+15s'""", conn)

#df = pd.read_csv('ci+原始链接补15s.csv',index_col=0)

driver = webdriver.Chrome('chromedriver')

for index, row in df.iterrows():
    oriurl = row['original_url']
    line = row['redir_url']
    if ((oriurl == '15s超时')|(oriurl == 'driver错误')|(oriurl == '弹窗错误')) and pd.isna(line)==False: #需要补充原始链接的行：判断原始链接为空的行，且redirlink不为空
        try:
            driver.set_page_load_timeout(200)
            driver.set_script_timeout(200)#这两种设置都进行才有效
            jssc = '''window.open("'''+ line.strip() + '''", 'new_window')'''
            driver.execute_script(jssc)
            driver.switch_to.window(driver.window_handles[-1])
            link = driver.current_url
        except TimeoutException:
            df.at[index, 'original_url'] = '200s超时'
            df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(index, '200s超时')
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

df.to_csv('ci+200s.csv',index=False)

# conn = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0214补充词条数据/Wiki+1.sqlite')
df.to_sql('ci+200s', conn, index=False, if_exists = 'replace')
conn.close()

over_count = ((df['original_url'] == '200s超时')|(df['original_url'] == 'driver错误')).sum()
print('后面需要处理的超时链接个数为', over_count)


#人工补足200s超时
link1 = 'https://baike.baidu.com/reference/50157160/7fe7rC6hCg-75LPSYfVKa9jJBDcV4OEDKrIFTF1p26BhcYDvoVqJg3oa3VotAjP_dwfeZjjJIkp7W_AtfDiuehmAzUqgX7UviMypxg'
link2 = 'https://baike.baidu.com/reference/8034979/aef5PvzGRcB5u1ZK8-cypHU9FCZilhSE_xYA8UBpXIGWhum9LzbbByG88Tj281fFsQ5y2VlSQYMe2IM4O4UxQyHX6XlhvaZ0CnMd5v0'
link3 = 'https://baike.baidu.com/reference/8034979/2b72Fm8ke9A5-tK8og8PFTRZ6CSslr829jAgViC19s-vINrCO6ktJvBjBGuxSyNycsEE1upDgFhbaf84pv-npr95GuLh-LlvtmWnAMZSg7vCNOUefI1nwCuH2arR'
link4 = 'https://baike.baidu.com/reference/59764769/b423nPS5fStJ9yKodHRj8nBJRN8GG_IP_H_4gaT7VxfFSEu1d427bsgRwcF51IKIDuK07IqChgKp-0uctg1yA7-kv_-Df9VfKJl3'
link5 = 'https://baike.baidu.com/reference/12061628/8b17ZC4wBAqWOvpYjtfS05TgE-5DYAGDvtO-PMpHxZRHZonxUr_uenZobSYaD4WXatYRv3hSVcsXfLoPML9faAk8r_MhUAg8'

tlink1 = 'https://www.gcs.gov.mo/detail/zh-hant/N20BDLplKR'
tlink2 = 'https://www.ettoday.net/news/20150319/477032.htm'
tlink3 = 'https://ent.sina.com.cn/s/h/2022-05-09/doc-imcwiwst6464205.shtml'
tlink4 = 'https://taiwan.huanqiu.com/article/48wOcNacEgW'
tlink5 = 'https://olympics.com/en/olympic-games/beijing-2022/mascot'


conn = sqlite.connect('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1.sqlite')
c = conn.cursor()
df = pd.read_sql("""SELECT * FROM 'ci+200s'""", conn)

df.loc[df['reference_url']==link1,'original_url'] = tlink1
df.loc[df['reference_url']==link2,'original_url'] = tlink2
df.loc[df['reference_url']==link3,'original_url'] = tlink3
df.loc[df['reference_url']==link4,'original_url'] = tlink4
df.loc[df['reference_url']==link5,'original_url'] = tlink5

df.loc[pd.isna(df['origin_url']) & pd.notna(df['redir_url']),'origin_url']=df['original_url']
# conn = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0214补充词条数据/Wiki+1.sqlite')
df.to_sql('ci2023-03-21', conn, index=False, if_exists='replace')
conn.close()

# #%%300s为限获取链接

# df = pd.read_csv('citation+原始链接100s-完整.csv',index_col=0)

# driver = webdriver.Chrome('chromedriver')

# for index, row in df.iterrows():
#     oriurl = row['original_url']
#     line = row['redir_url']
#     if ((oriurl == '100s超时')|(oriurl == 'driver错误')) and pd.isna(line)==False: #需要补充原始链接的行：判断原始链接为空的行，且redirlink不为空
#         try:
#             driver.set_page_load_timeout(300)
#             driver.set_script_timeout(300)#这两种设置都进行才有效
#             jssc = '''window.open("'''+ line.strip() + '''", 'new_window')'''
#             driver.execute_script(jssc)
#             driver.switch_to.window(driver.window_handles[-1])
#             link = driver.current_url
#         except TimeoutException:
#             df.at[index, 'original_url'] = '300s超时'
#             df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             print(index, '300s超时')
#         except UnexpectedAlertPresentException:
#             driver.switch_to.alert.accept()
#             df.at[index, 'original_url'] = link
#             df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             print(index, '弹窗错误')
#         except WebDriverException:
#             df.at[index, 'original_url'] = 'driver错误'
#             df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             print(index, 'driver错误')
#         else:
#             df.at[index, 'original_url'] = link
#             df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             print(index, '原始链接', driver.current_url)
#         driver.close()
#         driver.switch_to.window(driver.window_handles[-1])
    
# driver.quit()

# df.to_csv('citation+原始链接补300s.csv',index=False)

# conn = sqlite.connect('citation+原始链接补300s.sqlite')
# df.to_sql('citation+origi300s', conn, index=False)
# conn.close()

# over_count = ((df['original_url'] == '300s超时')|(df['original_url'] == 'driver错误')).sum()
# print('后面需要处理的超时链接个数为', over_count)

# #%%1000s为限获取链接
# df = pd.read_csv('citation+原始链接补300s.csv')
# df.index += 1

# driver = webdriver.Chrome('chromedriver')

# for index, row in df.iterrows():
#     oriurl = row['original_url']
#     line = row['redir_url']
#     if ((oriurl == '300s超时')|(oriurl == 'driver错误')) and pd.isna(line)==False: #需要补充原始链接的行：判断原始链接为空的行，且redirlink不为空
#         try:
#             driver.set_page_load_timeout(1000)
#             driver.set_script_timeout(1000)#这两种设置都进行才有效
#             jssc = '''window.open("'''+ line.strip() + '''", 'new_window')'''
#             driver.execute_script(jssc)
#             driver.switch_to.window(driver.window_handles[-1])
#             link = driver.current_url
#         except TimeoutException:
#             df.at[index, 'original_url'] = '1000s超时'
#             df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             print(index, '1000s超时')
#         except UnexpectedAlertPresentException:
#             driver.switch_to.alert.accept()
#             df.at[index, 'original_url'] = link
#             df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             print(index, '弹窗错误')
#         except WebDriverException:
#             df.at[index, 'original_url'] = 'driver错误'
#             df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             print(index, 'driver错误')
#         else:
#             df.at[index, 'original_url'] = link
#             df.at[index, 'status_collect_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             print(index, '原始链接', driver.current_url)
#         driver.close()
#         driver.switch_to.window(driver.window_handles[-1])
    
# driver.quit()

# df.to_csv('citation+原始链接补1000s.csv',index=True)

# conn = sqlite.connect('citation+原始链接补1000s.sqlite')
# df.to_sql('citation+origi600s', conn, index=True)
# conn.close()

# over_count = ((df['original_url'] == '1000s超时')|(df['original_url'] == 'driver错误')).sum()
# print('后面需要处理的超时链接个数为', over_count)





