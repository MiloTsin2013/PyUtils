#!/usr/bin/env python
# coding=utf-8

import time
import datetime
import os

def timeStampToTime(timestamp):
    '''把时间戳转化为时间'''
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)


def getSize(filePath):
    '''获取文件的大小,结果保留两位小数，单位为MB'''
    # filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)


def getAccessTime(filePath):
    '''获取文件的访问时间, 若刚创建则为创建时间'''
    # filePath = unicode(filePath,'utf8')
    t = os.path.getatime(filePath)
    return timeStampToTime(t)
    

def getCreateTime(filePath):
    '''获取文件的创建时间'''
    # filePath = unicode(filePath,'utf8')
    t = os.path.getctime(filePath)
    return timeStampToTime(t)


def getModifyTime(filePath):
    '''获取文件的修改时间, 若刚创建则为创建时间'''
    # filePath = unicode(filePath,'utf8')
    t = os.path.getmtime(filePath)
    return timeStampToTime(t)

def isModify(filePath, after=None, before=None):
    '''
    判断文件在某一时间段内是否修改过\n
    filePath    文件路径\n
    after       判断某个时间段之后 %Y-%m-%d %H:%M:%S 格式\n
    before      判断某个时间段之前 %Y-%m-%d %H:%M:%S 格式
    '''
    mtime = getModifyTime(filePath)
    if after and before:
        return after <= mtime <= before
    if after:
        return after <= mtime
    if before:
        return mtime <= before
    return True
