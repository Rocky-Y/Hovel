# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class LagouprojectPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],  
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  
        return cls(dbpool) 

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  
        query.addErrback(self._handle_error, item, spider) 
        return item

    def _conditional_insert(self, tx, item):
        # print item['name']
        sql = "insert into lgadress(name,url) values(%s,%s)"

        params = (item["name"], item["url"])
        tx.execute(sql, params)

    def _handle_error(self, failue, item, spider):
        print（'database operation exception!'， failue）

