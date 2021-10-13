"""..."""

import csv
from typing import Generator, List, Any
import yfinance as yf
from multiprocessing import Pool
from pandas_datareader import data as pdr


COMPANY_DATA_FIELDNAMES = [
    'symbol',
    'description',
    'city',
    'pe_ratio',
    'peg_ratio',
    'eps_ratio',
    'pb_ratio',
    'ps_ratio',
    'curr_ratio',
    'ebit_ratio',
    'roe_ratio'
]

COMPANY_HIST_FIELDNAMES = [
    'symbol',
    'Date',
    'Open', 'High', 'Low', 'Close', 
    'Volume', 'Dividends', 'Stock Splits'
]

COMPANY_BALANCE_FIELDNAMES = [
    'symbol',
    'Date',
    'Intangible Assets', 'Capital Surplus', 'Total Liab',
    'Total Stockholder Equity', 'Other Current Liab', 'Total Assets',
    'Common Stock', 'Other Current Assets', 'Retained Earnings',
    'Other Liab', 'Good Will', 'Treasury Stock', 'Other Assets', 'Cash',
    'Total Current Liabilities', 'Other Stockholder Equity',
    'Property Plant Equipment', 'Total Current Assets',
    'Long Term Investments', 'Net Tangible Assets', 'Net Receivables',
    'Long Term Debt', 'Inventory', 'Accounts Payable',
    'Deferred Long Term Asset Charges', 'Deferred Long Term Liab',
    'Short Term Investments', 'Short Long Term Debt']


def usa_symbols() -> Generator[str, None, None]:
    """Generates all USA company symbols"""
    with open('data/companies.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Country'] == 'United States':
                yield row['Symbol']


def get_usa_symbols() -> List[str]:
    """Return list of all USA company symbols"""
    tickers = []
    for ticker in usa_symbols():
        tickers.append(ticker)
    return tickers


def get_symbol_data(symbol: str) -> Any:
    """..."""
    print(symbol)
    
    company = yf.Ticker(symbol)
    company_data = {
        'symbol': symbol,
        'description': None,
        'city': None,
        'pe_ratio': None,
        'peg_ratio': None,
        'eps_ratio': None,
        'pb_ratio': None,
        'ps_ratio': None,
        'curr_ratio': None,
        'ebit_ratio': None,
        'roe_ratio': None,
        'balance_sheet': None,
        'history': None
    }

    if 'longBusinessSummary' in company.info:
        company_data['description'] = company.info['longBusinessSummary']

    if 'city' in company.info:
        company_data['city'] = company.info['city']

    if 'trailingPE' in company.info:
        company_data['pe_ratio'] = company.info['trailingPE']

    if 'pegRatio' in company.info:
        company_data['peg_ratio'] = company.info['pegRatio']

    if 'trailingEps' in company.info:
        company_data['eps_ratio'] = company.info['trailingEps']

    if 'priceToBook' in company.info:
        company_data['pb_ratio'] = company.info['priceToBook']

    if 'priceToSalesTrailing12Months' in company.info:
        company_data['ps_ratio'] = company.info['priceToSalesTrailing12Months']

    # MAKE TRIGGERS OUT OF THIS
    # company_data['curr_ratio'] = company.quarterly_balance_sheet.iloc[15, 0] / company.quarterly_balance_sheet.iloc[11, 0]
    # company_data['ebit_ratio'] = company.quarterly_balance_sheet.iloc[7, 0]
    # company_data['roe_ratio'] = company.quarterly_balance_sheet.iloc[4, 0] / company.quarterly_balance_sheet.iloc[1, 0]
    
    # try:
    #     print(company.quarterly_balance_sheet)
    #     balance_sheet = company.quarterly_balance_sheet
    #     if not balance_sheet.empty:
    #         balance_sheet = balance_sheet.T.rename_axis('Date').reset_index()
    #         balance_sheet['Date'] = balance_sheet['Date']
    #         company_data['balance_sheet'] = balance_sheet.to_dict('records')
    # except:
    #     pass
    
    try:
        history = company.history(period="10y")
        if not history.empty:
            history = history.reset_index()
            history['Date'] = history['Date']
            company_data['history'] = history.to_dict('records')
    except:
        pass
    
    return company_data


def main() -> None:
    """..."""

    symbols = get_usa_symbols()
    symbols = symbols

    with Pool(16) as p:
        companies = p.map(get_symbol_data, symbols)

    with open('data/company_data.csv', mode='w') as comp_data_file:
        comp_data_writer = csv.DictWriter(comp_data_file, 
                                          delimiter=',', 
                                          restval='nan',
                                          extrasaction='ignore',
                                          fieldnames=COMPANY_DATA_FIELDNAMES)
        comp_data_writer.writeheader()
                
        with open('data/company_history.csv', mode='w') as comp_hist_file:
            comp_hist_writer = csv.DictWriter(comp_hist_file, 
                                              delimiter=',', 
                                              restval='nan',
                                              extrasaction='ignore',
                                              fieldnames=COMPANY_HIST_FIELDNAMES)
            comp_hist_writer.writeheader()
            
            with open('data/company_balance_sheet.csv', mode='w') as comp_balance_file:
                comp_balance_writer = csv.DictWriter(comp_balance_file, 
                                                     delimiter=',',
                                                     restval='nan',
                                                     extrasaction='ignore',
                                                     fieldnames=COMPANY_BALANCE_FIELDNAMES)
                comp_balance_writer.writeheader()

                for company in companies:
                    symbol = company['symbol']
                    history = company.pop('history', None)
                    balance_sheet = company.pop('balance_sheet', None)
                    
                    print(symbol)
                    
                    comp_data_writer.writerow(company)

                    if history:
                        for entry in history:
                            entry['symbol'] = symbol
                            comp_hist_writer.writerow(entry)

                    # if balance_sheet:
                    #     for entry in balance_sheet:
                    #         entry['symbol'] = symbol
                    #         comp_balance_writer.writerow(entry)


# def test() -> None:
#     yf.pdr_override()
#     data = pdr.get_data_yahoo("SPY", start="2011-01-01", end="2021-01-01")
#     print(data)


if __name__ == "__main__":
    main()
