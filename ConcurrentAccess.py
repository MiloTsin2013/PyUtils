# encoding=utf-8
import requests
import threading
import time
import logging

logging.basicConfig(filename='logger.log', level=logging.INFO)

def access(url):
    ''' 访问链接 '''
    r = requests.get(url)
    logging.info(f"status_code:{r.status_code}")

    
# 继承类threading.Thread
class MyThread(threading.Thread):
    def __init__(self, n, url):
        # 这里要继承构造函数
        super(MyThread, self).__init__()
        # 可以定义自己的实例变量
        self.n = n
        self.url = url

    def run(self):
        logging.info(f'running task{self.n}')
        start_time = time.time()
        access(self.url)
        end_time = time.time()
        logging.info(f'task {self.n} over, cost {end_time-start_time}')

def test(num, url):
    ''' 多线程测试 '''
    # 得到开始时间
    start_time = time.time()
    # 声明空列表
    threads = []
    # 循环开启n个线程
    for i in range(num):
        t = MyThread(i, url)
        t.start()
        # 线程实例放入列表中
        threads.append(t)
        
    # 对线程实例所在列表再循环
    for res in threads:
        # 对每一个实例使用join()方法
        res.join()   
    # 获得结束时间
    end_time = time.time()
    # 计算花费时间
    spend_time = end_time - start_time
    # 打印花费时间
    logging.info(f"Total Cost:{spend_time}")
    
if __name__ == "__main__":
    url = "http://www.baidu.com"
    num = 50
    test(num, url)