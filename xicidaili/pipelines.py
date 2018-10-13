# -*- coding: utf-8 -*-
import pymysql


class DailiPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host="127.0.0.1",user="root",passwd="admin",db="daili")
        ip= item["ip_"]
        port = item["port_"]
        type = item["type_"]
        sql = "insert into proxy(ip, port_, type ) values ('"+ip+"','"+port+"','"+type+"')"

        conn.query(sql)
        conn.close()
        return item

