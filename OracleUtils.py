#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import cx_Oracle
# cx_Oracle 安装教程：https://cx-oracle.readthedocs.io/en/latest/installation.html

user = 'root'
pwd = '****'
host = 'localhost'
port = 1521
instance = 'ORCL'
# 连接
# 方法一
info = f'{user}/{pwd}@{host}:{port}/{instance}'
conn = cx_Oracle.connect(info)  
# # 方法二
# dsn_tns = cx_Oracle.makedsn(host, port, instance)
# conn = cx_Oracle.connect(user, pwd, dsn_tns)
cursor = conn.cursor() # 创建游标对象

def test():
    '''测试'''
    sql = 'select sysdate from dual'
    cursor.execute(sql)  # 执行命令
    data = cursor.fetchone() # 返回值
    print(f'Database time:{data}')  # 打印输出

# 增删改查
def add():
    '''增'''
    sql = "insert into QUESTION(TYPIC_ID, QUE_ID, QUE_TITLE) values('{TYPIC_ID}', '{QUE_ID}','{QUE_TITLE}')"
    params = {'TYPIC_ID':1, 'QUE_ID':1, 'QUE_TITLE':1}
    try: 
        cursor.execute(sql.format(**params))
        conn.commit()
        print("成功插入{}条数据".format(cursor.rowcount))
    except Exception as e:
        # 报错回滚
        conn.rollback()
        print(e)

def delete():
    '''删'''
    sql = "delete from QUESTION where TYPIC_ID = '{TYPIC_ID}'"
    params = {'TYPIC_ID':1}
    try:
        cursor.execute(sql.format(**params))
        conn.commit()
        print("成功删除{}条数据".format(cursor.rowcount))
    except Exception as e:
        # 报错回滚
        conn.rollback()
        print(e)

def update():
    '''改'''
    sql = "update QUESTION set QUE_ID = {QUE_ID} where TYPIC_ID = '{TYPIC_ID}'"
    params = {'TYPIC_ID':1, 'QUE_ID':2,}
    try: 
        cursor.execute(sql.format(**params))
        conn.commit()
        print("成功修改{}条数据".format(cursor.rowcount))
    except Exception as e:
        # 报错回滚
        conn.rollback()
        print(e)


def query():
    '''查'''
    sql = "select TYPIC_ID, QUE_ID, QUE_TITLE from QUESTION where TYPIC_ID = '{TYPIC_ID}'"
    params = {'TYPIC_ID':1}
    cursor.execute(sql.format(**params))
    #通过cursor.fetchone()读取一条数据
    data = cursor.fetchone()
    print("读取一条数据：{}".format(data))
    #通过cursor.fetchall()获取所有数据
    for i in cursor.fetchall():
        print("TYPIC_ID:{}, QUE_ID:{}, QUE_TITLE:{}".format(i[0],i[1],i[2]))
    print("共有{}条数据".format(cursor.rowcount))


if __name__ == "__main__":
    # test()
    # add()
    # update()
    # query()
    delete()
    cursor.close()  # 关闭游标对象
    conn.close()  # 关闭数据库