import pandas
from dataclasses import asdict

from city import SpainCity
from property import PropertyDetails
from scraper import HouseDetailsHarvester


class DataProvider:
    data_harvester: HouseDetailsHarvester

    def __init__(self):
        self.data_harvester = HouseDetailsHarvester()

    def retrieve_data(self, city: SpainCity) -> list[PropertyDetails]:
        data = self.data_harvester.harvest_data(city)

        df = pandas.DataFrame([asdict(e) for e in data])
        df.to_csv(f"{city}.csv", index=False)

        return data