#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrapy


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
        
        for ul in ul_list:
            #//*[@id="boxlist"]/div[3]/ul[1]/li[1]
            print(ul)
            print("--------------------------------")
            li_list=ul.xpath(".//li")
            for li in li_list:
                item={}
                #//*[@id="boxlist"]/div[3]/ul[1]/li[1]/span[1]/a
                item['url']=li.xpath(".//span/a/@href").extract_first()
                print(item)
                
            # print(li_list)
        

