"""
Script that performs a partial match to companies with similar names in order to fine the ticker symbol for company emission data.
"""

import csv
from numpy import newaxis, string_
import pandas as pd
import openpyxl
import math
from operator import itemgetter

def filterName(name):
    newName = name

    listOfCommonWords = ['common', 'inc', 'corporation', 'llc', 'holding', 'corp', 
    'energy', 'co', 'company', 'waste', 'us', 'center', 'holdings', 
    'industries', 'group', 'lp', 'partner', 'limited', 'stock', 'total', 'return', 'fund', 'share', 'shares', 'ltd'
    'floating', 'rate', 'perpetual', 'cumulative', 'depositary', 'every', 'class', 'depository']
    punctuation = ["'", '"', ',', '.', '!', '?', '#', '&', "*", '?', '-', '_', '(', ')', '[', ']', '{', '}', '<', '>', '~', '`']

    for ele in newName:
        if ele in punctuation:
            newName = newName.replace(ele, " ")

    newLoName = newName.split()
    finalList = []
    
    for word in newLoName:
        if word not in listOfCommonWords:
            finalList.append(word)

    return finalList

def partialMatch(emissionName, tickerName):
    overlap = list(set(emissionName) & set(tickerName))
    return (len(overlap) > len(emissionName)/2) or (len(overlap) > len(tickerName)/2)

companyAndSymbols = pd.read_csv("data/companies.csv")

companyEmmissionData = pd.read_csv("data/company_ghg.csv")

# {company original name : [filtered name]}
companyEmmissionNames = {}

# {Stock Ticker : [filtered name]}
companyTickerNames = {}

for name in companyEmmissionData['Company Name']:
    companyEmmissionNames[name] = filterName(name.lower())

compIndex = 0
for company in companyAndSymbols['Name']:
    companyTickerNames[companyAndSymbols['Symbol'][compIndex]] = filterName(company.lower())
    compIndex = compIndex+1

partialMatches = []

print('Starting the map')

for company in companyEmmissionNames.keys():
    for ticker in companyTickerNames.keys():
        if partialMatch(companyEmmissionNames[company], companyTickerNames[ticker]):
            partialMatches.append([ticker, company])
            break

print('Writing')

partialMatches.sort(key=itemgetter(0))

with open('data/companytoticker.csv', 'w') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['Company Name', 'Symbol'])

  for row in partialMatches:
    writer.writerow(row)

print('Finished Script')
    