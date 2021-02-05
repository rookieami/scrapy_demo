#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrapy
from util import *
import logging

from ..items import Zhibo8SpiderItem
from ..db import getEndTime
logger=logging.getLogger(__name__)
class Zhibo8Spider(scrapy.Spider): #继承Spider的子类
    name='zhibo8' #name属性,指定执行爬虫的时候指定爬虫
    allowed_domains = ["news.zhibo8.cc"]
    start_urls=[   #爬取列表
        'https://news.zhibo8.cc/zuqiu/more.htm',#直播8足球
        'https://news.zhibo8.cc/nba/more.htm',
    ]
    
    def parse(self,response):
        #处理start_urls地址对应的响应

        # print(response.request.url)
        # endTime=getEndTime(self.name)

        ul_list=response.xpath("//div[@class='dataList']//ul")
        # print(ul_list)
        catch_from=0
        catch_from=getFrom(self.name)

        tempTime=0
        for ul in ul_list:
            # print(ul)
            # print("--------------------------------")
            li_list=ul.xpath(".//li")
            
            print(response.request.url)
            for li in li_list:
                try:
                    item=Zhibo8SpiderItem()
                    #解析获取标签,标题,发布时间,url
                    tag="" #给初值,防止入库时None报错
                    tag=li.xpath("@data-label").extract_first()
                    tag=str(tag).strip(',') #删除首尾多余','
                    link=li.xpath(".//span/a/@href").extract_first()
                    url=""
                    url='https:'+link

                    title=""
                    title=li.xpath(".//span/a/text()").extract_first()
                    #/html/body/div[1]/div[2]/div[1]/div[1]/div[3]/ul[1]/li[1]/span[3]
                    time=li.xpath(".//span[@class='postTime']/text()").extract_first()
                    
                    item['catch_from']=catch_from
                    item['tag']=tag
                    item['url']=url
                    item['title']=title
                    item['origin_dis']=self.name
                    item['time']=time

                    # articleTime=time.mktime(time.timetuple())   #暂不使用,无法限制来源类型,足球最新会干扰篮球最新,考虑数据库添加字段
                    # if articleTime<endTime: #在最后一次入库前
                    #     break
                    # if tempTime<articleTime:
                    #     tempTime=articleTime #记录最近时间

                    #查一下数据库是否有这条数据,有的话
                    yield scrapy.Request(url,callback=self.req_content,meta={'item':item})
                except Exception as e:
                    logger.warning(e)
                    return
        # endTime=tempTime
                

    def req_content(self,response):
        '''
        访问正文,获取相关元素
        '''
        item=response.meta['item']

        #//*[@id="signals"]/p[1]/img
        img=""
        img=response.xpath(".//div[@class='content']/p//img/@src").extract_first()
        if img is not None and img !="":
            img='http:'+img
        p_list=response.xpath(".//div[@class='content']/p")
        content=""
        for p in p_list:
            content+=p.extract()
        item['img']=img
        item['content']=content

        yield item
        

