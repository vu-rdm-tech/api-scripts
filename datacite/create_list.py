'''
Title: Use the data gathered by datacite_rest_api.json to create a list you can filter in Excel
Author: Peter Vos

'''
from datetime import datetime
import json
import csv


def create_csv(json_file):
    data = json.load(open(json_file))
    pubcount = {}
    with open(json_file.replace('.json', '.csv'), mode='w', newline='', encoding='utf-8') as datafile:
        w = csv.writer(datafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['doi', 'name', 'affiliation', 'publisher'])
        for id in data:
            record = data[id]

            publisher = record['attributes']['publisher']
            if publisher in pubcount:
                pubcount[publisher] = pubcount[publisher] + 1
            else:
                pubcount[publisher] = 1
            c=record['attributes']['creators'][0]
            a=('; ').join(c['affiliation'])
            print(a)
            w.writerow([id, c['name'], a, publisher])
    print(pubcount)


create_csv('datacite20200228.json')
