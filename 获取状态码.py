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
    m1 = re.search(r'[/_](?P<year>20[0-2][0-9])[-/_]?(?P<month>[0-1][0-9])[-/_]?(?P<date>[0-3][0-9])[/_]', url) #如/2018/0324/
    #m2 = re.search(r'/NEW(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url) #如https://view.inews.qq.com/a/NEW2019082900295010?uid=
    m2 = re.search(r'view\.inews\.qq\.com/\S+(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url)
    m3 = re.search(r'/(?P<year>[0-2][0-9])[/-](?P<month>[0-1]?[0-9])[/-]?(?P<date>[0-3]?[0-9])/', url) #如/12/11-22/
    m4 = re.search(r'xinhuanet\.com/\S+(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url)
    
    
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
    if m1 == None and m0 == None and m2 == None and m3 == None and m4 == None:
        return None
    

df = pd.read_csv('citation+code.csv',index_col=('Unnamed: 0'))
df['url_time'] = ''
df['domain'] = ''

for index, row in df.iterrows():
    url = row['origin_url']
    if pd.isna(url) == False:
        domain = urlparse(url).netloc
        df.at[index, 'domain'] = domain 

        date = get_pubtime_by_url(url) #不能用urlpath来提取日期，因为urlpath不完整
        df.at[index, 'url_time'] = date
        
        print(index, url, date)
        
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
    m1 = re.search(r'[/_](?P<year>20[0-2][0-9])[-/_]?(?P<month>[0-1][0-9])[-/_]?(?P<date>[0-3][0-9])[/_]', url) #如/2018/0324/
    #m2 = re.search(r'/NEW(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url) #如https://view.inews.qq.com/a/NEW2019082900295010?uid=
    m2 = re.search(r'view\.inews\.qq\.com/\S+(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url)
    m3 = re.search(r'/(?P<year>[0-2][0-9])[/-](?P<month>[0-1]?[0-9])[/-]?(?P<date>[0-3]?[0-9])/', url) #如/12/11-22/
    m4 = re.search(r'xinhuanet\.com/\S+(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url)
    
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
    if m1 == None and m0 == None and m2 == None and m3 == None and m4 == None:
        return None

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0124补充卫健委等时间')

df = pd.read_csv('citation+code.csv',index_col=('Unnamed: 0'))

for index, row in df.iterrows():
    url = row['origin_url']
    if pd.isna(url) == False:
        
        date = get_pubtime_by_url(url) #不能用urlpath因为得到的urlpath并不完整
        
        df.at[index, 'url_time'] = date
        
        print(index, url, date)
        
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

#%% htmldate模块取时间
import re
from urllib.parse import urlparse
import requests
import pandas as pd
import numpy as np
import sqlite3 as sqlite
import os
from htmldate import find_date

#os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0124补充卫健委等时间')
os.chdir('/Volumes/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0124补充卫健委等时间')

df = pd.read_csv('citation+news-nhc-6.csv',index_col=('Unnamed: 0'))
df['htmldate_ori'] = ''
df['htmldate_upd'] = ''
df['url_time'] = '' #之前得到的时间删除，重新解析时间

def get_pubtime_by_url(url): 
    m0 = re.search(r'/t(?P<all>20\d{6})_', url) #如/t20150324_
    m1 = re.search(r'[/_](?P<year>20[0-2][0-9])[-/_]?(?P<month>[0-1][0-9])[-/_]?(?P<date>[0-3][0-9])[/_a-zA-Z]', url) #如/2018/0324/
    m2 = re.search(r'/NEW(?P<year>20[0-2][0-9])(?P<month>[0-1][0-9])(?P<date>[0-3][0-9])', url) #如https://view.inews.qq.com/a/NEW2019082900295010?uid=
    m3 = re.search(r'/(?P<year>[0-2][0-9])[/-](?P<month>[0-1]?[0-9])[/-]?(?P<date>[0-3]?[0-9])/', url) #如/12/11-22/
    
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
    if m1 == None and m0 == None and m2 == None and m3 == None:
        date = None
        return date

for index, row in df.iterrows():
    url = row['origin_url']
    if pd.isna(url) == False:
        date = get_pubtime_by_url(url) #不能用urlpath因为得到的urlpath并不完整
        df.at[index, 'url_time'] = date
        print(index, url, date)

print('时间解析完成')

for index, row in df.iterrows():
    url = row['origin_url']
    if pd.isna(url) == False:
        try:
            date = find_date(url, original_date=True)
            date1 = find_date(url, original_date=False)
        except ValueError:
            df.at[index, 'htmldate_ori'] = 'error'
            df.at[index, 'htmldate_upd'] = 'error'
            print(index,url,'error')
            continue
        else:
            df.at[index, 'htmldate_ori'] = date
            df.at[index, 'htmldate_upd'] = date1
            print(index,url,date)

#os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0125补充htmldate时间')
os.chdir('/Volumes/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0125补充htmldate时间')

df.to_csv("citation+html2date.csv",index=True)

conn3= sqlite.connect('citation+html2date.sqlite')
df.to_sql('citation+htmldate', conn3, index=True, if_exists = 'replace')
conn3.close()

#%%修正URL时间解析错误 20230126，之前为了容错/20190829af20结果引入了/20190836af67的噪音
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





#%%
testtext = """2008年中国南方雪灾是指自2008年1月3日起在中国发生的大范围低温、雨雪、冰冻等自然灾害。中国的上海、江苏、浙江、安徽、江西、河南、湖北、湖南、广东、广西、重庆、四川、贵州、云南、陕西、甘肃、青海、宁夏、新疆等20个省（区、市）均不同程度受到低温、雨雪、冰冻灾害影响。截至2月24日，因灾死亡129人，失踪4人，紧急转移安置166万人；农作物受灾面积1.78亿亩，成灾8764万亩，绝收2536万亩；倒塌房屋48.5万间，损坏房屋168.6万间；因灾直接经济损失1516.5亿元人民币。森林受损面积近2.79亿亩，3万只国家重点保护野生动物在雪灾中冻死或冻伤；受灾人口已超过1亿。其中安徽、江西、湖北、湖南、广西、四川和贵州等7个省份受灾最为严重。
中国国家气象部门的专家指出，这次大范围的雨雪过程应归因于与拉尼娜（反圣婴）现象有关的大气环流异常：环流自1月起长期经向分布使冷空气活动频繁，同时副热带高压偏强、南支槽活跃，源自南方的暖湿空气与北方的冷空气在长江中下游地区交汇，形成强烈降水。大气环流的稳定使雨雪天气持续，最终酿成这次雪灾。
北京：京呼航班全线延误首都机场因呼市突降大雪机场关闭，21日飞往呼和浩特共11趟航班全部延误，下午6时，所有航班的起飞时间都改在晚8时以后，但工作人员称，即使到了八点也不见得能够起飞。此外，北京飞往内蒙锡林浩特航班已经取消。铁路方面，北京西站候车大厅状况与往年春运期间无太多异常，未有旅客大面积滞留，大多列车可以准点出发，个别一两趟出现短时间晚点。
湖北：死亡人数升至14人据统计，湖北省积雪天数已达10天，为24年来之首，因灾死亡人数上升至14人，直接经济损失超过14亿元人民币，而雨雪天气将持续至25日。受暴雪天气影响，湖北省内九条高速公路中有五条再次关闭，但京珠高速已恢复运行。省客运集团有关负责人介绍，迄今为止由武汉发往全国各地的长途客运班车已有8800余次停运。天河机场亦有20余航班延误。截至20日，武汉市公安交通管理局122交通指挥中心共接到交通报警13199起。另外，武汉市中心城区多处水管冻裂，许多居民出现用水困难。至20日上午9时，全市24小时内共接到投诉1904起，直接停水754起，供水管网21日共发生两起800毫米主干管爆裂事故。"""


import re
import chardet
from datetime import datetime,timedelta


# 匹配正则表达式
matchs = {
    1:(r'\d{4}%s\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s\d{1,2}%s','%%Y%s%%m%s%%d%s %%H%s%%M%s%%S%s'),
    2:(r'\d{4}%s\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s','%%Y%s%%m%s%%d%s %%H%s%%M%s'),
    3:(r'\d{4}%s\d{1,2}%s\d{1,2}%s','%%Y%s%%m%s%%d%s'),
    4:(r'\d{2}%s\d{1,2}%s\d{1,2}%s','%%y%s%%m%s%%d%s'),
   
    # 没有年份
    5:(r'\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s\d{1,2}%s','%%m%s%%d%s %%H%s%%M%s%%S%s'),
    6:(r'\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s','%%m%s%%d%s %%H%s%%M%s'),
    7:(r'\d{1,2}%s\d{1,2}%s','%%m%s%%d%s'),
    

    # 没有年月日
    8:(r'\d{1,2}%s\d{1,2}%s\d{1,2}%s','%%H%s%%M%s%%S%s'),
    9:(r'\d{1,2}%s\d{1,2}%s','%%H%s%%M%s'),
}

# 正则中的%s分割
splits = [
    {1:[('年','月','日','点','分','秒'),('-','-','',':',':',''),('\/','\/','',':',':',''),('\.','\.','',':',':','')]},
    {2:[('年','月','日','点','分'),('-','-','',':',''),('\/','\/','',':',''),('\.','\.','',':','')]},
    {3:[('年','月','日'),('-','-',''),('\/','\/',''),('\.','\.','')]},
    {4:[('年','月','日'),('-','-',''),('\/','\/',''),('\.','\.','')]},

    {5:[('月','日','点','分','秒'),('-','',':',':',''),('\/','',':',':',''),('\.','',':',':','')]},
    {6:[('月','日','点','分'),('-','',':',''),('\/','',':',''),('\.','',':','')]},
    {7:[('月','日'),('-',''),('\/',''),('\.','')]},

    {8:[('点','分','秒'),(':',':','')]},
    {9:[('点','分'),(':','')]},
]

def func(parten,tp):
    re.search(parten,parten)
    

parten_other = '\d+天前|\d+分钟前|\d+小时前|\d+秒前'

class TimeFinder(object):

    def __init__(self,base_date=None):
        self.base_date = base_date
        self.match_item = []
        
        self.init_args()
        self.init_match_item()

    def init_args(self):
        # 格式化基础时间
        if not self.base_date:
            self.base_date = datetime.now()
        if self.base_date and not isinstance(self.base_date,datetime):
            try:
                self.base_date = datetime.strptime(self.base_date,'%Y-%m-%d %H:%M:%S')
            except Exception as e:
                raise 'type of base_date must be str of%Y-%m-%d %H:%M:%S or datetime'

    def init_match_item(self):
        # 构建穷举正则匹配公式 及提取的字符串转datetime格式映射
        for item in splits:
            for num,value in item.items():
                match = matchs[num]
                for sp in value:
                    tmp = []
                    for m in match:
                        tmp.append(m%sp)
                    self.match_item.append(tuple(tmp))

    def get_time_other(self,text):
        m = re.search('\d+',text)
        if not m:
            return None
        num = int(m.group())
        if '天' in text:
            return self.base_date - timedelta(days=num)
        elif '小时' in text:
            return self.base_date - timedelta(hours=num)
        elif '分钟' in text:
            return self.base_date - timedelta(minutes=num)
        elif '秒' in text:
            return self.base_date - timedelta(seconds=num)

        return None

    def find_time(self,text):
         # 格式化text为str类型
        if isinstance(text,bytes):
            encoding =chardet.detect(text)['encoding']
            text = text.decode(encoding)

        res = []
        parten = '|'.join([x[0] for x in self.match_item])

        parten = parten+ '|' +parten_other
        match_list = re.findall(parten,text)
        if not match_list:
            return None
        for match in match_list:
            for item in self.match_item:
                try:
                    date = datetime.strptime(match,item[1].replace('\\',''))
                    if date.year==1900:
                        date = date.replace(year=self.base_date.year)
                        if date.month==1:
                            date = date.replace(month=self.base_date.month)
                            if date.day==1:
                                date = date.replace(day=self.base_date.day)
                    res.append(datetime.strftime(date,'%Y-%m-%d %H:%M:%S'))
                    break
                except Exception as e:
                    date = self.get_time_other(match)
                    if date:
                        res.append(datetime.strftime(date,'%Y-%m-%d %H:%M:%S'))
                        break
        if not res:
            return None
        return res

def test():
    timefinder = TimeFinder(base_date='2008-01-01 00:00:00')
    #or text in testtext:
    res = timefinder.find_time(testtext)
    #print('text----',testtext)
    print('res',res)

if __name__ == '__main__':
    test()











