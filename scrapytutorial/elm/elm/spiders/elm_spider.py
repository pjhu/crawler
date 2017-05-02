# -*- coding: utf-8 -*-
import json
import scrapy
from ..items import ElmItem


class ElmSpider(scrapy.Spider):
    name = "elm"

    def start_requests(self):
        url_no_offset = "https://mainsite-restapi.ele.me/shopping/restaurants" \
                        "?extras%5B%5D=activities&geohash=wtw3dfs7rep&latitude=31.21548" \
                        "&limit=24&longitude=121.41608&offset="

        for offset in range(100):
            url = "".join([url_no_offset, str(offset*24), "&terminal=web"])
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        shops = json.loads(response.body.decode('UTF-8'))
        for shop in shops:
            item = ElmItem()
            item["name"] = shop["name"]
            item["shop_id"] = shop["id"]
            item["address"] = shop["address"]
            item["latitude"] = shop["latitude"]
            item["longitude"] = shop["longitude"]
            item["phone"] = shop["phone"]
            yield item

