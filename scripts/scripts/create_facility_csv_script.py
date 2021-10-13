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
"data/greenhouse_data/ghgp_data_2019",
"data/greenhouse_data/ghgp_data_by_year"]

all_facilities = {}
write_row = []

for filename in excelSheets:
    buildingData = pd.read_excel(filename+".xlsx", sheet_name=0, header=3)

    i = 0
    for building in buildingData["Facility Id"]:
        if building not in all_facilities.keys():
            all_facilities[building] = [str(building), buildingData["Facility Name"][i], buildingData["Address"][i], buildingData["City"][i], buildingData["State"][i], str(buildingData["Zip Code"][i]), buildingData["County"][i], str(buildingData["Latitude"][i]), str(buildingData["Longitude"][i])]
        i = i+1

write_row = []

for facility in all_facilities.keys():
    write_row.append(all_facilities.get(facility))

with open("data/facility_info.csv", "w", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Facility ID", "Name", "Address", "City", "State", "Zip Code", "County", "Latitude", "Longitude"])
    for row in write_row:
        writer.writerow(row)
