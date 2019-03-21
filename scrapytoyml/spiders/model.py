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
    transform_types = ['Без механизма', 'Дельфин', 'Книжка', "Еврокнижка", "Клик-кляк",
                       "Раскладушка", "Седафлекс", "Выкатной", "Гессен", "Пантограф (Тик-так)",
                       "Лит", "Реклайнер", "Еврософа"]

    def __init__(self, name=None, **kwargs):
        super(ModelSpider, self).__init__(name, **kwargs)
        self.typePrefixes = {'подушка':None,
                             'модульная система':'Модульные диваны',
                             'пуф':'Пуфы и банкетки',
                             'кухонный диван':'Кушетки',
                             'кресло':'Кресла и мешки',
                             'диван':'Прямые диваны',
                             'угловой диван':'Угловые диваны'
                             }
        self.categoryIds = {'Прямые диваны':'101', 'Угловые диваны':'102', 'Модульные диваны':'104',
                            'Кресла и мешки':'105', 'Пуфы и банкетки':'106','Кушетки':'107'}

    def parse(self, response):
        for href in response.css('div[id*=catalog-block]').css('a.product-name::attr(href)').getall():
            yield response.follow(href, self.parse_type)
            #yield scrapy.Request(response.urljoin(href), self.parse_model)

    def parse_type(self, response):
        t = self.typePrefixes[response.css('div[id*=product-header]').css('span::text')[1].get().lower()]
        if t == 'Прямые диваны':
            return self.parse_sofa(response)
        if t == 'Угловые диваны':
            return self.parse_corner(response)
        if t == 'Модульные диваны':
            return self.parse_sofa(response)
        elif t == 'Кресла и мешки':
            return self.parse_chair(response)
        elif t == 'Пуфы и банкетки':
            return self.parse_puf(response)
        elif t == 'Кушетки':
            return self.parse_couch(response)
        else:
            return

    def parse_puf(self, response):
        item = Offer()
        base_url = response.css('base::attr(href)').get()
        self._id_generator +=1
        product_header = response.css('div[id*=product-header]').css('span::text')[1].get().lower()
        item['currencyId'] = 'RUR'
        item['typePrefix'] = self.typePrefixes[product_header]
        item['categoryId'] = self.categoryIds[item['typePrefix']]
        item['url'] = response.url
        item['vendor'] = "Треви"
        item['_id'] = str(self._id_generator)
        item['_available'] = 'Под заказ'
        item['model'] = response.css('div[id*=product-header]').css('span::text').get()
        item['price'] = ""
        item.fields['price'] = {"from": "true"}
        item['old_price'] = ""
        item['description'] = "\n".join(response.css('div[id*=description-text]').css('p.bottom-text span::text').getall())
        picture = [urljoin(base_url, response.css('p.center img::attr(src)').get())]
        picture.extend(map(lambda x: urljoin(base_url, x), response.css('div[id*=foto-block] img::attr(src)').getall()))
        item['picture'] = picture[0]
        item['picture_1'] = picture[1] if len(picture)>1 else ""
        item['picture_2'] = picture[2] if len(picture)>2 else ""
        item['picture_3'] = picture[3] if len(picture)>3 else ""
        item['picture_4'] = picture[4] if len(picture)>4 else ""
        item['p_color'] = 'Любой'
        item['p_upholstery'] = "Ткань"
        item['p_cloth'] = ''
        item['country_of_origin'] = 'Беларусь'
        item['p_depth'] = ''
        item['p_width'] = ''
        item['p_height'] = ''
        item['p_box'] = 'Нет'
        item['p_remcover'] = 'Нет'
        item['p_series'] = item['model']
        item['p_filler'] = ""
        item['p_material'] = ""

        for tech in response.css('div[id*=tech-description-list]').css('p.bottom-text span::text').getall():
            if re.search(r'ниш[аи] для белья|хранения', tech):
                item['p_box'] = 'Да'
            re_filler = re.search(r'(пенополиуретан)', tech)
            if re_filler:
                item['p_filler'] = re_filler.group(1)
        return item

    def parse_couch(self, response):
        item = self.parse_puf(response)
        item['p_transform'] = 'Нет'
        item['p_transformation'] = "Без механизма"
        item['p_sleep_width'] = ''
        item['p_sleep_length'] = ''
        item['p_armrests'] = 'Нет'
        item['p_pillows'] = 'Нет'

        for tech in response.css('div[id*=tech-description-list]').css('p.bottom-text span::text').getall():
            re_trans = re.search(r'механизм\s+трансформации[ -"–«]*(\w+)[– »]*', tech)
            if re_trans:
                item['p_transform'] = 'Да'
                item['p_transformation'] = "Уникальная разработка"
                for transform_type in self.transform_types:
                    if transform_type.lower() in re_trans.group(1):
                        item['p_transformation'] = transform_type
                        break
            if re.search(r'подлокотник(и|ов)*', tech):
                item['p_armrests'] = 'Да'
            if re.search(r'пружина', tech):
                item['p_suspension'] =  'Да'
        return item

    def parse_sofa(self, response):
        item = self.parse_couch(response)
        item['p_bar'] = 'Нет'
        item['p_usb'] = 'Нет'
        if re.search('бар', item['description'].lower()):
            item['p_bar'] = 'Да'

        if re.search('usb', item['description'].lower()):
            item['p_usb'] = 'Да'
        return item

    def parse_chair(self, response):
        item = self.parse_sofa(response)
        item['p_chair'] = 'Кресло'
        return item

    def parse_corner(self, response):
        item = self.parse_sofa(response)
        item['p_corner'] = 'Универсальный'
        return item
