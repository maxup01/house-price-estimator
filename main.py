from city import SpainCity
from src.data import DataProvider
from src.predictor import PriceEstimator
from src.input import prompt_property_input
import argparse
import math

def main():
    parser = argparse.ArgumentParser(description="Scrape and predict property prices")
    parser.add_argument("city", help="city to scrape, e.g. marbella")

    try:
        city = SpainCity(parser.parse_args().city)

        data_provider = DataProvider()

        data = data_provider.retrieve_data(city)

        estimator = PriceEstimator(data)
        estimator.fit()

        property_input = prompt_property_input()

        price = estimator.estimate_price(property_input)

        print(f"\nEstimated price is: {math.ceil(price)}€")
    except ValueError:
        print("not a valid city")

if __name__ == "__main__":
    main()