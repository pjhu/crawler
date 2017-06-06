#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-06-06 10:55:14
# Project: cars

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://api.xin.com/car_search/search', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for offset in range(0, response.json['data']['total'], 20):
            self.crawl(''.join(['https://api.xin.com/car_search/search?offset=', str(offset)]), callback=self.current_page)

    @config(priority=2)
    def current_page(self, response):
        for carids in response.json['data']['list']:
            self.crawl(''.join(['https://api.xin.com/car_detail_new/view?carid=', str(carids['carid'])]), callback=self.detail_page)

    @config(priority=3)
    def detail_page(self, response):
        return dict(('-'.join(ks), str(v)) for ks, v in self.iteritems_nested(response.json))

    def iteritems_nested(self, d):
        def fetch(suffixes, v0):
            if isinstance(v0, dict):
                for k, v in v0.items():
                    for i in fetch(suffixes + [k], v):
                        yield i
            else:
                yield (suffixes, v0)
        return fetch([], d)
