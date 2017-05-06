# -*- coding: utf-8 -*-
import scrapy
from ..items import JsItem


class JsSpider(scrapy.Spider):
    name = 'js'
    allowed_domains = ["www.jianshu.com"]
    start_urls = ['http://www.jianshu.com']
    start_user = '8bad6e09c3c3'

    user_url = 'http://www.jianshu.com/users/{user}'
    followers_url = 'http://www.jianshu.com/users/{user}/followers?page={page}'
    following_url = 'http://www.jianshu.com/users/{user}/following?page={page}'

    def start_requests(self):
        yield scrapy.Request(url=self.user_url.format(user=self.start_user), callback=self.parse)

    def parse(self, response):
        item = JsItem()
        selector = scrapy.Selector(response)
        user_token = selector.xpath('//a[@class="name"]/@href[starts-with(.,"/u")]').extract_first()

        item['url_token'] = user_token.split('/')[-1]
        item['name'] = selector.xpath('//div[@class="title"]/a/text()').extract_first()

        user_info = selector.xpath('//div[@class="meta-block"]//p/text()').extract()
        user = [int(index) for index in user_info]
        item['following_count'] = user[0]
        item['followers_count'] = user[1]
        item['articles_count'] = user[2]
        item['words_count'] = user[3]
        item['like_count'] = user[4]
        yield item

        for page in range(1, item['following_count']//9+2):
            yield scrapy.Request(url=self.followers_url.format(user=item['url_token'], page=page),
                                 callback=self.parse_followers)
        for page in range(1, item['followers_count']//9+2):
            yield scrapy.Request(url=self.following_url.format(user=item['url_token'], page=page),
                                 callback=self.parse_following)

    def parse_followers(self, response):
        users = response.xpath('(//a[@class="name"]/@href[starts-with(.,"/u")])[position()>1]').extract()
        for user in users:
            yield scrapy.Request(url=self.user_url.format(user=user.split('/')[-1]), callback=self.parse)

    def parse_following(self, response):
        users = response.xpath('(//a[@class="name"]/@href[starts-with(.,"/u")])[position()>1]').extract()
        for user in users:
            yield scrapy.Request(url=self.user_url.format(user=user.split('/')[-1]), callback=self.parse)
