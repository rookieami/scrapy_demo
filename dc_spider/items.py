# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Zhibo8SpiderItem(scrapy.Item):
    catch_from=scrapy.Field() #来源平台 1直播吧
    url=scrapy.Field() #新闻链接
    title=scrapy.Field() #标题
    origin_dis=scrapy.Field() #文章来源
    img=scrapy.Field() #图片
    tag=scrapy.Field() #标签
    content=scrapy.Field() #文章内容
    time=scrapy.Field() #发布时间
