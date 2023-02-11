#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 13:21:32 2023

@author: zhangsiqi
"""
import os
import pandas as pd
import sqlite3 as sqlite
import datetime
import numpy as np
import re
from htmldate import find_date
import time

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0209补充发布时间戳')
#os.chdir('D:\zsq')
df = pd.read_csv('citation+time-2.csv', index_col=('Unnamed: 0'))

df['htmltimestamp']=pd.NaT

a =0

for index, row in df.iterrows():
    url = row['origin_url']
    dmname = row['domain']
    maindo = row['maindo']
    if pd.isna(url) == False and pd.isna(row['timestamp']) and any(ele in url for ele in ['.htm','.stm']) and pd.notna(row['pub_time']):
        #sina
        sina404 = ['2018.sina.com.cn/fra','general/2019-07-27/detail-ihytcitm4','hlj.sina.com.cn/news/ljyw','hebei.sina.com.cn/fashion/ssxj/2014-08-18/1606103209_2.','gd.sina.com.cn/yj/news/2014-06-21/1009807','013-01-30/093550296_2','detail-iicezzrr134','henan.sina.com.cn/health/n/2012-04-18/110','video.sina.','k.sina.com.','docID=fyiakwa4149447','1153595771521421574']
        if '新浪' in maindo and all(le not in dmname for le in sina404):
            a+=1
            try:
                date = find_date(url, outputformat='%Y-%m-%d %H:%M')
                #time.sleep(5)
            except ValueError:
                date = pd.NaT
            df.at[index,'htmltimestamp'] = date
            df.at[index,'timestamp'] = date
        #wangyi 
        wangyi404 = ['/special/0034073A/','live.163.com/room/772']
        if '网易' in maindo and all(le not in dmname for le in wangyi404):
            a+=1
            try:
                date = find_date(url, outputformat='%Y-%m-%d %H:%M')
                #time.sleep(5)
            except ValueError:
                date = pd.NaT
            df.at[index,'htmltimestamp'] = date
            df.at[index,'timestamp'] = date
        #tencent
        tencent404 = ['v.qq.com/'] 
        if '腾讯' in maindo and all(le not in dmname for le in tencent404):
            a+=1
            try:
                date = find_date(url, outputformat='%Y-%m-%d %H:%M')
                #time.sleep(5)
            except ValueError:
                date = pd.NaT
            df.at[index,'htmltimestamp'] = date
            df.at[index,'timestamp'] = date
        #haiwaiwang
        halwai404 = ['cn/n/2014/0410/c232620-20519243','china.haiwainet.cn/n/']
        if '海外网' in maindo and all(le not in dmname for le in halwai404):
            a+=1
            try:
                date = find_date(url, outputformat='%Y-%m-%d %H:%M')
                #time.sleep(5)
            except ValueError:
                date = pd.NaT
            df.at[index,'htmltimestamp'] = date
            df.at[index,'timestamp'] = date
        #sohu
        sohu404 = ['learning.sohu.com/20161009/n469805','roll.sohu.com/20140','mil.sohu.com/20150127/n','/media.sohu.com/201410']
        if '搜狐' in maindo and all(le not in dmname for le in sohu404):
            a+=1
            try:
                date = find_date(url, outputformat='%Y-%m-%d %H:%M')
                #time.sleep(5)
            except ValueError:
                date = pd.NaT
            df.at[index,'htmltimestamp'] = date
            df.at[index,'timestamp'] = date

#os.chdir('D:\zsq')
df.to_csv("citation+time4test.csv", index=True)

conn3= sqlite.connect('citation+time4test.sqlite')
df.to_sql('citation_time4', conn3, index=True, if_exists = 'replace')
conn3.close()

print(a)


# url = 'http://ent.sina.com.cn/s/h/2014-08-19/14564194416.shtml' #无误 时分
# url = 'https://news.sina.com.cn/c/2020-07-07/doc-iirczymm1066084.shtml' #无误 时分
# url = 'http://finance.sina.com.cn/fawen/yx/2018-04-16/doc-ifzcyxmv2396917.shtml' #无误 时分
# url = 'http://finance.sina.com.cn/consume/puguangtai/20120504/161411988703.shtml' #无误 时分
# url = 'http://finance.sina.com.cn/chanjing/sdbd/2016-04-06/doc-ifxqxcnr5381218.shtml' #无误 时分
# url = 'http://k.sina.com.cn/article_2011075080_77de9208020009o0z.html' #时分不对 这个有更新时间和创建时间
# url = 'http://mil.news.sina.com.cn/jssd/2017-08-31/doc-ifykqmrv5721032.shtml' #无误 时分
# url1 = 'https://news.sina.cn/gn/2018-10-28/detail-ihnaivxp7676316.d.html'#无误 时分
# url = 'http://sports.sina.com.cn/g/2010-12-01/07195345792.shtml' #无误 时分
# url = 'http://tech.sina.com.cn/it/2018-07-12/doc-ihfefkqq6801608.shtml' #无误 时分
# url = 'https://news.sina.cn/gn/2021-08-31/detail-iktzscyx1395666.d.html?sinawapsharesource=newsapp&wm=3200_0024' #无误 时分
# url = 'http://weather.news.sina.com.cn/news/2015/0813/1631110151.html' #无误 时分
# url = 'http://slide.ent.sina.com.cn/star/slide_4_86512_351411.html#p=1' #无误
# url = 'http://ent.sina.com.cn/s/m/2012-02-07/15343548043.shtml' #无误 时分
# url = 'http://2012.sina.com.cn/hx/other/pl/2012-08-01/023530679.shtml' #无误
# url = 'http://2018.sina.com.cn/fra/2018-06-26/doc-ihencxtu7739801.shtml' #分钟差一秒
# url = 'http://2018.sina.com.cn/fra/2018-06-30/doc-ihespqrx7173896.shtml'

# date = find_date(url, outputformat='%Y-%m-%d %H:%M')
# date1 = find_date(url1, outputformat='%Y-%m-%d %H:%M')

#%% 干脆全部跑一次
import os
import pandas as pd
import sqlite3 as sqlite
import datetime
import numpy as np
import re
from htmldate import find_date
import time

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0209补充发布时间戳')
#os.chdir('D:\zsq')
df = pd.read_csv('citation+time-2.csv', index_col=('Unnamed: 0'))

df['htmltimestamp']=pd.NaT


for index, row in df.iterrows():
    url = row['origin_url']
    dmname = row['domain']
    maindo = row['maindo']
    if pd.isna(url) == False and pd.isna(row['timestamp']) and any(ele in url for ele in ['.htm','.stm']) and pd.notna(row['pub_time']):
        try:
            date = find_date(url, outputformat='%Y-%m-%d %H:%M')
            #time.sleep(5)
        except ValueError:
            date = pd.NaT
        df.at[index,'htmltimestamp'] = date
        #df.at[index,'timestamp'] = date

#os.chdir('D:\zsq')
df.to_csv("citation+htmltimestamp.csv", index=True)

conn3= sqlite.connect('citation_htmltimestamp.sqlite')
df.to_sql('citation_time', conn3, index=True, if_exists = 'replace')
conn3.close()

#%%
#手动查看数据后在sql文件中修改了一些错误值,合并一下数据
import os
import pandas as pd
import sqlite3 as sqlite
import datetime
import numpy as np
import re
from htmldate import find_date
import time

conn0 = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0209补充发布时间戳/citation_htmltimestamp.sqlite')
df0 = pd.read_sql('SELECT * FROM citation', conn0, index_col='level_0')
conn0.close()


conn = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0209补充发布时间戳/citation+time2.sqlite')
df = pd.read_sql('SELECT * FROM citation_time', conn, index_col='level_0')
conn.close()

df['htmltimestamp'] = df0['htmltimestamp']

a =0
for index, row in df.iterrows():
    if pd.isna(row['timestamp']) and pd.notna(row['htmltimestamp']) and '00:00:00' not in row['htmltimestamp']:
        df.at[index,'timestamp'] = row['htmltimestamp']
        a+=1

df.to_csv("ci+stamp.csv", index=True)

conn1= sqlite.connect('ci+stamp.sqlite')
df.to_sql('citation', conn1, index=True, if_exists = 'replace')
conn1.close()

df = pd.read_csv('ci+stamp.csv', index_col='level_0')

con= sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情/Wiki.sqlite')
df.to_sql('ci', con, index=True, if_exists = 'replace')
con.close()

#%% 环球网很能打
# url = 'http://world.huanqiu.com/article/2015-04/6281533.html' #没有时分
# url = 'http://world.huanqiu.com/exclusive/2017-08/11085104.html' #完全错误

#%%wangyi 
wangyi404 = ['/special/0034073A/','live.163.com/room/772']
url = 'https://www.163.com/money/article/A41TABPR00254UF3.html' #无误 时分
url = 'https://www.163.com/money/article/9OAVJGIQ00253B0H.html'
url1 = 'http://3g.163.com/ntes/special/0034073A/article_share.html?docid=BQQPISSC00963VRO&spst=0&spss=newsapp&spsf=qq&spsw=1&token=P6Bd4B3SdaWo6c93UWYE7EdEyuM7gnnIjiRocxZPwN148ErR02zJ6/KXOnxX046I'#错误
url = 'http://chongqing.163.com/20/0124/19/F3M9IG1B04218FF3.html' #正确
url = 'http://live.163.com/room/77206.html' #错误
url = 'https://www.163.com/money/article/AR8DNB3700254TI5.html' #正确
url = 'http://world.163.com/14/0423/18/9QHMVAPL00014JB6.html'
url = 'https://3g.163.com/dy/article/FGUNFVDK0514R9OJ.html'#正确
url = 'https://c.m.163.com/news/a/DM0015KL0001899O.html?spss=newsapp'
url = 'https://www.163.com/ent/article/GH2NERFI00038FO9.html'

try:
    date = find_date(url, outputformat='%Y-%m-%d %H:%M')
    print(date)
except ValueError:
    print('该网址有问题')
    
#%%人民网
url = 'http://politics.people.com.cn/n/2014/1222/c70731-26255440.html' #没有时分
url = 'http://sports.people.com.cn/n1/2017/1117/c14820-29651198.html'

try:
    date = find_date(url, outputformat='%Y-%m-%d %H:%M')
    print(date)
except ValueError:
    print('该网址有问题')

#%%央视网
url = 'http://m.news.cctv.com/2019/10/08/ARTIFeB1lG54WtrGk3r6oUeA191008.shtml' #完全错误
url = 'http://m.news.cctv.com/2021/09/26/ARTIlXAAnWx57Hp446iUJZ5a210926.shtml' #完全错误
url = 'http://news.cctv.com/2016/09/17/ARTIZ513G646pt56pEsf4nQN160917.shtml' #完全错误
url = 'https://news.cctv.com/2014/03/16/VIDE1394937902722327.shtml' #正确
url = 'http://news.cctv.com/2016/09/07/ARTIh8crXCTNtMLTEOvGddtg160907.shtml' #完全错误

yangshi404 = ['m.news.cctv.com']    
try:
    date = find_date(url, outputformat='%Y-%m-%d %H:%M')
    print(date)
except ValueError:
    print('该网址有问题')
    
#%%腾讯
url = 'https://ent.qq.com/a/20180529/021440.htm?TPSecNotice' #无误
url = 'https://sports.qq.com/a/20150430/042731.htm' #无误
url = 'https://tech.qq.com/a/20180510/033050.htm' #无误
url = 'https://v.qq.com/x/cover/yg9gzzk8f982w5t.html?vid=O0010Ek37n3' #没有时分
url = 'https://finance.qq.com/a/20180421/011364.htm' #无误

tencent404 = ['v.qq.com/']    
try:
    date = find_date(url, outputformat='%Y-%m-%d %H:%M')
    print(date)
except ValueError:
    print('该网址有问题')

#%%海外网
url = 'http://news.haiwainet.cn/n/2019/0417/c3541083-31538538.html?baike' #无误
url = 'http://opinion.haiwainet.cn/n/2016/0714/c456317-30091551.html' #无误
url = 'http://tw.haiwainet.cn/n/2014/0410/c232620-20519243.html' #没有时分
url = 'https://news.haiwainet.cn/n/2022/0311/c3541093-32362152.html' #无误
url = 'http://fr.haiwainet.cn/n/2019/0416/c3541926-31537595.html?baike' #无误
url = 'http://china.haiwainet.cn/n/2013/1031/c345646-19866705.html' #时分错误
url = 'http://china.haiwainet.cn/n/2013/1031/c345646-19866705.html' #时分错误
url = 'http://china.haiwainet.cn/n/2014/0608/c345646-20716530.html' #时分错误

halwal402 = ['cn/n/2014/0410/c232620-20519243','china.haiwainet.cn/n/']
try:
    date = find_date(url, outputformat='%Y-%m-%d %H:%M')
    print(date)
except ValueError:
    print('该网址有问题')

#%%搜狐
url = 'http://news.sohu.com/20130822/n384779211.shtml' #正确
url = 'http://business.sohu.com/20150629/n415863081.shtml' #正确

sohu404 = ['learning.sohu.com/20161009/n469805','roll.sohu.com/20140','mil.sohu.com/20150127/n','/media.sohu.com/201410']

try:
    date = find_date(url, outputformat='%Y-%m-%d %H:%M')
    print(date)
except ValueError:
    print('该网址有问题')
