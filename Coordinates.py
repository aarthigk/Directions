import csv

import numpy as np
import pandas as pd
import requests
import json
import openpyxl
from pathlib import Path

xlsx_file = Path('bstops.xlsx')
#print(xlsx_file)
wb_obj = openpyxl.load_workbook(xlsx_file)
wsheet = wb_obj.active
for row in wsheet.iter_rows(max_row=85):
    for cell in row:
        print(cell.value, end=" ")
    print()

#def getCoordinates(places):

    baseurl="https://maps.googleapis.com/maps/api/geocode/json?address="+cell.value+"lagos Nigeria""&key=AIzaSyCxXp01-Oe7JfuR6J5lk9wPgqsNo3B6t8g"
    JSONContent = requests.get(baseurl).json()
    content = json.dumps(JSONContent, indent=4, sort_keys=True)
    coordinates = JSONContent['results']
    formattedData = []
    wtr = csv.writer(open('coordinates.csv', 'a'), delimiter=';', lineterminator='\n')
    if 'error' not in JSONContent:
        for i in coordinates:
            formattedData.append(i['formatted_address'])
            formattedData.append(i['geometry'])
            print(formattedData)
            wtr.writerow([formattedData])


