#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def readCSV(path):
    '''读取 CSV'''
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        for row in reader:
            # <class 'list'>
            print(row)

def writeCSV(path):
    '''写入 CSV'''
    # Windows 中不加 newline=''，每写完一行会有一个空行
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 写一行
        writer.writerow(['name','class'])
        # 写多行
        writer.writerows([['name','class'],['wang',1],['zhao',2]])

def addCSV(path):
    '''追加 CSV'''
    with open(path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name','class'])
        writer.writerows([['name','class'],['wang',1],['zhao',2]])

def readCSV_dic(path):
    '''读取 CSV（以字典形式）'''
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        # 获取列名
        print(reader.fieldnames)
        for row in reader:
            # <class 'collections.OrderedDict'>
            print(row)
            print(row.get('name'))
            print(row['class'])

def writeCSV_dic(path):
    '''写入 CSV（以字典形式）'''
    # Windows 中不加 newline=''，每写完一行会有一个空行
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name','class'])
        # 设置列名
        writer.writeheader()
        # 若未在构造 DictWriter 时设置 fieldnames，则可用以下方法（实则为 writeheader() 函数内容 ）
        # fileheader = ["name", "class"]
        # writer.writerow(dict(zip(fileheader, fileheader)))
        # 写一行
        writer.writerow({'name': 'Li', 'class': '80'})
        # 写多行
        writer.writerows([{'name': 'Zhao', 'class': '100'},{'name': 'Zhang', 'class': '90'}])
            

if __name__ == "__main__":
    path = '1.csv'
    # readCSV(path)
    # writeCSV(path)
    # addCSV(path)
    writeCSV_dic(path)
    readCSV_dic(path)