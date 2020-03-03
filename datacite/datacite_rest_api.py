'''
Title: Get records from datacite api by author affiliation
Author: Peter Vos

https://support.datacite.org/docs/api

No api key is needed. API is very slow. Max page size is 25.
There are two ways to get authors by affiliation:
1. By string: query=creators.affiliation.name:<query string>, note this is case-sensitive
2. By affiliation-id, this is done by ROR, see https://ror.org. The VU has id https://ror.org/008xxew50
'''
from datetime import datetime
import time
import json
import requests, requests_cache

# cache the responses in a sqlite database file
requests_cache.install_cache(cache_name='datacite_requests_cache', allowable_methods=('GET', 'POST'))


def _do_request(query, page=1, size=25, type="dataset", affiliation_id=''):
    '''
    Do the query request

    :param query:
    :param page:
    :param size:
    :param type:
    :param affiliation_id:
    :return: json result in a dict
    '''
    params = {
        "query": query,
        "page[number]": page,
        "page[size]": size,
        "resource-type-id": type,
        "affiliation-id": affiliation_id
    }
    res = requests.get('https://api.datacite.org/dois', params=params)
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


def get_records(query, data, affiliation_id='', max_author=1, type="dataset"):
    '''
    Do the initial query, and loop through the pages. Append the records to data only if the first author affiliation contains VU or Vrije

    :param query:
    :param data:
    :param affiliation_id:
    :return:
    '''
    d = _do_request(query, affiliation_id=affiliation_id, type=type)
    print('total: %s' % d['meta']['total'])
    print('total pages: %s' % d['meta']['totalPages'])
    for page in range(1, d['meta']['totalPages']):
        print(f'page {page}')
        d = _do_request(query=query, page=page, affiliation_id=affiliation_id, type=type)
        for record in d['data']:
            # check first author
            n=0
            while n < max_author and n < len(record['attributes']['creators']):
                c = record['attributes']['creators'][n]
                n=n+1
                # a bit of extra cleaning
                for a in c['affiliation']:
                    if (a.lower().find('vu ') > -1 or a.lower().find('vrije') > -1) and (a.lower().find(
                            'brussel') == -1 and a.lower().find('medical center') == -1):
                        data[record['id']] = record
    return data


today_str = datetime.now().strftime('%Y%m%d')
#for type in ['dataset','software']:
for type in ['']:
    data = {}

    # cast a wide net, we will filter later
    affs = ['*vrije*', '*vu*', '*VU*', '*Vrije*']
    for affiliation in affs:
        query = f'creators.affiliation.name:{affiliation}'
        #data = get_records(query, data, max_author=3)
        data = get_records(query, data, max_author=1, type=type)

    # by ROR, although we should already have those
    data = get_records('*', data, affiliation_id='https://ror.org/008xxew50', max_author=1, type=type)
    _store(data, f'datacite_{type}{today_str}.json')
