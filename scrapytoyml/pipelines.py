# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xml.etree.ElementTree as ET
import datetime

class ItemXMLPipeline(object):

    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        self.tree = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(xmlfile=crawler.settings.get('XMLFILE'))

    def open_spider(self, spider):
        try:
            self.tree = ET.parse(self.xmlfile)
        except FileNotFoundError:
            self.tree = ET.ElementTree()
            root = ET.Element('yml_catalog', attrib={'date': "{0:%Y-%m-%d %H:%M}".format(datetime.datetime.now())})
            shop = ET.SubElement(root, 'shop')
            self.tree._setroot(root)

    def close_spider(self, spider):
        self.tree.write(self.xmlfile, encoding='utf-8', xml_declaration=True)

    def process_item(self, item, spider):
        shop = self.tree.find('shop')
        offer = ET.SubElement(shop, 'offer', attrib={"id":item['_id'],
                                                     'type': "vendor.model",
                                                     'group_id': item.get('_group_id', default=''),
                                                     'available':item.get('_available',default='false')
                                                     }
                              )
        for key in (x for x in item.keys() if not x.startswith("_")):
            value = item.get(key)
            if isinstance(value, list):
                for l in value:
                    p = ET.SubElement(offer, key, attrib=item.fields[key])
                    p.text = l
            elif key.startswith("p_"):
                p = ET.SubElement(offer, 'param', attrib=item.fields[key])
                p.text = value
            else:
                p = ET.SubElement(offer, key, attrib=item.fields[key])
                p.text = value

        """
        typePrefix = ET.SubElement(offer, 'typePrefix')
        typePrefix.text = item.get('typePrefix')
        categoryId = ET.SubElement(offer, 'categoryId')
        categoryId.text = item.get('categoryId', default="")
        vendor = ET.SubElement(offer, 'vendor')
        vendor.text=item.get('vendor')
        model = ET.SubElement(offer, 'model')
        model.text = item.get('model')
        description = ET.SubElement(offer, 'description')
        description.text = item.get('description')
        url = ET.SubElement(offer, 'url')
        url.text=item.get('url', default="")
        for pic in item.get('picture', default=""):
            p = ET.SubElement(offer, 'picture')
            p.text = pic
        price = ET.SubElement(offer, 'price', attrib={'from':"true"})
        price.text=item.get('price', default="")
        currency = ET.SubElement(offer, 'currencyId')
        currency.text = item.get('currencyId', default='RUR')
        country = ET.SubElement(offer, 'country_of_origin')
        country.text=item.get('country_of_origin', default='Беларусь')
        notes = ET.SubElement(offer, 'sales_notes')
        notes.text=item.get('sales_notes', default="")
        p_series = ET.SubElement(offer, 'param', attrib={"name":"Линейка"})
        p_series.text=item.get('p_series', default="")
        p_modular = ET.SubElement(offer, 'param', attrib={"name":"Модульный"})
        p_modular.text=item.get('p_modular', default='нет')
        p_corner = ET.SubElement(offer, 'param', attrib={"name":"Угловой"})
        p_corner.text = item.get('p_corner', default='нет')
        ET.SubElement(offer, 'param', attrib={"name":"Механизм трансформации"})
        text = item.get('p_transformation', default="")
        ET.SubElement(offer, 'param', attrib={"name":"Обивка"}, text=item.get('p_upholstery', default=""))
        ET.SubElement(offer, 'param', attrib={"name":"Наполнитель"}, text=item.get('p_filler', default=""))
        ET.SubElement(offer, 'param', attrib={"name":"Материал"}, text=item.get('p_material', default=""))
        ET.SubElement(offer, 'param', attrib={"name":"Пружинный блок"}, text=item.get('p_suspension', default='нет'))
        ET.SubElement(offer, 'param', attrib={"name":"Ящик для белья"}, text=item.get('p_box', default='нет'))
        ET.SubElement(offer, 'param', attrib={"name":"Подлокотники"}, text=item.get('p_armrests', default='нет'))
        if item['p_modular'] == 'да':
            ET.SubElement(offer, 'param', attrib={"name": "Ширина от", 'unit':'см'}, text=item.get('p_width', default=""))
            ET.SubElement(offer, 'param', attrib={"name": "Ширина до", 'unit':'см'}, text=item.get('p_width', default=""))
            ET.SubElement(offer, 'param', attrib={"name": "Глубина от", 'unit':'см'}, text=item.get('p_depth', default=""))
            ET.SubElement(offer, 'param', attrib={"name": "Глубина до", 'unit':'см'}, text=item.get('p_depth', default=""))
            ET.SubElement(offer, 'param', attrib={"name": "Ширина спального места от", 'unit':'см'}, text=item.get('p_sleep_width', default=""))
            ET.SubElement(offer, 'param', attrib={"name": "Глубина спального места от", 'unit':'см'}, text=item.get('p_sleep_depth', default=""))
        else:
            ET.SubElement(offer, 'param', attrib={"name": "Ширина", 'unit': 'см'}, text=item.get('p_width', default=""))
            ET.SubElement(offer, 'param', attrib={"name": "Глубина", 'unit':'см'}, text=item.get('p_depth', default=""))
            ET.SubElement(offer, 'param', attrib={"name": "Ширина спального места", 'unit': 'см'},
                          text=item.get('p_sleep_width', default=""))
            ET.SubElement(offer, 'param', attrib={"name": "Глубина спального места", 'unit': 'см'},
                          text=item.get('p_sleep_depth', default=""))
        ET.SubElement(offer, 'param', attrib={"name": "Высота", 'unit':'см'}, text=item.get('p_height', default=""))
        """
        return item
