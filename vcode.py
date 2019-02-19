#!/usr/bin/env python
# -*- coding:utf-8 -*-

import string
import random

def getVCode(length):
    '''生成验证码'''
    text=string.printable
    vcode="".join(random.sample(text[0:62],length))
    return vcode


if __name__ == "__main__":
    print(getVCode(4))
