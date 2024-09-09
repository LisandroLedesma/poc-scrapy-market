# Supermarket Scraper - Test

## Descripción
Este proyecto es un **web scraper** desarrollado con **Scrapy** y **Selenium**, diseñado para extraer productos y sus precios de diferentes sucursales de un supermercado online. El objetivo principal del proyecto es automatizar la recolección de datos de productos de diversas sucursales mediante técnicas de scraping, con el soporte de inicio de sesión y selección de sucursales a través de Selenium.
Fue parte de una POC que hice para mi proyecto final de la carrera Ingeniería en Sistemas de Información, se siguió iterando pero lo dejó acá porque se me hizo bonito 😁.


## Tecnologías Utilizadas 👨‍💻
- **Python**: Lenguaje principal.
- **Scrapy**: Framework para scraping web.
- **Selenium**: Para manejar el inicio de sesión y la navegación de sitios web dinámicos.
- **Poetry**: Manejo de dependencias y gestión del entorno virtual.
- **.env**: Manejo de variables de entorno para credenciales y configuraciones.

## Instalación 👈

1. **Clona este repositorio** 👈

    ```bash
    git clone https://github.com/tu-usuario/supermarket-scraper.git
    cd supermarket-scraper
    ```

2. **Instala las dependencias utilizando Poetry** 👈

    ```bash
    poetry install
    ```

3. **Crea un archivo `.env`** en la raíz del proyecto con las siguientes variables de entorno 👈

    ```bash
    LOGIN_EMAIL=tu_email
    LOGIN_PASSWORD=tu_contraseña
    BRANCHES=["Ruta 20", "Otra Sucursal", "Tercera Sucursal"]
    ```

## Uso

1. **Ejecuta el scraper** con el siguiente comando 🤖

    ```bash
    poetry run scrapy crawl supermami -o productos.json
    ```

    Esto iniciará el proceso de scraping para las sucursales listadas en el archivo `.env` y generará un archivo `productos.json` con los datos extraídos.
    Aclaración importante, tengo las urls que quería revisar para la POC.

