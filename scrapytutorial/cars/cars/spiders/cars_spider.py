# -*- coding:utf-8 -*-

import json
import scrapy
from ..items import CarsItem


class ElmSpider(scrapy.Spider):
    name = "cars"

    def start_requests(self):
        url_no_offset = "https://api.xin.com/car_search/search?offset="

        for offset in range(0, 2420147, 20):
            url = ''.join([url_no_offset, str(offset)])
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cars = json.loads(response.body.decode('UTF-8'))
        for car in cars['data']['list']:
            item = CarsItem()
            item["car"] = car
            yield item
