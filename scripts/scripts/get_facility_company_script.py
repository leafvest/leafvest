import csv
import pandas as pd
import openpyxl
import math
from operator import itemgetter

excelSheets = ["data/greenhouse_data/ghgp_data_2010",
"data/greenhouse_data/ghgp_data_2011",
"data/greenhouse_data/ghgp_data_2012",
"data/greenhouse_data/ghgp_data_2013",
"data/greenhouse_data/ghgp_data_2014",
"data/greenhouse_data/ghgp_data_2015",
"data/greenhouse_data/ghgp_data_2016",
"data/greenhouse_data/ghgp_data_2017",
"data/greenhouse_data/ghgp_data_2018",
"data/greenhouse_data/ghgp_data_2019"]

companyData = pd.read_excel("data/greenhouse_data/ghgp_data_parent_company_10_2020.xls", sheet_name=None)
sheet = ['2019', '2018', '2017', '2016','2015','2014','2013','2012','2011','2010']

facilityCompany = {}

for year in sheet:

    i = 0
    for company in companyData[year]["PARENT COMPANY NAME"]:
        facilityCompany[company] = [companyData[year]["GHGRP FACILITY ID"][i], year]
        i = i+1

companyTicker = pd.read_csv("data/companytoticker.csv")    
tickerDict = {}

j = 0
for company in companyTicker["Symbol"]:
    tickerDict[company] = companyTicker["Company Name"][j]
    j = j+1

write_row = []

for company in facilityCompany.keys():
    if company in tickerDict.keys():
        compData = facilityCompany.get(company)
        write_row.append([tickerDict.get(company), compData[0], compData[1]])

with open("data/facility_company_by_year.csv", "w", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Ticker Symbol", "Facility ID", "Year"])
    for row in write_row:
        writer.writerow(row)