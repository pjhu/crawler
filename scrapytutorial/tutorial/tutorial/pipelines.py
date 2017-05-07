# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class ZhMysqlPipeline(object):

    def __init__(self):
        self._mysql = None

    def open_spider(self, spider):
        self._mysql = pymysql.connect(host='localhost', user='root',
                                      password='', db='crawler_zh', charset='utf8')

    def close_spider(self, spider):
        self._mysql.close()

    def process_item(self, item, spider):
        insert_shops = "INSERT INTO `users` " \
                       "(`url_token`, `name`, `gender`, `following_count`, `follower_count`," \
                       " `following_columns_count`, `following_topic_count`, `articles_count`)"

        insert_value = "VALUES ({url_token!r}, {name!r}, {gender}, {following_count}," \
                       "{follower_count}, {following_columns_count}, {following_topic_count}, {articles_count});"\
            .format(**item)
        ddl = "\n".join([insert_shops, insert_value])

        try:
            with self._mysql.cursor() as cursor:
                # Create a new record
                cursor.execute(ddl)

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                self._mysql.commit()
        except Exception as inst:
            print(inst)
            self._mysql.close()
        return item


class JsMysqlPipeline(object):

    def __init__(self):
        self._mysql = None

    def open_spider(self, spider):
        self._mysql = pymysql.connect(host='localhost', user='root',
                                      password='', db='crawler_js', charset='utf8')

    def close_spider(self, spider):
        self._mysql.close()

    def process_item(self, item, spider):
        insert_shops = "INSERT INTO `users` " \
                       "(`url_token`, `name`, `following_count`, `followers_count`," \
                           " `articles_count`, `words_count`, `like_count`)"

        insert_value = "VALUES ({url_token!r}, {name!r}, {following_count}," \
                       "{followers_count}, {articles_count}, {words_count}, {like_count});"\
            .format(**item)
        ddl = "\n".join([insert_shops, insert_value])

        with self._mysql.cursor() as cursor:
            # Create a new record
            cursor.execute(ddl)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self._mysql.commit()
        return item
