#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 16:54:28 2023

@author: zhangsiqi
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


#%% mobile or not
df['mobile'] = 0
df.loc[df['maindo'].str.contains('应用程序|移动端网页版',regex=True),'mobile'] = 1
smobile = df['mobile'].value_counts()

# 合并同一系列的渠道
df['channel'] = df['maindo']
df['channel'] = df['channel'].replace(regex =['\+（应用程序）','（移动端网页版）','（应用程序）','（电子报）','-网站','（移动端网页版/应用程序）'], value = '')
schannel = df['channel'].value_counts()

#%% gov or not
df['org'] = None

df.loc[df['maindo'].str.contains('其他网站（非政府机构）'),'org'] = '缺失'
df.loc[(df['maindo'].str.contains('G20官网|国际奥委会|国际足联|中国一带一路|中非合作论坛',regex=True))&(df['org'].isna()),'org'] = '跨国合作与国际组织网站' 
df.loc[(df['domain'].str.contains('\.gov\.cn|cdc\.cn|.cssn\.cn',regex=True))&(df['org'].isna()),'org'] = '政府机构网站'#含中国社会科学网
df.loc[(df['domain'].str.contains('www.baidu.com'))&(df['org'].isna()),'org'] = '搜索引擎'

smissingorg = df['channel'].loc[df['org'].isna()].value_counts()

df.loc[df['org'].isna(),'org'] = '门户网站与新闻平台' #微博都是官方账号


#df.loc[(df['domain'].str.contains('.gov.cn'))&(df['org'].isna()),'org'] = '新闻平台（含公众账号）'

#%%
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

#%% 导出各表单
import os
import sqlite3 as sqlite
import pandas as pd

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情')
conn= sqlite.connect('Wiki.sqlite')


#将sqlite表单写入多张csv
def sql2csv(table_name, sqldb):
    table = pd.read_sql_query('SELECT * FROM '+ table_name, sqldb)
    table.index += 1
    table.to_csv(table_name+'sql.csv', index=True)
    
sql2csv('events',conn)
sql2csv('citation',conn)
sql2csv('edithistory',conn)
sql2csv('wikilink',conn)
sql2csv('topeditor',conn)
sql2csv('wikitext',conn)
sql2csv('science',conn)

def sql2excel(table_name, sqldb):
    table = pd.read_sql_query('SELECT * FROM '+ table_name, sqldb)
    table.index += 1
    table.to_excel(table_name+'.xlsx',index=True)
    
sql2excel('events',conn)
sql2excel('citation',conn)
sql2excel('edithistory',conn)
sql2excel('wikilink',conn)
sql2excel('topeditor',conn)
sql2excel('wikitext',conn)
sql2excel('science',conn)        

conn.close() #关闭sql
#%% 补充变量编辑者数量及对应编辑次数、引用次数
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
#%% csv连接数据：补充编辑历史的实际编辑时间 2023-02-08
import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re
import datetime

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0208补全编辑时间戳')

dfev = pd.read_csv('eventssql.csv', index_col='Unnamed: 0')
dfti = pd.read_csv('alleditime.csv', index_col='Unnamed: 0')

#dfev['update_time'] = pd.to_datetime(dfev['update_time'])

#屠呦呦 bug 因为爬取中断后直接从中间页面开始导致新抓取时实际抓取到的还是第一页的，所以25条编辑历史重复了 6292-6316
dftu = pd.read_csv('tuyou.csv', index_col='Unnamed: 0')
dftu['edit_entryindex']=range(126,151)
dfti = dfti.drop(index=range(6292,6317))

#替换掉重复的屠呦呦编辑历史
df0 = dfti[:6292]
df1 = dfti[6292:]
dfti = pd.concat([df0,dftu,df1],ignore_index=True, sort=False)#合并不保留原索引，启用新的自然索引：
#剔除2023.1.18及以后的编辑历史
dfti['update_time'] = pd.to_datetime(dfti['update_time'])
dfti['date'] = dfti['update_time'].dt.date
dfti['baseline'] = datetime.datetime(2023,1,18)
dfti = dfti[dfti['date']< dfti['baseline']]

#把每个事件的编辑历史索引更正
namelist = dfti['entry'].unique()

