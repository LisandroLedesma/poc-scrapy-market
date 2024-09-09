import os
from dotenv import load_dotenv
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .BaseSuperMarket import BaseSupermarketSpider
from ..items import SuperMamiItem

load_dotenv()


class SupermamiSpider(BaseSupermarketSpider):
    name = "supermami"
    allowed_domains = ["dinoonline.com.ar"]
    start_urls = [
        "https://www.dinoonline.com.ar/super/categoria/supermami-almacen-encurtidos-y-escabeche/_/N-1prtbco",
        "https://www.dinoonline.com.ar/super/categoria/supermami-almacen-endulzantes/_/N-6k4dnm",
        "https://www.dinoonline.com.ar/super/categoria/supermami-almacen-arroz-y-pastas-secas/_/N-ku47iy"
    ]

    # Definimos las sucursales conocidas como una lista fija
    branches = os.getenv("BRANCHES").split(",")

    rules = (
        Rule(LinkExtractor(allow=(r".*/super/producto/*",)), callback="parse_item", follow=False),
    )

    def __init__(self, *args, **kwargs):
        super(SupermamiSpider, self).__init__(*args, **kwargs)

        branches = ["Ruta 20", "Sucursal 1", "Sucursal 2", "Sucursal 3", "Sucursal 4"]

        # Iniciar sesión y seleccionar la primera sucursal
        self.login_and_select_branch("https://www.dinoonline.com.ar/super/login", self.branches[0])

    def start_requests(self):
        # Iteramos sobre las sucursales
        for branch in self.branches:
            self.change_branch(branch)  # Cambiar la sucursal
            for url in self.start_urls:
                # Realizar las solicitudes con las cookies obtenidas
                yield scrapy.Request(url, cookies={cookie['name']: cookie['value'] for cookie in self.cookies},
                                     meta={'branch': branch})  # Pasamos la sucursal actual en meta

    def parse_item(self, response):
        # Obtener la sucursal actual de las meta data
        branch = response.meta.get('branch', 'N/A')

        loader = ItemLoader(item=SuperMamiItem(), response=response)
        loader.add_css("name", "h1.texto_titulo_prod_dest::text", first=True)
        loader.add_css("price", "div.precio-unidad span::text", first=True)
        loader.add_css("brand", "td.productInfo::text", first=True)
        loader.add_value("branch", branch)  # Agregamos la sucursal desde meta

        return loader.load_item()

    def change_branch(self, branch_name):
        """
        Lógica para cambiar la sucursal seleccionada en el sitio web.
        """
        self.driver.get("https://www.dinoonline.com.ar/super/checkout/addressSuper.jsp")
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "panel-title"))
        )

        # Encuentra todos los paneles
        panels = self.driver.find_elements(By.CLASS_NAME, "panel-default")

        for panel in panels:
            title_element = panel.find_element(By.CLASS_NAME, "panel-title")
            if f"Super Mami - {branch_name}" in title_element.text:
                submit_button = panel.find_element(By.CSS_SELECTOR, "input[type='submit']")
                submit_button.click()
                break  # Cambiamos a la sucursal correcta
        # Actualizamos las cookies después de cambiar de sucursal
        self.cookies = self.driver.get_cookies()

    def close_driver(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    def close(self, reason):
        self.close_driver()
        super().close(reason)