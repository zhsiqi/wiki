#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 16:35:04 2023

@author: zhangsiqi
提取URL中的年月日和域名
已完成，超快的运行时间
"""
import re
from urllib.parse import urlparse
import pandas as pd

#大部分正确但极个别不适用，还是分开写比较合适
#m = re.search(r'/(?P<year>(20)?[0-2][0-9])[/-]?(?P<month>[0-1]?[0-9])[/-]?(?P<date>[0-3]?[0-9])?/(t(?P<all>20\d{6})_)?', url)

#https://www.guancha.cn/SongLuZheng/2017_08_31_425112.shtml
#https://view.inews.qq.com/k/20220310A04PC100?web_channel=wap&openApp=false
#https://view.inews.qq.com/a/NEW2021051000405401?uid=&devid=60968872-C4D0-4028-B806-4AFE70C19325&qimei=60968872-c4d0-4028-b806-4afe70c19325


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
        return date, 'm1匹配'
    if m0:
        #print(m0.group())
        date = m0.groupdict()['all'][:4] +'-'+ m0.groupdict()['all'][4:6] +'-'+ m0.groupdict()['all'][6:8]
        return date, 'm0匹配'
    if m2:
        date = m2.groupdict()['year']+'-'+ m2.groupdict()['month']+'-'+ m2.groupdict()['date']
        return date, 'm2匹配'
    if m3:
        date = '20'+m3.groupdict()['year']+'-'+ m3.groupdict()['month']+'-'+ m3.groupdict()['date']
        return date, 'm3匹配'
    if m4:
        date = m4.groupdict()['year']+'-'+ m4.groupdict()['month']+'-'+ m4.groupdict()['date']
        return date, 'm4匹配'
    if m1 == None and m0 == None and m2 == None and m3 == None and m4 == None:
        return None, '都不匹配'




url0 = 'https://www.chinacdc.cn/jkzt/crb/zl/szkb_11803/jszl_11809/202212/t20221225_263104.html'
url1 = 'http://news.xinhuanet.com/2011-04/22/c_121336202.htm' #bug
url2 = 'https://news.haiwainet.cn/n/2022/0311/c3541093-32362152.html'
url3 = 'http://news.xinhuanet.com/politics/2012-03/03/c_111596840.htm' #bug
url4 = 'http://henan.163.com/12/0810/10/88HQPPG20227019U.html'
url5 = 'http://henan.163.com/2019/03-12/test.html' #bug
url6 = 'http://henan.163.com/2019-03-31/test.html' #bug
url7 = 'https://xian.qq.com/a/20110310/000409.htm'
url8 = 'https://wjw.fujian.gov.cn/ztzl/gzbufk/yqtb/202205/t20220528_5921301.htm'
url9 = 'http://www.gongyishibao.com/News/2011-7/139342.aspx'
url10 = 'https://ent.sina.com.cn/s/m/2021-01-19/doc-ikftssan8334372.shtml'
url11 = 'http://www.xinhuanet.com/talking/20170510a/'
url12 = 'https://view.inews.qq.com/k/20220310A04PC100?web_channel=wap&openApp=false'
url13 = 'https://view.inews.qq.com/a/NEW2021051000405401?uid=&devid=60968872-C4D0-4028-B806-4AFE70C19325&qimei=60968872-c4d0-4028-b806-4afe70c19325'

print(get_pubtime_by_url(url0))
print(get_pubtime_by_url(url1))
print(get_pubtime_by_url(url2))
print(get_pubtime_by_url(url3))
print(get_pubtime_by_url(url4))
print(get_pubtime_by_url(url5))
print(get_pubtime_by_url(url6))
print(get_pubtime_by_url(url7))
print(get_pubtime_by_url(url8))
print(get_pubtime_by_url(url9))
print(get_pubtime_by_url(url10))
print(get_pubtime_by_url(url11))
print(get_pubtime_by_url(url12))
print(get_pubtime_by_url(url13))


# domain

df = pd.read_csv('0116成功结果/citation+code.csv',index_col=('Unnamed: 0'))

for index, row in df.iterrows():
    url = row['origin_url']
    if pd.isna(url) == False:
        domain = urlparse(url).netloc
        urlpath = urlparse(url).path
        date = get_pubtime_by_url(urlpath)
        print(index, domain, url, date)



