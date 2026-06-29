from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class HouseDetailsHarvester:
    driver: WebDriver

    def __init__(self):
        service = Service(ChromeDriverManager().install())

        options = Options()
        options.add_argument("--headless")

        self.driver = webdriver.Chrome(service = service, options = options)
        
