# -*- coding: utf-8 -*-
import scrapy


class ModelSpider(scrapy.Spider):
    name = 'model'
    #allowed_domains = ['http://trevi.by']
    start_urls = ['http://trevi.by/katalog-mebeli']

    def parse(self, response):
        for href in response.css('div[id*=catalog-block]').css('a.product-name::attr(href)').getall():
            yield response.follow(href, self.parse_model)
            #yield scrapy.Request(response.urljoin(href), self.parse_model)

    def parse_model(self, response):
        model = response.css('div[id*=product-header]').css('span::text').get()
        _type = response.css('div[id*=product-header]').css('span::text')[1].get()
        yield {'model': model, 'type': _type}
