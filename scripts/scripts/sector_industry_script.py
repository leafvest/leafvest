import csv
import pandas as pd
import openpyxl
import math
from operator import itemgetter

def write(filename, header, write_row):
    with open(filename, "w", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in write_row:
            writer.writerow(row)

companies = pd.read_csv("data/companies.csv")

sectors = []

for sector in companies["Sector"]:
    if [sector] not in sectors:
        sectors.append([sector])

industries = []

for industry in companies["Industry"]:
    if [industry] not in industries:
        industries.append([industry])

write("data/sectorData.csv", ["Sector"], sectors)
write("data/industryData.csv", ["Industry"], industries)