#namelist = dfti['entry'].unique().tolist()
dfti['edit_entryindex']=np.nan
dfti['edit_count']=np.nan
dfti['year']=None
dfti['event']=None
dfti['event_id']=None
dfti['entryindex']=None

for index, row in dfev.iterrows():
    i = row['entry']
    j = row['editcount']
    length = len(dfti[dfti['entry']==i])
    if length != j:
        print(i, j, '新采集的',length, '编辑次数变了')
    dfti.loc[dfti['entry']==i,'edit_entryindex'] = range(1,length+1)
    dfti.loc[dfti['entry']==i,'edit_count'] = length
    
    dfti.loc[dfti['entry']==i,'year'] = row['year']
    dfti.loc[dfti['entry']==i,'event'] = row['event']    
    dfti.loc[dfti['entry']==i,'event_id'] = row['event_id']
    dfti.loc[dfti['entry']==i,'entryindex'] = row['entryindex']
    
    # dfti.loc[dfti['entry']==i,'edit_entryindex'] = range(1,length+1) 死活想不明白为啥改成series就只能赋值第一个事件

# conn= sqlite.connect('置换.sqlite')
# dfti.to_sql('edit', conn, index=True, if_exists = 'replace')
# conn.close()

# dfti = dfti[['entry','edit_entryindex', 'update_time','author_name','edit_time']]
# dfti['edit_entryindex']=dfti['edit_entryindex'].astype(np.int64)
# dfap = pd.merge(df, dfti, how='left',on=['entry','update_time','author_name','edit_entryindex'])
dfti.drop(['baseline','date','time_di'],inplace=True,axis=1)

dfed = pd.read_csv('edithistorysql.csv', index_col='Unnamed: 0')
dfed['update_time'] = pd.to_datetime(dfed['update_time'])
dfed.year = dfed.year.astype('str')
dfed.event_id = dfed.event_id.astype('str')
dfed.edit_entryindex = dfed.edit_entryindex.astype('str')

dfmis = dfed[4448:4449]
dfmis['edit_time']=pd.NaT
dfmis.loc[:,'edit_time'] = pd.to_datetime('2014-03-08 08:59:00') 

#dfmis['edit_time']=pd.to_datetime('2014-03-08 08:59')

#插入缺失值
dfti.edit_count = dfti.edit_count.astype(int)
dfti1 = dfti[:4448]
dfti2 = dfti[4448:]
dfti = pd.concat([dfti1,dfmis,dfti2],ignore_index=True, sort=False)#合并不保留原索引，启用新的自然索引：
dfti.loc[dfti['entry']=='3·8马来西亚航班失踪事件','edit_count'] = 175

#下面导出数据很无语，因为老是parameter不对，最后直接导出csv再导入csv为sql了
os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0208补全编辑时间戳')
dfti.to_csv('edittimeall.csv',index=True)

df = pd.read_csv('edittimeall.csv',index_col='Unnamed: 0')
df.index += 1
# conn= sqlite.connect('edi+time.sqlite')
# df.to_sql('edit+time', conn, index=True, if_exists = 'replace')
# conn.close()
os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情')

conn= sqlite.connect('Wiki.sqlite')
df.to_sql('edit_time', conn, index=True, if_exists = 'replace')
conn.close()

#%% 通过引用日期找到引用的具体的时间
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

#%% 引入事件开始时间数据 2023-02-10
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

#%% 词条的首尾编辑时间和时间差 2023-02-10
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


#又是历久弥新的时间格式不匹配事件
df = pd.read_csv('events+timestamp+evtype.csv',index_col=0)

df.to_sql('events', conn, index=True, if_exists = 'replace')    
conn.close()


#又是历久弥新的时间格式转换
df.start_cl = pd.to_datetime(df['start_cl'])
df.edi_start = pd.to_datetime(df['edi_start'])
df.edi_end = pd.to_datetime(df['edi_end'])

df.edi_range = pd.to_timedelta(df['edi_range'])
df.create_range = pd.to_timedelta(df['create_range'])

df['edi_range_y'] = df['edi_range'] / np.timedelta64(1, 'Y')


#按年分组
grouped = df.groupby('year')

#编辑历史时间跨度
gr_des = grouped.describe()
gr_des.to_excel('gr_des.xlsx', index=True)

