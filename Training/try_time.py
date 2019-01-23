# encoding=utf-8
import time

# 获取当前时间戳 time.time()
t = time.time()
print("当前时间戳",t)

# 时间戳转换为时间元组 time.localtime(t)
lt = time.localtime(t)
print("时间元组",lt)
time.sleep(2)
# time.localtime() 不加参数即为获得当前时间的时间元组
lt = time.localtime()
print("时间元组",lt)

# 格式化时间 time.asctime(lt)
ft = time.asctime(lt)
print("格式化时间",ft)

# 自定义格式化时间 2011-11-11 11:11:11
ft1 = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime())
print("格式化时间1",ft1)

# 自定义格式化时间 Sat Mar 28 22:24:24 2016
ft2 = time.strftime(r"%a %b %d %H:%M:%S %Y", time.localtime())
print("格式化时间2",ft2)

"""
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
%D 01/01/70 格式的时间
"""

# 将格式化时间转换为时间元组
a = "Fri Dec 21 15:14:17 2018"
t1 = time.strptime(a,r"%a %b %d %H:%M:%S %Y")
print(t1)

# 将时间元组转换为时间戳
t2 = time.mktime(t1)
print(t2)




# 0时间戳 经查，因为本地时间（北京时间（GMT +8））比0时区时间多了8小时，所以转换的时候就在小时上多了8小时
print("0时间戳1",time.localtime(0))
# 0时间戳 UTC时区（0时区）1970-1-1 0:0:0
print("0时间戳2",time.gmtime(0))

# 计算时间差
t1 = time.time()
time.sleep(2)
t2 = time.time()
print(time.strftime(r"%H:%M:%S", time.gmtime(t2-t1)))