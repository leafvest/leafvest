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

year = 2010
write_row = []

for filename in excelSheets:
    facilityGHG = pd.read_excel(filename+".xlsx", sheet_name=0, header=3)

    i = 0
    for facility in facilityGHG["Facility Id"]:
        write_row.append([facility, str(year), facilityGHG["CO2 emissions (non-biogenic) "][i], facilityGHG["Methane (CH4) emissions "][i], facilityGHG["Nitrous Oxide (N2O) emissions "][i]])
        i = i+1
    
    year = year+1

with open("data/facility_ghg_by_year.csv", "w", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Facility ID", "Year", "CO2 Emissions", "Methane (CH4) Emissions", "Nitrous Oxide (N2O) Emissions"])
    for row in write_row:
        writer.writerow(row)