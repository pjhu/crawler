# -*- coding: utf-8 -*-
import json
import scrapy
from ..items import TutorialItem


class ZhSpider(scrapy.Spider):
    name = "zh"
    start_user = "pengjinhu"
    user_request_data = '?include=url_token,name,gender,following_count,follower_count,' \
                        'following_columns_count,following_topic_count,articles_count'

    follow_request_data = "?include=data[*].url_token"

    def start_requests(self):
        user_url = ''.join(['https://www.zhihu.com/api/v4/members/', self.start_user, self.user_request_data])
        yield scrapy.Request(url=user_url, callback=self.parse)

    def parse(self, response):
        user = json.loads(response.body.decode('UTF-8'))
        item = TutorialItem()
        for field in item.fields:
            if field in user.keys():
                item[field] = user[field]
        yield item

        followers_url = ''.join(['https://www.zhihu.com/api/v4/members/',
                                 user['url_token'], '/followers', self.follow_request_data, '&offset=0&limit=20'])
        yield scrapy.Request(url=followers_url, callback=self.parse_followers)

        followees_url = ''.join(['https://www.zhihu.com/api/v4/members/',
                                 user['url_token'], '/followees', self.follow_request_data, '&offset=0&limit=20'])
        yield scrapy.Request(url=followees_url, callback=self.parse_followees)

    def parse_followers(self, response):
        followers = json.loads(response.body.decode('UTF-8'))
        for user in followers['data']:
            # exclude no url_token user, such as name is \u77e5\u4e4e\u7528\u6237(zhihuyonghu)
            if user['url_token']:
                followers_url = ''.join(['https://www.zhihu.com/api/v4/members/',
                                         user['url_token'], self.user_request_data])
                yield scrapy.Request(url=followers_url, callback=self.parse)
        if 'paging' in followers.keys() and followers.get('paging').get('is_end') == False:
            yield scrapy.Request(url=followers.get('paging').get('next'), callback=self.parse_followers)

    def parse_followees(self, response):
        followees = json.loads(response.body.decode('UTF-8'))
        for user in followees['data']:
            print(user['url_token'])
            # exclude no url_token user, such as name is \u77e5\u4e4e\u7528\u6237(zhihuyonghu)
            if user['url_token']:
                followees_url = ''.join(['https://www.zhihu.com/api/v4/members/',
                                         user['url_token'], self.user_request_data])
                yield scrapy.Request(url=followees_url, callback=self.parse)
        if 'paging' in followees.keys() and followees.get('paging').get('is_end') == False:
            yield scrapy.Request(url=followees.get('paging').get('next'), callback=self.parse_followees)