#词条编辑起止时间平均值
edi_end_mean = grouped.agg({'edi_start':'mean','edi_end':'mean'})
edi_end_mean.to_excel('edi_end_mean.xlsx',sheet_name='test_new',index=True)

#所有的词条编辑起止时间均值
df['edi_start'].mean() #Timestamp('2015-10-01 18:03:02.752293632')
df['edi_end'].mean() #Timestamp('2022-04-14 04:40:40.733945088')

# 写入已有Excel文件的新表单
# writer = pd.ExcelWriter('model_predict.xlsx',mode='a', engine='openpyxl',if_sheet_exists='new')
# df.to_excel(writer, sheet_name='sheet1')
# writer.save()
# writer.close()


#%% 画图(时间趋势\)
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0210补充事件时间')
plt.rc('font',family='Times New Roman')

df = pd.read_excel('events+timestamp+evtype+range.xlsx',index_col=0)

#又是历久弥新的时间格式转换
df.start_cl = pd.to_datetime(df['start_cl'])
df.edi_start = pd.to_datetime(df['edi_start'])
df.edi_end = pd.to_datetime(df['edi_end'])
df.docu_start = pd.to_datetime(df['docu_start'])

#更新了事件数据所以时间差重算
df.create_range = pd.NaT
#df['create_range'] = df['docu_start'] - df['start_cl'] #开始记录-事件发生

df.edi_range = pd.NaT
df['edi_range'] = df['edi_end'] - df['docu_start'] #事件开始-事件创建

#时间差格式处理：delta
df.edi_range = pd.to_timedelta(df['edi_range'])
#df.create_range = pd.to_timedelta(df['create_range'])

#时间差单位处理成年/日
df['edi_range_y'] = df['edi_range'] / np.timedelta64(1, 'Y')
#df['cre_range_d'] = df['create_range'] / np.timedelta64(1, 'D') 

#数据表按年分组
grouped = df.groupby('year')

#编辑历史时间跨度：数据描述
gr_des = grouped.describe()
gr_des.to_excel('gr_des_4.xlsx', index=True)
# = grouped['edi_range_y'].median()

alldescribe = df.describe()
alldescribe.to_excel('all_des_5.xlsx', index=True)


df.to_csv('events+timestamp+evtype+range+event.csv',index=True)
df.to_excel('events+timestamp+evtype+range+event.xlsx',index=True)

#2023-02-13按事件找到最早的词条编辑时间
#取出正经的当年事件的事件词条
df1 = df[pd.isna(df['notforyearevent'])]

#按事件找到词条的最早创建时间:按事件groupby/透视的行

evgroup= df1.groupby('event_id')
evgroupmin = evgroup.min()
docu_star_min = evgroup['docu_start'].min()
ev_star_min = evgroup['start_cl'].min()

#以事件为单位计算创建速度
evgroupmin.create_range = pd.NaT
#时间差=开始记录时间-事件发生时间
evgroupmin['create_range'] = evgroupmin['docu_start'] - evgroupmin['start_cl']
#时间差数据格式化 delta
evgroupmin.create_range = pd.to_timedelta(evgroupmin['create_range'])
#时间差数据转天数
evgroupmin['cre_range_d'] = evgroupmin['create_range'] / np.timedelta64(1, 'D')

evgroupmin.to_excel('evgroupmin.xlsx', index=True)

evdata = evgroupmin[['event','year','start_cl','cre_range_d','disaster','antici']] #这个表的索引就是event_id

evdata.to_excel('evdata.xlsx',index=True)

#event总体描述
allev_des = evdata.describe()
allev_des.to_excel('allev_des.xlsx', index=True)

#使用antici分组,完成数据描述
anticigr = evdata.groupby('antici')

antici_des = anticigr.describe()
antici_des.to_excel('antici_des.xlsx', index=True)

#使用disater组,完成数据描述
disasgr = evdata.groupby('disaster')

disasgr_des = disasgr.describe()
disasgr_des.to_excel('disasgr_des.xlsx', index=True)


#创建时间分箱形图，都太难看了
evdata.boxplot(column='cre_range_d',by='year',figsize=(7,4.45)).get_figure().savefig('create.png',dpi=300,bbox_inches='tight')

evdata.boxplot(column='cre_range_d',figsize=(4,8)).get_figure().savefig('create-boxl.png',dpi=300,bbox_inches='tight')


