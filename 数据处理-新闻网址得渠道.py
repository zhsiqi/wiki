#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 02:10:25 2023

@author: zhangsiqi

（1）根据参考资料的网址建立对应的渠道
（2）根据编辑时间得到引用的时间戳

"""

import pandas as pd
import numpy as np
import os
import matplotlib.pylab as plt
import sqlite3 as sqlite
import re
import datetime
from dateutil.parser import parse
from dateutil import rrule
from dateutil import relativedelta

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0127补齐sourcetime')

df = pd.read_csv('citation.csv', index_col='Unnamed: 0')


#%% 新建列聚合网页等渠道
df['maindo'] = None

df.loc[(df['domain'].str.contains('ishare.ifeng')) & (df['maindo'].isna()),'maindo'] = '凤凰新闻（应用程序）'
df.loc[(df['domain'].str.contains('ifeng.')) & (df['maindo'].isna()),'maindo'] = '凤凰网'
df.loc[(df['domain'].str.contains('163.')) & (df['maindo'].isna()),'maindo'] = '网易网'
df.loc[(df['origin_url'].str.contains('sinawap')) & (df['maindo'].isna()),'maindo'] = '新浪新闻（应用程序）'
df.loc[(df['domain'].str.contains('weibo.com')) & (df['maindo'].isna()),'maindo'] = '新浪微博-网站'
df.loc[(df['domain'].str.contains('sina.')) & (df['maindo'].isna()),'maindo'] = '新浪网'
df.loc[(df['domain'].str.contains('weixin.')) & (df['maindo'].isna()),'maindo'] = '腾讯微信公众平台'
df.loc[(df['domain'].str.contains('view.inews.qq')) & (df['maindo'].isna()),'maindo'] = '腾讯新闻（应用程序）'
df.loc[(df['domain'].str.contains('qq.')) & (df['maindo'].isna()),'maindo'] = '腾讯网'
df.loc[(df['domain'].str.startswith('m.sohu.')) & (df['maindo'].isna()),'maindo'] = '搜狐网（移动端网页版）'
df.loc[(df['domain'].str.contains('sohu.')) & (df['maindo'].isna()),'maindo'] = '搜狐网'
df.loc[(df['domain'].str.contains('baike.baidu')) & (df['maindo'].isna()),'maindo'] = '百度百科-网站'
df.loc[(df['domain'].str.contains('baijiahao.baidu')) & (df['maindo'].isna()),'maindo'] = '百度百家号'
df.loc[(df['domain'].str.startswith('mbd.baidu')) & (df['maindo'].isna()),'maindo'] = '百度百家号（应用程序）'#也是应用程序，这个mbd本身覆盖不止百家号码
df.loc[(df['domain'].str.contains('www.baidu.com')) & (df['maindo'].isna()),'maindo'] = '百度搜索引擎'

df.loc[(df['domain'].str.contains('jiemian.')) & (df['maindo'].isna()),'maindo'] = '界面新闻-网站'
df.loc[(df['domain'].str.startswith('m.thepaper.')) & (df['maindo'].isna()),'maindo'] = '澎湃新闻（移动端网页版/应用程序）'#也是APP
df.loc[(df['domain'].str.contains('thepaper.')) & (df['maindo'].isna()),'maindo'] = '澎湃新闻-网站'

df.loc[(df['domain'].str.contains('xhpfmapi')) & (df['maindo'].isna()),'maindo'] = '新华社（应用程序）'
df.loc[(df['domain']=='m.news.cn') & (df['maindo'].isna()),'maindo'] = '新华网（移动端网页版）'
df.loc[(df['domain'].str.contains('.xinhuanet.')) & (df['maindo'].isna()),'maindo'] = '新华网'
df.loc[(df['domain']=='www.news.cn') & (df['maindo'].isna()),'maindo'] = '新华网'
df.loc[(df['domain']=='education.news.cn') & (df['maindo'].isna()),'maindo'] = '新华网'

df.loc[(df['domain'].str.contains('content-static.cctvnews')) & (df['maindo'].isna()),'maindo'] = '央视新闻（应用程序）'
df.loc[(df['domain']=='app.cctv.com') & (df['maindo'].isna()),'maindo'] = '央视新闻（应用程序）'
df.loc[(df['domain'].str.startswith('m.news.cctv')) & (df['maindo'].isna()),'maindo'] = '央视网（移动端网页版）'
df.loc[(df['domain'].str.contains('cntv.c')) & (df['maindo'].isna()),'maindo'] = '央视网'
df.loc[(df['domain'].str.contains('cctv.com')) & (df['maindo'].isna()),'maindo'] = '央视网'
df.loc[(df['domain'].str.contains('.cnr.cn')) & (df['maindo'].isna()),'maindo'] = '央广网'

df.loc[(df['domain']=='bj.bjd.com.cn') & (df['maindo'].isna()),'maindo'] = '北京日报（应用程序）'
df.loc[(df['domain']=='ie.bjd.com.cn') & (df['maindo'].isna()),'maindo'] = '北京日报（应用程序）'
df.loc[(df['domain'].str.contains('bjd.com.cn')) & (df['maindo'].isna()),'maindo'] = '北京日报网'
df.loc[(df['domain'].str.startswith('m.haiwainet')) & (df['maindo'].isna()),'maindo'] = '海外网（移动端网页版）'
df.loc[(df['domain'].str.contains('haiwainet.cn')) & (df['maindo'].isna()),'maindo'] = '海外网'

df.loc[(df['domain'].str.startswith('m.chinanews')) & (df['maindo'].isna()),'maindo'] = '中国新闻网（应用程序）'
df.loc[(df['domain'].str.contains('chinanews.')) & (df['maindo'].isna()),'maindo'] = '中国新闻网'
df.loc[(df['domain'].str.startswith('m.gmw.')) & (df['maindo'].isna()),'maindo'] = '光明网（移动端网页版）'
df.loc[(df['domain'].str.contains('.gmw.')) & (df['maindo'].isna()),'maindo'] = '光明网'

df.loc[(df['domain'].str.contains('.peopleapp.')) & (df['maindo'].isna()),'maindo'] = '人民日报（应用程序）'
df.loc[(df['domain'].str.contains('paper.people.')) & (df['maindo'].isna()),'maindo'] = '人民日报（电子报）'
df.loc[(df['domain'].str.startswith('m.people.cn')) & (df['maindo'].isna()),'maindo'] = '人民网（移动端网页版）'
df.loc[(df['domain'].str.contains('app.people.cn')) & (df['maindo'].isna()),'maindo'] = '人民网+（应用程序）'
df.loc[(df['domain'].str.contains('.people.cn')) & (df['maindo'].isna()),'maindo'] = '人民网'
df.loc[(df['domain'].str.contains('.people.com')) & (df['maindo'].isna()),'maindo'] = '人民网'

df.loc[(df['domain'].str.startswith('m.huanqiu')) & (df['maindo'].isna()),'maindo'] = '环球网（移动端网页版）'
df.loc[(df['domain'].str.contains('hqtime.')) & (df['maindo'].isna()),'maindo'] = '环球时报（应用程序）'
df.loc[(df['domain'].str.contains('huanqiu')) & (df['maindo'].isna()),'maindo'] = '环球网'
df.loc[(df['domain'].str.contains('m.bjnews.com.cn')) & (df['maindo'].isna()),'maindo'] = '新京报（应用程序）'
df.loc[(df['domain'].str.contains('epaper.bjnews.com.cn')) & (df['maindo'].isna()),'maindo'] = '新京报（电子报）'
df.loc[(df['domain'].str.contains('bjnews.com.cn')) & (df['maindo'].isna()),'maindo'] = '新京报网'
#3w.huanqiu 是个啥 https://3w.huanqiu.com/a/24d596/48NJJN9tgG4

df.loc[(df['domain'].str.contains('china.com.cn')) & (df['maindo'].isna()),'maindo'] = '中国网'
df.loc[(df['domain'].str.endswith('.china.com')) & (df['maindo'].isna()),'maindo'] = '中华网'
df.loc[(df['domain'].str.contains('rmzxb.com')) & (df['maindo'].isna()),'maindo'] = '人民政协网'
df.loc[(df['domain'].str.contains('.youth.cn')) & (df['maindo'].isna()),'maindo'] = '中国青年网'
df.loc[(df['domain'].str.contains('.cankaoxiaoxi.')) & (df['maindo'].isna()),'maindo'] = '参考消息网'
df.loc[(df['domain'].str.contains('m.ckxx.net')) & (df['maindo'].isna()),'maindo'] = '参考消息（应用程序）'
df.loc[(df['domain'].str.contains('js7tv.')) & (df['maindo'].isna()),'maindo'] = '中国军视网'
df.loc[(df['domain'].str.contains('.81.cn')) & (df['maindo'].isna()),'maindo'] = '中国军网'
df.loc[(df['domain'].str.contains('.ce.cn')) & (df['maindo'].isna()),'maindo'] = '中国经济网'
df.loc[(df['domain'].str.contains('.chinadaily.com')) & (df['maindo'].isna()),'maindo'] = '中国日报网'
df.loc[(df['domain'].str.contains('.cri.cn')) & (df['maindo'].isna()),'maindo'] = '国际在线-网站'

df.loc[(df['domain'].str.contains('m.nbd.com')) & (df['maindo'].isna()),'maindo'] = '每日经济新闻（应用程序）'
df.loc[(df['domain'].str.contains('.nbd.com')) & (df['maindo'].isna()),'maindo'] = '每经网'
df.loc[(df['domain'].str.contains('.mrjjxw.')) & (df['maindo'].isna()),'maindo'] = '每经网'
df.loc[(df['domain'].str.contains('.guancha.cn')) & (df['maindo'].isna()),'maindo'] = '观察者网'
df.loc[(df['domain'].str.contains('.caixin.com')) & (df['maindo'].isna()),'maindo'] = '财新网'
df.loc[(df['domain'].str.contains('.caijing.com')) & (df['maindo'].isna()),'maindo'] = '财经网'
df.loc[(df['domain'].str.contains('.hexun.com')) & (df['maindo'].isna()),'maindo'] = '和讯网'


df.loc[(df['domain'].str.contains('hznews.')) & (df['maindo'].isna()),'maindo'] = '杭州网'
df.loc[(df['domain'].str.contains('.xhby.')) & (df['maindo'].isna()),'maindo'] = '新华报业网'
df.loc[(df['domain'].str.contains('sichuan.scol.')) & (df['maindo'].isna()),'maindo'] = '四川在线-网站'
df.loc[(df['domain'].str.contains('.dzwww.')) & (df['maindo'].isna()),'maindo'] = '大众网'
df.loc[(df['domain'].str.contains('epaper.ynet')) & (df['maindo'].isna()),'maindo'] = '北京青年报（电子报）'
df.loc[(df['domain'].str.contains('ynet.')) & (df['maindo'].isna()),'maindo'] = '北青网'
#df.loc[(df['domain'].str.startswith('t.ynet')) & (df['maindo'].isna()),'maindo'] = '北青网（移动端网页版）' 不好判断

df.loc[(df['domain'].str.contains('takefoto.')) & (df['maindo'].isna()),'maindo'] = '北晚在线-网站'
df.loc[(df['domain'].str.contains('shobserver')) & (df['maindo'].isna()),'maindo'] = '上观新闻（应用程序）'
df.loc[(df['domain'].str.contains('jfdaily.')) & (df['maindo'].isna()),'maindo'] = '上观新闻网'
df.loc[(df['domain'].str.contains('n.cztv')) & (df['maindo'].isna()),'maindo'] = '新蓝网'
df.loc[(df['domain'].str.contains('ynet')) & (df['maindo'].isna()),'maindo'] = '北青网'
df.loc[(df['domain'].str.contains('kankanews')) & (df['maindo'].isna()),'maindo'] = '看看新闻-网站'


df.loc[(df['domain'].str.contains('www.g20chn')) & (df['maindo'].isna()),'maindo'] = 'G20官网'
df.loc[(df['domain'].str.contains('olympics')) & (df['maindo'].isna()),'maindo'] = '国际奥委会官网'
df.loc[(df['domain'].str.contains('.fifa.')) & (df['maindo'].isna()),'maindo'] = '国际足联官网'
df.loc[(df['domain'].str.contains('www.yidaiyilu.gov.cn')) & (df['maindo'].isna()),'maindo'] = '中国一带一路网'
df.loc[(df['domain'].str.contains('focacsummit')) & (df['maindo'].isna()),'maindo'] = '2018年中非合作论坛北京峰会官网'#由外交部所有

#政府
df.loc[(df['domain'].str.contains('.cssn.cn')) & (df['maindo'].isna()),'maindo'] = '中国社会科学网'
df.loc[(df['domain'].str.contains('.moh.gov')) & (df['maindo'].isna()),'maindo'] = '国家卫生健康委网站'
df.loc[(df['domain'].str.contains('.nhc.gov')) & (df['maindo'].isna()),'maindo'] = '国家卫生健康委网站'#部门有更新
df.loc[(df['domain'].str.contains('.mofcom.gov')) & (df['maindo'].isna()),'maindo'] = '商务部网站'
df.loc[(df['domain'].str.contains('www.gov.cn')) & (df['maindo'].isna()),'maindo'] = '中国政府网'
df.loc[(df['domain'].str.contains('cdc.cn')) & (df['maindo'].isna()),'maindo'] = '疾病预防控制中心网站'
df.loc[(df['domain'].str.contains('ccdi.gov')) & (df['maindo'].isna()),'maindo'] = '中央纪委国家监委网站'
df.loc[(df['domain'].str.contains('www.xichang.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站' #'西昌市人民政府网站'
df.loc[(df['domain'].str.contains('www.beijing.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站' #'北京市人民政府网站'
df.loc[(df['domain'].str.contains('www.fujian.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.fuzhou.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.hunan.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.hubei.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.quanzhou.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('.hebei.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.jiangsu.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.zjc.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.anshun.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.ak.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.haishu.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.sc.gov')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('wjw.fujian.gov')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'#'福建省卫生健康委网站'
df.loc[(df['domain'].str.contains('wsjk.')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('mfa.gov')) & (df['maindo'].isna()),'maindo'] = '外交部网站'
df.loc[(df['domain'].str.contains('.cppcc.gov.cn')) & (df['maindo'].isna()),'maindo'] = '中国政协网'
df.loc[(df['domain'].str.contains('.mem.gov.cn')) & (df['maindo'].isna()),'maindo'] = '应急管理部网站'
df.loc[(df['domain'].str.contains('.cppcc.gov.cn')) & (df['maindo'].isna()),'maindo'] = '中国政协网'
df.loc[(df['domain'].str.contains('www.npc.gov.cn')) & (df['maindo'].isna()),'maindo'] = '中国人大网'
df.loc[(df['domain'].str.contains('chinapeace.')) & (df['maindo'].isna()),'maindo'] = '中国长安网'
df.loc[(df['domain'].str.contains('www.spp.gov.cn')) & (df['maindo'].isna()),'maindo'] = '最高人民检察院网站'
df.loc[(df['domain'].str.contains('www.court.gov.cn')) & (df['maindo'].isna()),'maindo'] = '最高人民法院网站'
df.loc[(df['domain'].str.contains('www.moe.gov.cn')) & (df['maindo'].isna()),'maindo'] = '教育部网站'
df.loc[(df['domain'].str.contains('cnda.cfda.gov.cn')) & (df['maindo'].isna()),'maindo'] = '国家药监局网站'
df.loc[(df['domain'].str.contains('www.mof.gov.cn')) & (df['maindo'].isna()),'maindo'] = '财政部网站'
df.loc[(df['domain'].str.contains('www.moc.gov.cn')) & (df['maindo'].isna()),'maindo'] = '交通运输部网站' #部门有更新
df.loc[(df['domain'].str.contains('www.forestry.gov.cn')) & (df['maindo'].isna()),'maindo'] = '国家林草局网站'
df.loc[(df['domain'].str.contains('cea.gov.')) & (df['maindo'].isna()),'maindo'] = '中国地震局网站'
#df.loc[(df['domain'].str.contains('s.scio.gov.')) & (df['maindo'].isna()),'maindo'] = '国务院新闻办公室网站'
df.loc[(df['domain'].str.contains('www.scio.gov.')) & (df['maindo'].isna()),'maindo'] = '国务院新闻办公室网站'
df.loc[(df['domain'].str.contains('www.mlr.gov.')) & (df['maindo'].isna()),'maindo'] = '自然资源部网站' #部门有更新
df.loc[(df['domain'].str.contains('www.cma.gov.')) & (df['maindo'].isna()),'maindo'] = '中国气象局网站'
df.loc[(df['domain'].str.contains('www.spb.gov.')) & (df['maindo'].isna()),'maindo'] = '国家邮政局网站'
df.loc[(df['domain'].str.contains('www.mod.gov.')) & (df['maindo'].isna()),'maindo'] = '国防部网'
df.loc[(df['domain'].str.contains('www.chinatax.gov.')) & (df['maindo'].isna()),'maindo'] = '税务总局网站'

#其他填充
df.loc[(df['domain'].str.contains('.gov.cn')) & (df['maindo'].isna()),'maindo'] = '其他网站（政府机构）'
df.loc[df['maindo'].isna(),'maindo'] = '其他网站（非政府机构）'

#
print(df['maindo'].isna().sum())


#%% 移动端与PC端
df['mobile'] = 0
df.loc[df['maindo'].str.contains('应用程序|移动端网页版',regex=True),'mobile'] = 1
smobile = df['mobile'].value_counts()

# 合并同一系列的渠道
df['channel'] = df['maindo']
df['channel'] = df['channel'].replace(regex =['\+（应用程序）','（移动端网页版）','（应用程序）','（电子报）','-网站','（移动端网页版/应用程序）'], value = '')
schannel = df['channel'].value_counts()

#%% 是否政府机构
df['org'] = None

df.loc[df['maindo'].str.contains('其他网站（非政府机构）'),'org'] = '缺失'
df.loc[(df['maindo'].str.contains('G20官网|国际奥委会|国际足联|中国一带一路|中非合作论坛',regex=True))&(df['org'].isna()),'org'] = '跨国合作与国际组织网站' 
df.loc[(df['domain'].str.contains('\.gov\.cn|cdc\.cn|.cssn\.cn',regex=True))&(df['org'].isna()),'org'] = '政府机构网站'#含中国社会科学网
df.loc[(df['domain'].str.contains('www.baidu.com'))&(df['org'].isna()),'org'] = '搜索引擎'

smissingorg = df['channel'].loc[df['org'].isna()].value_counts()

df.loc[df['org'].isna(),'org'] = '门户网站与新闻平台' #微博都是官方账号


#df.loc[(df['domain'].str.contains('.gov.cn'))&(df['org'].isna()),'org'] = '新闻平台（含公众账号）'


# nodo = df[df['maindo'].isna()]
# nodo.to_csv("未映射域名632条.csv", index=True)
df.to_excel('citation.xlsx',index=True)
conn= sqlite.connect('BaiduWiki.sqlite')
df.to_sql('citation', conn, index=True, if_exists = 'replace')
conn.close()

#这个有问题
# conn= sqlite.connect('BaiduWiki.sqlite')
# c = conn.cursor()
# c.execute('''ALTER TABLE citation ADD COLUMN channel''')
# conn.commit()
# sc = '''INSERT INTO citation (channel) VALUES (?)'''
# values = [(x,) for x in df['maindo']]
# #df['maindo'].tolist()
# c.executemany(sc, values)
# conn.commit()
# c.close()
# conn.close()
#%% 联立引用日期和编辑时间，找到引用的具体的时间
import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情')
conn= sqlite.connect('Wiki.sqlite')

dfev = pd.read_sql('SELECT * FROM events', conn, index_col='index')
dfci = pd.read_sql('SELECT * FROM citation', conn)
dfedi = pd.read_sql('SELECT * FROM edit_time', conn,index_col='index')

dfci['ci_timestamp'] = pd.NaT
dfci['ci_time_count'] = np.nan

for index, row in dfev.iterrows():
#for index, row in dfev[20:21].iterrows():
    #去除空值后返回独特的引用日期
    if row['editcount'] > 0:
        #下面两行都要去除序列里的空值
        dfci_ev = dfci.loc[dfci['entry'] == row['entry'],'cite_time'].dropna().unique() 
        dfedi_ev = dfedi.loc[dfedi['entry'] == row['entry'],'edit_time'].dropna()
        for time in dfci_ev:
            a = dfedi_ev[dfedi_ev.str.startswith(time)].tolist() #找到匹配的编辑时间
            if a:#如果匹配上
                dfci.loc[(dfci['entry']==row['entry']) & (dfci['cite_time']==time),'ci_timestamp'] = str(a)
                dfci.loc[(dfci['entry']==row['entry']) & (dfci['cite_time']==time),'ci_time_count'] = len(a)
            else:
                dfci.loc[(dfci['entry']==row['entry']) & (dfci['cite_time']==time),'ci_timestamp'] = None
                dfci.loc[(dfci['entry']==row['entry']) & (dfci['cite_time']==time),'ci_time_count'] = np.nan
            #print(a)

dfci.to_sql('cittion_edtime', conn, index=True, if_exists = 'replace')    
conn.close()

dfci.to_csv('cittion_edtime.csv',index=True)

#%
conn0 = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情/Wiki.sqlite')
df0 = pd.read_sql('SELECT * FROM ci', conn0, index_col='level_0')

df0['ci_timestamp']=dfci['ci_timestamp']
df0['ci_time_count']=dfci['ci_time_count']

df0.to_sql('ci', conn0, index=True, if_exists = 'replace')    
conn0.close()

#%% 清洗整理新闻发布时间戳数据

import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re
import datefinder

conn = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情/Wiki.sqlite')
df = pd.read_sql('SELECT * FROM ci', conn)


df['tistamp_cl'] = df['timestamp'].replace(regex=['\n', '日'], value=' ') 
df['tistamp_cl'] = df['tistamp_cl'].replace(regex=['年', '月'], value='-')
df['tistamp_cl'] = df['tistamp_cl'].replace(regex =[r'[\u4e00-\u9fa5]'], value=' ') 
df['tistamp_cl'] = df['tistamp_cl'].replace(regex =['：','　www.gov.cn ','【','】','“','”','　:  ',': -  '], value='') 
df['finestamp']=pd.NaT

for index, row in df.iterrows():
    if pd.notna(row['tistamp_cl']) and ':' in row['tistamp_cl']: #剔除timestamp中没有时分的
        if 'org/zg2016/hbjs/index.html' not in row['origin_url']: #g20官网有几个年份不完整导致识别错误
            text = row['tistamp_cl']
        else:
            text = '20' + row['tistamp_cl'].strip()
        matches = datefinder.find_dates(text, strict=True)
        #time=pd.NaT
        for match in matches:
            time=match
        df.at[index, 'finestamp'] = time

# conn1 = sqlite.connect('test.sqlite')
# df.index += 1
# df.to_sql('test', conn1, index=True, if_exists = 'replace')
# conn1.close()

df.drop(columns=['tistamp_cl','test'],inplace=True)

df.index += 1
df.to_sql('ci', conn, index=False, if_exists = 'replace')    
conn.close()


#%% 清洗整理引用时间戳数据

import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re
import datefinder
from ast import literal_eval

conn = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情/Wiki.sqlite')
df = pd.read_sql('SELECT * FROM ci', conn)

df['test']=None
df['one_citime']=pd.NaT
df['stamp_di']=pd.to_timedelta(0)

for index, row in df.iterrows():
    if pd.notna(row['ci_timestamp']):
        ele = literal_eval(row['ci_timestamp'])
        df.at[index,'test'] = ele
        if len(ele)==1:
            df.at[index,'one_citime']=pd.to_datetime(ele[0])
        else:
            df.at[index,'stamp_di']=pd.to_datetime(ele[0])-pd.to_datetime(ele[-1])

b = df['one_citime']
c = df['stamp_di']
dis = c.value_counts()

df.drop(columns=['test','index'],inplace=True)

df.index += 1
df.to_sql('ci', conn, index=True, if_exists = 'replace')    
conn.close()

#%% 联立事件开始时间数据 2023-02-10
import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re
import datefinder
from ast import literal_eval
import datefinder
from datetime import datetime

conn = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情/Wiki.sqlite')
df = pd.read_sql('SELECT * FROM events', conn)

dfev = pd.read_excel('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0210补充事件时间/events.xlsx')
dfe = dfev[['entryindex','entry','start_time','uncovertime','once','end_time']]

dfm = pd.merge(df, dfe, how='left', on=['entryindex','entry'])

dfm.drop(columns=['index'],inplace=True)

#处理时间格式
def time_clean(series):
    series = series.replace(regex=['秒', '日'], value=' ')
    series = series.replace(regex=['年', '月'], value='-')
    series = series.replace(regex=['时', '点', '分'], value=':')
    series = series.replace(regex=['  '], value=' ')
    series = series.replace(r':$', value='', regex=True)
    return series

dfm.start_time = time_clean(dfm['start_time'])
# dfm.once = time_clean(dfm['once'])
# dfm.end_time = time_clean(dfm['end_time'])

dfm.start_time.astype(str)
# dfm.once.astype(str)
# dfm.end_time.astype(str)

dfm['start_cl'] = pd.NaT
# dfm['once_cl'] = pd.NaT
# dfm['end_cl'] = pd.NaT

def get_date(df,textrow,targetrow):
    for index, row in df.iterrows():
        if pd.notna(row[textrow]):
            matches = datefinder.find_dates(row[textrow], strict=True)
            for match in matches:
                time=match
            df.at[index, targetrow] = time

get_date(dfm,'start_time','start_cl')
# get_date(dfm,'once','once_cl')
# get_date(dfm,'end_time','end_cl')


# for index, row in dfm.iterrows():
#     if pd.notna(row['start_time']):
#         matches = datefinder.find_dates(row['start_time'], strict=True)
#         for match in matches:
#             time=match
#         dfm.at[index, 'start_cl'] = time


#下面两种做法老是报错，单个测试字符串又没错，不理解
# for index, row in dfm.iterrows():
#     dfm.at[index, 'start_time']=pd.to_datetime(row['start_time'])

# dfm.start_time = pd.Timestamp(dfm['start_time'])
# dfm.once = pd.Timestamp(dfm['once'])
# dfm.end_time = pd.Timestamp(dfm['end_time'])


dfm.index += 1
dfm.to_sql('events', conn, index=True, if_exists = 'replace')    
conn.close()

#%% 修改事件时间 联立事件类型
import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re
from datetime import datetime


conn= sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情/Wiki.sqlite')

df = pd.read_sql('SELECT * FROM events', conn, index_col='index')

df.start_cl = pd.to_datetime(df['start_cl'])
df.edi_start = pd.to_datetime(df['edi_start'])
df.edi_end = pd.to_datetime(df['edi_end'])

df.edi_range = pd.to_timedelta(df['edi_range'])
df.create_range = pd.to_timedelta(df['create_range'])

df.create_range = pd.NaT
df['create_range'] = df['edi_start'] - df['start_cl']

#终于学会这个apply 每行遍历，按列计算，虽然这是一个由于手误写错变量名引发的解决方案（哭泣
#下面两行尝试下来，至少两列相减pandas会自己处理缺失值
df['test'] = df.apply(lambda row: row['edi_start'] - row['start_cl'] if pd.notna(row['edi_start']) and pd.notna(row['start_cl']) else pd.NaT, axis=1)
df['test1'] = df.apply(lambda row: row['edi_start'] - row['start_cl'], axis=1)

df.drop(columns=['test','test1'],inplace=True)


# 创建词条时间差均值
df['create_range'][df['create_range']>pd.to_timedelta(0)].mean()

# 联立事件类型
dfty = pd.read_excel('/Users/zhangsiqi/Desktop/毕业论文代码mini/evtype.xlsx')

dfm = pd.merge(df, dfty, how='left', on=['entry'])

dfm.drop(columns=['index'],inplace=True)


os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0210补充事件时间')
dfm.to_csv('events+timestamp+evtype.csv',index=True)
dfm.to_excel('events+timestamp+evtype.xlsx',index=True)


#又是历久弥新的时间格式不匹配事件，只能反复导出导入
df = pd.read_csv('events+timestamp+evtype.csv',index_col=0)

df.to_sql('events', conn, index=True, if_exists = 'replace')    
conn.close()

#%%%% 找到词条的首尾编辑时间，生成编辑时间差 2023-02-10
import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re
from datetime import datetime


conn= sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情/Wiki.sqlite')

dfev = pd.read_sql('SELECT * FROM events', conn, index_col='index')
dfedi = pd.read_sql('SELECT * FROM edit_time', conn, index_col='index')

dfev['edi_start'] = pd.NaT
dfev['edi_end'] = pd.NaT
dfev['edi_range'] = np.nan
dfev['create_range'] = np.nan

for index, row in dfev.iterrows():
#for index, row in dfev[20:21].iterrows():
    #去除空值后返回独特的引用日期
    if row['editcount'] > 0:
        #下面两行都要去除序列里的空值
        dfedi_ev = dfedi.loc[dfedi['entry'] == row['entry'],'edit_time'].dropna().unique()
        dfev.at[index,'edi_start'] = pd.to_datetime(dfedi_ev[-1])
        dfev.at[index,'edi_end'] = pd.to_datetime(dfedi_ev[0])
        dfev.at[index,'edi_range'] = pd.to_datetime(dfedi_ev[0]) - pd.to_datetime(dfedi_ev[-1])
        if pd.notna(row['start_cl']):
            dfev.at[index,'create_range'] = pd.to_datetime(dfedi_ev[-1]) - pd.to_datetime(row['start_cl'])


os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0210补充事件时间')
dfev.to_csv('events+timestamp.csv',index=True)
dfev.to_excel('events+timestamp.xlsx',index=True)

# dfev.edi_start = dfev['edi_start'].map(lambda _: _.strftime("%Y-%m-%d %H:%M"), na_action='ignore')
# dfev.edi_end = dfev['edi_end'].map(lambda _: _.strftime("%Y-%m-%d %H:%M"), na_action='ignore')

#又是历久弥新的时间格式不匹配事件
df1 = pd.read_csv('events+timestamp.csv',index_col=0)

df1.to_sql('events', conn, index=True, if_exists = 'replace')    
conn.close()


#%% 感觉用户用不着？补充变量：编辑者数量及对应编辑次数、引用次数
import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re

dfev = pd.read_csv('eventssql.csv', index_col='Unnamed: 0')
dfev['author_count'] = np.nan
dfev['author_dic'] = None
dfedi = pd.read_csv('edithistorysql.csv', index_col='Unnamed: 0')

dfev['cite_count'] = np.nan
dfwt = pd.read_csv('wikitextsql.csv', index_col='Unnamed: 0')

for index, row in dfev.iterrows():
#for index, row in dfev[141:142].iterrows():
    dfau = dfedi.loc[dfedi['entry'] == row['entry'],'author_name']
    if not dfau.empty:
        author_count = dfau.nunique()
        distri = pd.DataFrame(dfau.value_counts().reset_index()) #这里一定要reset index要不然生成的数据框只有一列
        author_dic = str(dict(zip(distri.iloc[:,0],distri.iloc[:,1])))
    else:
        author_count = np.nan
        author_dic = None
    dfev.at[index, 'author_count'] = author_count
    dfev.at[index, 'author_dic'] = str(author_dic)
    
    dfci = dfwt.loc[dfwt['entry'] == row['entry'],'cited_item']
    if not dfci.empty:
        cilist = [ele for ele in dfci if ele == ele]
        ci_str = '; '.join(cilist)
        ci_li = ci_str.split('; ')
        dash_li = [el.strip('[]') for el in ci_li if '-' in el] #[94-95]
        if not dash_li: #如果没有出现 ‘【1-3】’的情况
            cite_count = len(ci_li)
            #print(ci_li)
        else:
            nodash_li = [int(el.strip('[]')) for el in ci_li if '-' not in el]
            for j in dash_li:
                start = re.search(r'(?P<start>\d+)\-',j)
                end = re.search(r'\-(?P<end>\d+)',j)
                real_li = range(int(start.groupdict()['start']),int(end.groupdict()['end'])+1)
                nodash_li.extend(real_li)
            cite_count = len(nodash_li)
    else:
        cite_count = np.nan
    dfev.at[index, 'cite_count'] = cite_count


# for index, row in dfev.iterrows():
#     dfci = dfwt.loc[dfwt['entry'] == row['entry'],'cited_item']
#     if not dfci.empty:
#         cilist = [ele for ele in dfci if ele == ele]
#         ci_str = '; '.join(cilist)
#         ci_li = ci_str.split('; ')
#         dash_li = [el.strip('[]') for el in ci_li if '-' in el] #[94-95]
#         if not dash_li: #如果没有出现 ‘【1-3】’的情况
#             cite_count = len(ci_li)
#             #print(ci_li)
#         else:
#             nodash_li = [int(el.strip('[]')) for el in ci_li if '-' not in el]
#             for j in dash_li:
#                 start = re.search(r'(?P<start>\d+)\-',j)
#                 end = re.search(r'\-(?P<end>\d+)',j)
#                 real_li = range(int(start.groupdict()['start']),int(end.groupdict()['end'])+1)
#                 nodash_li.extend(real_li)
#             cite_count = len(nodash_li)
#     else:
#         cite_count = np.nan
#     dfev.at[index, 'cite_count'] = cite_count


conn= sqlite.connect('Wiki.sqlite')
dfev.to_sql('events', conn, index=True, if_exists = 'replace')
conn.close()
    
dfev.to_csv('events.csv',index=True)
dfev.to_excel('events.xlsx',index=True)

