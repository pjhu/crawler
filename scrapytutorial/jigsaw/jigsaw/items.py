# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JigsawItem(scrapy.Item):
    # define the fields for your item here like:
    capability = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    role = scrapy.Field()
    grade = scrapy.Field()
    region = scrapy.Field()
    home_office = scrapy.Field()
    staffing_office = scrapy.Field()
    working_office = scrapy.Field()
    total_years = scrapy.Field()
    tw_years = scrapy.Field()
    consulting = scrapy.Field()


class StaffItem(scrapy.Item):
    # define the fields for your item here like:
    file_urls = scrapy.Field()
    files = scrapy.Field()
