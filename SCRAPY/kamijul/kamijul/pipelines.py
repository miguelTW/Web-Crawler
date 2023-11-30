# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
from scrapy import Request
import csv

import pandas as pd
import matplotlib.pyplot as plt

class KamijulPipeline(object):
    def __init__(self):
        self.files = {}
        self.items = []
    
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline
    
    def spider_opened(self, spider):
        file = open('%s_items41.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ['titulo', 'precio', 'categoria', 'cantidad']
        self.exporter.start_exporting()
        
    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
    
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        self.items.append(dict(item))
        return item
    
    
    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        #df = pd.DataFrame('%s_items40.csv' % spider.name)
        #df = pd.read_csv('mykamijul_items41.csv')
        
        #se crea una grafica tipo pastel de las categorias y su porcentaje
        datos = df['categoria'].value_counts(normalize=True) * 100
        plt.figure(figsize=(9,9))
        plt.pie(datos, labels=datos.index, autopct='%1.1f%%')
        plt.title('Grafico de Categorias')
        plt.savefig('grafico.png')
        plt.show()
        
        #hacer una descripcion de la columna categoria
        datos = df['categoria'].describe()
        datos_describe = pd.DataFrame(datos)
        datos_describe.to_csv('estadisticas_categoria.csv', header=True)
        
        #hacer una descripcion de la columna precio
        datos = df['precio'].describe()
        datos_describe = pd.DataFrame(datos)
        datos_describe.to_csv('estadisticas_precio.csv', header=True)
        
        #cual es el libro con mas cantidad de disponibles
        datos = df.loc[df['cantidad'].idxmax()]
        datos_maximo = pd.DataFrame(datos)
        datos_maximo.to_csv('maximoid.csv', header=True)
        
        #cual es libro mas caro
        datos = df.loc[df['precio'].idxmax()]
        datos_precio = pd.DataFrame(datos)
        datos_precio.to_csv('maximo_precio.csv', header=True)
        
        #cual es la categoria en donde hay mas libros diferentes y los guarda en un archivo .csv
        datos_categoria = df['categoria'].value_counts()
        categoria_max = datos_categoria.idxmax()
        total_categoria_lib = datos_categoria.max()
        categoria_max_lib = df[df['categoria'] == categoria_max]
        
        categoria_max_lib.to_csv('categoria_max_lib.csv', header=True)
        #print(df.describe())
        #df.to_csv(f"{spider.name}_items_analysis.csv", index=False)
    #def process_item(self, item, spider):
    #   return item