#找出箱形图的对应值
# 计算 四分位差
QR = 7.24 #前面描述统计输出的四分位数，直接粘贴过来计算出QR
# 下限 与 上线
low_limit = 0.46 - 1.5 * QR
up_limit = 7.70 + 1.5 * QR
print('下限为：', low_limit)
print('上限为：', up_limit)
print('异常值有：', evdata['cre_range_d'][(evdata['cre_range_d'] < low_limit) + (evdata['cre_range_d'] > up_limit)])
#上面按1.5标准差计算，下限为： -10.4,上限为： 18.56,有36个异常值

#异常值单独取出
flyer = evdata[['cre_range_d','event']][(evdata['cre_range_d'] < low_limit) + (evdata['cre_range_d'] > up_limit)]

# low_limit1 = 0.47 - 3 * QR
# up_limit1 = 7.80 + 3 * QR
# print('下限为：', low_limit1)
# print('上限为：', up_limit1)
# flyer = evdata[['cre_range_d','event']][(evdata['cre_range_d'] < low_limit1) + (evdata['cre_range_d'] > up_limit1)]
# print('异常值有：', len(flyer))
# #上面按1.5标准差计算，有31个异常值

#除去异常值的中间值,创建直方图
cdata = evdata['cre_range_d'][(evdata['cre_range_d'] > low_limit) & (evdata['cre_range_d'] < up_limit)]

chist = cdata.plot.hist(bins=17,figsize=(5,5),
                        xticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                        edgecolor="white",
                        linewidth=0.4
                )
chist.get_figure().savefig('create+histcenter17-1.png',dpi=300,bbox_inches='tight') #,grid=True

#xticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

#不剔除异常值，创建直方图
evdata['cre_range_d'].plot.hist(bins=40,figsize=(5,5),
                                edgecolor="white",
                                linewidth=0.4).get_figure().savefig('createhistalll4.png',dpi=300,bbox_inches='tight')


#编辑历史数据透视表
table = df.pivot_table(index='entryindex',columns='year',values='edi_range_y')

#pandas success
year_edi_range = table.plot.hist(subplots=True, layout=(4, 3),
                                  figsize=(20,26),sharex=False,
                                  fontsize=20)



table.plot(subplots=True, kind='hist', grid=True, legend=True, stacked=False, 
           sharex=True, sharey=True, 
           layout=(4,3),figsize=(22,22),fontsize=20)

#%% 分正负数描述创建时间差 2023-02-15
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0210补充事件时间')
plt.rc('font',family='Times New Roman')
#提高行内plot显示清晰度
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')

df = pd.read_excel('events+timestamp+evtype+range+event.xlsx',index_col=0)

#又是历久弥新的时间格式转换
df.start_cl = pd.to_datetime(df['start_cl'])
df.edi_start = pd.to_datetime(df['edi_start'])
df.edi_end = pd.to_datetime(df['edi_end'])
df.docu_start = pd.to_datetime(df['docu_start'])

# #数据表按年分组,描述编辑间隔
# grouped = df.groupby('year')
# #编辑历史时间跨度：数据描述
# gr_des = grouped.describe()
# gr_des.to_excel('gr_des_5.xlsx', index=True)
# # = grouped['edi_range_y'].median()
# alldescribe = df.describe()
# alldescribe.to_excel('all_des_6.xlsx', index=True)

#2023-02-13按事件找到最早的词条编辑时间
#取出正经的当年事件的事件词条
df1 = df[pd.isna(df['notforyearevent'])]

#按事件找到词条的最早创建时间:按事件groupby/透视的行
evgroup= df1.groupby('event_id')
evgroupmin = evgroup.min() #拿出最小值
# docu_star_min = evgroup['docu_start'].min() 手动查看用的
# ev_star_min = evgroup['start_cl'].min() 手动查看用的

#以事件为单位计算创建速度
evgroupmin.create_range = pd.NaT
#时间差=开始记录时间-事件发生时间
evgroupmin['create_range'] = evgroupmin['docu_start'] - evgroupmin['start_cl']
#时间差数据格式化 delta
evgroupmin.create_range = pd.to_timedelta(evgroupmin['create_range'])
#时间差数据转天数
evgroupmin['cre_range_d'] = evgroupmin['create_range'] / np.timedelta64(1, 'D')

