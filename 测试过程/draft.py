#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 21:14:08 2022

@author: zhangsiqi
"""
from urllib.parse import unquote
from urllib.parse import urlparse
import requests
from os import path
import time
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import sqlite3 as sqlite


browser = webdriver.Chrome(executable_path = '/Users/zhangsiqi/opt/anaconda3/bin/chromedriver')

cookies = {
    'zhishiTopicRequestTime': '1661827301845',
    'BIDUPSID': '3C3CB214132757685D3A8221F479E496',
    'PSTM': '1537443294',
    '__yjs_duid': '1_bc4c7ccdc417b0e5aa90b36df028fef81620385718241',
    'ZFY': 'uPTMDrpQRQHF:AEN5a:ASY6P6wQI3Zi0w8cn:BKlLBBynY:C',
    'BAIDUID': '01F1FC0AFD7C78051DA2019A1CCE5CDB:SL=0:NR=10:FG=1',
    'BAIDUID_BFESS': '01F1FC0AFD7C78051DA2019A1CCE5CDB:SL=0:NR=10:FG=1',
    'BDUSS': 'VBTWpONWttLXloRWYwNlZSbVhoczZOVy1ZWnlxNDVkMjV3TmtUa3piWER-eFZqRVFBQUFBJCQAAAAAAAAAAAEAAADwRVAb1Ma25Of3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMNy7mLDcu5iY1',
    'BDUSS_BFESS': 'VBTWpONWttLXloRWYwNlZSbVhoczZOVy1ZWnlxNDVkMjV3TmtUa3piWER-eFZqRVFBQUFBJCQAAAAAAAAAAAEAAADwRVAb1Ma25Of3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMNy7mLDcu5iY1',
    'Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a': '1661251662',
    'H_WISE_SIDS': '110085_179347_180636_188745_194529_196428_197471_204427_204906_209568_210321_211435_212296_212867_212967_213028_213357_215727_216374_216715_216841_216941_217084_217167_218315_218567_218620_219404_219558_219942_219946_220639_221121_221479_221502_221697_221734_221874_221915_221920_222299_222335_222397_222466_222522_222539_222605_222617_222620_222625_222780_222845_222862_223064_223144_223192_223218_223238_223343_223374_223474_223769_223844_223898_223906_223917_224055_224080_224086_224099_224116_224159_224196_224261_224267_224429_224438_224754_224801_224980_225332_225373_225436_225515_225736_225917_226049',
    'BK_SEARCHLOG': '%7B%22key%22%3A%5B%22%E9%A6%99%E6%B8%AF%E5%8D%A0%E9%A2%86%E4%B8%AD%E7%8E%AF%22%2C%22%E9%A6%99%E6%B8%AF%20%E5%8D%A0%E9%A2%86%20%E4%B8%AD%E7%8E%AF%22%2C%22%E9%A6%99%E6%B8%AF%20%E4%B8%AD%E7%8E%AF%22%2C%22MH370%22%2C%223%C2%B78%E9%A9%AC%E6%9D%A5%E8%A5%BF%E4%BA%9A%E8%88%AA%E7%8F%AD%E5%A4%B1%E8%B8%AA%E4%BA%8B%E4%BB%B6%22%2C%22%E9%A6%99%E6%B8%AF%E5%A5%B6%E7%B2%89%E9%99%90%E8%B4%AD%22%2C%22%E5%A5%B6%E7%B2%89%E9%99%90%E8%B4%AD%E4%BB%A4%22%2C%22%E5%88%98%E9%93%81%E7%94%B7%E6%A1%88%22%2C%229%C2%B718%E7%94%98%E8%82%83%E5%88%9D%E4%B8%AD%E7%94%9F%E5%8F%91%E5%B8%96%E8%A2%AB%E5%88%91%E6%8B%98%22%2C%229%C2%B717%E7%94%98%E8%82%83%E5%88%9D%E4%B8%AD%E7%94%9F%E5%8F%91%E5%B8%96%E8%A2%AB%E5%88%91%E6%8B%98%E4%BA%8B%E4%BB%B6%22%2C%223%C2%B74%E9%95%BF%E6%98%A5%E7%9B%97%E8%BD%A6%E6%9D%80%E5%A9%B4%E6%A1%88%22%2C%22%E6%B5%B7%E5%8D%97%E5%B9%BC%E5%A5%B3%E5%BC%80%E6%88%BF%E6%A1%88%22%2C%22%E6%A0%A1%E9%95%BF%E5%B8%A6%E5%A5%B3%E7%94%9F%E5%BC%80%E6%88%BF%E6%A1%88%22%2C%22%E9%BE%9A%E7%88%B1%E7%88%B1%E6%A1%88%22%2C%22%E9%BE%9A%E7%88%B1%E7%88%B1%22%2C%22%E9%99%95%E8%A5%BF%20%E6%88%BF%E5%A7%90%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%E6%A1%88%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%20%E6%AD%BB%E5%88%91%22%2C%22%E9%BB%84%E6%B5%A6%E6%B1%9F%E6%AD%BB%E7%8C%AA%E4%BA%8B%E4%BB%B6%22%5D%7D',
    'H_WISE_SIDS_BFESS': '110085_179347_180636_188745_194529_196428_197471_204427_204906_209568_210321_211435_212296_212867_212967_213028_213357_215727_216374_216715_216841_216941_217084_217167_218315_218567_218620_219404_219558_219942_219946_220639_221121_221479_221502_221697_221734_221874_221915_221920_222299_222335_222397_222466_222522_222539_222605_222617_222620_222625_222780_222845_222862_223064_223144_223192_223218_223238_223343_223374_223474_223769_223844_223898_223906_223917_224055_224080_224086_224099_224116_224159_224196_224261_224267_224429_224438_224754_224801_224980_225332_225373_225436_225515_225736_225917_226049',
    'ZD_ENTRY': 'google',
    'baikeVisitId': 'f76e8aba-797e-47b9-9a6f-d857e5bf79e9',
    'RT': '"z=1&dm=baidu.com&si=lmtcvn6ru09&ss=l7fl2fhf&sl=2&tt=22k&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=2k5&ul=13ofl"',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'zhishiTopicRequestTime=1661827301845; BIDUPSID=3C3CB214132757685D3A8221F479E496; PSTM=1537443294; __yjs_duid=1_bc4c7ccdc417b0e5aa90b36df028fef81620385718241; ZFY=uPTMDrpQRQHF:AEN5a:ASY6P6wQI3Zi0w8cn:BKlLBBynY:C; BAIDUID=01F1FC0AFD7C78051DA2019A1CCE5CDB:SL=0:NR=10:FG=1; BAIDUID_BFESS=01F1FC0AFD7C78051DA2019A1CCE5CDB:SL=0:NR=10:FG=1; BDUSS=VBTWpONWttLXloRWYwNlZSbVhoczZOVy1ZWnlxNDVkMjV3TmtUa3piWER-eFZqRVFBQUFBJCQAAAAAAAAAAAEAAADwRVAb1Ma25Of3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMNy7mLDcu5iY1; BDUSS_BFESS=VBTWpONWttLXloRWYwNlZSbVhoczZOVy1ZWnlxNDVkMjV3TmtUa3piWER-eFZqRVFBQUFBJCQAAAAAAAAAAAEAAADwRVAb1Ma25Of3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMNy7mLDcu5iY1; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1661251662; H_WISE_SIDS=110085_179347_180636_188745_194529_196428_197471_204427_204906_209568_210321_211435_212296_212867_212967_213028_213357_215727_216374_216715_216841_216941_217084_217167_218315_218567_218620_219404_219558_219942_219946_220639_221121_221479_221502_221697_221734_221874_221915_221920_222299_222335_222397_222466_222522_222539_222605_222617_222620_222625_222780_222845_222862_223064_223144_223192_223218_223238_223343_223374_223474_223769_223844_223898_223906_223917_224055_224080_224086_224099_224116_224159_224196_224261_224267_224429_224438_224754_224801_224980_225332_225373_225436_225515_225736_225917_226049; BK_SEARCHLOG=%7B%22key%22%3A%5B%22%E9%A6%99%E6%B8%AF%E5%8D%A0%E9%A2%86%E4%B8%AD%E7%8E%AF%22%2C%22%E9%A6%99%E6%B8%AF%20%E5%8D%A0%E9%A2%86%20%E4%B8%AD%E7%8E%AF%22%2C%22%E9%A6%99%E6%B8%AF%20%E4%B8%AD%E7%8E%AF%22%2C%22MH370%22%2C%223%C2%B78%E9%A9%AC%E6%9D%A5%E8%A5%BF%E4%BA%9A%E8%88%AA%E7%8F%AD%E5%A4%B1%E8%B8%AA%E4%BA%8B%E4%BB%B6%22%2C%22%E9%A6%99%E6%B8%AF%E5%A5%B6%E7%B2%89%E9%99%90%E8%B4%AD%22%2C%22%E5%A5%B6%E7%B2%89%E9%99%90%E8%B4%AD%E4%BB%A4%22%2C%22%E5%88%98%E9%93%81%E7%94%B7%E6%A1%88%22%2C%229%C2%B718%E7%94%98%E8%82%83%E5%88%9D%E4%B8%AD%E7%94%9F%E5%8F%91%E5%B8%96%E8%A2%AB%E5%88%91%E6%8B%98%22%2C%229%C2%B717%E7%94%98%E8%82%83%E5%88%9D%E4%B8%AD%E7%94%9F%E5%8F%91%E5%B8%96%E8%A2%AB%E5%88%91%E6%8B%98%E4%BA%8B%E4%BB%B6%22%2C%223%C2%B74%E9%95%BF%E6%98%A5%E7%9B%97%E8%BD%A6%E6%9D%80%E5%A9%B4%E6%A1%88%22%2C%22%E6%B5%B7%E5%8D%97%E5%B9%BC%E5%A5%B3%E5%BC%80%E6%88%BF%E6%A1%88%22%2C%22%E6%A0%A1%E9%95%BF%E5%B8%A6%E5%A5%B3%E7%94%9F%E5%BC%80%E6%88%BF%E6%A1%88%22%2C%22%E9%BE%9A%E7%88%B1%E7%88%B1%E6%A1%88%22%2C%22%E9%BE%9A%E7%88%B1%E7%88%B1%22%2C%22%E9%99%95%E8%A5%BF%20%E6%88%BF%E5%A7%90%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%E6%A1%88%22%2C%22%E5%A4%8F%E4%BF%8A%E5%B3%B0%20%E6%AD%BB%E5%88%91%22%2C%22%E9%BB%84%E6%B5%A6%E6%B1%9F%E6%AD%BB%E7%8C%AA%E4%BA%8B%E4%BB%B6%22%5D%7D; H_WISE_SIDS_BFESS=110085_179347_180636_188745_194529_196428_197471_204427_204906_209568_210321_211435_212296_212867_212967_213028_213357_215727_216374_216715_216841_216941_217084_217167_218315_218567_218620_219404_219558_219942_219946_220639_221121_221479_221502_221697_221734_221874_221915_221920_222299_222335_222397_222466_222522_222539_222605_222617_222620_222625_222780_222845_222862_223064_223144_223192_223218_223238_223343_223374_223474_223769_223844_223898_223906_223917_224055_224080_224086_224099_224116_224159_224196_224261_224267_224429_224438_224754_224801_224980_225332_225373_225436_225515_225736_225917_226049; ZD_ENTRY=google; baikeVisitId=f76e8aba-797e-47b9-9a6f-d857e5bf79e9; RT="z=1&dm=baidu.com&si=lmtcvn6ru09&ss=l7fl2fhf&sl=2&tt=22k&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=2k5&ul=13ofl"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}



# 下面试了一下如果失效链接跳转到了网站主页，不会报错

#             redirlink = 'http://www.xinhuanet.com//politics/2011-08/10/c_121842569_2.htm'
#             jsscript = '''window.open("'''+ redirlink + '''", 'new_window')''' 
#             browser.execute_script(jsscript) #在新标签页打开redirect链接
#             browser.close() #关闭参考资料的第一层标签页
#             browser.switch_to.window(browser.window_handles[-1])
            
#             origilink = browser.current_url #记录当下链接，也即参考资料的实际链接
#             print(origilink)


x = 1 #dataframe行序号
for line in open("address1.txt"):
    # print('line',line.strip())
    wangzhi = urlparse(line.strip()) #从URL中解析出各个部分
    # print('wangzhi', wangzhi[2])
    entryname = unquote(wangzhi[2][6:]) #从解析结果中提取出事件内容部分并且转成中文给html文件命名，
    #命名中的斜杠要删除,否则后面新建html有问题
    if '/' in entryname:
        entryname = entryname.split('/')[0]
    
    filename = entryname + "requests" + ".html"  # 保存的文件名
    filename1 = entryname + ".html"  # 保存的文件名
    
    if path.exists(filename):  # 检查文件是否存在，若存在就跳过(避免重复文件)
        continue
    
    browser.get(line.strip()) #selenium获取网页
    actions = ActionChains(browser)
    original_window = browser.current_window_handle #记录 百科的原始标签页
    
    #新建标签页打开参考资料页面
    ref_links = browser.find_elements(By.CLASS_NAME,'wiki-lemma-icons_reference-link') #找到链接
    if ref_links:
        for ref_link in ref_links:
            ref_link.click() #点击参考资料链接，打开新标签页
            browser.switch_to.window(browser.window_handles[-1]) 
             # 如果页面直接显示的初始链接，马上记录下来
            redirlink = browser.find_element(By.CLASS_NAME,'link').get_attribute('href')
            print(redirlink) # 参考资料的redirect链接
            
            
            #linkconti = browser.find_element(By.CLASS_NAME,'link')
            
            jsscript = '''window.open("'''+ redirlink + '''", 'new_window')''' 
            browser.execute_script(jsscript) #在新标签页打开redirect链接
            browser.close() #关闭参考资料的第一层标签页
            browser.switch_to.window(browser.window_handles[-1])
            
            origilink = browser.current_url #记录当下链接，也即参考资料的实际链接
            print(origilink)
            browser.close() #关闭实际链接的标签页
            browser.switch_to.window(original_window) #回到原初的百科页面
            response = requests.get(origilink.strip(), cookies=cookies, headers=headers)
            print('http状态码', response.status_code)
        
        # 如果这个页面是有效的，继续抓文字，如果无效的，返回左边的标签页保存下图片

browser.quit()