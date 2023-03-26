#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 00:02:27 2023

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
from urllib.parse import urlparse
import requests

#%%
conn= sqlite.connect("/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1.sqlite")
c = conn.cursor()

df = pd.read_sql('SELECT * FROM ci_reindex', conn)



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

df.loc[df['reference_url']==link1,'original_url'] = tlink1
df.loc[df['reference_url']==link2,'original_url'] = tlink2
df.loc[df['reference_url']==link3,'original_url'] = tlink3
df.loc[df['reference_url']==link4,'original_url'] = tlink4
df.loc[df['reference_url']==link5,'original_url'] = tlink5

df.loc[df['reference_url']==link1,'origin_url'] = tlink1
df.loc[df['reference_url']==link2,'origin_url'] = tlink2
df.loc[df['reference_url']==link3,'origin_url'] = tlink3
df.loc[df['reference_url']==link4,'origin_url'] = tlink4
df.loc[df['reference_url']==link5,'origin_url'] = tlink5

df.loc[pd.isna(df['origin_url']) & pd.notna(df['redir_url']),'origin_url']=df['original_url']
# conn = sqlite.connect('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0214补充词条数据/Wiki+1.sqlite')
df.to_sql('ci_reindex_urlt', conn, index=False, if_exists='replace')


#%% 从URL中提取日期和域名
#修正URL时间解析错误 20230126，之前为了容错/20190829af20结果引入了/20190836af67的噪音

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

df = pd.read_sql('SELECT * FROM ci_reindex_urlt', conn)



for index, row in df.iterrows():
    url = row['origin_url']
    if url:
        df.at[index, 'domain'] = urlparse(url).netloc
    if pd.notna(url) and pd.isna(row['channel']):
        date = get_pubtime_by_url(url) #不能用urlpath因为得到的urlpath并不完整
        df.at[index, 'url_time'] = date

df.to_sql('ci_reindex_urlt', conn, index=False, if_exists = 'replace')


mob = df[df['domain'].str.startswith('m.')==1]['domain'].value_counts()

#%% 新建列聚合网页等渠道

df['maindo']= None


df.loc[(df['domain'].str.contains('www.dahebao.cn')) & (df['maindo'].isna()),'maindo'] = '大河报网'
df.loc[(df['domain'].str.contains('www.gzdaily.cn')) & (df['maindo'].isna()),'maindo'] = '广州日报(网站)'
df.loc[(df['domain'].str.contains('paper.nandu.com')) & (df['maindo'].isna()),'maindo'] = '南方都市报(网站)'
df.loc[(df['domain'].str.contains('kuaixun.stcn.com')) & (df['maindo'].isna()),'maindo'] = '证券时报网'
df.loc[(df['domain'].str.contains('epaper.jinghua.cn')) & (df['maindo'].isna()),'maindo'] = '京华时报(网站)'
df.loc[(df['domain'].str.contains('politics.scdaily.cn')) & (df['maindo'].isna()),'maindo'] = '四川日报网'
df.loc[(df['domain'].str.contains('sjb.qlwb.com.cn')) & (df['maindo'].isna()),'maindo'] = '齐鲁晚报（电子报）'
df.loc[(df['domain'].str.contains('szb.hkwb.net')) & (df['maindo'].isna()),'maindo'] = '海口晚报（电子报）'
df.loc[(df['domain'].str.contains('v5share.cdrb.com.cn')) & (df['maindo'].isna()),'maindo'] = '锦观新闻（应用程序）'
df.loc[(df['domain'].str.contains('www.21jingji.com')) & (df['maindo'].isna()),'maindo'] = '21世纪经济网'
df.loc[(df['domain'].str.contains('www.bbtnews.com.cn')) & (df['maindo'].isna()),'maindo'] = '北京商报网'
df.loc[(df['domain'].str.contains('www.dailyqd.com')) & (df['maindo'].isna()),'maindo'] = '青报网'
df.loc[(df['domain'].str.contains('www.changjiangtimes.com')) & (df['maindo'].isna()),'maindo'] = '长江商报（网站）'
df.loc[(df['domain'].str.contains('www.jinbw.com.cn')) & (df['maindo'].isna()),'maindo'] = '今报网'
df.loc[(df['domain'].str.contains('www.njdaily.cn')) & (df['maindo'].isna()),'maindo'] = '南报
df.loc[(df['domain'].str.contains('www.qlwb.com.cn')) & (df['maindo'].isna()),'maindo'] = '齐鲁晚报（网站）'
df.loc[(df['domain'].str.contains('www.wccdaily.com.cn')) & (df['maindo'].isna()),'maindo'] = 'huaxidushibao'
df.loc[(df['domain'].str.contains('www.xtrb.cn')) & (df['maindo'].isna()),'maindo'] = '牛城晚报(电子报)'