evgroupmin.to_excel('evgroupmin.xlsx', index=True)

evdata = evgroupmin[['event','year','start_cl','docu_start','cre_range_d','disaster','antici']] #这个表的索引就是event_id

evdata.to_excel('evdata.xlsx',index=True)

#event总体描述
allev_des = evdata.describe()
allev_des.to_excel('allev_des.xlsx', index=True)

#使用时间差的正负值分组，数据描述
positive = evdata.groupby(evdata.cre_range_d>0)

posi_des = positive.describe()
posi_des.to_excel('posi_des.xlsx', index=True)

#基于正负小组使用时间范围分组，完成数据描述
pocen = positive.get_group(True)['cre_range_d']
multigr = pd.cut(pocen, bins=[0,1,3,7,30,100,np.inf])
multigr_des = pocen.groupby(multigr).describe()
multigr_des.to_excel('posimulti_des.xlsx', index=True)

necen = positive.get_group(False)['cre_range_d']
manygr = pd.cut(necen, bins=[-3000,-1000,-100,0])
manygr_des = necen.groupby(manygr).describe()
manygr_des.to_excel('negmulti_des.xlsx', index=True)


#使用antici分组,完成数据描述
anticigr = evdata.groupby('antici')

antici_des = anticigr.describe()
antici_des.to_excel('cre_antici_des.xlsx', index=True)

#使用disater组,完成数据描述
disasgr = evdata.groupby('disaster')

disasgr_des = disasgr.describe()
disasgr_des.to_excel('cre_disasgr_des.xlsx', index=True)




#创建时间分箱形图，都太难看了
evdata.boxplot(column='cre_range_d',by='year',figsize=(7,4.45)).get_figure().savefig('create.png',dpi=300,bbox_inches='tight')

evdata.boxplot(column='cre_range_d',figsize=(4,8)).get_figure().savefig('create-boxl.png',dpi=300,bbox_inches='tight')

#按照正负数分别画直方图
hispo = pocen[pocen<30].plot.hist(
    bins=22,figsize=(6,5),
    xticks=[0,1,2,3,4,5,6,7,8,9,10,15,20],
    edgecolor="white",
    linewidth=0.4
                )
# hispo = positive.get_group(True)['cre_range_d'].plot.hist(bins=17,figsize=(5,5),
#                         xticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
#                         edgecolor="white",
#                         linewidth=0.4
#                 )
hispo.get_figure().savefig('his-pos<30.png',dpi=300,bbox_inches='tight') #,grid=True

#找出箱形图的对应值
# 计算 四分位差
QR = 7.24 #前面描述统计输出的四分位数，直接粘贴过来计算出QR
# 下限 与 上线
low_limit = 0.46 - 1.5 * QR
up_limit = 7.70 + 1.5 * QR
print('下限为：', low_limit)
print('上限为：', up_limit)
abnormal = evdata['cre_range_d'][(evdata['cre_range_d'] < low_limit) + (evdata['cre_range_d'] > up_limit)]
print('异常值有：', len(abnormal))
#上面按1.5标准差计算，下限为： -10.4,上限为： 18.56,有36个异常值

#异常值单独取出
flyer = evdata[['cre_range_d','event']][(evdata['cre_range_d'] < low_limit) + (evdata['cre_range_d'] > up_limit)]

# low_limit1 = 0.47 - 3 * QR
# up_limit1 = 7.80 + 3 * QR
# print('下限为：', low_limit1)
# print('上限为：', up_limit1)
# flyer = evdata[['cre_range_d','event']][(evdata['cre_range_d'] < low_limit1) + (evdata['cre_range_d'] > up_limit1)]
# print('异常值有：', len(flyer))
# #上面按1.5标准差计算，有31个异常值

#除去异常值的中间值,创建直方图
cdata = evdata['cre_range_d'][(evdata['cre_range_d'] > low_limit) & (evdata['cre_range_d'] < up_limit)]

chist = cdata.plot.hist(bins=17,figsize=(5,5),
                        xticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                        edgecolor="white",
                        linewidth=0.4
                )
chist.get_figure().savefig('create+histcenter17-1.png',dpi=300,bbox_inches='tight') #,grid=True

#xticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

