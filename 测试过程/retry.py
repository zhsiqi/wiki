#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:49:31 2023

@author: zhangsiqi
"""

import requests
from os import path
import time
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import sqlite3 as sqlite
import math
import datetime
from tenacity import retry, retry_if_exception_type, wait_fixed

browser = webdriver.Chrome(executable_path = 'chromedriver')
browser.get('https://baike.baidu.com/historylist/%E9%9D%96%E5%BA%B7%E4%B9%8B%E5%8F%98/905269#page1') 


#submit_time = version.find_element(By.CLASS_NAME, 'submitTime').text
print('0')
@retry(retry = retry_if_exception_type(StaleElementReferenceException),wait=wait_fixed(2))
def get_elements(driver, name):
    print('尝试',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),name)
    targets = driver.find_element(By.CLASS_NAME, name)
    print('尝试成功')
    return targets
    #print('重试2')

versions = browser.find_elements(By.TAG_NAME, 'tr')
for m, version in enumerate(versions[1:], start = 1):
    submit_time = get_elements(version, 'submitTime').text
    contri_card = get_elements(version, 'uname')
    contributor_name = contri_card.text
    contributor_id = contri_card.get_attribute('data-uid')
    print(submit_time)
    print(contributor_name)
    print(contributor_id)

browser.quit()
# b = get_elements(browser, 'uname')

# print(b.text)

# @retry(retry = retry_if_exception_type(StaleElementReferenceException))
# def get_elements(driver, name):
#     targets = driver.find_element(By.CLASS_NAME, name)
#     print('等待重试')