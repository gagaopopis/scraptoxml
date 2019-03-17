# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urljoin
from scrapytoyml.items import Offer


class ModelSpider(scrapy.Spider):
    name = 'model'
    #allowed_domains = ['http://trevi.by']
    start_urls = ['http://trevi.by/katalog-mebeli']

    _id_generator = 0
    group_ids = {}
    _group_id_generator = 0

    def parse(self, response):
        for href in response.css('div[id*=catalog-block]').css('a.product-name::attr(href)')[0].getall():
            yield response.follow(href, self.parse_model)
            #yield scrapy.Request(response.urljoin(href), self.parse_model)

    def parse_model(self, response):
        item = Offer()
        base_url = response.css('base::attr(href)').get()
        self._id_generator +=1
        item['_id'] = str(self._id_generator)
        item['model'] = response.css('div[id*=product-header]').css('span::text').get()
        item['typePrefix'] = response.css('div[id*=product-header]').css('span::text')[1].get()
        item['url'] = response.url
        item['vendor'] = "Треви"
        item['description'] = response.css('div[id*=description-text]').css('p.bottom-text span::text').get()
        item['picture'] = [urljoin(base_url, response.css('p.center img::attr(src)').get())]
        for imgs in response.css('div[id*=foto-block] img::attr(src)').getall():
            item['picture'].append(urljoin(base_url, imgs))
        item['categoryId'] = ""
        item['price'] = ""
        item.fields['price'] = {"from":"true"}
        item['currencyId'] = 'RUR'
        item['country_of_origin'] = 'Беларусь'
        #item['sales_notes'] = ""
        item['p_series'] = ""
        item['p_upholstery'] = ""
        item['p_filler'] = ""
        item['p_material'] = ""
        item['p_transformation'] = "нет"
        item['p_suspension'] = "нет"
        item['p_modular'] = "да" if 'модульная' in item['typePrefix'].lower() else "нет"
        item['p_corner'] = 'да' if 'угловой' in item['typePrefix'].lower() else "нет"
        item['p_box'] = 'нет'
        item['p_armrests'] = 'нет'
        #item['p_recliner'] = 'нет'
        item['p_width'] = ''
        item['p_depth'] = ''
        item['p_height'] = ''
        #item['p_sleep_width'] = ''
        #item['p_sleep_depth'] = ''

        for tech in response.css('div[id*=tech-description-list]').css('p.bottom-text span::text').getall():
            if re.search(r'ниш[аи] для белья|хранения', tech):
                item['p_box'] = 'есть'
            re_filler = re.search(r'(пенополиуретан)', tech)
            if re_filler:
                item['p_filler'] = re_filler.group(1)
            re_trans = re.search(r'механизм\s+трансформации[ -"–«]*(\w+)[– »]*', tech)
            if re_trans:
                item['p_transformation'] = re_trans.group(1)
            if re.search(r'пружина', tech):
                item['p_suspension'] =  'есть'
            #if re.search('реклайнер', tech):
            #    item['p_recliner'] = 'да'

        return item