#不剔除异常值，创建直方图
evdata['cre_range_d'].plot.hist(bins=40,figsize=(5,5),
                                edgecolor="white",
                                linewidth=0.4).get_figure().savefig('createhistalll4.png',dpi=300,bbox_inches='tight')



#%%还是pandas 终于成功版。。。。


plt.rc('font',family='Times New Roman')

ax=table.plot(subplots=True, kind='hist', grid=True, legend=True, stacked=False, 
           sharex=True, sharey=True, figsize=(9,12),
           layout=(4,3))

#我搞不懂啊，为什么是这么取出来的，这不是取的第一个子图吗？通过测试证明，里面怎么取数字都不影响
ax[0,0].get_figure().savefig('name+3',dpi=300,bbox_inches='tight')

ax[2,2].get_figure().savefig('[2+2]',dpi=300,bbox_inches='tight')



#%%还是pandas 成功版。。。。继续整活


plt.rc('font',family='Times New Roman')

ax=table.plot(subplots=True, kind='hist', grid=True, legend=True, stacked=False, 
           sharex=True, sharey=True, figsize=(9,12),
           layout=(4,3))

ax.set_title('5 plots')

plt.title('5 plots')
ax[0,0].set_title('5 plots')

plt.show()

fig = ax[0,0].get_figure() #标题左上角
fig1 = ax[3,1].get_figure() #标题左上角
fig2 = ax[2,2].get_figure() #标题左上角

#查看每个figure的axes，结果一模一样
fig1.get_axes()

#原来最后一个标题加在了被隐藏的axis，所以图片看不到

#箱图基本成了，只差注释
df.boxplot(column='edi_range_y',by='year',figsize=(7,4.45)).get_figure().savefig('box+1.png',dpi=300,bbox_inches='tight')

#matplot 多个箱形图
import matplotlib.pyplot as plt
import numpy as np

#按年分组并得到每个组的edi_range_y值
tablebox = df.groupby('year')['edi_range_y']

tableboxli = []
tablenameli = []
for name, group in tablebox:
    tableboxli.append(group)
    tablenameli.append(name)

plt.grid(True)  #显示网格

plt.boxplot(tableboxli, labels=tablenameli, showmeans=True)  # 绘制箱线图


plt.savefig('box+6.png',dpi=300,bbox_inches='tight')
plt.show()  # 显示图片


#boxprops=dict(linewidth=0.8)
#plt.boxplot(tableboxli, labels=tablenameli, showmeans=True, boxprops=boxprops)  # 绘制箱线图

# import matplotlib as mpl
# mpl.rcParams['lines.linewidth'] = 0.8

#%% 时间线图
df['edi_start_d']=df['edi_start'].dt.date
df['edi_end_d']=df['edi_end'].dt.date


#下面是只画出两条线

dates=[df[0:1]['edi_start_d'],df[0:1]['edi_end_d']]
dates1 = [df[1:2]['edi_start_d'],df[0:1]['edi_end_d']]
# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(12, 3), constrained_layout=True)
ax.set(title="timeline")

ax.plot(dates, np.zeros_like(dates), "-o", color="k", markerfacecolor="w")  # Baseline and markers on it.
ax.plot(dates1, np.zeros_like(dates)-1, "-o", color="k", markerfacecolor="w")  # Baseline and markers on it.

# remove y axis and spines
#ax.yaxis.set_visible(False)
# format xaxis with 4 month intervals
ax.xaxis.set_major_locator(mdates.YearLocator(1))


plt.show()


#下面是画出所有事件的时间线
fig, ax = plt.subplots(figsize=(12, 40), constrained_layout=True)
ax.set(title="timeline")

for index, row in df.iterrows():
    if row['editcount']>0:
        dates=[row["edi_start_d"],row["edi_end_d"]]
        value=[220-index,220-index]
        ax.plot(dates, value, "-o", color="k", markerfacecolor="w")
        # fig.add_trace(go.Scatter(x=[start, end], y=[value, value],
        #                 mode='lines'))  

ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.set_ylim([0, 221]) #设置Y轴范围
ax.yaxis.set_visible(False) #隐藏Y轴
plt.show()


# format xaxis with 4 month intervals
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")




#%%

f, axes = plt.subplots(4,3,figsize=(12,15),sharex='all',sharey='all')
f.delaxes(axes[3,2]) #删除多余的图

