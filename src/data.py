import os
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
        path = f"{city.value}.csv"

        if os.path.exists(path):
            df = pandas.read_csv(path)

            return [PropertyDetails(**row) for row in df.to_dict(orient="records")]

        data = self.data_harvester.harvest_data(city)

        df = pandas.DataFrame([asdict(e) for e in data])
        df.to_csv(path, index=False)

        return data