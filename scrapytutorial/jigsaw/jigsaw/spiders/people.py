# -*- coding: utf-8 -*-
import scrapy
from ..items import JigsawItem


class People(scrapy.Spider):
    name = 'jigsaw'
    url = 'https://jigsaw.thoughtworks.net'
    cookie = {'_jigsaw_session': 'xxxxxxxxxxxxxx'}

    def start_requests(self):
        first_page = '/consultants/search?utf8=%E2%9C%93&criteria[free_text]=&criteria[assignment_on]=&' \
                     'criteria[work_in_office]=ConsultantStaffingInOffice' \
                     '&criteria[business_unit]=10061,10081,10121,10201,10220,10361,10364,10400,10401,10402,10403,' \
                     '10461,10481,10541,199495847,568772936,637217163,868334766,1649050217,1767921759:ALL' \
                     '&criteria[office]=10000,10020,10062,10082,10100,10122,10140,10141,10202,10221,10240,10280,' \
                     '10300,10340,10362,10365,10380,10420,10421,10422,10440,10462,10482,10483,10500,10520,22270260,' \
                     '37774119,56723499,238263284,274224486,572949587,737701363,941368446,1043881161,1251963107,' \
                     '1258037696,1298141972,1353005657,1405963073,1519613848,1589838442,1687817654,1783454458,' \
                     '1850820317,1904399856,1904805734,1904805743,2004939589&criteria[role]=&criteria[grade][]=10080' \
                     '&criteria[grade][]=1690207768&criteria[grade][]=421965466&criteria[grade][]=793282783' \
                     '&criteria[grade][]=226178682&criteria[grade][]=323252734&criteria[grade][]=10060,10061,10062,' \
                     '10063,10000,10004,10026,10027,10029&criteria[total_years_of_experience]=' \
                     '&criteria[tw_years_of_experience]=&criteria[show_all]=0&criteria[show_all]=true' \
                     '&criteria[skills][5][]=Executive%20Advisory&criteria[skills][5][]=Financial%20model%20Advisory' \
                     '&criteria[skills][5][]=Organisational%20Transformation&criteria[skills][5][]=Strategy' \
                     '&criteria[skills][5][]=Value%20Driven%20Portfolio%20Management%20(Edge)' \
                     '&criteria[skills][4][]=Executive%20Advisory&criteria[skills][4][]=Financial%20model%20Advisory' \
                     '&criteria[skills][4][]=Organisational%20Transformation&criteria[skills][4][]=Strategy' \
                     '&criteria[skills][4][]=Value%20Driven%20Portfolio%20Management%20(Edge)' \
                     '&criteria[skills][3][]=Executive%20Advisory&criteria[skills][3][]=Financial%20model%20Advisory' \
                     '&criteria[skills][3][]=Organisational%20Transformation&criteria[skills][3][]=Strategy' \
                     '&criteria[skills][3][]=Value%20Driven%20Portfolio%20Management%20(Edge)' \
                     '&criteria[skills][2][]=Executive%20Advisory&criteria[skills][2][]=Financial%20model%20Advisory' \
                     '&criteria[skills][2][]=Organisational%20Transformation&criteria[skills][2][]=Strategy' \
                     '&criteria[skills][2][]=Value%20Driven%20Portfolio%20Management%20(Edge)' \
                     '&criteria[skills][1][]=Executive%20Advisory&criteria[skills][1][]=Financial%20model%20Advisory' \
                     '&criteria[skills][1][]=Organisational%20Transformation&criteria[skills][1][]=Strategy' \
                     '&criteria[skills][1][]=Value%20Driven%20Portfolio%20Management%20(Edge)&criteria[rm_profile]=' \
                     '&criteria[assignable]=include_nonassignable_twer&ajax_update=consultant_search_results' \
                     '&view=general_view&commit=Search'
        yield scrapy.Request(url=self.url + first_page, cookies=self.cookie, callback=self.parse)

    def parse(self, response):
        selector = scrapy.Selector(response)
        print("current page: ", selector.xpath('//em[@class="current"]/text()').extract_first())
        users = selector.xpath('//tr[contains(@class, "odd") or contains(@class, "even")]')
        for user in users:
            url = user.xpath('.//a/@href').extract_first().strip()
            yield scrapy.Request(url=self.url+url, cookies=self.cookie, callback=self.parse_profile)
        next_page = selector.xpath('//*[@class="next_page"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(url=self.url + next_page, cookies=self.cookie, callback=self.parse)

    def parse_profile(self, response):
        selector = scrapy.Selector(response)
        item = JigsawItem()
        item['name'] = selector.xpath('//div[@id="preferred-name"]/text()').extract_first().strip()
        item['role'] = selector.xpath('//span[@id="primary-role"]/text()').extract_first().strip()
        item['grade'] = selector.xpath('//span[@id="grade"]/text()').extract_first().strip()
        offices = selector.xpath('//div[@id="offices-summary"]//em[@class="value"]/text()')
        item['region'] = offices.extract_first().split('-')[-1].strip()
        item['home_office'] = offices[0].extract().split('-')[0].strip()
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


