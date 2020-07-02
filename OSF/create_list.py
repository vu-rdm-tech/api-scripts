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
        w.writerow(['url', 'name', 'institution', 'startYear', 'endYear', 'title', 'department', 'numberOfNodes', 'numberOfPreprints', 'numberOfRegistrations'])
        for id in data:
            record = data[id]
            print(record)
            e=record['attributes']['employment'][0]
            w.writerow([record['links']['html'], record['attributes']['full_name'], e['institution'], e['startYear'],e['endYear'], e['title'], e['department'], record['numberOfNodes'], record['numberOfPreprints'], record['numberOfRegistrations'] ])
    print(pubcount)


create_csv('osf_users_20200702.json')
