# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import scrapy
from scrapy.pipelines.files import FilesPipeline


class JigsawPipeline(object):

    def __init__(self):
        self.file = None
        self.spamwriter = None

    def open_spider(self, spider):
        self.file = open('items.csv', 'a+', newline='')
        self.spamwriter = csv.writer(self.file, delimiter=",")
        self.spamwriter.writerow(["capability", "id", "name", "gender", "role", "grade", "region", "home_office",
                                  "staffing_office", "working_office", "total_years", "tw_years", "consulting"])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = [item["capability"], item["id"], item["name"], item["role"], item["gender"], item["grade"],
                item["region"], item["home_office"], item["staffing_office"], item["working_office"],
                item["total_years"], item["tw_years"], item["consulting"]]
        self.spamwriter.writerow(line)
        return item


class StaffPipeline(FilesPipeline):
    cookie = {'_jigsaw_session': '5a585a1d059be25987cd33da3b15a3af'}

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, cookies=self.cookie)

    def item_completed(self, results, item, info):
        item['files'] = [x['path'] for ok, x in results if ok]
        return item
