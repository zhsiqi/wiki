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
            if a:#如果匹配上了
                dfci.loc[(dfci['entry']==row['entry']) & (dfci['cite_time']==time),'ci_timestamp'] = str(a)
                dfci.loc[(dfci['entry']==row['entry']) & (dfci['cite_time']==time),'ci_time_count'] = len(a)
            else:
                dfci.loc[(dfci['entry']==row['entry']) & (dfci['cite_time']==time),'ci_timestamp'] = None
                dfci.loc[(dfci['entry']==row['entry']) & (dfci['cite_time']==time),'ci_time_count'] = np.nan
            #print(a)

dfci.to_sql('cittion_edtime', conn, index=False, if_exists = 'replace')    
conn.close()

#%% 画时间趋势图
import pandas as pd 
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.pyplot import MultipleLocator #设置坐标轴刻度
from matplotlib.font_manager import *
# import earthpy as et

df = pd.read_csv("edithistorysql.csv", index_col='Unnamed: 0')
dfev = pd.read_csv('eventssql.csv', index_col='Unnamed: 0')

df['update_time'] = pd.to_datetime(df['update_time'])
df['date'] = pd.to_datetime(df['update_time']).dt.date

plt.style.use('seaborn')
#myfont = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
#修改坐标轴字号

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



