#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrapy
from util import *
import logging

from ..items import Zhibo8SpiderItem

logger=logging.getLogger(__name__)
class Zhibo8Spider(scrapy.Spider): #继承Spider的子类
    name='zhibo8' #name属性,指定执行爬虫的时候指定爬虫
    allowed_domains = ["news.zhibo8.cc"]
    start_urls=[   #爬取列表
        'https://news.zhibo8.cc/zuqiu/more.htm',#直播8足球
        'https://news.zhibo8.cc/nba/more.htm',
    ]
    headers={   
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                'Accept-Language': "zh-CN,zh;q=0.9",
                'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            }

    # #重写请求方法
    # def start_requests(self):
    #     for url in start_urls:
    #         print(url)
    #         yield scrapy.Request(url=url,headers=headers,timeout=5)

    def parse(self,response):
        #处理start_urls地址对应的响应
        ul_list=response.xpath("//div[@class='dataList']//ul")
        # print(ul_list)
        catch_from=0
        catch_from=getFrom(self.name)
        for ul in ul_list:
            # print(ul)
            print("--------------------------------")
            li_list=ul.xpath(".//li")
            for li in li_list:
                try:
                    item=Zhibo8SpiderItem()
                    #解析获取标签,标题,发布时间,url
                    tag=li.xpath("@data-label").extract_first()
                    tag=str(tag).strip(',') #删除首尾多余','
                    link=li.xpath(".//span/a/@href").extract_first()
                    url='https:'+link
                    title=li.xpath(".//span/a/text()").extract_first()
                    #/html/body/div[1]/div[2]/div[1]/div[1]/div[3]/ul[1]/li[1]/span[3]
                    time=li.xpath(".//span[@class='postTime']/text()").extract_first()
                    
                    item['catch_from']=catch_from
                    item['tag']=tag
                    item['url']=url
                    item['title']=title
                    item['origin_dis']=self.name
                    item['time']=time
                    yield scrapy.Request(url,callback=self.req_content,meta={'item':item})
                except Exception as e:
                    logger.warning(e)

    def req_content(self,response):
        '''
        访问正文,获取相关元素
        '''
        # item=Zhibo8SpiderItem()
        item=response.meta['item']
        print(item)
        img=response.xpath("//img/@src").extract_first()
        img='http:'+img
        # print(img)
        p_list=response.xpath("//p")
        # print(p_list)
        content=''
        for p in p_list:
            content+=p.extract()
        item['img']=img
        item['content']=content

        yield item
        # print(content)
        

