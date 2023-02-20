#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 17:30:11 2022

@author: zhangsiqi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 16:05:40 2022

@author: zhangsiqi
"""

# -*- coding: utf-8 -*-
# from urllib.parse import quote
from urllib.parse import unquote
from urllib.parse import urlparse
from os import path
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import lxml

#========第一步：事件名称汉字转URL编码=============

# atest = quote("中文")
# print(atest)


# urlparse('https://baike.baidu.com/item/%E6%97%A5%E6%9C%AC9%E7%BA%A7%E5%9C%B0%E9%9C%87')输出结果
# ParseResult(scheme='https', 
#             netloc='baike.baidu.com', 
#             path='/item/%E6%97%A5%E6%9C%AC9%E7%BA%A7%E5%9C%B0%E9%9C%87', 
#             params='', query='', fragment='')

# create a dataframe to store target data
df = pd.DataFrame(columns=['event','viewcount','votecount','topeditor'])

#========第一步：根据词条网址获取网页内容============
browser = webdriver.Chrome(executable_path = '/Users/zhangsiqi/opt/anaconda3/bin/chromedriver')

x = 1 #dataframe行序号
for line in open("address.txt"):
    # print('line',line.strip())
    wangzhi = urlparse(line.strip()) #从URL中解析出各个部分
    # print('wangzhi', wangzhi[2])
    entryname = unquote(wangzhi[2][6:]) #从解析结果中提取出事件内容部分并且转成中文给html文件命名
    # print('entryname', entryname)
    
    filename = entryname + ".html"  # 保存的文件名
    
    if path.exists(filename):  # 检查文件是否存在，若存在就跳过(避免重复文件)
        continue

    print(entryname)
    

    browser.get(line.strip()) #selenium获取网页
    

    with open(filename, "w", encoding='utf-8') as g: #selenium方式保存的html
        g.write(browser.page_source)
    
    # 利用bs定位元素并提取数据
    soup = BeautifulSoup(open(filename))
    
    viewcount = soup.find(id = "j-lemmaStatistics-pv").text #浏览量
    votecount = soup.find("span", class_="vote-count").text #点赞量
    topeditor = soup.find("a", class_="username").attrs #突出贡献用户

    
    # viewcount = browser.find_element(By.ID, "j-lemmaStatistics-pv").text #浏览量
    # votecount = browser.find_element(By.CLASS_NAME, "vote-count").text #点赞量
    # topeditor = browser.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/dl/dd[2]/ul/li/a[1]").text #突出贡献用户

    # 写入数据框
    df.loc[x] = [entryname, viewcount, votecount, topeditor]
    x += 1
    
    # 等待数秒继续下一个
    time.sleep(8)

browser.close()
g.close()
df.to_csv('3event.csv')
#========第二步：解析html，获取特定要素============
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    