# -*- coding: utf-8 -*-


from itemadapter import ItemAdapter

from mysql.connector.pooling import MySQLConnectionPool
from twisted.enterprise import adbapi
class DcSpiderPipeline:
    ''' 
    存取爬取的数据
    '''
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def  from_settings(cls,settings):
        dbparms=dict(
            host=settings["MYSQL_HOST"],
            DB=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool("MySQLConnectionPool",**dbparms)
        #实例化一个对象
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query=self.dbpool.runInteraction(self.insert_db, item)
        query.addErrBack(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        #处理异常的插入
        print(failure)
    
    def do_insert(self,cursor,item):
        insert_sql,params=item.get_insert_sql()
        print(insert_sql,params)
        try:
            cursor.execute(insert_sql,params)
        except Exception as e:
            print(e)