df.loc[(df['domain'].str.contains('www.ithome.com')) & (df['maindo'].isna()),'maindo'] = 'IT之家(网站)'
df.loc[(df['domain'].str.contains('ishare.ifeng')) & (df['maindo'].isna()),'maindo'] = '凤凰新闻（应用程序）'
df.loc[(df['domain'].str.contains('ifeng.')) & (df['maindo'].isna()),'maindo'] = '凤凰网'
df.loc[(df['domain'].str.contains('c.m.163.')) & (df['maindo'].isna()),'maindo'] = '网易网（应用程序）'
df.loc[(df['domain'].str.contains('3g.163.com')) & (df['maindo'].isna()),'maindo'] = '网易网（应用程序）'
df.loc[(df['domain'].str.contains('m.163.')) & (df['maindo'].isna()),'maindo'] = '网易网（移动端网页版）'
df.loc[(df['domain'].str.contains('163.')) & (df['maindo'].isna()),'maindo'] = '网易网'


df.loc[(df['origin_url'].str.contains('sinawap')) & (df['maindo'].isna()),'maindo'] = '新浪新闻（应用程序）'
df.loc[(df['domain']==('m.weibo.cn')) & (df['maindo'].isna()),'maindo'] = '新浪微博（移动端网页版）'
df.loc[(df['domain'].str.contains('weibo.com')) & (df['maindo'].isna()),'maindo'] = '新浪微博-网站'
df.loc[(df['domain'].str.contains('.sina.cn')) & (df['maindo'].isna()),'maindo'] = '新浪网(应用程序)'
df.loc[(df['domain'].str.contains('sina.com')) & (df['maindo'].isna()),'maindo'] = '新浪网'

df.loc[(df['domain'].str.contains('weixin.')) & (df['maindo'].isna()),'maindo'] = '腾讯微信公众平台（移动端网页版）'
df.loc[(df['domain'].str.contains('view.inews.qq')) & (df['maindo'].isna()),'maindo'] = '腾讯新闻（应用程序）'
df.loc[(df['domain'].str.contains('qq.')) & (df['maindo'].isna()),'maindo'] = '腾讯网'

df.loc[(df['domain'].str.startswith('3g.k.sohu.com')) & (df['maindo'].isna()),'maindo'] = '搜狐网（应用程序）'
df.loc[(df['domain'].str.startswith('m.sohu.')) & (df['maindo'].isna()),'maindo'] = '搜狐网（移动端网页版）'
df.loc[(df['domain'].str.contains('sohu.')) & (df['maindo'].isna()),'maindo'] = '搜狐网'
df.loc[(df['domain'].str.contains('baike.baidu')) & (df['maindo'].isna()),'maindo'] = '百度百科-网站'
df.loc[(df['domain'].str.contains('baijiahao.baidu')) & (df['maindo'].isna()),'maindo'] = '百度百家号'
df.loc[(df['domain'].str.contains('mbd.baidu.')) & (df['maindo'].isna()),'maindo'] = '百度百家号（应用程序）'#也是应用程序，这个mbd本身覆盖不止百家号码
df.loc[(df['domain'].str.contains('www.baidu.com')) & (df['maindo'].isna()),'maindo'] = '百度搜索引擎'

df.loc[(df['domain'].str.contains('jiemian.')) & (df['maindo'].isna()),'maindo'] = '界面新闻-网站'
df.loc[(df['domain'].str.startswith('m.thepaper.')) & (df['maindo'].isna()),'maindo'] = '澎湃新闻（移动端网页版/应用程序）'#也是APP
df.loc[(df['domain'].str.contains('thepaper.')) & (df['maindo'].isna()),'maindo'] = '澎湃新闻-网站'


df.loc[(df['domain']=='jjckb.xinhuanet.com') & (df['maindo'].isna()),'maindo'] = '经济参考报'
df.loc[(df['domain'].str.contains('api3.cls.cn')) & (df['maindo'].isna()),'maindo'] = '财联社（应用程序）'
df.loc[(df['domain'].str.contains('xhpfmapi')) & (df['maindo'].isna()),'maindo'] = '新华社（应用程序）'
df.loc[(df['domain'].str.contains('h.xinhuaxmt')) & (df['maindo'].isna()),'maindo'] = '新华社（应用程序）'
df.loc[(df['domain']=='m.news.cn') & (df['maindo'].isna()),'maindo'] = '新华网（移动端网页版）'
df.loc[(df['domain']=='m.xinhuanet.com') & (df['maindo'].isna()),'maindo'] = '新华网（移动端网页版）'
df.loc[(df['domain']=='sports.news.cn') & (df['maindo'].isna()),'maindo'] = '新华网'
df.loc[(df['domain']=='english.news.cn') & (df['maindo'].isna()),'maindo'] = '新华网'
df.loc[(df['domain']=='bj.news.cn') & (df['maindo'].isna()),'maindo'] = '新华网'
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
df.loc[(df['domain'].str.contains('app.people.cn')) & (df['maindo'].isna()),'maindo'] = '人民网（应用程序）'
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
df.loc[(df['domain'].str.endswith('3g.china.com')) & (df['maindo'].isna()),'maindo'] = '中华网（移动端网页版）'
df.loc[(df['domain'].str.endswith('.china.com')) & (df['maindo'].isna()),'maindo'] = '中华网'
df.loc[(df['domain'].str.contains('rmzxb.com')) & (df['maindo'].isna()),'maindo'] = '人民政协网'
df.loc[(df['domain'].str.contains('.youth.cn')) & (df['maindo'].isna()),'maindo'] = '中国青年网'
df.loc[(df['domain'].str.contains('zqb.cyol.com')) & (df['maindo'].isna()),'maindo'] = '中国青年报（电子报）'
df.loc[(df['domain'].str.contains('news.cyol.com')) & (df['maindo'].isna()),'maindo'] = '中青在线'
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
df.loc[(df['domain'].str.contains('m.guancha.cn')) & (df['maindo'].isna()),'maindo'] = '观察者网（移动端网页版）'

