"""Showcase how to use companies.csv file"""

import csv
from typing import Generator, List


def usa_tickers() -> Generator[str, None, None]:
    """Generates all USA company tickers"""
    with open('company.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Country'] == 'United States':
                yield row['Symbol']


def get_usa_tickers() -> List[str]:
    """Return list of all USA company tickers"""
    tickers = []
    for ticker in usa_tickers():
        tickers.append(ticker)
    return tickers


def main() -> None:
    """Print tickers of all US stocks"""
    for ticker in usa_tickers():
        print(ticker)


if __name__ == "__main__":
    main()
