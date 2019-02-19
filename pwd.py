#!/usr/bin/env python
# -*- coding:utf-8 -*-
import string

def judge(pwd):
    '''判断密码强度'''
    flag = [0, 0, 0, 0]
    symbol = string.punctuation
    for i in pwd:
        if i.isupper():
            flag[0] = 1
        elif i.islower():
            flag[1] = 1
        elif i.isdigit():
            flag[2] = 1
        elif i in symbol:
            flag[3] = 1
    return sum(flag)

if __name__ == '__main__':
    print(judge(input("input:")))