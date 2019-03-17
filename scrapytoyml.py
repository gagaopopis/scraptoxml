# -*- coding: utf-8 -*-\
#!/usr/bin/env /home/pasha/workspace/workspace-py/scrap_to_yandexyml/.venv/bin/python

import xml.etree.ElementTree as ET
import xml.dom.minidom
import datetime
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

xml_file_name = os.path.join(os.path.dirname(__file__), "catalog.xml")

def build_root_xml():
    tree = ET.ElementTree()
    root = ET.Element('yml_catalog', attrib={'date':"{0:%Y-%m-%d %H:%M}".format(datetime.datetime.now())})
    root.text='\n'
    tree._setroot(root)
    tree.write(xml_file_name, encoding='utf-8', xml_declaration=True)

def add_shop_to_xml():
    tree = ET.parse(xml_file_name)
    root = tree.getroot()
    shop = ET.SubElement(root, 'shop')
    name = ET.SubElement(shop, 'name')
    name.text = "Треви"
    company = ET.SubElement(shop, 'company')
    company.text = 'ООО Ферст'
    url = ET.SubElement(shop, 'url')
    url.text = "http://trevi.by"
    currencies = ET.SubElement(shop, 'currencies')
    currency = ET.SubElement(currencies, 'currency', attrib={'id':'RUR', 'rate':"1"})
    categories = ET.SubElement(shop, 'categories')
    category = ET.SubElement(categories, 'category', attrib={'id':"1"})
    category.text = "Мягкая мебель"
    delivery = ET.SubElement(shop, 'delivery-options')
    ET.SubElement(delivery, 'option', attrib={'cost':"5000", 'days':""})
    tree.write(xml_file_name, encoding='utf-8', xml_declaration=True)
    
def main2():
    #build_root_xml()
    #add_shop_to_xml()
    dom = xml.dom.minidom.parse(xml_file_name)
    pretty_xml_as_string = dom.toprettyxml()
    print(pretty_xml_as_string)


def main():
    os.remove(xml_file_name)
    s = get_project_settings()
    s.set('XMLFILE', xml_file_name, priority='project')
    process = CrawlerProcess(s)

    # 'followall' is the name of one of the spiders of the project.
    process.crawl('model')
    process.start()  # the script will block here until the crawling is finished

if __name__ == '__main__':
    main()
    main2()