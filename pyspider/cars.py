#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-05-26 14:46:02
# Project: car

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.xin.com/shanghai/s/', callback=self.brands)

    @config(age=10 * 24 * 60 * 60)
    def brands(self, response):
        brands = response.doc('#select1 > div > ul.brand-cars.clearfix dd > a')
        for each in brands.items():
            self.crawl(each.attr.href, callback=self.current_page)

    @config(priority=2)
    def current_page(self, response):
        cars = response.doc('#search_container > div._list-con.list-con.clearfix > ul > li > a')
        for each in cars.items():
            self.crawl(each.attr.href, callback=self.detail_page)

        next_page = response.doc('#search_container > div.con-page.search_page_link > a:last-child')
        if next_page.text() == "下一页":
            self.crawl(next_page.attr.href, callback=self.current_page)

    @config(priority=3)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
