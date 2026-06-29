import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

THINK_SPAIN_URL = "https://www.thinkspain.com/es/venta-viviendas"

class HouseDetailsHarvester:
    driver: WebDriver

    def __init__(self):
        service = Service(ChromeDriverManager().install())

        options = Options()
        options.add_argument("--headless")

        self.driver = webdriver.Chrome(service = service, options = options)
    
    def polite_pause(lowest: float = 2.0, highest: float = 5.0) -> None:
        time.sleep(random.uniform(lowest, highest))
