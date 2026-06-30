from city import SpainCity
from src.data import DataProvider
from src.predictor import PriceEstimator
from src.input import prompt_property_input
import argparse

def main():
    parser = argparse.ArgumentParser(description="Scrape and predict property prices")
    parser.add_argument("city", help="city to scrape, e.g. marbella")

    try:
        city = SpainCity(parser.parse_args().city)

        data_provider = DataProvider()

        data = data_provider.retrieve_data(city)

        estimator = PriceEstimator(data)
        print(estimator.X)
        print(estimator.y)
        estimator.fit()

        property_input = prompt_property_input()

        price = estimator.estimate_price(property_input)

        print(f"Estimated price is: {price}€")
    except ValueError:
        print("not a valid city")

if __name__ == "__main__":
    main()