df.loc[(df['domain'].str.contains('.guancha.cn')) & (df['maindo'].isna()),'maindo'] = '观察者网'
df.loc[(df['domain'].str.contains('.caixin.com')) & (df['maindo'].isna()),'maindo'] = '财新网'
df.loc[(df['domain'].str.contains('.caijing.com')) & (df['maindo'].isna()),'maindo'] = '财经网'
df.loc[(df['domain'].str.contains('.hexun.com')) & (df['maindo'].isna()),'maindo'] = '和讯网'
df.loc[(df['domain'].str.contains('m.voc.com.cn')) & (df['maindo'].isna()),'maindo'] = '湖南日报（应用程序）'
df.loc[(df['domain'].str.contains('zjrb.zjol.com')) & (df['maindo'].isna()),'maindo'] = '浙江日报（电子报）'
df.loc[(df['domain'].str.contains('zjnews.zjol.com.cn')) & (df['maindo'].isna()),'maindo'] = '浙江在线-网站'

df.loc[(df['domain'].str.contains('hznews.')) & (df['maindo'].isna()),'maindo'] = '杭州网'
df.loc[(df['domain'].str.contains('.xhby.')) & (df['maindo'].isna()),'maindo'] = '新华报业网'
df.loc[(df['domain'].str.contains('sichuan.scol.')) & (df['maindo'].isna()),'maindo'] = '四川在线-网站'
df.loc[(df['domain'].str.contains('.dzwww.')) & (df['maindo'].isna()),'maindo'] = '大众网'
df.loc[(df['domain'].str.contains('epaper.ynet')) & (df['maindo'].isna()),'maindo'] = '北京青年报（电子报）'
df.loc[(df['domain'].str.contains('ynet.')) & (df['maindo'].isna()),'maindo'] = '北青网'
#df.loc[(df['domain'].str.startswith('t.ynet')) & (df['maindo'].isna()),'maindo'] = '北青网（移动端网页版）' 不好判断

