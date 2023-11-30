from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from kamijul.items import KamijulItem
from scrapy.exceptions import CloseSpider


class  kamijul(CrawlSpider):
    name = 'mykamijul'
    allowed_domains = ['books.toscrape.com']
    item_count = 0

    start_urls = ['https://books.toscrape.com/catalogue/category/books_1/']
    
    rules = (
        #Rule(LinkExtractor(allow="catalogue/category/books/")),
        #se crean estas reglas para que pueda buscar entre las paginas y entre los libros a la vista
        Rule(LinkExtractor(allow=(), restrict_xpaths = ('//li[@class="next"]/a'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths = ('//h3/a')), callback='parse_item', follow=False),
        #Rule(LinkExtractor(allow=(), restrict_xpaths = ('//h3/a')), callback='parse_item', follow=False),
        
        #Rule(LinkExtractor(allow=(), restrict_xpaths = ('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li[1]/article/h3/a')), callback='parse_item', follow=False),
        #Rule(LinkExtractor(allow="catalogue" , deny="category"), callback="parse_item"),

    )
    
    def parse_item(self, response):
        libro_item = KamijulItem()
        #se obtiene el titulo y la categoria por medio de xpath
        libro_item['titulo'] = response.xpath('normalize-space(//h1/text())').extract()
        libro_item['categoria'] = response.xpath('normalize-space(//*[@id="default"]/div/div/ul/li[3]/a/text())').extract()
        
        #quitamos el simbolo £ para que solo quede el precio y lo convertimos a float
        precios_limpiar = response.css('.price_color::text').get().replace('£','')
        precios_enteros = float(precios_limpiar)
        libro_item['precio'] = precios_enteros
        
        #limpiamos el texto innecesario para despues convertir la cantidad a enteros
        cantidad_limpiar = response.css('.availability::text')[1].get().replace('\n', '').replace(' ', '').replace('Instock(','').replace('available)', '')
        cantidad_enteros = int(cantidad_limpiar)
        libro_item['cantidad'] = cantidad_enteros
        
        #este es un contador para tomar la cantidad en este caso de libros con sus atributos que indique el if
        self.item_count += 1
        if self.item_count > 500:
            raise CloseSpider('item_exceeded')
        yield libro_item

#//li[@class="next"]/a LINK A LA SIGUIENTE PAGINA
#//h3[@class] LINK A LOS LIBROS 
#//h1 TOMAR EL TITULO DEL LIBRO
#//p[@class="price_color"] EL PRECIO DEL LIBRO
#//*[@id="default"]/div/div/ul/li[3]/a/text() TOMAR LA CATEGORIA DEL LIBRO
#//*[@id="content_inner"]/article/table/tbody/tr[6]/td CANTIDAD DE LIBROS DISPONIBLES
