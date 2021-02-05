# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import sched
import time
from datetime import datetime
import os

schedule=sched.scheduler(time.time,time.sleep)

def start(fromName:list):
    # process=CrawlerProcess(get_project_settings())
    # process.crawl(fromName)
    # process.start()
    for fN in fromName:
        st="scrapy crawl "+fN
        os.system(st)

#周期性调度触发函数
def func():
    start('zhibo8')

def performl(inc):
    schedule.enter(inc,0,performl,(inc,))
    func()


def main():
    #第一个参数 多少秒后执行任务
    #优先级 0最高
    #任务
    #定时执行函数名函数的参数
    schedule.enter(0,0,performl,(300,))  #暂时间隔5分钟执行一次

if __name__=='__main__':
    main()
    schedule.run()