df.loc[(df['domain'].str.contains('takefoto.')) & (df['maindo'].isna()),'maindo'] = '北晚在线-网站'
df.loc[(df['domain'].str.contains('export.shobserver')) & (df['maindo'].isna()),'maindo'] = '上观新闻（应用程序）'
df.loc[(df['domain'].str.contains('web.shobserver')) & (df['maindo'].isna()),'maindo'] = '上观新闻-网站'
df.loc[(df['domain'].str.contains('jfdaily.')) & (df['maindo'].isna()),'maindo'] = '上观新闻网'
df.loc[(df['domain'].str.contains('n.cztv')) & (df['maindo'].isna()),'maindo'] = '新蓝网'
df.loc[(df['domain'].str.contains('ynet')) & (df['maindo'].isna()),'maindo'] = '北青网'
df.loc[(df['domain'].str.contains('kankanews')) & (df['maindo'].isna()),'maindo'] = '看看新闻-网站'
df.loc[(df['domain']=='www.thecover.cn') & (df['maindo'].isna()),'maindo'] = '封面新闻'
df.loc[(df['domain'].str.contains('m.thecover.cn')) & (df['maindo'].isna()),'maindo'] = '封面新闻（应用程序）'
df.loc[(df['domain'].str.contains('static.cdsb.com')) & (df['maindo'].isna()),'maindo'] = '红星新闻（应用程序）'
df.loc[(df['domain'].str.contains('static.dingxinwen.com')) & (df['maindo'].isna()),'maindo'] = '河南日报（应用程序）'
df.loc[(df['domain'].str.contains('static.nfapp.southcn.com')) & (df['maindo'].isna()),'maindo'] = '南方日报（应用程序）'
df.loc[(df['original_url'].str.contains('wap.cqcb.com/shangyou_news/')) & (df['maindo'].isna()),'maindo'] = '上游新闻网（应用程序）'
df.loc[(df['original_url'].str.contains('http://qz.fjsen.com/')) & (df['maindo'].isna()),'maindo'] = '东南网'
df.loc[(df['domain'].str.contains('kscgc.sctv-tf.com')) & (df['maindo'].isna()),'maindo'] = '四川广播电视台（应用程序）'
df.loc[(df['domain'].str.contains('cbgc.scol.com.cn')) & (df['maindo'].isna()),'maindo'] = '四川日报（应用程序）'
df.loc[(df['domain'].str.contains('ccwb.1news.cc')) & (df['maindo'].isna()),'maindo'] = '长春晚报'
df.loc[(df['domain'].str.contains('cqcbepaper.cqnews.net')) & (df['maindo'].isna()),'maindo'] = '重庆晨报'
df.loc[(df['domain'].str.contains('daily.cnnb.com.cn')) & (df['maindo'].isna()),'maindo'] = '宁波日报（电子报）'
df.loc[(df['domain'].str.contains('epaper.scjjrb.com')) & (df['maindo'].isna()),'maindo'] = '四川经济日报（电子报）'
df.loc[(df['domain'].str.contains('epaper.tibet3.com')) & (df['maindo'].isna()),'maindo'] = '青海法制报（电子报）'
df.loc[(df['domain'].str.contains('gzdaily.dayoo.com')) & (df['maindo'].isna()),'maindo'] = '广州日报（电子报）'
df.loc[(df['domain'].str.contains('.takungpao.com')) & (df['maindo'].isna()),'maindo'] = '大公网'
df.loc[(df['domain'].str.contains('newpaper.dahe.cn')) & (df['maindo'].isna()),'maindo'] = '大河报（电子报）'
df.loc[(df['domain'].str.contains('news.cnhubei.com')) & (df['maindo'].isna()),'maindo'] = '荆楚网'
df.loc[(df['domain'].str.contains('news.hbtv.com.cn')) & (df['maindo'].isna()),'maindo'] = '湖北网络广播电视台-网站'
df.loc[(df['domain'].str.contains('news.southcn.com')) & (df['maindo'].isna()),'maindo'] = '南方网'
df.loc[(df['domain'].str.contains('news.wenweipo.com')) & (df['maindo'].isna()),'maindo'] = '香港文汇网'
df.loc[(df['domain'].str.contains('photo.wenweipo.com')) & (df['maindo'].isna()),'maindo'] = '香港文汇网'
df.loc[(df['domain'].str.contains('newspaper.jcrb.com')) & (df['maindo'].isna()),'maindo'] = '检察日报-电子报'
df.loc[(df['domain'].str.contains('qjwb.thehour.cn')) & (df['maindo'].isna()),'maindo'] = '钱江晚报-电子报'
df.loc[(df['domain'].str.contains('rmfyb.chinacourt.org')) & (df['maindo'].isna()),'maindo'] = '人民法院报-电子报'
df.loc[(df['domain'].str.contains('shanghai.xinmin.cn')) & (df['maindo'].isna()),'maindo'] = '新民网'
df.loc[(df['domain'].str.contains('www.brtn.cn')) & (df['maindo'].isna()),'maindo'] = '北京网络广播电视台'
df.loc[(df['domain'].str.contains('www.cet.com.cn')) & (df['maindo'].isna()),'maindo'] = '中国经济新闻网'
df.loc[(df['domain'].str.contains('www.ycwb.com')) & (df['maindo'].isna()),'maindo'] = '金羊网'
df.loc[(df['domain'].str.contains('www.yangtse.com')) & (df['maindo'].isna()),'maindo'] = '扬子晚报网'
df.loc[(df['domain'].str.contains('www.mnw.cn')) & (df['maindo'].isna()),'maindo'] = '闽南网'
df.loc[(df['domain'].str.contains('www.ettoday.net')) & (df['maindo'].isna()),'maindo'] = '东森新闻云'
df.loc[(df['domain'].str.contains('news.qingdaonews.com')) & (df['maindo'].isna()),'maindo'] = '青岛新闻网'
df.loc[(df['domain'].str.contains('www.sznews.com')) & (df['maindo'].isna()),'maindo'] = '深圳新闻网'
df.loc[(df['domain'].str.contains('www.toutiao.com')) & (df['maindo'].isna()),'maindo'] = '今日头条'
df.loc[(df['domain'].str.contains('www.dfdaily.com')) & (df['maindo'].isna()),'maindo'] = '东方早报'
df.loc[(df['domain'].str.contains('www.henandaily.cn')) & (df['maindo'].isna()),'maindo'] = '河南日报网'
df.loc[(df['domain'].str.contains('www.hxnews.com')) & (df['maindo'].isna()),'maindo'] = '海峡网'

df.loc[(df['domain'].str.contains('www.legaldaily.com.cn')) & (df['maindo'].isna()),'maindo'] = '法制网'
df.loc[(df['domain'].str.contains('www.stdaily.com')) & (df['maindo'].isna()),'maindo'] = '中国科技网'
df.loc[(df['domain'].str.contains('www.chinacourt.org')) & (df['maindo'].isna()),'maindo'] = '中国法院网'
df.loc[(df['domain'].str.contains('www.gongyishibao.com')) & (df['maindo'].isna()),'maindo'] = '公益时报网'
df.loc[(df['domain'].str.contains('news.sciencenet.cn')) & (df['maindo'].isna()),'maindo'] = '科学网'
df.loc[(df['domain'].str.contains('www.apdnews.com')) & (df['maindo'].isna()),'maindo'] = '亚太日报'

