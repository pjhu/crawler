# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
from elasticsearch import Elasticsearch


class CarsPipeline(object):
    __type__ = 'youxin'

    def __init__(self, index='cars'):
        self.index = index
        self.es = Elasticsearch(hosts=['10.202.129.165:9200', '10.202.129.167:9200', '10.202.129.168:9200'])

        self.es.indices.create(index=self.index, ignore=400)
        if not self.es.indices.get_mapping(index=self.index, doc_type=self.__type__):
            self.es.indices.put_mapping(index=self.index, doc_type=self.__type__, body={
                "_all": {"enabled": True},
                "properties": {
                    "taskid": {"enabled": False},
                    "project": {"type": "string", "index": "not_analyzed"},
                    "url": {"enabled": False},
                }
            })

    def process_item(self, item, spider):
        obj = {
            'result': item['car'],
            'updatetime': time.time(),
        }
        return self.es.index(index=self.index, doc_type=self.__type__,
                             body=obj, id='%s:%s' % ('youxin', item['car']['carid']))
        return item
