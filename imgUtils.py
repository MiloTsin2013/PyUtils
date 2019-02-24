#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import base64

def decode_base64(data):
    # base64 编码长度为 4 的倍数，缺少补 '='
    missing_padding = 4 - len(data)%4
    if 0 < missing_padding < 4:
        data += '=' * missing_padding
    return base64.b64decode(data)

def saveImgFromBase64(base64Codes, filename):
    # 去掉头 'data:image/png;base64,'
    base64Codes = base64Codes.split(",")[-1]
    imgdata = decode_base64(base64Codes)
    file = open(filename, 'wb')
    file.write(imgdata)
    file.close()


if __name__ == "__main__":
    strs = ''''''
    filename = r'1.jpg'
    saveImgFromBase64(strs, filename)