df.loc[(df['domain'].str.contains('sputniknews.cn')) & (df['maindo'].isna()),'maindo'] = '俄罗斯卫星通讯社'
df.loc[(df['domain'].str.contains('www.asahi.com')) & (df['maindo'].isna()),'maindo'] = '朝日新闻'
df.loc[(df['domain'].str.contains('www.bbc.com')) & (df['maindo'].isna()),'maindo'] = '英国广播公司'

df.loc[(df['domain'].str.contains('www.g20chn')) & (df['maindo'].isna()),'maindo'] = 'G20官网'
df.loc[(df['domain'].str.contains('olympics')) & (df['maindo'].isna()),'maindo'] = '国际奥委会官网'
df.loc[(df['domain'].str.contains('.fifa.')) & (df['maindo'].isna()),'maindo'] = '国际足联官网'
df.loc[(df['domain'].str.contains('www.yidaiyilu.gov.cn')) & (df['maindo'].isna()),'maindo'] = '中国一带一路网'
df.loc[(df['domain'].str.contains('focacsummit')) & (df['maindo'].isna()),'maindo'] = '2018年中非合作论坛北京峰会官网'#由外交部所有
df.loc[(df['domain'].str.contains('www.beijing2022.cn')) & (df['maindo'].isna()),'maindo'] = '北京2022年冬奥委会官网'
df.loc[(df['domain'].str.contains('results.beijing2022.cn')) & (df['maindo'].isna()),'maindo'] = '北京2022年冬奥委会官网'
df.loc[(df['domain'].str.contains('www.who.int')) & (df['maindo'].isna()),'maindo'] = '世界卫生组织官网'
df.loc[(df['domain'].str.contains('2017.beltandroadforum.org')) & (df['maindo'].isna()),'maindo'] = ''''“一带一路”国际合作高峰论坛官网'''
df.loc[(df['domain'].str.contains('www.olympic.cn')) & (df['maindo'].isna()),'maindo'] = '中国奥委会官网'

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
df.loc[(df['domain'].str.contains('sc.isd.gov.hk')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站' #香港
df.loc[(df['domain'].str.contains('www.gov.mo')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站' #澳门
df.loc[(df['domain'].str.contains('www.gcs.gov.mo')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站' #澳门
df.loc[(df['domain'].str.contains('www.sansha.gov.cn')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.zjkcl.gov.cn')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('www.yn.gov.cn')) & (df['maindo'].isna()),'maindo'] = '地方人民政府网站'
df.loc[(df['domain'].str.contains('appweb.scpublic.cn')) & (df['maindo'].isna()),'maindo'] = '四川发布（应用程序）'


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
df.loc[(df['domain'].str.contains('hc.jiangxi.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('sxwjw.shaanxi.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('wjw.ah.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('wjw.beijing.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'

df.loc[(df['domain'].str.contains('www.gzhfpc.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('www.hebwst.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['origin_url'].str.contains('www.jl.gov.cn/szfzt/jlzxd/yqtb')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('www.xjhfpc.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('www.zjwjw.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'

df.loc[(df['domain'].str.contains('wjw.hubei.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('wjw.hunan.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('wjw.jiangsu.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('wjw.nmg.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('wjw.shanxi.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('wst.hainan.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
df.loc[(df['domain'].str.contains('www.hnwsjsw.gov.cn')) & (df['maindo'].isna()),'maindo'] = '各地卫生健康委网站'


df.loc[(df['domain'].str.contains('www.diaoyudao.org.cn')) & (df['maindo'].isna()),'maindo'] = '钓鱼岛官网'
df.loc[(df['domain'].str.contains('www.cusdn.org.cn')) & (df['maindo'].isna()),'maindo'] = '中国城市低碳经济网'
df.loc[(df['domain'].str.contains('news.ceic.ac.cn')) & (df['maindo'].isna()),'maindo'] = '中国地震台网'



df.loc[(df['domain'].str.contains('.gov.cn')) & (df['maindo'].isna()),'maindo'] = '其他网站（政府机构）'
df.loc[(df['domain'].str.contains('.gov.hk')) & (df['maindo'].isna()),'maindo'] = '其他网站（政府机构）'
df.loc[(df['domain'].str.contains('.edu.cn')) & (df['maindo'].isna()),'maindo'] = '高校等教育机构网站'


df.to_sql('ci_reindex_urlt', conn, index=False, if_exists = 'replace')

print(df['maindo'].isna().sum())

#%%



df.loc[df['maindo'].isna(),'maindo'] = '其他网站（待确定）'

#
print(df['maindo'].isna().sum())


#%% 移动端与PC端
df['mobile'] = 0
df.loc[(df['maindo'].str.contains('应用程序|移动端网页版')) & (df['maindo'].notna()),'mobile'] = 1

df['mobile'].sum()

# 合并同一系列的渠道
df['channel'] = df['maindo']
df['channel'] = df['channel'].replace(regex =['\+（应用程序）','（移动端网页版）','（应用程序）','（电子报）','-电子报','-网站','（移动端网页版/应用程序）'], value = '')
schannel = df['channel'].value_counts()

df.to_sql('ci_allnewtime', conn, index=False, if_exists = 'replace')
# df.to_sql('ci_reindex_urlt', conn, index=False, if_exists = 'replace')


#=========2023-03-23补充新闻发布时间============
dfnhc = pd.read_csv('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0322/citation+nhc.csv')

dfwjwadd = dfnhc[['original_url','origin_url','timestamp']]

dfm =  pd.merge(df, dfwjwadd, how='left', on=['original_url'])

dfm['timestamp_x'].replace(regex=['None'], value='',inplace=True)

dfm['timestamp_x'] = dfm['timestamp_x'].combine_first(dfm['timestamp_y'])

dfnewsadd = pd.read_csv('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0322/ci+time+1.csv')

dfm['timestamp_x'] = dfm['timestamp_x'].combine_first(dfnewsadd['timestamp'])

#dfm.index += 1
dfm.to_sql('ci_time', conn, index=False, if_exists = 'replace')


#漏了爬取的时间点，再来
df = pd.read_sql('SELECT * FROM ci_time_hd', conn)
dfnewsadd = pd.read_csv('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0322/ci+time+1.csv')
df['timestamp_x'] = df['timestamp_x'].combine_first(dfnewsadd['timestamp'])

df['domain']=None
for index, row in df.iterrows():
    url = row['origin_url_x']
    if url:
        df.at[index, 'domain'] = urlparse(url).netloc
        
df.loc[df['htmltimestamp'] == '2023-03-23 00:00','htmltimestamp'] = None
df.loc[(df['htmltimestamp'].astype(str).str.contains('01-01 00:00') & (df['htmltimestamp'].astype(str).notna())),'htmltimestamp'] = None 
df.loc[pd.to_datetime(df['htmltimestamp']) > datetime.datetime(2023,1,17,00,00,00),'htmltimestamp'] = None


   
dmli = ['www.jfdaily.com','www.81.cn','www.js7tv.cn','www.cet.com.cn',
        'ie.bjd.com.cn','t.ynet.cn','wsjkw.gd.gov.cn','www.mofcom.gov.cn','www.mod.gov.cn','www.gcs.gov.mo',
        'www.gov.mo', '3g.k.sohu.com','k.sina.com.cn', 'm.bjnews.com.cn','slide.sports.sina','slide.ent.sina.com.cn',
        'cj.sina.com.cn','k.sina.cn','news.hbtv.com.cn','m.voc.com.cn','www.thepaper.cn','m.thepaper.cn','hqtime.huanqiu.com',
        '3w.huanqiu.com','baijiahao.baidu.com','static.cdsb.com','new.qq.com','news.cnhubei.com','photo.wenweipo.com',
        'www.dailyqd.com','www.gd.gov.cn','www.gooood.cn','www.hunantoday.cn','www.ithome.com','www.qlwb.com.cn',
        'www.sport.gov.cn','www.wyzxwk.com','zj.zjol.com.cn','export.shobserver.com','www.sport.gov.cn','www.gd.gov.cn','api3.cls.cn',
        'china.huanqiu.com','ent.ifeng.com','finance.ifeng.com','ishare.ifeng.com','m.sohu.com','news.hnr.cn']

 
orili = ['www.sohu.com/a','www.xinhuanet.com/world','news.ifeng.com/c/']

#将正确无误的htmldate库提取出的时间补到handtime列
for index, row in df.iterrows():
    url = row['origin_url_x']
    domain = row['domain']
    if pd.notna(url) and pd.isna(row['timestamp_x']) and pd.isna(row['org']) and pd.notna(row['htmltimestamp']):
        if any(w in domain for w in dmli):
            df.at[index, 'handtime'] = row['htmltimestamp']
        if any(k in url for k in orili):
            df.at[index, 'handtime'] = row['htmltimestamp']

#dfm.index += 1
df.to_sql('ci_allnewtime', conn, index=False, if_exists = 'replace')

1. 两个白名单
2. 写文字
#%% 合并多个新闻发布日

#列的清理
dfci['handtime'] = dfci['handtime'].replace(regex =['无法访问','NA'], value = pd.NaT) #日期的空值为NaT
dfci['handtime'] = dfci['handtime'].replace(np.NaN, value = pd.NaT)
dfci[['handtime']]= dfci[['handtime']].values.astype(str) #将数据类型转化为str
dfci['handtime'] = pd.to_datetime(dfci['handtime']).dt.date #只保留【年-月-日】

dfci['timestamp_x'] = dfci['timestamp_x'].replace(regex=['超时错误'], value = pd.NaT)
dfci['handtime'] = dfci['handtime'].replace(regex =['无法访问', 'NA'], value = pd.NaT)
# dfci['htmldate_ori'] = dfci['htmldate_ori'].replace(regex=['error'], value = pd.NaT)
# dfci['htmldate_upd'] = dfci['htmldate_upd'].replace(regex=['error'], value = pd.NaT)

#重叠不同源时间:直接复制sourcetime到新列,然后将urltime不为空的值重叠到pubtime一列

dfci1 = pd.read_csv('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0322/ciall拼接pub.csv')

dfci['pub_time'] = dfci1['pub_time']

dfci['pub_time'] = dfci['pub_time'].combine_first(dfci['source_time'])
dfci['pub_time'] = dfci['pub_time'].combine_first(dfci['handtime'])#先重叠手动记录的时间
dfci['pub_time'] = dfci['pub_time'].combine_first(dfci['timestamp_x'])#再重叠爬虫抓的时间
dfci['pub_time'] = dfci['pub_time'].combine_first(dfci['url_time'])#再重叠URL解析的时间

print(dfci.isnull().sum())
dfci.to_csv('ciall拼接pub.csv')
dfci.to_excel('ciall拼接pub_1.xlsx')
#将数据类型转化为时间，统一时间格式为yyyy-mm-dd，然后用减法，

#%清洗整理新闻发布时间戳数据 汉字替换为符号

dfci['pub_time'] = dfci['pub_time'].replace(regex=['来源: '], value='')
dfci['pub_time'] = dfci['pub_time'].replace(regex=['年', '月'], value='-')
dfci['pub_time'] = dfci['pub_time'].replace(regex =[r'[\u4e00-\u9fa5]'], value='')
dfci['pub_time'] = dfci['pub_time'].replace(regex=['\n', '日'], value=' ') 
dfci['pub_time'] = dfci['pub_time'].replace(regex =['：','　www.gov.cn ','【','】','“','”','　:  ',': -  '], value='') 

dfci['pub_time'] = dfci['pub_time'].replace(regex =['-8-'], value='-08-')
dfci['pub_time'] = dfci['pub_time'].replace(regex =['-9-'], value='-09-')
dfci['pub_time'] = dfci['pub_time'].replace(regex =['-1-'], value='-01-')
dfci['pub_time'] = dfci['pub_time'].replace(regex =['-2-'], value='-02-')
dfci['pub_time'] = dfci['pub_time'].replace(regex =['-3-'], value='-03-')

# dfci['pub_time'] = dfci['pub_time'].replace(regex =['-5'], value='-05')
# dfci['pub_time'] = dfci['pub_time'].replace(regex =['-3'], value='-03')
# dfci['pub_time'] = dfci['pub_time'].replace(regex =['-4'], value='-04')
# dfci['pub_time'] = dfci['pub_time'].replace(regex =['-6'], value='-06')
# dfci['pub_time'] = dfci['pub_time'].replace(regex =['-7'], value='-07')
# dfci['pub_time'] = dfci['pub_time'].replace(regex =['-8'], value='-08')
dfci['pub_time'] = dfci['pub_time'].replace(regex =['2017.05.12'], value='2017-05-12')
dfci['pub_time'] = dfci['pub_time'].replace(regex =['　- '], value='')


dfci['cite_time'] = pd.to_datetime(dfci['cite_time']).dt.date
dfci['pub_time'] = pd.to_datetime(dfci['pub_time']).dt.date #dt.date，只保留【年-月-日】
dfci['source_time'] = pd.to_datetime(dfci['source_time']).dt.date

dfci['time_di'] = dfci['cite_time'] - dfci['pub_time']

dfci['time_di'] = dfci['time_di'].map(lambda x:x.days) #计算出天数
#dfc['time_di_d'] = dfc['time_di'] / np.timedelta64(1, 'D') #不知道两种计算天数有何区别
dfci['time_di_d'] = dfci['time_di']

dfci.loc[dfci['time_di']<0,'time_di'] = np.nan #将time_di的负值清洗掉
#将df写入 csv sql

multi_ci = pd.cut(dfci['time_di_d'], bins=[0,1,7,30,365,np.inf], include_lowest=True)
multi_ci_des = dfci['time_di_d'].groupby(multi_ci).describe()

multi_ci_des.to_excel('cite_di_multi_des.xlsx', index=True)

dfci['time_di_d'].describe()
# count    12425.000000
# mean        73.936982
# std        361.210924
# min          0.000000
# 25%          0.000000
# 50%          0.000000
# 75%          1.000000
# max       7760.000000
dfci['time_di_d'][dfci['time_di_d']<7].hist(bins=7)

dfci.to_excel('ciall.xlsx')


#%% 词条汇总引用速度
#按年分组数据
grouptry = dfci.groupby('entry')
grouptrymin = grouptry.min()
grouptrymax = grouptry.max()

grouptrymin['cite_range'] = grouptrymax['cite_time'] - grouptrymin['cite_time']
grouptrymin['cite_range_y'] = grouptrymin['cite_range'] / np.timedelta64(1, 'Y') #引用操作的编辑历史事件跨度：年
grouptrymin.reset_index(inplace=True)
entrycite = grouptrymin[['cite_range','cite_range_y','entry','year']]

grouptrymax.to_excel('entry_cite_max.xlsx',index=True)

# #编辑历史时间跨度，按年分组描述
# gr_des = grouptry.describe()
# gr_des.to_excel('gr_des_2023-02-17.xlsx', index=True)

#每年：词条编辑的起止时间点的平均值
time_di_mean = grouptry.agg({'time_di_d':'mean'})
time_di_mean.reset_index(inplace=True)
evtype = df1[['entry','type']]
time_di_mean = pd.merge(time_di_mean, evtype, how='left', on=['entry'])
time_di_mean = pd.merge(time_di_mean, entrycite, how='left', on=['entry'])

time_di_mean.to_excel('entry_cite_di_range.xlsx',index=True)

time_di_mean['di_days'] = time_di_mean['cite_range_x'].map(lambda x:x.days) 

multi_cirange = pd.cut(time_di_mean['di_days'], bins=[0,30,180,365,1095,1825,np.inf], include_lowest=True)
multi_cirange_des = time_di_mean['di_days'].groupby(multi_cirange).describe()

multi_cirange_des.to_excel('citerange_di_multi_des.xlsx', index=True)
# time_di_mean['di_days'].describe()
# count     257.000000
# mean      766.739300
# std       956.261727
# min         0.000000
# 25%        24.000000
# 50%       317.000000
# 75%      1244.000000
# max      3462.000000
# Name: di_days, dtype: float64

multi_cirange = pd.cut(time_di_mean['cite_range_y_y'], bins=[0,0.083,0.16,0.5,1,2,3,4,5,8,np.inf], include_lowest=True)
multi_cirange_des = time_di_mean['cite_range_y_y'].groupby(multi_cirange).describe()



#所有的词条编辑起止时间均值
df['edi_start'].mean() #Timestamp('2015-11-18 11:51:23.097345024')
df['edi_end'].mean() #Timestamp('2022-04-09 18:35:25.374449408')
alldescribe = df.describe()
alldescribe.to_excel('all_des_2023-02-17-1.xlsx', index=True)


df.to_excel('year_edirange.xlsx',index=True)


#dfci[['pub_time']]= dfci[['pub_time']].values.astype(str) #将数据类型转化为str

# import datefinder


# dfci['finestamp']=pd.NaT

# for index, row in dfci.iterrows():
#     if pd.notna(row['tistamp_cl']) and ':' in row['tistamp_cl']: #剔除timestamp中没有时分的
#         if 'org/zg2016/hbjs/index.html' not in row['origin_url']: #g20官网有几个年份不完整导致识别错误
#             text = row['tistamp_cl']
#         else:
#             text = '20' + row['tistamp_cl'].strip()
#         matches = datefinder.find_dates(text, strict=True)
#         #time=pd.NaT
#         for match in matches:
#             time=match
#         dfci.at[index, 'finestamp'] = time

# # conn1 = sqlite.connect('test.sqlite')
# # dfci.index += 1
# # dfci.to_sql('test', conn1, index=True, if_exists = 'replace')
# # conn1.close()

# dfci.drop(columns=['tistamp_cl','test'],inplace=True)



# conn = sqlite.connect('test2.sqlite')
# df.to_sql('citation', conn, index=True, if_exists = 'replace')
# conn.close() #我不理解怎么只到了这个步骤，英文日期自动变数字了？


#%% 是否政府机构
df['org'] = None

#df.loc[df['maindo'].isna(),'org'] = '缺失'
df.loc[(df['maindo'].str.contains('其他网站（待确定）|中国城市低碳经济网|高校等教育机构网站|中国地震台网|钓鱼岛官网|百度搜索',regex=True))&(df['org'].isna()),'org'] = '其他' 
df.loc[(df['maindo'].str.contains('G20官网|奥委|奥运|国际足联|一带一路|中非合作论坛|世界卫生组织',regex=True))&(df['org'].isna()),'org'] = '跨国合作与国际组织网站' 
df.loc[(df['domain'].str.contains('\.gov\.cn|cdc\.cn',regex=True))&(df['org'].isna()),'org'] = '政府机构网站'
df.loc[(df['domain'].str.contains('www.baidu.com'))&(df['org'].isna()),'org'] = '搜索引擎'



smissingorg = df['channel'].loc[df['org'].isna()].value_counts()

df.loc[df['org'].isna(),'org'] = '门户网站与新闻平台' #微博都是官方账号


#df.loc[(df['domain'].str.contains('.gov.cn'))&(df['org'].isna()),'org'] = '新闻平台（含公众账号）'


# nodo = df[df['maindo'].isna()]
# nodo.to_csv("未映射域名632条.csv", index=True)
dfci.to_excel('citation.xlsx',index=True)


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

