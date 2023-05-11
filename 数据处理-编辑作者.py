#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 01:38:46 2023

@author: zhangsiqi
"""

#%% 感觉用户用不着？补充变量：编辑者数量及对应编辑次数、引用次数
import pandas as pd
import numpy as np
import os
import sqlite3 as sqlite
import re

os.chdir('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0512补充作者')

dfev = pd.read_excel('eventf.xlsx', index_col='index')
dfev['author_count_1'] = np.nan
dfev['author_dic_1'] = None
dfedi = pd.read_excel('edit_time_reindex.xlsx', index_col='index')

dfev['cite_count_1'] = np.nan
dfwt = pd.read_excel('wikitext.xlsx')

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
    dfev.at[index, 'author_count_1'] = author_count
    dfev.at[index, 'author_dic_1'] = str(author_dic)
    
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
    dfev.at[index, 'cite_count_1'] = cite_count


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
#     dfev.at[index, 'cite_count_1'] = cite_count


# conn= sqlite.connect('Wiki.sqlite')
# dfev.to_sql('events', conn, index=True, if_exists = 'replace')
# conn.close()
    
dfev.to_csv('events.csv',index=True)
dfev.to_excel('events.xlsx',index=True)


#%% 集合所有的作者

auall = dfedi['author_name']
author_count = auall.nunique() #6279个作者
alldistri = pd.DataFrame(auall.value_counts().reset_index()) #这里一定要reset index要不然生成的数据框只有一列
alldistri.to_excel('作者编辑次数分布.xlsx',index=True)
auall_dic = str(dict(zip(alldistri.iloc[:,0],alldistri.iloc[:,1])))