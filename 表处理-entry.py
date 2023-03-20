#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 19:24:36 2023

@author: zhangsiqi
"""

from os import path
import numpy as np
import pandas as pd
import re
import sqlite3 as sqlite
import math
import datetime
import os
import numpy as np
import pandas as pd
import re
import sqlite3 as sqlite
import math
import datetime
import os


os.chdir('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0210补充事件时间')

#%% 读取、创建数据库等
evtable = pd.read_excel('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0210补充事件时间/events+timestamp+evtype+range.xlsx')
entryall = evtable['entry'].unique().tolist()

# 创建sql数据库
#sqname = 'BaiduWiki['+ datetime.datetime.now().strftime('%m-%d-%H:%M].sqlite')
os.chdir('/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0214补充词条数据')
conn= sqlite.connect("/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0319/Wiki+1.sqlite")
c = conn.cursor()

dfev = pd.read_sql('SELECT * FROM events', conn)
dfev_ev = dfev['entry'].unique().tolist()

#去除重复


c.execute('DELETE FROM events WHERE events.rowid NOT IN (SELECT min(events.rowid) FROM events GROUP BY entry);')

#========删除多余词条的数据================
#取出 多余的词条名
ev_di = list(set(dfev_ev).difference(set(entryall)))


def del_sql(sheet, entry):
    sql_script = '''DELETE FROM ''' + sheet + ''' WHERE entry = "''' + entry + '''";'''
    return sql_script

# test = del_sql("ci", "脱贫攻坚")
# print(del_sql("ci", "脱贫攻坚"))

for i in ev_di:
    # DELETE FROM "test" WHERE "entry" = '毕福剑';
    c.execute(del_sql("ci",i))
    c.execute(del_sql("citation",i))
    c.execute(del_sql("cittion_edtime",i))
    c.execute(del_sql("edit_time",i))
    c.execute(del_sql("edithistory",i))
    c.execute(del_sql("events",i))
    c.execute(del_sql("final_events",i))
    c.execute(del_sql("final_events_0319",i))
    c.execute(del_sql("relevance",i))
    c.execute(del_sql("science",i))
    c.execute(del_sql("topeditor",i))
    c.execute(del_sql("wikilink",i))
    c.execute(del_sql("wikitext",i))

    conn.commit()
    
c.close()
conn.close()