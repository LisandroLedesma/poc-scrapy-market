from scrapy.spiders import CrawlSpider
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



class BaseSupermarketSpider(CrawlSpider):
    def __init__(self, *args, **kwargs):
        super(BaseSupermarketSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Activa el modo headless
        chrome_options.add_argument("--disable-gpu")  # Deshabilita la GPU (recomendado en headless)
        chrome_options.add_argument("--no-sandbox")  # Deshabilita el sandbox (útil en algunos entornos de CI)
        chrome_options.add_argument(
            "--disable-dev-shm-usage")  # Deshabilita el uso compartido de la memoria (para evitar problemas en entornos con poca memoria)

        self.driver = webdriver.Chrome(options=chrome_options)  # Inicializa el navegador Chrome
        self.cookies = {}

    def login_and_select_branch(self, login_url, branch_name):
        # Navega a la página de inicio de sesión
        self.driver.get(login_url)

        # Encuentra y completa los campos de inicio de sesión
        email_input = self.driver.find_element(By.ID, "login")
        email_input.send_keys("lichaledesma31@gmail.com")

        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("Deadpoool1")
        password_input.send_keys(Keys.RETURN)


        # Lógica para seleccionar la sucursal basada en branch_name
        # Puedes navegar a la página de selección de sucursal
        self.driver.get("https://www.dinoonline.com.ar/super/checkout/addressSuper.jsp")
        # Espera a que los paneles estén cargados
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "panel-title"))
        )

        # Encuentra todos los paneles
        panels = self.driver.find_elements(By.CLASS_NAME, "panel-default")

        for panel in panels:
            # Busca el título del panel
            title_element = panel.find_element(By.CLASS_NAME, "panel-title")
            if f"Super Mami - {branch_name}" in title_element.text:
                # Si el título coincide, encuentra y haz clic en el botón de submit
                submit_button = panel.find_element(By.CSS_SELECTOR, "input[type='submit']")
                submit_button.click()
                break  # Salimos del loop ya que encontramos el panel correcto

        # Obtén las cookies de la sesión para usarlas en Scrapy
        self.cookies = self.driver.get_cookies()

    def close_driver(self):
        if hasattr(self, 'driver'):
            self.driver.quit()  # Cierra el navegador si está inicializado

    def close(self, reason):
        self.close_driver()  # Cierra el navegador al finalizar el scraping
        # No se llama a super().close(reason) aquí porque es la clase base
