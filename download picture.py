#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 00:28:36 2023

@author: zhangsiqi
"""

# 仅用于下载图片

import wget


url = 'https://www.python.org/static/img/python-logo@2x.png'
wget.download(url, 'logo.png')
