'''
Title: Use the data gathered by datacite_rest_api.json to create a list you can filter in Excel
Author: Peter Vos

'''
from datetime import datetime
import json
import csv


def create_csv(json_file):
    pubcount = {}
    with open(json_file, encoding="utf8") as jsonfile:
        data = json.load(jsonfile)
        with open(json_file.replace('.json', '.csv'), mode='w', newline='', encoding='utf-8') as datafile:
            w = csv.writer(datafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(['url', 'author', 'dataverse', 'date'])
            for item in data['data']['items']:
                w.writerow([item['url'], ('; ').join(item['authors']), item['name_of_dataverse'], item['published_at']])


create_csv('dataversenl20200302.json')
