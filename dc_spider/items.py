# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DcSpiderItem(scrapy.Item):
    '''
    定义爬取字段以及对字段的处理
    '''
    tag=scrapy.Field() #标签
    url=scrapy.Field() #新闻链接
    title=scrapy.Field() #标题
    time=scrapy.Field() #发布时间
    img=scrapy.Field() #图片
    content=scrapy.Field() #文章内容

    def get_insert_sql(self):
        insert_sql="""
        insert into article_origin(
            catcg_from,origin_url,title,origin_display_author,img_url,all_tags,origin_content,origin_public_at
        )
        values(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params=(
            1,self["url"],self["title"],'zhibo8',self["img"],self["tag"],self["content"],self["time"]
        )
        return insert_sql,params
class Zhibo8SpiderHomeItem(scrapy.Item):
    '''
    直播吧新闻首页Item
    '''
    tag=scrapy.Field() #标签
    url=scrapy.Field() #新闻链接
    title=scrapy.Field() #标题
    time=scrapy.Field() #发布时间

    def parse(self,request):
        

class Zhibo8SpiderItem(Zhibo8SpiderHomeItem):
    '''
    直播吧新闻Item
    含新闻图片,正文
    '''

    