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

##处理表格




os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0127补齐sourcetime')

df = pd.read_csv('citation.csv', index_col='Unnamed: 0')

#新建列聚合网页等渠道
df['maindo'] = None

df.loc[(df['domain'].str.contains('ifeng.')) & (df['maindo'].isna()),'maindo'] = '凤凰网'
df.loc[(df['domain'].str.contains('163.')) & (df['maindo'].isna()),'maindo'] = '网易网'
df.loc[(df['origin_url'].str.contains('sinawap')) & (df['maindo'].isna()),'maindo'] = '新浪新闻（应用程序）'
df.loc[(df['domain'].str.contains('sina.')) & (df['maindo'].isna()),'maindo'] = '新浪网'
df.loc[(df['domain'].str.contains('weixin.')) & (df['maindo'].isna()),'maindo'] = '微信公众号平台'

df.loc[(df['domain'].str.contains('view.inews.qq')) & (df['maindo'].isna()),'maindo'] = '腾讯新闻（应用程序）'
df.loc[(df['domain'].str.contains('qq.')) & (df['maindo'].isna()),'maindo'] = '腾讯网'

df.loc[(df['domain'].str.contains('sohu.')) & (df['maindo'].isna()),'maindo'] = '搜狐网'
df.loc[(df['domain'].str.contains('jiemian.')) & (df['maindo'].isna()),'maindo'] = '界面新闻'
df.loc[(df['domain'].str.contains('baijiahao.baidu')) & (df['maindo'].isna()),'maindo'] = '百度百家号'
df.loc[(df['domain'].str.contains('mbd.baidu')) & (df['maindo'].isna()),'maindo'] = '百度百家号(移动端)'#注，本研究中的均是百家好

df.loc[(df['domain'].str.contains('.')) & (df['maindo'].isna()),'maindo'] = '界面新闻'

df.loc[(df['domain'].str.contains('m.thepaper.')) & (df['maindo'].isna()),'maindo'] = '澎湃新闻（移动端）'
df.loc[(df['domain'].str.contains('thepaper.')) & (df['maindo'].isna()),'maindo'] = '澎湃新闻'

df.loc[(df['domain'].str.contains('xhpfmapi')) & (df['maindo'].isna()),'maindo'] = '新华社（应用程序）'
df.loc[(df['domain'].str.contains('.xinhuanet.')) & (df['maindo'].isna()),'maindo'] = '新华网'
df.loc[(df['domain']=='www.news.cn') & (df['maindo'].isna()),'maindo'] = '新华网'
df.loc[(df['domain']=='education.news.cn') & (df['maindo'].isna()),'maindo'] = '新华网'
df.loc[(df['domain']=='m.news.cn') & (df['maindo'].isna()),'maindo'] = '新华网（移动端）'

df.loc[(df['domain'].str.contains('content-static.cctvnews')) & (df['maindo'].isna()),'maindo'] = '中央广播电视总台-央视新闻（应用程序）'
df.loc[(df['domain']=='app.cctv.com') & (df['maindo'].isna()),'maindo'] = '中央广播电视总台-央视新闻（应用程序）'
df.loc[(df['domain'].str.contains('m.news.cctv')) & (df['maindo'].isna()),'maindo'] = '央视网（移动端）'
df.loc[(df['domain'].str.contains('cntv.com')) & (df['maindo'].isna()),'maindo'] = '央视网'
df.loc[(df['domain'].str.contains('cctv.com')) & (df['maindo'].isna()),'maindo'] = '央视网'
df.loc[(df['domain'].str.contains('.cnr.cn')) & (df['maindo'].isna()),'maindo'] = '央广网'

df.loc[(df['domain']=='bj.bjd.com.cn') & (df['maindo'].isna()),'maindo'] = '北京日报（应用程序）'
df.loc[(df['domain']=='ie.bjd.com.cn') & (df['maindo'].isna()),'maindo'] = '北京日报（应用程序）'
df.loc[(df['domain'].str.contains('bjd.com.cn')) & (df['maindo'].isna()),'maindo'] = '北京日报网'
df.loc[(df['domain'].str.contains('m.haiwainet')) & (df['maindo'].isna()),'maindo'] = '海外网（移动端）'
df.loc[(df['domain'].str.contains('haiwainet.cn')) & (df['maindo'].isna()),'maindo'] = '海外网'

df.loc[(df['domain'].str.contains('m.chinanews')) & (df['maindo'].isna()),'maindo'] = '中国新闻网（应用程序）'
df.loc[(df['domain'].str.contains('chinanews.')) & (df['maindo'].isna()),'maindo'] = '中国新闻网'

df.loc[(df['domain'].str.contains('m.gmw.')) & (df['maindo'].isna()),'maindo'] = '光明网（移动端）'
df.loc[(df['domain'].str.contains('m.people.cn')) & (df['maindo'].isna()),'maindo'] = '人民网（移动端）'
df.loc[(df['domain'].str.contains('app.people.cn')) & (df['maindo'].isna()),'maindo'] = '人民网+（应用程序）'

df.loc[(df['domain'].str.contains('m.huanqiu')) & (df['maindo'].isna()),'maindo'] = '环球网（移动端）'
df.loc[(df['domain'].str.contains('hqtime.')) & (df['maindo'].isna()),'maindo'] = '环球时报（应用程序）'
df.loc[(df['domain'].str.contains('huanqiu')) & (df['maindo'].isna()),'maindo'] = '环球网'

3w.huanqiu 是个啥 https://3w.huanqiu.com/a/24d596/48NJJN9tgG4

有无移动端
df.loc[(df['domain'].str.contains('www.ce.cn')) & (df['maindo'].isna()),'maindo'] = '中国经济网'


政府
df.loc[(df['domain'].str.contains('.nhc.gov')) & (df['maindo'].isna()),'maindo'] = '中华人民共和国国家卫生健康委员会网站'
www.gov.cn 中华人民共和国中央人民政府网站