axes[0,0].hist(df['edi_range_y'][df['year']==2011])
axes[0,0].grid(True) #是否产生网格
axes[0,0].legend(labels=('2011'), loc='lower left')

axes[0,1].hist(df['edi_range_y'][df['year']==2012])
axes[0,1].legend()
axes[0,2].hist(df['edi_range_y'][df['year']==2013])
axes[0,2].legend()

axes[1,0].hist(df['edi_range_y'][df['year']==2014])
axes[1,0].legend()
axes[1,1].hist(df['edi_range_y'][df['year']==2015])
axes[1,1].legend()
axes[1,2].hist(df['edi_range_y'][df['year']==2016])
axes[1,2].legend()

axes[2,0].hist(df['edi_range_y'][df['year']==2017])
axes[2,0].legend()
axes[2,1].hist(df['edi_range_y'][df['year']==2018])
axes[2,1].legend()
axes[2,2].hist(df['edi_range_y'][df['year']==2019])
axes[2,2].legend()
axes[2,2].xaxis.set_tick_params(which='both', labelbottom=True, labeltop=False)  #强制控制x轴的显示

axes[3,0].hist(df['edi_range_y'][df['year']==2020])
axes[3,0].legend()
axes[3,1].hist(df['edi_range_y'][df['year']==2021])
axes[3,1].legend()

plt.show()

#简化上面的重复
def sub_plot(row, column, catename, catelist, value):
    index=0
    for i in range(0,row):
        for j in range(0,column):
            axes[i,j].hist(df[value][df[catename]==catelist[index]])
            #修改坐标轴字号
            plt.yticks(fontproperties = 'Times New Roman',size = 18)
            plt.xticks(fontproperties = 'Times New Roman',size = 18)
            index+=1
            if index==len(catelist):
                break
     
cateli=df['year'].unique().tolist()
sub_plot(4,3,'year',cateli,'edi_range_y')
#%%

import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.pyplot import MultipleLocator #设置坐标轴刻度
from matplotlib.font_manager import *


df = pd.read_csv("edithistorysql.csv", index_col='Unnamed: 0')
dfev = pd.read_csv('eventssql.csv', index_col='Unnamed: 0')

df['update_time'] = pd.to_datetime(df['update_time'])
df['date'] = pd.to_datetime(df['update_time']).dt.date

plt.style.use('seaborn')
#myfont = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
#plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


for index, row in dfev[0:1].iterrows():
    if not pd.isna(row['editcount']):
        df1 = df[df['entry'] == row['entry']]
        df1group = df1.groupby('date').count()
        #df1group['date'] = df1group.index
        #pc95 = df1group['edit_count'].quantile(0.9)
        df1group['Percentile Rank'] = df1group['edit_count'].rank(pct = True)
        #df1group = pd.DataFrame(df1.groupby('date').count())
        startt = df1group.index[0]
        endt = startt + pd.Timedelta(days=180)
        subset = df1group[startt:endt]
        #print(startt, endt)
        #x = pd.date_range(start=startt, end=endt, freq="30D") 
        
        # Create figure and plot space
        fig, ax = plt.subplots(figsize=(40, 10)) #figsize=(40, 10)搭配字体大小35
        
        # Add x-axis and y-axis
        #ax.bar(subset.index.values, subset['edit_count'],color='navy')
        ax.bar(subset.index.values, subset['edit_count'])
        
        #修改时间轴的刻度
        x_major_locator=MultipleLocator(30)#把x轴的刻度间隔设置为30个单位（即一个月），并存在变量里
        ax=plt.gca() #ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)#把x轴的主刻度设置为x的倍数
        #plt.xlim(-0.5,11)#把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
        
        #设置坐标轴标记和坐标轴标签的字体
        plt.xlabel('时间', fontsize=35)
        plt.ylabel('词条编辑次数', fontsize=35)
        plt.yticks(fontproperties = 'Times New Roman', size = 35, fontweight='normal')
        plt.xticks(fontproperties = 'Times New Roman', size = 35, fontweight='normal')
        
        plt.savefig('%s.png' %(row['entry']), bbox_inches='tight', dpi=300) #tight去除输出时四周白边
        plt.show()
        #subset['edit_count'].plot(figsize=(40,10))
    

#持续时间：最后一天-第一天





conn1.close()            



