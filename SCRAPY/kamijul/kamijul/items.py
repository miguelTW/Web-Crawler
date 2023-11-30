# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KamijulItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #agregamos los items que vamos a utilizar 
    titulo = scrapy.Field()
    precio = scrapy.Field()
    categoria = scrapy.Field()
    cantidad = scrapy.Field()
    
    pass
