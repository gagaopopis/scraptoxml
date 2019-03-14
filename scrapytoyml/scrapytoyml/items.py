# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class Offer(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = Field()
    group_id = Field()
    availability = Field(default="false")
    _type = "vendor.model"
    typePrefix = Field()
    vendor =  Field()
    model = Field()
    description = Field()
    ulr = Field()
    price = Field()
    currencyId = Field(default='RUR')
    country_of_origin = Field(default="Беларусь")
    picture = Field()
    series = Field()
    upholstery = Field()
    filler = Field()
    matrial = Field()
    color = Field()
    wood_type = Field()
    transformation = Field()
    suspension = Field()
    suspension_type = Field()
    modular = Field(default='нет')
    box = Field(default='нет')
    armrests = Field(default='нет')
    corner = Field(default='нет')
    width = Field()
    depth = Field()
    height = Field()
    sleep_width = Field()
    sleep_depth = Field()