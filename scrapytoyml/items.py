# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class Offer(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = Field()   # уникальный идентификатор модели во всей коллекции
    _group_id = Field()  # идентификатор модели сли несколько разных вариантов одной модели
    _available = Field()
    typePrefix = Field()    # тип мебели
    categoryId = Field()
    vendor =  Field()   # производитель
    model = Field()
    description = Field()   # описание модели
    url = Field()
    price = Field()
    currencyId = Field()
    country_of_origin = Field()
    picture = Field()
    sales_notes = Field()
    p_series = Field(name="Линейка")    #  товарная линейка
    p_upholstery = Field(name="Обивка")    # обивка
    p_filler = Field(name="Наполнение")    #  наполнение
    p_material = Field(name="Материал")   #   материал элементов конструкции
    p_color = Field(name="Цвет") # цвет
    p_wood_type = Field(name="Цвет дерева") # тип деревянной поверхности
    p_transformation = Field(name="Механизм трансформации")    # система трансформации
    p_suspension = Field(name="Пружинный блок")    # пружина
    p_modular = Field(name="Модульный")  # модульная система
    p_box = Field(name="Ящик для белья")  # ящик для белья
    p_armrests = Field(name="Подлокотники") # подлокотники
    p_corner = Field(name="Угловой")   # угловой диван
    #p_recliner = Field(name="Кресло-реклайнер") # кресло-реклайнер
    p_width = Field(name="Ширина")
    p_depth = Field(name="Глубина")
    p_height = Field(name="Высота")
    p_sleep_width = Field(name="Ширина спального места")   # ширина спального места
    p_sleep_depth = Field(name="Глубина спального места")   # глубина спального места