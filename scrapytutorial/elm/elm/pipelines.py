# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql.cursors


class ElmPipeline(object):
    def process_item(self, item, spider):
        return item


class ElmJsonWriterPipeline(object):

    def __init__(self):
        self._file = None

    def open_spider(self, spider):
        self._file = open("items.json", "w")

    def close_spider(self, spider):
        self._file.close()

    def process_item(self, item, spider):
        json.dump(dict(item), self._file)
        self._file.write("\n")
        return item


class ElmMysqlPipeline(object):

    def __init__(self):
        self._mysql = None

    def open_spider(self, spider):
        self._mysql = pymysql.connect(host='localhost', user='root',
                                      password='', db='crawler_elm', charset='utf8')

    def close_spider(self, spider):
        self._mysql.close()

    def process_item(self, item, spider):
        insert_shops = "INSERT INTO `shops` " \
                       "(`name`, `shop_id`, `address`, `latitude`, `longitude`, `phone`)"

        insert_value = "VALUES ({name!r}, {shop_id!r}, {address!r}, {latitude}, {longitude}, {phone!r});"\
            .format(**item)
        ddl = "\n".join([insert_shops, insert_value])

        try:
            with self._mysql.cursor() as cursor:
                # Create a new record
                cursor.execute(ddl)

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                print(ddl)
                self._mysql.commit()
        except Exception as inst:
            print(inst)
            self._mysql.close()
        return item



