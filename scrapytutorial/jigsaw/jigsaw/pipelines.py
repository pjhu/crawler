# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json


class JigsawPipeline(object):

    def __init__(self):
        self.file = None
        self.spamwriter = None

    def open_spider(self, spider):
        self.file = open('items.csv', 'a+', newline='')
        self.spamwriter = csv.writer(self.file, delimiter=",")
        self.spamwriter.writerow(["name", "role", "grade", "region", "home_office",
                                  "working_office", "total_years", "tw_years", "consulting"])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = [item["name"], item["role"], item["grade"], item["region"], item["home_office"], item["working_office"],
                item["total_years"], item["tw_years"], item["consulting"]]
        self.spamwriter.writerow(line)
        return item
