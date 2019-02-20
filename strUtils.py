#!/usr/bin/env python
# -*- coding:utf-8 -*-

def hasChinese(s):
    '''包含汉字的返回TRUE'''
    for c in s:
        if '\u4e00' <= c <= '\u9fa5':
            return True
    return False

def changeCode(string):
    '''UTF-16 中文编码转换'''
    return string.encode('utf-8').decode('unicode_escape')