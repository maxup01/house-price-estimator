# House Price Estimator

Estimate Spanish property prices from real market data. The tool scrapes current listings from [thinkSPAIN](https://www.thinkspain.com) for a chosen city, fits a log-linear regression model on them, and predicts the price of a property you describe.

## How it works

1. **Scrape** — a headless Chrome (Selenium) crawler pages through thinkSPAIN search results for the given city, collecting ~90 listings and extracting price, property type, bedrooms, bathrooms, built area, and plot area from each detail page.
2. **Cache** — scraped data is saved to `<city>.csv` (e.g. `marbella.csv`). On later runs the CSV is reused, so scraping happens only once per city.
3. **Fit** — a linear regression (least squares on `log(price)`) is trained on the numeric features plus a one-hot encoding of property type.
4. **Predict** — you enter your property's details interactively and get an estimated price in euros.

## Requirements

- Python 3.12
- Google Chrome (for the Selenium scraper)
- Dependencies: `pandas`, `numpy`, `selenium`, `webdriver-manager`

## Setup

Using conda:

```bash
conda env create -f environment.yml
conda activate house-price-estimator
```

## Usage

```bash
python main.py marbella
```

The city must be one of the supported thinkSPAIN slugs defined in `src/city.py` — major cities (madrid, barcelona, valencia, malaga, sevilla...), coastal towns (marbella, estepona, torrevieja, denia...), islands (mallorca, ibiza, tenerife...), and whole regions (costa-del-sol, costa-blanca...).

You'll then be prompted for the property details:

```
Enter the property details:

Property type ['Chalet', 'Apartamento', 'Casa', 'Piso', 'Ático', 'Bungalow']: Apartamento
Bedrooms: 3
Bathrooms: 2
Built area (m²): 120
Plot area (m²) (leave blank if none):

Estimated price is: 512345€
```

## Project structure

```
main.py              # CLI entry point
environment.yml      # conda environment spec
marbella.csv         # sample scraped dataset (Marbella)
src/
  city.py            # SpainCity enum of supported thinkSPAIN city slugs
  scraper.py         # Selenium scraper (listing URLs + detail extraction)
  data.py            # DataProvider: CSV cache or fresh scrape
  property.py        # PropertyDetails / PropertyInput dataclasses
  predictor.py       # PriceEstimator: least-squares fit on log(price)
  input.py           # interactive CLI prompts with validation
```

## Model notes

- Target is `log(price_eur)`, so predictions are multiplicative in the features and never negative.
- Property type is one-hot encoded with the first category (alphabetically) as the baseline.
- Missing numeric values (e.g. no plot area for apartments) are treated as 0.
- With ~90 samples per city, treat estimates as rough ballpark figures, not appraisals.

## Notes on scraping

The scraper waits a random 2–5 seconds between page loads to be polite to thinkSPAIN's servers. Site markup may change over time; selectors live in `src/scraper.py`.
