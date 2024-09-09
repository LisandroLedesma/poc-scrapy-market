from scrapy import signals
from scrapy.exceptions import NotConfigured


class SeleniumMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # Esta función es llamada por Scrapy para crear el middleware.
        ext = cls()

        # Conectar las señales de Scrapy para saber cuándo se ha terminado de procesar
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        return ext

    def process_spider_output(self, response, result, spider):
        # Aquí es donde puedes procesar los resultados devueltos por los métodos del spider.
        for item in result:
            yield item

    def spider_closed(self, spider):
        # Este método se ejecuta cuando se cierra el spider.
        if hasattr(spider, 'close_driver'):
            spider.close_driver()