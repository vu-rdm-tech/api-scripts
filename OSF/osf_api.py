'''
Title: Get records from OSF by general search
Author: Peter Vos

https://developer.osf.io/#tag/Search%2Fpaths%2F~1search~1users~1%2Fget

'''
import math
from datetime import datetime
import time
import json
import requests, requests_cache

# cache the responses in a sqlite database file
requests_cache.install_cache(cache_name='osf_requests_cache', allowable_methods=('GET', 'POST'))

def _getNodes(userId):
    res = requests.get(f'https://api.osf.io/v2/users/{userId}/nodes/?format=json')
    print(res.url)

    total=res.json()['links']['meta']['total']
    return total

def _getRegistrations(userId):
    res = requests.get(f'https://api.osf.io/v2/users/{userId}/registrations/?format=json')
    print(res.url)
    total=res.json()['links']['meta']['total']
    return total

def _getPreprints(userId):
    res = requests.get(f'https://api.osf.io/v2/users/{userId}/preprints/?format=json')
    print(res.url)
    total=res.json()['links']['meta']['total']
    return total

def _do_request(query, page=1):
    '''
    Do the query request

    :param query:
    :param page:
    :return: json result in a dict
    '''
    params = {
        "q": query,
        "page": page,
        "format": "json"
    }
    res = requests.get('https://api.osf.io/v2/search/users/', params=params)
    print(res.url)
    return res.json()


def _store(data, filename):
    '''
    Store the data dict as a json file

    :param data: dict
    :param filename: string
    :return:
    '''
    with open(filename, 'w') as f:
        json.dump(data, f, indent=1)


def get_records(query, data):
    '''
    Do the initial query, and loop through the pages. Append the records to data only if the
    attributes.employment.institution attribute contains vu or vrije

    :param query:
    :param data:
    :return:
    '''
    d = _do_request(query)
    print('total: %s' % d['links']['meta']['total'])
    totalPages = math.ceil(d['links']['meta']['total']/10)
    print('total pages: %s' % totalPages)
    for page in range(1, totalPages):
        print(f'page {page}')
        d = _do_request(query=query, page=page)
        for record in d['data']:
            for e in record['attributes']['employment']:
                print(e)
                a=e['institution']
                if (a.lower().find('vu ') > -1 or a.lower().find('vrije') > -1 or a.lower().find('free') > -1) and (a.lower().find(
                        'brussel') == -1 and a.lower().find('medical center') == -1) and ('endYear'in e and e['endYear']==''):
                    data[record['id']] = record
                    data[record['id']]['numberOfNodes']=_getNodes(record['id'])
                    data[record['id']]['numberOfRegistrations']=_getRegistrations(record['id'])
                    data[record['id']]['numberOfPreprints']=_getPreprints(record['id'])
    return data


today_str = datetime.now().strftime('%Y%m%d')
#for type in ['dataset','software']:

data = {}

# cast a wide net, we will filter later
affs = ['vrije', 'vu', 'free']
for affiliation in affs:
    query = affiliation
    data = get_records(query, data)

print(len(data))

_store(data, f'osf_users_{today_str}.json')

