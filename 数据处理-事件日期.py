#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:59:40 2023

@author: zhangsiqi
"""
#%% 测试网友代码从文本中提取时间
testtext = """2008年中国南方雪灾是指自2008年1月3日起在中国发生的大范围低温、雨雪、冰冻等自然灾害。中国的上海、江苏、浙江、安徽、江西、河南、湖北、湖南、广东、广西、重庆、四川、贵州、云南、陕西、甘肃、青海、宁夏、新疆等20个省（区、市）均不同程度受到低温、雨雪、冰冻灾害影响。截至2月24日，因灾死亡129人，失踪4人，紧急转移安置166万人；农作物受灾面积1.78亿亩，成灾8764万亩，绝收2536万亩；倒塌房屋48.5万间，损坏房屋168.6万间；因灾直接经济损失1516.5亿元人民币。森林受损面积近2.79亿亩，3万只国家重点保护野生动物在雪灾中冻死或冻伤；受灾人口已超过1亿。其中安徽、江西、湖北、湖南、广西、四川和贵州等7个省份受灾最为严重。
中国国家气象部门的专家指出，这次大范围的雨雪过程应归因于与拉尼娜（反圣婴）现象有关的大气环流异常：环流自1月起长期经向分布使冷空气活动频繁，同时副热带高压偏强、南支槽活跃，源自南方的暖湿空气与北方的冷空气在长江中下游地区交汇，形成强烈降水。大气环流的稳定使雨雪天气持续，最终酿成这次雪灾。
北京：京呼航班全线延误首都机场因呼市突降大雪机场关闭，21日飞往呼和浩特共11趟航班全部延误，下午6时，所有航班的起飞时间都改在晚8时以后，但工作人员称，即使到了八点也不见得能够起飞。此外，北京飞往内蒙锡林浩特航班已经取消。铁路方面，北京西站候车大厅状况与往年春运期间无太多异常，未有旅客大面积滞留，大多列车可以准点出发，个别一两趟出现短时间晚点。
湖北：死亡人数升至14人据统计，湖北省积雪天数已达10天，为24年来之首，因灾死亡人数上升至14人，直接经济损失超过14亿元人民币，而雨雪天气将持续至25日。受暴雪天气影响，湖北省内九条高速公路中有五条再次关闭，但京珠高速已恢复运行。省客运集团有关负责人介绍，迄今为止由武汉发往全国各地的长途客运班车已有8800余次停运。天河机场亦有20余航班延误。截至20日，武汉市公安交通管理局122交通指挥中心共接到交通报警13199起。另外，武汉市中心城区多处水管冻裂，许多居民出现用水困难。至20日上午9时，全市24小时内共接到投诉1904起，直接停水754起，供水管网21日共发生两起800毫米主干管爆裂事故。"""

testtext = """2011年10月13日下午5点30分，广东佛山南海黄岐的广佛五金城里，2岁女童小悦悦在过马路时不慎被一辆面包车撞倒并两度碾压，随后肇事车辆逃逸，随后开来的另一辆车辆直接从已经被碾压过的女童身上再次开了过去，七分钟内在女童身边经过的十几个路人，都对此冷眼漠视，只有最后一名拾荒阿姨陈贤妹上前施以援手，由此引发网友广泛热议。2011年10月21日，小悦悦经医院全力抢救无效，于0时32分离世。2011年10月24日上午，广东佛山南海区检察院称已批准逮捕小悦悦碾压案嫌疑人。"""

import re
import chardet
from datetime import datetime,timedelta


# 匹配正则表达式
matchs = {
    1:(r'\d{4}%s\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s\d{1,2}%s','%%Y%s%%m%s%%d%s %%H%s%%M%s%%S%s'),
    2:(r'\d{4}%s\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s','%%Y%s%%m%s%%d%s %%H%s%%M%s'),
    3:(r'\d{4}%s\d{1,2}%s\d{1,2}%s \d{1,2}%s','%%Y%s%%m%s%%d%s %%H%s'),
    4:(r'\d{4}%s\d{1,2}%s\d{1,2}%s','%%Y%s%%m%s%%d%s'),
    5:(r'\d{2}%s\d{1,2}%s\d{1,2}%s','%%y%s%%m%s%%d%s'),
   
    # 没有年份
    6:(r'\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s\d{1,2}%s','%%m%s%%d%s %%H%s%%M%s%%S%s'),
    7:(r'\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s','%%m%s%%d%s %%H%s%%M%s'),
    8:(r'\d{1,2}%s\d{1,2}%s \d{1,2}%s','%%m%s%%d%s %%H%s'),
    9:(r'\d{1,2}%s\d{1,2}%s','%%m%s%%d%s'),

    # 没有年和月，20日上午9时23分06秒，20日上午9时23分，20日上午9时,21日，
    10:(r'\d{1,2}%s \d{1,2}%s\d{1,2}%s\d{1,2}%s','%%d%s %%H%s%%M%s%%S%s'), 
    11:(r'\d{1,2}%s \d{1,2}%s\d{1,2}%s','%%d%s %%H%s%%M%s'),
    12:(r'\d{1,2}%s \d{1,2}%s','%%d%s %%H%s'),
    13:(r'\d{1,2}%s','%%d%s'),
    
    # # 没有年月日
    # 14:(r'\d{1,2}%s\d{1,2}%s\d{1,2}%s','%%H%s%%M%s%%S%s'),
    # 15:(r'\d{1,2}%s\d{1,2}%s','%%H%s%%M%s'),
}

# 正则中的%s分割
splits = [
    {1:[('年','月','日','时','分','秒'),('年','月','日','点','分','秒'),
        ('年','月','日早上','时','分','秒'),('年','月','日早上','点','分','秒'),
        ('年','月','日上午','时','分','秒'),('年','月','日上午','点','分','秒'),
        ('年','月','日下午','时','分','秒'),('年','月','日下午','点','分','秒'),
        ('年','月','日晚上','时','分','秒'),('年','月','日晚上','点','分','秒'),
        ('年','月','日凌晨','时','分','秒'),('年','月','日凌晨','点','分','秒'),
        ('年','月','日晚','时','分','秒'),('年','月','日晚','点','分','秒'),
        ('-','-','',':',':',''),('\/','\/','',':',':',''),('\.','\.','',':',':','')]},
    {2:[('年','月','日','时','分'),('年','月','日','点','分'),
        ('年','月','日早上','时','分'),('年','月','日早上','点','分'),
        ('年','月','日上午','时','分'),('年','月','日上午','点','分'),
        ('年','月','日下午','时','分'),('年','月','日下午','点','分'),
        ('年','月','日晚','时','分'),('年','月','日晚','点','分'),
        ('年','月','日晚上','时','分'),('年','月','日晚上','点','分'),
        ('年','月','日凌晨','时','分'),('年','月','日凌晨','点','分'),
        ('-','-','',':',''),('\/','\/','',':',''),('\.','\.','',':','')]},
    {3:[('年','月','日','时'),('年','月','日','点'),('-','-','',':'),('\/','\/','',':'),('\.','\.','',':')]},
    {4:[('年','月','日'),('-','-',''),('\/','\/',''),('\.','\.','')]},
    {5:[('年','月','日'),('-','-',''),('\/','\/',''),('\.','\.','')]},

    {6:[('月','日','时','分','秒'),('月','日','点','分','秒'),('-','',':',':',''),('\/','',':',':',''),('\.','',':',':','')]},
    {7:[('月','日','时','分'),('月','日','点','分'),('-','',':',''),('\/','',':',''),('\.','',':','')]},
    {8:[('月','日','时'),('月','日','点'),('-','',':'),('\/','',':'),('\.','',':')]},
    {9:[('月','日'),('-',''),('\/',''),('\.','')]},
    
    {10:[('日','时','分','秒'),('日','点','分','秒'),('',':',':','')]},
    {11:[('日','时','分'),('日','点','分'),('',':','')]},
    {12:[('日','时'),('日','点')]},
    {13:[('日')]},
    
    # {14:[('点','分','秒'),(':',':','')]},
    # {15:[('点','分'),(':','')]},
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
    timefinder = TimeFinder(base_date='2011-01-01 00:00:00')
    #or text in testtext:
    res = timefinder.find_time(testtext)
    #print('text----',testtext)
    print('res',res)

if __name__ == '__main__':
    test()


#%%

import re
import pandas as pd
import numpy as np
import os
import datefinder
import sqlite3 as sqlite
import datetime
import time

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0204删除多余疫情')
df = pd.read_csv('wikitextsql.csv')
dfev = pd.read_csv('eventssql.csv', index_col='Unnamed: 0')

df['date_strict'] = pd.NaT
df['withmon'] = pd.NaT
df['date_more'] = pd.NaT

df['text_copy'] = df['wiki_text'].replace(regex =['-','小时','0—24时','0时—24时'], value = 'interval ')
#df['text_copy'] = df['text_copy'].replace(to_replace =r'\d+(\.\d+)万|亿|公|千|米', value = 'interval ', regex=True)

df['text_copy'] = df['text_copy'].replace(to_replace =r'次年\d+月', value = 'interval ', regex=True)
df['text_copy'] = df['text_copy'].replace(to_replace =r'\d+年\d+个多?月', value = 'interval ', regex=True)

df['text_copy'] = df['text_copy'].replace(to_replace =r'\d+(\.\d+)([\u4e00-\u9fa5]|\u3002|\uff1b|\uff0c|\uff1a|\u201c|\u201d|\uff08|\uff09|\u3001|\uff1f|\u300a|\u300b)', value = 'interval ', regex=True)
df['text_copy'] = df['text_copy'].replace(to_replace =r'\d+月(底|上旬|中旬|下旬|末|初|\u3002|\uff1b|\uff0c|\uff1a|\u201c|\u201d|\uff08|\uff09|\u3001|\uff1f|\u300a|\u300b)', value = 'interval ', regex=True)
df['text_copy'] = df['text_copy'].replace(regex =['年','月'], value = '-')

df['text_copy'] = df['text_copy'].replace(to_replace =r'(上午|早上|早|凌晨)(\d+)(点|时)[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]', value = r'\2:00am ', regex=True)
df['text_copy'] = df['text_copy'].replace(to_replace =r'(下午|中午|晚上|晚)(\d+)(点|时)[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]', value = r'\2:00pm ', regex=True)

df['text_copy'] = df['text_copy'].replace(to_replace = r'(下午|晚上|晚|夜)(\d+)(点|时)(\d+)分?', value = r'\2:\4pm', regex=True)
df['text_copy'] = df['text_copy'].replace(to_replace = r'(上午|早上|早|凌晨)(\d+)(点|时)(\d+)分?', value = r'\2:\4am', regex=True)

df['text_copy'] = df['text_copy'].replace(regex =['点','时','分'], value = ':')
df['text_copy'] = df['text_copy'].replace(regex =['秒','日'], value = ' ')

for index, row in dfev.iterrows():
#for index, row in df[0:50].iterrows():
    year = row['year']
    #base_time = datetime.datetime(year,1,1)
    df_wev = df[df['entry'] == row['entry']]
    for windex, wrow in df_wev.iterrows(): 
        if pd.notna(wrow['text_copy']):
            text = wrow['text_copy']
            matches = datefinder.find_dates(text, strict=True)
            timeli = []
            for match in matches:
                if match.year < 2024 and match.year > 2000:
                    timeli.append(str(match))
                    #base_time = match
            df_wev.at[windex,'date_strict'] = str(timeli)
            
            matches_blur = datefinder.find_dates(text, source=True)
            origin_timeli = []
            for match in matches_blur:
                b = match[1]
                origin_timeli.append(b)
            withm = [i for i in origin_timeli if '-' in i]
            df_wev.at[windex,'withmon'] = str(withm)
            
    df.loc[df['entry'] == row['entry'],'date_strict'] = df_wev['date_strict']
    df.loc[df['entry'] == row['entry'],'withmon'] = df_wev['withmon']


conn3= sqlite.connect('wikitexttime-base.sqlite')
df.to_sql('wikitexttime', conn3, index=True, if_exists = 'replace')
conn3.close()




#if match.year > 1999

#%%
import datefinder
import re
from zhon.hanzi import punctuation


text = '2011-8-8 20:30:05 thus gygsYu gysd  gcdysg 9-9 '
text = '钱云会（1957年10月13日-2010年12月25日)男，汉族，浙江省温州市乐清市蒲岐镇寨桥村人，2005年当选村主任后，因土地纠纷问题带领村民上访。在5年的上访过程中，先后3次被投入看守所。2010年12月25日上午9时，被工程车撞死。有网友爆料，钱云会是被“有些人故意害死的”，乐清市公安局在随后的发布会上称，这是一起交通肇事事故，钱云会当时撑一把雨伞从右侧向左侧横穿马路，工程车紧急刹车但仍与死者发生碰撞，造成钱云会当场死亡。2011年1月29日，据报道公安机关已查获了钱云会出事当天所戴的附有微录设备的手表。'
#text = '《铁路旅客意外伤害强制保险条例》规定每个人赔付两万元保险金额；发生死亡的情况下，《铁路交通事故应急救援和调查处理条例》规定，旅客人身伤亡赔偿限额为，行李损失赔偿限额为。三项相加的上限应该是。事故给出的赔偿91.5万突破了这样的数额。中国人民大学等机构召开了研讨会，探讨事故赔偿的法律问题，也有学者撰文对赔偿问题提出意见。'
text = '2011年10月13日下午5点30分'

#df['text_copy'] = df['text_copy'].replace(to_replace =r'(上午|早上|早|凌晨)\d(点|时)[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]', value = ':', regex=True)

text = re.sub(r'\d+(\.?\d+)万|亿|元|美元|%', 'interval ', text)
text = re.sub(r'-', 'interval ', text)
text = re.sub(r'(上午|早上|早|凌晨)(\d)(点|时)[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]',r'\2:00am ',text)

text = re.sub(r'(下午|晚上|晚|夜)(\d)(点|时)[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]',r'\2:00pm ',text)

text = re.sub(r'(下午|晚上|晚|夜)(\d+)(点|时)(\d+)',r'\2:\4 pm',text)
text = re.sub(r'小时', 'interval', text)
text = re.sub(r'年|月', '-', text)
text = re.sub(r'点|时|分', ':', text)
text = re.sub(r'秒|日', ' ', text)


matches = datefinder.find_dates(text,source=True)

for match in matches:
    print(match)

#%%
import datetime
import time

timestr = '1991-02-07 00:00:00'

date_time = datetime.datetime.strptime(timestr,'%Y-%m-%d %H:%M:%S')
time_time = time.mktime(date_time.timetuple())




