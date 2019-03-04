#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pymysql

# 连接数据库
conn = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    passwd = "****",
    db = "test",
    charset = "utf8"
)
# 获取游标
# cursor = conn.cursor()
# 获取字典游标
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
print(cursor)

# 增删改查操作

def add():
    '''向数据库中插入数据'''
    sql = "insert into student(name,age) values('{name}',{age})"
    params = {'name':'lily','age':18}
    try:
        #执行sql
        cursor.execute(sql.format(**params))
        conn.commit()
        print("成功插入{}条数据".format(cursor.rowcount))
    except Exception as e:
        # 报错回滚
        conn.rollback()
        print(e)

def delete():
    '''删除数据库中的信息'''
    sql = "delete from student where name = '{name}'"
    params = {'name':'1'}
    try:
        cursor.execute(sql.format(**params))
        conn.commit()
        print("成功删除{}条数据".format(cursor.rowcount))
    except Exception as e:
        # 报错回滚
        conn.rollback()
        print(e)

def update():
    '''修改数据库中的信息'''
    sql = "update student set age = {age} where name = '{name}'"
    params = {'name':'lily','age':15}
    try:
        cursor.execute(sql.format(**params))
        conn.commit()
        print("成功修改{}条数据".format(cursor.rowcount))
    except Exception as e:
        # 报错回滚
        conn.rollback()
        print(e)

def query():
    '''查询数据库中的数据'''
    sql = "select name,age from student"
    #返回执行语句的影响行数
    num = cursor.execute(sql)
    print(f'查询到{num}条数据')
    #移动游标
    cursor.scroll(1,mode='relative')
    #通过cursor.fetchone()读取一条数据
    stu = cursor.fetchone()
    print("读取一条数据：{}".format(stu))
    #通过cursor.fetchmany(size=2)读取多条数据
    stus = cursor.fetchmany(size=2)
    print("读取2条数据：{}".format(stus))
    #通过cursor.fetchall()获取所有数据
    for i in cursor.fetchall():
        #print("姓名：{} 年龄：{}".format(i[0],i[1]))
        print("姓名：{} 年龄：{}".format(i['name'],i['age']))
    #返回执行语句的影响行数
    print("共有{}条数据".format(cursor.rowcount))


if __name__ == "__main__":
    # add()
    # update()
    # query()
    delete()

    cursor.close()  # 关闭游标对象
    conn.close()  # 关闭数据库

