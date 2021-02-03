
from mysql.connector.pooling import MySQLConnectionPool
import ..settings
from contextlib import closing
database={
    'host':settings.MYSQL_HOST,
    'db':settings.MYSQL_DBNAME,
    'user':settings.MYSQL_USER,
    'passwd':settings.MYSQL_PASSWORD,
    'charset':'utf8',
    'use_unicode':True,
}
ds=MySQLConnectionPool(pool_size=2,database)

def insertData(data:dict,status:bool)->tuple:
    '''
    插入数据,入库前判断是否需要查询该条记录是否存在
    data :需要入库的数据
    status:数据状态 T 完整,F 缺失
    '''
    respTup=()
    tableName='article_origin' #完整初稿表
    if status==False:
        tableName='article_origin_broken' #缺失表
    if data['url'] is None: 
        return respTup
    dataStatus=quertDataStatus(tableName,data['url'])
    if dataStatus==True:  #数据已存在
        return respTup
    #数据不存在,执行插入操作
    sql="""insert into %s (`catch_from`,`origin_url`,`title`,`origin_display_author`,`img_url`,
    `all_tags`,`origin_content`,`origin_publish_at`)values(%s,%s,%s,%s,%s,%s,%s,%s) """
    params_tup=(
        tableName,data['catch_from'],data['url'],data['title'],data['origin_dis'],data['img'],
        data['tag'],data['content'],data['time'],
    )
    with closing(ds.get_connection()) as conn, closing(conn.cursor()) as cur:
        cur.execute(sql,params_tup)
        id=int(cur.lastrowid)
        respTup=(id,)+params_tup #追加插入后的数据id
        conn.commit()
    return respTup
def quertDataStatus(tableName:str,url:str)->bool:
    '''
    检查是否已存在该条数据
    '''
    sql="select id from %s where origin_url='%s'" %(tableName,url)

    with closing(ds.get_connection()) as conn,closing(conn.cursor()) as cur:
        cur.execute(querySql)
        id=cur.fetchone()
        if id is not None and id[0] >0:
            print("新闻数据已经存在,id:%s" % (id[0]))
            return True
        return False
