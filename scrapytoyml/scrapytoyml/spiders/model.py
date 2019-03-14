# -*- coding: utf-8 -*-
import scrapy


class ModelSpider(scrapy.Spider):
    name = 'model'
    #allowed_domains = ['http://trevi.by']
    start_urls = ['http://trevi.by/katalog-mebeli']

    _id_generator = 0
    group_ids = {}
    _group_id_generator = 0

    def parse(self, response):
        for href in response.css('div[id*=catalog-block]').css('a.product-name::attr(href)').getall():
            yield response.follow(href, self.parse_model)
            #yield scrapy.Request(response.urljoin(href), self.parse_model)

    def parse_model(self, response):
        self._id_generator +=1
        _id = str(self._id_generator)
        model = response.css('div[id*=product-header]').css('span::text').get()
        if model not in group_ids.keys():
            self._group_id_generator += 1
            group_id = str(self._group_id_generator)
            self.group_ids[model] = group_id
            group_id = self._group_id_generator
        else:
            group_id = self.group_ids[model]

        typePrefix = response.css('div[id*=product-header]').css('span::text')[1].get()
        url = response.url
        vendor = "Треви"
        description = response.css('div[id*=description-text]').css('p.bottom-text span::text').get()
        if 'модульная' in typePrefix:
            modular = 'да'
        if 'угловой' in typePrefix:
            corner = 'да' 
        for tech in response.css('div[id*=tech-description-list]').css('p.bottom-text span::text').getall():
            if re.search(r'ниш[аи] для белья|хранения', tech):
                pass
            re_filler = re.search(r'(пенополиуретан)', tech)
            if re_filler:
                filler = re_filler.group(1)
            re_trans = re.search(r'трансформации|механизм\s*-\s*\"(\w)\"', tech)
            if re_trans:
                transformation = re_trans.group(1)             
            if re.search(r'пружина', tech):
                pass 
        picture = [response.css('div[id*=product-header]').css('img::src').get()]
        for imgs in response.css('div[id*=foto-block]').css('ims::src')[0-3].getall():
            picture.append(imgs)
        yield {'model': model, 'typePrefix': typePrefix, 'url':url, 'description':description,
        'picture':picture}
