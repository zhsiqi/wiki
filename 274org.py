#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 05:36:30 2023

@author: zhangsiqi
"""

dfci['org'] = None

#dfci.loc[dfci['maindo'].isna(),'org'] = '缺失'
dfci.loc[(dfci['maindo'].str.contains('其他网站（待确定）|中国城市低碳经济网|高校等教育机构网站|中国地震台网|钓鱼岛官网|百度搜索',regex=True))&(dfci['org'].isna()),'org'] = '其他' 
dfci.loc[(dfci['maindo'].str.contains('G20官网|奥委|奥运|国际足联|一带一路|中非合作论坛|世界卫生组织',regex=True))&(dfci['org'].isna()),'org'] = '跨国合作与国际组织网站' 
dfci.loc[(dfci['domain'].str.contains('\.gov\.cn|cdc\.cn',regex=True))&(dfci['org'].isna()),'org'] = '政府机构网站'
dfci.loc[(dfci['domain'].str.contains('www.baidu.com'))&(dfci['org'].isna()),'org'] = '搜索引擎'


dfci.loc[(dfci['org'].isna()) & (dfci['reference_url'].notna()),'org'] = '门户网站与新闻平台' #微博都是官方账号