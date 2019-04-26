# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy import log

class JingdongPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码格式
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数
        return cls(dbpool)  # 相当于dbpool付给了这个类

    def __init__(self, dbpool):
        self.dbpool = dbpool


    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, goods_ider)  # 调用异常处理方法
        return item

         # 写入数据库中
    def _conditional_insert(self, tx, item):
        sql = "insert into jingdong(goods_id,goods_name,link,shop_name,price,comments) values(%s,%s,%s,%s,%s,%s)"

        params = (
        item["goods_id"], item["goods_name"], item["link"], item["shop_name"],item["price"], item["comments"])
        tx.execute(sql, params)
        
        # 错误处理方法
    def _handle_error(self, failue, item, goods_ider):
        print('--------------database operation exception!!-----------------')
        print(failue)