# -*- coding: utf-8 -*-
import defind

import logging 
from contextlib import closing
from store import ds,req_url

# logger=logging.getLogger(__name__)
def getFrom(catchFrom):
    '''
    根据来源码获取平台名称
    '''
    catch_from=defind.OTHER
    if catchFrom == defind.ZHIBO8:
        catch_from=defind.FROMZHIBO8
    
    return catch_from

def checkDataIntegrity(data:dict)->bool:
    '''
    检查数据完整性
    data,传入dict
    status,返回状态 ,T : 完整 F : 缺失
    '''
    status=True
    for value in data.values():
        if value is None:
            status=False
            return status
    return status


    