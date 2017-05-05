# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    url_token = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    following_count = scrapy.Field()
    follower_count = scrapy.Field()
    following_columns_count = scrapy.Field()
    following_topic_count = scrapy.Field()
    articles_count = scrapy.Field()
