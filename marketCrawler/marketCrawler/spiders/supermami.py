from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from ..items import SuperMamiItem

class SupermamiSpider(CrawlSpider):
    name = "supermami"
    allowed_domains = ["dinoonline.com.ar"]
    start_urls = ["https://www.dinoonline.com.ar/super/categoria/supermami-almacen/_/N-1tjm8rd"]

    rules = (
        Rule(LinkExtractor(allow=(r".*/super/categoria/supermami-almacen-conservas*",), deny=(r".*/brand-*",))),
        Rule(LinkExtractor(allow=(r".*/super/producto/*",)), callback="parse_item"),
    )

    def parse_item(self, response):
        """
         response.css("h1.texto_titulo_prod_dest::text").get()
         response.css('div.precio-unidad span::text').get()
         response.css("td.productInfo::text").get()
        """
        l = ItemLoader(item=SuperMamiItem(), response=response)
        l.add_css("name", "h1.texto_titulo_prod_dest::text")
        l.add_css("price", "div.precio-unidad span::text")
        l.add_css("brand", "td.productInfo::text")
        l.add_value("branch", "San Vicente")
        return l.load_item()
