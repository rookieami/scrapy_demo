
from mysql.connector.pooling import MySQLConnectionPool
from scrapy.utils.project import get_project_settings
from contextlib import closing

settings=get_project_settings()
database={
    'host':settings.get('MYSQL_HOST'),
    'db':settings.get('MYSQL_DBNAME'),
    'user':settings.get('MYSQL_USER'),
    'passwd':settings.get('MYSQL_PASSWORD'),
    'charset':'utf8mb4',
    'use_unicode':True,
}
ds=MySQLConnectionPool(pool_size=5,**database)

def insertData(sql:str,status:bool,data:dict)->int:
    '''
    插入数据,入库前判断是否需要查询该条记录是否存在
    data :需要入库的数据
    status:数据状态 T 完整,F 缺失
    '''
    respId=0
    tableName='article_origin' #完整初稿表
    if status==False:
        tableName='article_origin_broken' #缺失表
    if data['url'] is None: 
        return respId
    dataStatus=quertDataStatus(tableName,data['url'])
    if dataStatus==True:  #数据已存在
        return respId
    #数据不存在,执行插入操作
    params_tup=(
        data['catch_from'],data['url'],data['title'],data['origin_dis'],data['img'],
        data['tag'],data['content'],data['time'],
    )
    with closing(ds.get_connection()) as conn, closing(conn.cursor()) as cur:
        cur.execute(sql,params_tup)
        id=int(cur.lastrowid)
        respId=id    #(id,)+params_tup #追加插入后的数据id
        conn.commit()
    return respId
def quertDataStatus(tableName:str,url:str)->bool:
    '''
    检查是否已存在该条数据
    '''
    sql="select id from %s where origin_url='%s'" %(tableName,url)

    with closing(ds.get_connection()) as conn,closing(conn.cursor()) as cur:
        cur.execute(sql)
        id=cur.fetchone()
        if id is not None and id[0] >0:
            print("新闻数据已经存在,id:%s" % (id[0]))
            return True
        return False

def getTags(tags:str)->list:
    '''
    获取tag id
    '''
    sql="SELECT id FROM `tags`  WHERE tag_content IN("
    indexNum=0
    for tag in tags.split(','):
        if indexNum>0:
            sql+=','
        sql+="'%s'"%tag
        indexNum+=1
    sql+=')'
    with closing(ds.get_connection()) as conn,closing(conn.cursor()) as cur:
        cur.execute(sql)
        ids=cur.fetchall()
        conn.commit()
    if len(ids)==0:
        return None
    print(ids)
    return ids

def insertTagAbout(sql:str,params:tuple):
    '''
    数据关联tag进行入库
    '''
    try:
        with closing(ds.get_connection()) as conn,closing(conn.cursor()) as cur:
            cur.execute(sql,params)
            conn.commit()
    except Exception as e:
        logger.warning(e)


def getEndTime(catch_from:str):
    '''获取最后入库时间,返回时间戳
    '''
    respTime = 0
    sqlone = "select origin_publish_at from article_origin where origin_display_author=%s ORDER BY origin_publish_at desc LIMIT 1 "%catch_from
    with closing(ds.get_connection()) as conn, closing(conn.cursor()) as cur:
        cur.execute(sqlone)
        endTime = cur.fetchone()
    sqlTwo = "select origin_publish_at from article_origin_broken  where origin_display_author=%s ORDER BY origin_publish_at desc LIMIT 1 "% catch_from
    with closing(ds.get_connection()) as conn, closing(conn.cursor()) as cur:
        cur.execute(sqlTwo)
        brokenEndTime = cur.fetchone()
    if endTime is not None and brokenEndTime is not None:
        if endTime[0] > brokenEndTime[0]:
            respTime = endTime[0]
            return time.mktime(respTime.timetuple())
        respTime = brokenEndTime[0]

    if respTime==0:
        return 0
    return time.mktime(respTime.timetuple())

 