#%% 画图(时间趋势\)
import pandas as pd 
import numpy as np

df = pd.read_csv('/Users/zhangsiqi/Desktop/毕业论文代码mini/专门输出数据表/0210补充事件时间/events+timestamp+evtype.csv',index_col=0)
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

#透视表
table = df.pivot_table(index='entryindex',columns='year',values='edi_range_y')


#pandas success

plott=table.plot(subplots=True, kind='hist', grid=True, legend=True, stacked=False, 
           sharex=True, sharey=True, 
           layout=(4,3),figsize=(20,26),fontsize=20)

table.plot(subplots=True, kind='hist', grid=True, legend=True, stacked=False, 
           sharex=True, sharey=True, figsize=(10,13),
           layout=(4,3))




import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.pyplot import MultipleLocator #设置坐标轴刻度
from matplotlib.font_manager import *

fig, ax = plt.subplots()

table.plot(subplots=True, kind='hist', grid=True, legend=True, stacked=False, 
           sharex=True, sharey=True, figsize=(10,13),
           layout=(4,3),ax=ax)



pdaxes = table.plot(subplots=True, kind='hist', grid=True, legend=True, stacked=False, 
           sharex=True, sharey=True, figsize=(10,13),
           layout=(4,3))

#%% 当前
f, ax = plt.subplots(4,3,figsize=(10,13))
#ax = ax.flatten()
f.delaxes(ax[-1][-1]) #删除多余的图
ax[-1][-1].set_axis_off()


table.plot(subplots=True, kind='hist', grid=True, legend=True, stacked=False, 
           sharex=True, sharey=True, figsize=(10,13),
           ax=ax)


fig = plt.gcf()
ax = plt.gca()

plt.show()



df.groupby('year').plot(kind='hist', x='edi_range_y', ax=axes, legend=True)



#%%

axes[0,0]= pdaxes[0,0] 
axes[0,1]= pdaxes[0,1] 
axes[0,2]= pdaxes[0,2] 

axes[1,0]= pdaxes[1,0] 
axes[1,1]= pdaxes[1,1] 
axes[1,2]= pdaxes[1,2] 


axes[2,0]= pdaxes[2,0] 
axes[2,1]= pdaxes[2,1] 
axes[2,2]= pdaxes[2,2] 

axes[3,0]= pdaxes[3,0] 
axes[3,1]= pdaxes[3,1] 

axes[0,0].plot()


for i in axes:
    for j in i:
        j.get_figure()
        

plt.savefig('test.png',bbox_inches='tight', dpi=300)

f, axes = plt.subplots(4,3,figsize=(12,15))
f.delaxes(axes[3,2]) #删除多余的图

f.text(0.06, 0.5, 'Yaxis - Create this Ylabel by fig.text() function -- line18', va='center', rotation='vertical', fontsize='x-large')
f.text(0.5, 0.05, 'Xaxis - Create this Xlabel by fig.text() function -- line19', va='center', ha='center', fontsize='x-large')

#%%
#简化下面的重复
def sub_plot(row, column, catename, catelist, value):
    index=0
    #text_kwargs=dict(fontsize=20, family='Times New Roman')
    for i in range(0,row):
        for j in range(0,column):
            axes[i,j].hist(df[value][df[catename]==catelist[index]])
            #修改坐标轴字号
            axes[i,j].xaxis.set_label_text('X Axis', family='Times New Roman', fontsize=15)
            # plt.yticks(fontproperties = 'Times New Roman',size = 18)
            # plt.xticks(fontproperties = 'Times New Roman',size = 18)
            index+=1
            if index==len(catelist):
                break
     
cateli=df['year'].unique().tolist()
sub_plot(4,3,'year',cateli,'edi_range_y')



axes[0,0].hist(df['edi_range_y'][df['year']==2011])
axes[0,0].legend()
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

axes[3,0].hist(df['edi_range_y'][df['year']==2020])
axes[3,0].legend()
axes[3,1].hist(df['edi_range_y'][df['year']==2021])
axes[3,1].legend()


#%%

df = pd.read_csv("edithistorysql.csv", index_col='Unnamed: 0')
dfev = pd.read_csv('eventssql.csv', index_col='Unnamed: 0')

df['update_time'] = pd.to_datetime(df['update_time'])
df['date'] = pd.to_datetime(df['update_time']).dt.date


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



