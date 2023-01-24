#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 22:19:24 2023

@author: zhangsiqi
"""

import requests
import pandas as pd
import numpy as np
import sqlite3 as sqlite

#%% 拼接原始链接和新的表
#%%将sqlite表单写入多张csv
# 链接sql数据库，删除不完整的201412  
conn = sqlite.connect('BaiduWiki[01-16-00:33].sqlite')
c = conn.cursor()

c.execute(''' DELETE FROM events where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM citations where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM edithistory where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM wikilink where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM topeditor where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM wikitext where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

c.execute(''' DELETE FROM science where event_id = 201412 ''')
conn.commit()
print( "Total number of rows deleted :" , conn.total_changes)

conn.close()



def sql2csv(table_name, sqldb):
    table = pd.read_sql_query('SELECT * FROM '+ table_name, sqldb)
    table.index += 1
    table.to_csv(table_name + '[01-16-00:33]' +'sql.csv', index=True)

sql2csv('events',conn)
sql2csv('citations',conn)
sql2csv('edithistory',conn)
sql2csv('wikilink',conn)
sql2csv('topeditor',conn)
sql2csv('wikitext',conn)
sql2csv('science',conn)

c.close()
conn.close() #关闭sql

# %% 合并csv
def mergecsv(a,b):
    dfa = pd.read_csv(a,index_col=('Unnamed: 0'))
    dfb = pd.read_csv(b,index_col=('Unnamed: 0'))
    df = pd.concat([dfa,dfb], ignore_index=True, sort=False)
    df.index += 1
    df.to_csv(a[:-20]+'.csv',index=True)

mergecsv('topeditor[01-16-00:33]sql.csv', 'topeditor[01-16-23:00]sql.csv')
mergecsv('events[01-16-00:33]sql.csv', 'events[01-16-23:00]sql.csv')
mergecsv('edithistory[01-16-00:33]sql.csv', 'edithistory[01-16-23:00]sql.csv')
mergecsv('citations[01-16-00:33]sql.csv', 'citations[01-16-23:00]sql.csv')
mergecsv('science[01-16-00:33]sql.csv', 'science[01-16-23:00]sql.csv')
mergecsv('wikilink[01-16-00:33]sql.csv', 'wikilink[01-16-23:00]sql.csv')
mergecsv('wikitext[01-16-00:33]sql.csv', 'wikitext[01-16-23:00]sql.csv')

#%% 补全csv中的原始链接
df_new = pd.read_csv('citations.csv') ##等待补全链接的数据

df_ori = pd.read_csv('citation+原始链接全.csv')[['event','reference_index','reference_text','original_url']] #补充的原始链接
df_ori = df_ori.rename(columns={'event':'entry'})
df_ori = df_ori.rename(columns={'original_url':'origin_url'})
df_ori = df_ori.rename(columns={'reference_index':'reference_entryindex'})
df_ori['reference_entryindex'] = df_ori['reference_entryindex'].astype('int')
print(df_ori.dtypes)
print(df_new.dtypes)

df = pd.merge(df_new, df_ori, on=['entry','reference_text','reference_entryindex'], how='left')
print(df.dtypes)

df.at[6080,'origin_url'] = 'https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_11809/202301/t20230101_263164.html'
df.at[6081,'origin_url'] = 'https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_12208/202301/t20230101_263165.html'

conn1= sqlite.connect('com_citations.sqlite')
df.to_sql('com_citations', conn1, index=False)
conn1.close()

df.to_csv("citation.csv",index=False)


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

#%% 处理链接超时等错误状态码

















#%% 提取日期和域名
import re
from urllib.parse import urlparse
import requests
import pandas as pd
import numpy as np
import sqlite3 as sqlite
import os

#大部分正确但极少数不适用，还是分开写比较合适
#m = re.search(r'/(?P<year>(20)?[0-2][0-9])[/-]?(?P<month>[0-1]?[0-9])[/-]?(?P<date>[0-3]?[0-9])?/(t(?P<all>20\d{6})_)?', url)

def get_pubtime_by_url(url):
    m0 = re.search(r'/t(?P<all>20\d{6})_', url) #如/t20150324_
    m1 = re.search(r'[/_](?P<year>20[0-2][0-9])[/-_]?(?P<month>[0-1][0-9])[/-_]?(?P<date>[0-3][0-9])[/_a-zA-Z]', url) #如/2018/0324/
    m2 = re.search(r'/NEW(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url) #如https://view.inews.qq.com/a/NEW2019082900295010?uid=
    m3 = re.search(r'/(?P<year>[0-2][0-9])[/-](?P<month>[0-1]?[0-9])[/-]?(?P<date>[0-3]?[0-9])/', url) #如/12/11-22/
    
    if m0:
        #print(m0.group())
        date = m0.groupdict()['all'][:4] +'-'+ m0.groupdict()['all'][4:6] +'-'+ m0.groupdict()['all'][6:8]
        return date
    elif m1:
        date = m1.groupdict()['year']+'-'+ m1.groupdict()['month']+'-'+ m1.groupdict()['date']
        return date
    elif m2:
        date = m1.groupdict()['year']+'-'+ m1.groupdict()['month']+'-'+ m1.groupdict()['date']
        return date
    elif m3:
        date = '20'+m3.groupdict()['year']+'-'+ m3.groupdict()['month']+'-'+ m3.groupdict()['date']
        return date

df = pd.read_csv('citation+code.csv',index_col=('Unnamed: 0'))
df['url_time'] = ''
df['domain'] = ''

for index, row in df.iterrows():
    url = row['origin_url']
    if pd.isna(url) == False:
        domain = urlparse(url).netloc
        df.at[index, 'domain'] = domain 

        urlpath = urlparse(url).path
        date = get_pubtime_by_url(urlpath)
        
        df.at[index, 'url_time'] = date
        
        print(index, urlpath, date)
        
df.to_csv("citation+code+resolve.csv",index=True)

conn3= sqlite.connect('citation+code+resolve.sqlite')
df.to_sql('citation+code+resolve', conn3, index=True, if_exists = 'replace')
conn3.close()

#语音播报结束
import pyttsx3
engine = pyttsx3.init()  # 创建engine并初始化
engine.say("本程序运行结束")
engine.runAndWait()  # 等待语音播报完毕


over_count = df['url_time'].isna().sum()
print('后面需要处理的时间个数为', over_count) #后面需要处理的超时等链接个数为 

#%% 解析时间修正 20230124
import re
from urllib.parse import urlparse
import requests
import pandas as pd
import numpy as np
import sqlite3 as sqlite
import os

#大部分正确但极少数不适用，还是分开写比较合适
#m = re.search(r'/(?P<year>(20)?[0-2][0-9])[/-]?(?P<month>[0-1]?[0-9])[/-]?(?P<date>[0-3]?[0-9])?/(t(?P<all>20\d{6})_)?', url)

#https://www.guancha.cn/SongLuZheng/2017_08_31_425112.shtml
#https://view.inews.qq.com/k/20220310A04PC100?web_channel=wap&openApp=false
#https://view.inews.qq.com/a/NEW2021051000405401?uid=&devid=60968872-C4D0-4028-B806-4AFE70C19325&qimei=60968872-c4d0-4028-b806-4afe70c19325
#http://ln.ifeng.com/news/detail_2015_01/03/3368692_0.shtml
#http://qd.ifeng.com/sd/detail_2014_08/21/2800454_0.shtml
#http://www.xinhuanet.com/politics/2018lh/zb/20180317a/?baike
#http://www.xinhuanet.com/talking/20170510a/
#https://new.qq.com/rain/a/20210307A01FUW00
#https://view.inews.qq.com/a/NEW2017080800730005 这个是坏链接
#https://view.inews.qq.com/k/20210726A06WGG00?web_channel=wap&openApp=false
#https://www.guancha.cn/internation/2020_04_28_548511.shtml

def get_pubtime_by_url(url):
    m0 = re.search(r'/t(?P<all>20\d{6})_', url) #如/t20150324_
    m1 = re.search(r'[/_](?P<year>20[0-2][0-9])[/-_]?(?P<month>[0-1][0-9])[/-_]?(?P<date>[0-3][0-9])[/_a-zA-Z]', url) #如/2018/0324/
    #m2 = re.search(r'/(?P<year>20[0-2][0-9])[/-]?(?P<month>[0-1]?[0-9])/', url) #如/2020-10/ 放弃只有年月没有日期的
    m2 = re.search(r'/NEW(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url) #如https://view.inews.qq.com/a/NEW2019082900295010?uid=
    m3 = re.search(r'/(?P<year>[0-2][0-9])[/-](?P<month>[0-1]?[0-9])[/-]?(?P<date>[0-3]?[0-9])/', url) #如/12/11-22/
    
    if m0:
        #print(m0.group())
        date = m0.groupdict()['all'][:4] +'-'+ m0.groupdict()['all'][4:6] +'-'+ m0.groupdict()['all'][6:8]
        return date
    elif m1:
        date = m1.groupdict()['year']+'-'+ m1.groupdict()['month']+'-'+ m1.groupdict()['date']
        return date
    elif m2:
        date = m1.groupdict()['year']+'-'+ m1.groupdict()['month']+'-'+ m1.groupdict()['date']
        return date
    # if m2:
    #     date = [m2.groupdict()['year'], m2.groupdict()['month'], 'None']
    #     return date
    elif m3:
        date = '20'+m3.groupdict()['year']+'-'+ m3.groupdict()['month']+'-'+ m3.groupdict()['date']
        return date

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0124补充卫健委等时间')

df = pd.read_csv('citation+code.csv',index_col=('Unnamed: 0'))


for index, row in df.iterrows():
    url = row['origin_url']
    if pd.isna(url) == False:
        urlpath = urlparse(url).path
        date = get_pubtime_by_url(urlpath)
        
        df.at[index, 'url_time'] = date
        
        print(index, urlpath, date)
        
      
df.to_csv("citation+update-url-time.csv",index=True)

conn3= sqlite.connect('citation+update-url-time.sqlite')
df.to_sql('citation+code+resolve', conn3, index=True, if_exists = 'replace')
conn3.close()

#语音播报结束
import pyttsx3
engine = pyttsx3.init()  # 创建engine并初始化
engine.say("本程序运行结束")
engine.runAndWait()  # 等待语音播报完毕


over_count = df['url_time'].isna().sum()
print('后面需要处理的时间个数为', over_count) #后面需要处理的超时等链接个数为 




