#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 16:54:28 2023

@author: zhangsiqi
"""
#%% 分正负数 事件类型 描述创建时间差 2023-02-15
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

df.create_range = pd.NaT
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

#按照正负数分别画直方图看看
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

#%%编辑数量 历史跨度 时间动态 2023-02-17
import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re
from datetime import datetime
import matplotlib.pyplot as plt

import seaborn as sns
plt.rc('font',family='Times New Roman')
#提高行内plot显示清晰度
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')


dfall = pd.read_excel('events+timestamp+evtype+range.xlsx')

#去除拉伸开始时间的词条
df = dfall[pd.isna(dfall['del_edi_range'])]

#又是历久弥新的时间格式转换
df.edi_start = pd.to_datetime(df['edi_start'])
df.edi_end = pd.to_datetime(df['edi_end'])

df.edi_range = pd.NaT
df.edi_range = df['edi_end'] - df['edi_start']
df.edi_range = pd.to_timedelta(df['edi_range'])

df['edi_range_y'] = df['edi_range'] / np.timedelta64(1, 'Y')

#词条年均的编辑数量
df['edi_by_year'] = df['editcount']/df['edi_range_y']

#按年分组
grouped = df.groupby('year')

#编辑历史时间跨度，整体描述
gr_des = grouped.describe()
gr_des.to_excel('gr_des_2023-02-17.xlsx', index=True)

#词条编辑起止时间平均值
edi_end_mean = grouped.agg({'edi_start':'mean','edi_end':'mean'})
edi_end_mean.to_excel('edi_end_mean_023-02-17-1.xlsx',sheet_name='test_new',index=True)


#所有的词条编辑起止时间均值
df['edi_start'].mean() #Timestamp('2015-11-18 11:51:23.097345024')
df['edi_end'].mean() #Timestamp('2022-04-09 18:35:25.374449408')
alldescribe = df.describe()
alldescribe.to_excel('all_des_2023-02-17-1.xlsx', index=True)


df.to_excel('year_edirange.xlsx',index=True)


multic = pd.cut(df['edi_by_year'], bins=[0,1,6,12,24,36,np.inf])
multigr3_des = df['edi_by_year'].groupby(multic).describe()
multigr3_des.to_excel('edibyyear_multi_des.xlsx', index=True)


grtime = df.groupby(multic)
for name, gr in grtime:
    print(name)
    print(gr['entry'][1:15])

timegr1 = grtime.get_group('(0.0, 1.0]')


# 写入已有Excel文件的新表单
# writer = pd.ExcelWriter('model_predict.xlsx',mode='a', engine='openpyxl',if_sheet_exists='new')
# df.to_excel(writer, sheet_name='sheet1')
# writer.save()
# writer.close()
#每年度的时间跨度箱图，只差注释
df.boxplot(column='edi_range_y',by='year',figsize=(7,4.45)).get_figure().savefig('box2023-02-17.png',dpi=300,bbox_inches='tight')

#词条年均的编辑数量箱图
df.boxplot(column='edi_by_year',by='year',figsize=(7,4.45)).get_figure().savefig('box-evry2023-02-17.png',dpi=300,bbox_inches='tight')

dfediy = df[df['edi_by_year']<40] #每年编辑次数少于40
dfediy.boxplot(column='edi_by_year',by='year',figsize=(7,4.45)).get_figure().savefig('box1-evry2023-02-17.png',dpi=300,bbox_inches='tight')

#直方图
dfediy.edi_by_year.hist(bins=36)
dfediy['edi_by_year'][dfediy.edi_by_year<1].count() #16个

#动态分布 热力图
dfedi = pd.read_csv('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0214补充词条数据/edithistory02-14-14-25sql.csv')
dfedi.update_time = pd.to_datetime(dfedi['update_time'])

dfedi["Year"] = dfedi['update_time'].dt.year.astype(int)
dfedi["Month"] = dfedi['update_time'].dt.month.astype(int)

#按年月两个维度进行数据透视
entrygr = dfedi.groupby('entry')

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/图表输出/热力图')

maxli = []

i=1
for name, group in entrygr:
    htable = group.groupby(["Year", "Month"]).agg({'entry':'count'})
    htable1 = htable.pivot_table(index='Year', columns='Month', values='entry').fillna(0).astype(int)
    maxcount = np.max(np.array(htable1))
    #maxli.append(np.max(np.array(htable1)))
    
    f, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(data=htable1,cmap="Blues",square=True,
                annot=True,
                #vmin=0, vmax=231, #这个最大值是遍历找出来的
                annot_kws={"fontsize":10},
                fmt='.3g', #显示完整三位数标注
                linewidths=1,ax=ax) #sns.set_context({"figure.figsize":(8,8)})
    ax.set_xlabel("Month",fontsize=15)
    ax.set_ylabel("Year",fontsize=15)
    ax.tick_params(axis='both', which='both', length=0) #短横线（tick）好丑，去掉
    ax.xaxis.tick_top()
    plt.yticks(size = 11)
    plt.xticks(size = 11)
    for t in ax.texts:
        if float(t.get_text())>0:
            t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
        else:
            t.set_text("") # if not it sets an empty text
    eid = group['event_id'].iloc[0] #取出事件id
    filename = str(eid) +' - ' + name+'.png'
    plt.savefig(filename,dpi=300,bbox_inches='tight')
    #plt.show()
    print(filename)
    i+=1
    # if i > 30:
    #     break
#print('月最大值是',max(maxli))
#最大数分布
maxdata = pd.DataFrame(maxli, columns = ['a'])
maxdata.a.value_counts()

#按年一个维度进行数据透视
entrygr = dfedi.groupby('entry')

for name, group in entrygr:
    htable = group.groupby("Year").agg({'entry':'count'})
    htable1 = htable.pivot_table(index='Year', columns='Month', values='entry').fillna(0).astype(int)
    sns.set_context({"figure.figsize":(8,8)})
    #sns.heatmap(data=htable1,square=True)
    sns.heatmap(data=htable1,cmap="Blues",square=True)
    
    print(name)




#pandas success
year_edi_range = table.plot.hist(subplots=True, layout=(4, 3),
                                  figsize=(20,26),sharex=False,
                                  fontsize=20)


#
multi = pd.cut(dfediy['edi_by_year'], bins=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,np.inf])
multigr_des = dfediy['edi_by_year'].groupby(multi).describe()

multia = pd.cut(dfediy['edi_by_year'], bins=[0,1,2,4,6,8,12,24,np.inf])
multigr1_des = dfediy['edi_by_year'].groupby(multia).describe()

multib = pd.cut(dfediy['edi_by_year'], bins=[0,1,6,12,24,np.inf])
multigr2_des = dfediy['edi_by_year'].groupby(multib).describe()

multigr2_des.to_excel('edibyyear_multi_des.xlsx', index=True)
#%% 参考资料的引用速度 2023-02-18
import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re
from datetime import datetime
import matplotlib.pyplot as plt

import seaborn as sns
plt.rc('font',family='Times New Roman')
#提高行内plot显示清晰度
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')

os.chdir('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0217')
dfc = pd.read_csv('ci初稿.csv')
evci = dfc.groupby('entry').describe()

allcides = evci['reference_count'].describe()
allcides.to_excel('allci_des.xlsx',index=True)

#又是历久弥新的时间格式转换
dfc.cite_time = dfc['cite_time'].replace(regex =['日期2020-6-6'], value = '2020-06-06')
dfc.pub_time = pd.to_datetime(dfc['pub_time'])
dfc.cite_time = pd.to_datetime(dfc['cite_time'])
dfc.one_citime = pd.to_datetime(dfc['one_citime'])
dfc.finestamp = pd.to_datetime(dfc['finestamp'])


dfc.time_di = pd.NaT
dfc.time_di = dfc['cite_time'] - dfc['pub_time']
dfc.time_di = pd.to_timedelta(dfc['time_di'])

dfc.time_di = dfc['time_di'].replace(regex =['日期2020-6-6'], value = '2020-06-06')

dfc['fine_di'] = dfc['one_citime'] - dfc['finestamp']
dfc.fine_di = pd.to_timedelta(dfc['fine_di'])

dfc['fine_di_d'] = dfc['fine_di'] / np.timedelta64(1, 'D')
dfc['time_di_d'] = dfc['time_di'] / np.timedelta64(1, 'D')

dfc.loc[dfc['time_di_d']<0,'time_di_d'] = np.nan

multi_ci = pd.cut(dfc['time_di_d'], bins=[0,1,7,30,365,np.inf], include_lowest=True)
multi_ci_des = dfc['time_di_d'].groupby(multi_ci).describe()

multi_ci_des.to_excel('citedi_multi_des.xlsx', index=True)

dfc['time_di_d'].describe()
# count    4985.000000
# mean      133.412839
# std       456.468312
# min         0.000000
# 25%         0.000000
# 50%         0.000000
# 75%         3.000000
# max      5235.000000
dfc['time_di_d'][dfc['time_di_d']<7].hist(bins=7)


dfc.boxplot(column=('time_di_d'))


#%% 还画了自己觉得很炫酷的11个编辑历史跨度的子直方图
import matplotlib.pyplot as plt
plt.rc('font',family='Times New Roman')
#编辑历史数据透视表
table = df.pivot_table(index='entryindex',columns='year',values='edi_range_y')

#pandas success
year_edi_range = table.plot.hist(subplots=True, layout=(4, 3),
                                  figsize=(20,26),sharex=False,
                                  fontsize=20,grid=True)

#(1)上面等价于table.plot(kind='hist', ....)
#（2）legend显得很小，因为figsize很大，如果figsize设置为(9,12)或者（10，13.5），legend大小很舒服

#我搞不懂啊，为什么下面这样取出来的是一整张图，这不是取的第一个和第6个子图吗？通过测试证明，里面数字怎么取都不影响
year_edi_range[0,0].get_figure().savefig('name+3',dpi=300,bbox_inches='tight')
year_edi_range[2,2].get_figure().savefig('[2+2]',dpi=300,bbox_inches='tight')

#继续整活、学习ax的


ax = table.plot(subplots=True, kind='hist', grid=True, legend=True, stacked=False, 
           sharex=True, sharey=True, figsize=(9,12),
           layout=(4,3))

ax.set_title('5 plots')#这样会报错：'numpy.ndarray' object has no attribute 'set_title'

plt.title('5 plots') #一个大空白图有了标题5 plots

ax[0,0].set_title('5 plots') #这样也不会有任何的标题显示出来

fig = ax[0,0].get_figure() 
#然后在控制窗口直接输入fig回车查看，能看到标题在左上角,也即第一个子图
fig1 = ax[3,1].get_figure() 
#同样在控制行查看，标题也在左上角
fig2 = ax[2,2].get_figure() 
#同样操作结果依然标题左上角

#查看每个figure的axes，结果一模一样
fig.get_axes()
fig1.get_axes()
fig2.get_axes()

ax[3,2].set_title('5 plots') 
#控制台 直接 ax 查看，这样给最后一个子图增加了标题

fig, axes = plt.subplots(4,3)

test = table.plot(subplots=True, kind='hist', grid=True, legend=True, stacked=False, 
           sharex=True, sharey=True, figsize=(9,12),
           layout=(4,3),ax=axes) #test是数组，axes不是数组

axes.set_ylabel('tets')
axes.set_title('whither +++ plots')

test[2,1].set_title('5 plots')
fig.suptitle('Errorbar subsampling') #这样又有一个顶端的大标题了
axes.get_title() #输出whither plots，不懂它去哪里了

#此时控制台axes:<AxesSubplot:title={'center':'whither +++ plots'}>
#此时控制台fig：一张图没有whither的title

axes.figure #也没有whither的title

fig.get_axes() #也没有显示哪个subplot有whither plot这个标题

plt.show()

#%%matplot绘制多个箱形图，没有pandas好看
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



#%% matplotlib不可见式画图
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

#%%初识matplotlib
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


#%% 同时叠加所有事件的时间线图，时间太多，图很丑
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
        



