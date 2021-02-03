# -*- coding: utf-8 -*-

import logging

from util import checkDataIntegrity
from db import insertData
logger=logging.getLogger(__name__)

class Zhibo8SpiderPipeline(object):
    ''' 
    管道,对数据进行处理,存储等
    '''
    def process_item(self,item,spider):

        #检查数据是否完整
        staus=checkDataIntegrity(item)
        if staus==False:
            #写入缺失表
            _=insertData(item,status)
        #数据完整

        #匹配数据标签

        #格式化文章内容与标题

        #完整表入库



        print(item)
        # pass
    def matchTags(self,item):
    '''
    匹配标签   #待定,思路:遍历tag ,查询数据库是否有对应标签,存在,追加标签表id  关联存储,不存在,丢弃到未找到标签表
    '''
        pass