#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:41:55 2023

@author: zhangsiqi
"""

from waybackpy import WaybackMachineSaveAPI
from waybackpy import WaybackMachineCDXServerAPI


url = "https://news.qq.com/a/20111025/000604.htm"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
save_api = WaybackMachineSaveAPI(url, user_agent)
save_api.save()
save_api.cached_save
save_api.timestamp()
save_api.headers
save_api.archive_url

#%%
cdx = WaybackMachineCDXServerAPI(url, user_agent)
# cdx = WaybackMachineCDXServerAPI(url, user_agent, start_timestamp=2016, end_timestamp=2017)

for item in cdx.snapshots():
    print(item.archive_url)

    
