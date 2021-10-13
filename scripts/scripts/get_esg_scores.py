"""Get ESG scores for each US Stock"""

from typing import Any
import get_all_tickers
import requests

JSON = Any
REFINITIV_ESG = 'https://www.refinitiv.com/bin/esg/esgsearchresult?ricCode='


def us_stocks() -> JSON:
    """Generate US Stocks"""
    stock_data = PyTickerSymbols()
    indices = stock_data.get_all_indices()
    for index in indices:
        stocks = stock_data.get_stocks_by_index(index)
        for stock in stocks:
            if stock['country'] == 'United States':
                yield stock


def get_json(url: str) -> JSON:
    """..."""
    r = requests.get(url)
    return r.json()


def refinitiv_get_esg_score(ticker: str) -> JSON:
    """..."""
    esg_data = get_json(f'{REFINITIV_ESG}{ticker}')

    if not esg_data:
        esg_data = get_json(f'{REFINITIV_ESG}{ticker}.O')

    if not esg_data:
        print(f'!!! {ticker} !!!')
        esg_score = None
    else:
        esg_score: JSON = esg_data['esgScore']

    return esg_score


def main() -> None:
    """Print ESG scores for each US Stock"""
    # stock_count = 0
    # esg_score_count = 0
    # for stock in us_stocks():
    #     stock_count += 1
    #     ticker = stock['symbol']
    #     esg_score = refinitiv_get_esg_score(ticker)
    #     if esg_score:
    #         esg_score_count += 1
    # print(stock_count)
    # print(esg_score_count)

    from inspect import getmembers
    print(getmembers(get_all_tickers))
    count = 0
    tickers = get_all_tickers.get_tickers()

    for _ in tickers:
        count += 1

    # count = 0
    # stock_data = PyTickerSymbols()
    # indices = stock_data.get_all_indices()
    # for index in indices:
    #     stocks = stock_data.get_stocks_by_index(index)
    #     for stock in stocks:
    #         if stock['country'] == 'United States':
    #             count += 1
    print(count)


if __name__ == "__main__":
    main()
