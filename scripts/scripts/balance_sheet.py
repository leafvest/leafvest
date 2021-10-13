import json
import csv
import pandas as pd
import openpyxl
import math
from operator import itemgetter
import requests

#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

companies = pd.read_csv('data/company_refinitiv_esg.csv')

write_row = []

i = 250
for ticker in companies['symbol']:
    if i == 0:
        break
    else:
        try:
            url = ("https://financialmodelingprep.com/api/v3/income-statement/"+str(ticker)+"?limit=120&apikey=c550937522c8e996a828d0dc93a359ba")

            parsed = get_jsonparsed_data(url)

            for j in range(5):
                field = parsed[j].get("date")
                field2 = parsed[j].get("fillingDate")
                field3 = parsed[j].get("acceptedDate")
                field4 = parsed[j].get("period")
                field5 = parsed[j].get("revenue")
                field6 = parsed[j].get("costOfRevenue")
                field7 = parsed[j].get("grossProfit")
                field8 = parsed[j].get("grossProfitRatio")
                field9 = parsed[j].get("researchAndDevelopmentExpenses")
                field10 = parsed[j].get("generalAndAdministrativeExpenses")
                field11 = parsed[j].get("sellingAndMarketingExpenses")
                field12 = parsed[j].get("otherExpenses")
                field13 = parsed[j].get("operatingExpenses")
                field14 = parsed[j].get("costAndExpenses")
                field15 = parsed[j].get("interestExpense")
                field16 = parsed[j].get("depreciationAndAmortization")
                field17 = parsed[j].get("ebitda")
                field18 = parsed[j].get("ebitdaratio")
                field19 = parsed[j].get("operatingIncome")
                field20 = parsed[j].get("operatingIncomeRatio")
                field21 = parsed[j].get("totalOtherIncomeExpensesNet")
                field22 = parsed[j].get("incomeBeforeTax")
                field23 = parsed[j].get("incomeBeforeTaxRatio")
                field24 = parsed[j].get("incomeTaxExpense")
                field25 = parsed[j].get("netIncome")
                field26 = parsed[j].get("netIncomeRatio")
                field27 = parsed[j].get("eps")
                field28 = parsed[j].get("epsdiluted")
                field29 = parsed[j].get("weightedAverageShsOut")
                field30 = parsed[j].get("weightedAverageShsOutDil")

                comp_row = [ticker, field, field2, field3, field4, field5, field6, field7, field8, field9, 
                field10, field11, field12, field13, field14, field15, field16, field17, field18, field19, field20, 
                field21, field22, field23, field24, field25, field26, field27, field28, field29, field30]

                write_row.append(comp_row)

                print(comp_row)
        except:
            print("Went to exception.")

    i = i-1

with open("data/balance_sheet.csv", "w") as file:
    writer = csv.writer(file)

    header = ['Symbol', 'Date', 'Filling Date', 'Accepted Date', 'Period', 'Revenue', 'Cost of Revenue', 'Gross Profit', 'Gross Profit Ratio', 'R&D Expenses'
        'Gen&Admin Expenses', 'Sale&Market Expenses', 'Other Expenses', 'Operating Expenses', 'Cost and Expenses', 'Interest Expense', 'Depreciation and Amortization'
        'Earning Before Taxes', 'Earning Before Taxes Ratio', 'Operating Income', 'Operating Income Ratio', 'Total Other Income Expenses', 'Income Before Tax'
        'Income Before Tax Ratio', 'Income Tax Expense', 'Net Income', 'Net Income Ratio', 'EPS', 'EPS Diluted', 'Weighted Average SHS Out', 'Weighted Average SHS Out Diluted']

    writer.writerow(header)
    for row in write_row:
        writer.writerow(row)

