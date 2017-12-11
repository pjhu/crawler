# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from ..items import JigsawItem


class People(scrapy.Spider):
    name = 'jigsaw'
    url = 'https://jigsaw.thoughtworks.net'
    cookie = {'_jigsaw_session': '5a585a1d059be25987cd33da3b15a3af'}
    skills = ['Organisational+Transformation', 'Strategy', 'Financial+model+Advisory',
              'Value+Driven+Portfolio+Management+%28Edge%29', 'Executive+Advisory']

    def start_requests(self):
        for i in range(1, 6):
            for skill in self.skills:
                skill_url = self.url + '/consultants/search?utf8=✓&criteria%5Bfree_text%5D=&criteria%5Bassignment_' \
                                       'on%5D=&criteria%5Bwork_in_office%5D=ConsultantStaffingInOffice&criteria' \
                                       '%5Bbusiness_unit%5D=10061%2C10081%2C10121%2C10201%2C10220%2C10361%2C10364' \
                                       '%2C10400%2C10401%2C10402%2C10403%2C10461%2C10481%2C10541%2C199495847' \
                                       '%2C568772936%2C637217163%2C868334766%2C1649050217%2C1767921759%3AALL&' \
                                       'criteria%5Boffice%5D=10000%2C10020%2C10062%2C10082%2C10100%2C10122' \
                                       '%2C10140%2C10141%2C10202%2C10221%2C10240%2C10280%2C10300%2C10340%2C10362' \
                                       '%2C10365%2C10380%2C10420%2C10421%2C10422%2C10440%2C10462%2C10482%2C10483' \
                                       '%2C10500%2C10520%2C22270260%2C37774119%2C56723499%2C238263284%2C274224486' \
                                       '%2C572949587%2C737701363%2C941368446%2C1043881161%2C1251963107%2C1258037696' \
                                       '%2C1298141972%2C1353005657%2C1405963073%2C1519613848%2C1589838442' \
                                       '%2C1687817654%2C1783454458%2C1850820317%2C1904399856%2C1904805734' \
                                       '%2C1904805743%2C2004939589&criteria%5Brole%5D=&criteria' \
                                       '%5Bgrade%5D%5B%5D=10080&criteria%5Bgrade%5D%5B%5D=1690207768&' \
                                       'criteria%5Bgrade%5D%5B%5D=421965466' \
                                       '&criteria%5Bgrade%5D%5B%5D=793282783&criteria' \
                                       '%5Bgrade%5D%5B%5D=226178682&criteria%5Bgrade%5D%5B%5D=323252734' \
                                       '&criteria%5Bgrade%5D%5B%5D=10060%2C10061%2C10062%2C10063%2C10000%2C10004' \
                                       '%2C10026%2C10027%2C10029&criteria%5Btotal_years_of_experience%5D=&criteria' \
                                       '%5Btw_years_of_experience%5D=&criteria%5Bshow_all%5D=0&criteria%5Bshow_all' \
                                       '%5D=true&criteria%5Bskills%5D%5B' + str(i) + '%5D%5B%5D=' + skill + \
                            '&criteria%5Brm_profile%5D=&criteria%5Bassignable' \
                            '%5D=include_nonassignable_twer&ajax_update' \
                            '=consultant_search_results&view=general_view&commit=Search'
                yield scrapy.Request(url=skill_url, cookies=self.cookie, meta={'skill': skill}, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(response)
        print("current page: ", selector.xpath('//em[@class="current"]/text()').extract_first())
        users = selector.xpath('//tr[contains(@class, "odd") or contains(@class, "even")]')
        for user in users:
            url = user.xpath('.//a/@href').extract_first().strip()
            yield scrapy.Request(url=self.url+url, cookies=self.cookie, meta={'skill': response.meta['skill']},
                                 callback=self.parse_profile)
        next_page = selector.xpath('//*[@class="next_page"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(url=self.url + next_page, cookies=self.cookie, meta={'skill': response.meta['skill']},
                                 callback=self.parse)

    def parse_profile(self, response):
        selector = scrapy.Selector(response)
        item = JigsawItem()
        item['capability'] = urllib.parse.unquote(response.meta['skill']).replace('+', ' ')
        item['id'] = response.url.split('/')[-1]
        item['name'] = selector.xpath('//div[@id="preferred-name"]/text()').extract_first().strip()
        item['gender'] = selector.xpath('//span[@class="gender"]/text()').extract_first().strip()
        item['role'] = selector.xpath('//span[@id="primary-role"]/text()').extract_first().strip()
        item['grade'] = selector.xpath('//span[@id="grade"]/text()').extract_first().strip()
        offices = selector.xpath('//div[@id="offices-summary"]//em[@class="value"]/text()')
        item['region'] = offices.extract_first().split('-')[-1].strip()
        item['home_office'] = offices[0].extract().split('-')[0].strip()
        item['staffing_office'] = offices[1].extract().split('-')[0].strip()
        item['working_office'] = offices[2].extract().split('-')[0].strip()
        years = selector.xpath('//div[@id="total-experience"]')
        item['total_years'] = years.xpath('./text()').extract_first().split(',')[0].strip()
        item['tw_years'] = years.xpath('./em/text()').extract_first().strip()

        consulting_item = selector.xpath('//div[@class="rating-group"]/h3[text()="Consulting"]/..//li')
        consulting = {}
        for consult in consulting_item:
            name = consult.xpath('.//div/text()').extract_first()
            star = len(consult.xpath('.//div[@class="rating"]/i[contains(@class, "filled-level")]'))
            consulting[name] = star
        item['consulting'] = consulting
        yield item


