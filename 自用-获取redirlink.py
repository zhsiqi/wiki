#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 00:41:36 2023

@author: zhangsiqi
"""


import time
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.keys import Keys
import pandas as pd


df = pd.read_csv('indexcitationssql.csv')
df['redir_url'] = 'NA'
browser = webdriver.Chrome(executable_path = 'chromedriver')

print(df.at[716,'reference_url'])
print(pd.isna(df.at[716,'reference_url']))

for index, row in df.iterrows():
    # print('line',line.strip())
    line = row['reference_url']
    if not pd.isna(line): #判断不为空值
        browser.get(line.strip()) #selenium获取网页
        
        wait = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(((By.CLASS_NAME,'link'))))
        
        redir_url = browser.find_element(By.CLASS_NAME,'link').get_attribute('href') #得到参考资料真实链接
        df.at[index, 'redir_url'] = redir_url
    time.sleep(0.5)
browser.quit()

df.to_csv('补充完毕的citation.csv')

print('redir链接补充成功')