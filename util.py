# -*- coding: utf-8 -*-
import defind

import logging 
from contextlib import closing
import re
import requests

import json
logger=logging.getLogger(__name__)
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
        if value is None or value =="":
            status=False
            return status
    return status

def fromatContent(content:str, word:str):
    '''
    格式化文本内容
    '''
     # 去除\n
    content = content.replace('\n','') #\n替换为空格
    # 替换style属性
    st = re.search('style="[^=]*?"', content)
    if st is not None:
        content = re.sub('style="[^=]*?"', '', content, 0)  # 替换所有的style为空格

    #替换class=
    st=re.search('class="[^=]*?"',content)
    if st is not None:
        content=re.sub('class="[^=]*?"','',content,0)

    #去除style标签
    st=re.search('<style+>(.+)</style>',content)
    if st is not None:
        content=re.sub('<style+>(.+)</style>','',content,0)
        
    # 去除 span标签
    st = re.search('<span\s*[^>]*>', content)
    if st is not None:
        content = re.sub('<span\s*[^>]*>', '', content, 0)
        content = re.sub('</span>', '', content, 0)

    # 去除img标签
    st = re.search('<img.*?(?:>|\/>)', content)
    if st is not None:
        content = re.sub('<img.*?(?:>|\/>)', '', content, 0)

    #过滤iframe标签
    st = re.search('<iframe[\s\S]+</iframe *>', content)
    if st is not None:
        content = re.sub('<iframe[\s\S]+</iframe *>', '', content, 0)
    #过滤input
    st=re.search('<input[\s\S]+</input *>',content)
    if st is not None:
        content = re.sub('<input[\s\S]+</input *>', '', content, 0)
    #过滤frameset
    st=re.search('<frameset[\s\S]+</frameset *>',content)
    if st is not None:
        content = re.sub('<frameset[\s\S]+</frameset *>', '', content, 0)
    # 去除链接,仅保留内容
    st = re.search('<a[^>]+>(.+)</a>', content)  # 正文去除<a></a>标签,内含超链接\
    if st is not None:
        content = re.sub('<a[^>]*>','', content, 0)
        content = re.sub('</a>', '', content, 0)
        # content=re.sub('<a[^>]+>(.+)</a>','',content,0)

    #去除空的<strong></strong>
    content=content.replace('<strong></strong>','')
    # 去除空的<p><\P>
    content = re.sub(
        '<p[^>]*>(\s|&nbsp;|</?\s?br\s?/?>)*</?p>', '', content, 0)
    # 过滤注释
    content = re.sub('<!--[^>]*-->', '', content, 0)

    # 敏感词替换为空格
    content = content.replace(word,'')
    content = content.replace('视频代码结束','')

    #去除空的div
    content=content.replace('<div ></div>','')

    #去除作者 最后一对<p>标签
    index=content.rfind('<p>')
    content=content[:index]
    
    return content
    


def mixInsertUpdateSql(insert_key_list, update_key_list, except_list, table_name, is_many=False):
    '''   
    # 将数据整合成insert update sql语句
    # insert_key_list 要插入得key数组
    # update_key_list 要更新得key数组
    # except_list insert_key_list 和 update_key_list 的差别key数组
    # is_many  是否是  execute many 插入
    # return string
    # update by bobo 2020-05-29
    '''
    update_sql = ''
    insert_sql = ' ('
    insert_values_sql = ' ('
    insert_index = 0
    update_index = 0
    for key in insert_key_list:
        if insert_index > 0:
            insert_sql += ','
            insert_values_sql += ','
        insert_sql += ('`'+key+'`')
        insert_values_sql += '%s'
        insert_index += 1
        if key in except_list:
            continue
        if update_index > 0:
            update_sql += ','
        update_index += 1

        if is_many == True:
            # 这里必须拼 `` 防止关键字.太坑了 2020-07-03
            update_sql += ('`'+key+'`'+'=values(`'+key+'`)')
        else:
            update_sql += ('`'+key+'`'+'=%s')

    insert_sql += ') '
    insert_values_sql += ') '
    sql = 'INSERT INTO `' + table_name + '`' + insert_sql + ' VALUES ' + \
        insert_values_sql + ' ON DUPLICATE KEY UPDATE ' + update_sql
    return sql

def request_Wash_article(item:dict,id):
    url="http://192.168.3.98:8081/v1/article/remake"
    try:
        data={
                "saved_id":id,"catch_from":item['catch_from'],
                "origin_url":item['url'],"title":item['title'],
                "origin_author":item['origin_dis'],"content":item['content'],
                "img_url":item['img'],"all_tags":item['tag'],
                "origin_publish_at":item['time'],
            }
        resp=requests.post(url=url,data=data)
        jsonstr=json.loads(resp.text)
        if jsonstr["code"]!=0:
            print("数据未正常进行处理,line: 152,id:%s"% id)
    except Exception as e:
        logger.warning(e)
        return
