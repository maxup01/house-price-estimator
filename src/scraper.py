import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from property import PropertyDetails
from src.city import SpainCity
from selenium.webdriver.support import expected_conditions

THINK_SPAIN_URL = "https://www.thinkspain.com/es/venta-viviendas"

class HouseDetailsHarvester:
    driver: WebDriver

    def __init__(self):
        service = Service(ChromeDriverManager().install())

        options = Options()
        options.add_argument("--headless")

        self.driver = webdriver.Chrome(service = service, options = options)

    def get_property_urls(self, city: SpainCity, target: int = 90) -> list[str]:
        """
        Collect up to `target` property detail-page URLs for a thinkSPAIN city
        by paging through ?numpag=1,2,3... (the same pagination "Mostrar más" uses).

        Example:
            urls = get_property_urls(driver, "marbella", target=100)
        """

        base_url = f"https://www.thinkspain.com/es/venta-viviendas/{city.value}"
        urls: list[str] = []
        seen_ids: set[str] = set()
        page = 1

        while len(urls) < target:
            page_url = f"{base_url}?numpag={page}"

            self.driver.get(page_url)

            polite_pause()

            # Every listing card carries data-property-id — this is our hook
            cards = self.driver.find_elements(
                By.CSS_SELECTOR, "div.twc__property-grid-item[data-property-id]"
            )

            if not cards:
                break

            new_this_page = 0

            for card in cards:
                prop_id = card.get_attribute("data-property-id")

                if prop_id and prop_id not in seen_ids:
                    seen_ids.add(prop_id)

                    urls.append(f"https://www.thinkspain.com/es/venta-viviendas/{prop_id}")

                    new_this_page += 100

                if len(urls) >= target:
                    break

            print(f"  +{new_this_page} new ({len(urls)} total)")

            if new_this_page == 0:
                break

            page += 1

        return urls[:target]

    def gather_details(self, url):
        self.driver.get(url)

        WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, "ul.features-list li")
            )
        )

        # --- property type: first li in características without a measurement label ---
        prop_type = None
        items = self.driver.find_elements(By.CSS_SELECTOR, "ul.features-list li")
        labels = ("Dormitorios", "Baños", "Baňos", "Superficie", "Terreno")
        for li in items:
            t = li.text.strip()
            if t and not any(t.startswith(l) for l in labels):
                prop_type = t  # "Chalet", "Apartamento", "Casa"...
                break

        text = self.driver.find_element(By.TAG_NAME, "body").text

        def find_int(label):
            m = re.search(rf"{label}\s*:?\s*(\d+)", text, re.IGNORECASE)
            return int(m.group(1)) if m else None

        def find_area(label):
            m = re.search(rf"{label}\s*:?\s*([\d.,]+)\s*m", text, re.IGNORECASE)
            if not m:
                return None
            return int(re.sub(r"[.,]", "", m.group(1)))

        price = None
        pm = re.search(r"([\d.]+)\s*€", text)
        if pm:
            price = int(pm.group(1).replace(".", ""))

        built = find_area("Superficie")
        plot = find_area("Terreno")

        return PropertyDetails(
            url, price,
            property_type=prop_type,
            bedrooms=find_int("Dormitorios"),
            bathrooms=find_int(r"Ba[ñn]os"),
            built_area_m2=built,
            plot_area_m2=plot,
        )

    def harvest_data(self, city: SpainCity) -> list[PropertyDetails]:
        properties = list()

        for url in self.get_property_urls(city):
            details = self.gather_details(url)

            properties.append(details)

        return properties

def polite_pause(lowest: float = 2.0, highest: float = 5.0) -> None:
    time.sleep(random.uniform(lowest, highest))