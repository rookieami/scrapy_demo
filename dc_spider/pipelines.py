# -*- coding: utf-8 -*-

import logging

from util import checkDataIntegrity,fromatContent,mixInsertUpdateSql,request_Wash_article
from dc_spider.db import insertData,getTags,insertTagAbout



logger=logging.getLogger(__name__)

class Zhibo8SpiderPipeline(object):
    ''' 
    管道,对数据进行处理,存储等
    '''
    def process_item(self,item,spider):

        #检查数据是否完整

        # print(spider.name)
        staus=checkDataIntegrity(item)
        if staus==False: #数据缺失
            #写入缺失表
            self.insertMissData(item)
            return
        #数据完整
        #格式化文章内容与标题
        item=self.formatArticle(item)

        #完整表入库
        #检查格式化后的数据完整性,主要防止正文格式化后为空
        status=checkDataIntegrity(item)
        if staus==False: #数据缺失
            #写入缺失表
            self.insertMissData(item)
            return

        id=self.insertIntactData(item)
        if id==0:
            #已存在数据,不进行后续操作
            return

        #匹配数据标签 ,入关联表库
        self.matchTags(item,id)

        #文章内容进行洗稿请求
        # self.washArticle(item,id)
        

    def  formatArticle(self,item):
        '''
        格式化文章标题和内容
        '''
        #标题处理
        if item['title']is not None:
            title=item['title']
            item['title']=title.replace("直播吧",'') #敏感词置换为空格
        #格式化文本内容,去除相关元素和敏感词
        if item['content'] is not None:
            content=item['content']
            item['content']=fromatContent(content,"直播吧")
        return item
    def insertMissData(slef,item):
        '''
        缺失数据入库
        '''
        #写入缺失表
        update_key_list=[
            'catch_from', #来源
            'origin_url', #原贴地址
            'title',  #文章标题
            'origin_display_author', #文章来源
            'img_url', #封面图地址
            'all_tags', #原文标签
            'origin_content', #原文内容
            'origin_publish_at',#原文发布时间
            ]
            
        insert_key_list=update_key_list
        tableName='article_origin_broken'
        sql=mixInsertUpdateSql(insert_key_list,update_key_list,[],tableName,True)
        _=insertData(sql,False,item)
        
    def insertIntactData(self,item):
        '''
        完整数据入库
        '''
        update_key_list=[
            'catch_from', #来源
            'origin_url', #原贴地址
            'title',  #文章标题
            'origin_display_author', #文章来源
            'img_url', #封面图地址
            'all_tags', #原文标签
            'origin_content', #原文内容
            'origin_publish_at',#原文发布时间
        ]
        insert_key_list=update_key_list
        tableName='article_origin'
        sql=mixInsertUpdateSql(insert_key_list,update_key_list,[],tableName,True)
        #入库
        id =insertData(sql,True,item)
        return id

    def matchTags(self,item,id):
        '''
        匹配标签   #待定,思路:遍历tag ,查询数据库是否有对应标签,存在,追加标签表id  关联存储,不存在,丢弃到未找到标签表
        '''
        #查询tags表关联id
        ids=getTags(item['tag'])
        if ids is None:
            insert_key_list=[  #此处确认是一个,还是逗号分割全部存入   #暂时全部存
                'need_by_article',
                'tag_content',
            ]
            tableName='unkown_tags'
            sql=mixInsertUpdateSql(insert_key_list,insert_key_list,[],tableName,True)
            #入库
            params=(id,item['tag'])
            _=insertTagAbout(sql,params)
            return
        #存在
        insert_key_list=[
            'article_id',
            'tag_id',
        ]
        tableName='article_tag_binding'
        sql=mixInsertUpdateSql(insert_key_list,insert_key_list,[],tableName,True)
        for tagid in ids:
            for tag in tagid:
                if tag is not None:
                    params=(id,tag)
                    _=insertTagAbout(sql,params)

    def washArticle(self,item,id):
        #组装数据
        request_Wash_article(item,id)
