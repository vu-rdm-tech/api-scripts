# https://api.datacite.org/dois?query=creators.affiliation.name:%22Vrije%20Universiteit%20Amsterdam%22&resource-type-id=dataset
# https://api.datacite.org/dois?query=creators.affiliation.name:%22Vrije+UniversiteitAmsterdam%22&page=1&size=100&resource-type-id=dataset
# https://search.datacite.org/works?query=creators.affiliation.name%3AVU*&affiliation-id=https%3A%2F%2Fror.org%2F008xxew50
# https://support.datacite.org/docs/api
import json

import requests


def _do_request(query, page=1, size=25, type="dataset", affiliation_id=''):
    params = {
        "query": query,
        "page": page,
        "size": size,
        "resource-type-id": type,
        "affiliation-id": affiliation_id
    }
    res = requests.get('https://api.datacite.org/dois', params=params)
    print(res.url)
    return res.json()


def _store(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=1)


def get_records(query, data, affiliation_id=''):
    d = _do_request(query, affiliation_id=affiliation_id)
    print('total: %s' % d['meta']['total'])
    print('total pages: %s' % d['meta']['totalPages'])
    for page in range(1, d['meta']['totalPages']):
        print(f'page {page}')
        d = _do_request(query=query, page=page, affiliation_id=affiliation_id)
        for record in d['data']:
            data[record['id']] = record
    return data


data = {}

affs=['"Vrije Universiteit Amsterdam"','"VU University Amsterdam"','VU*','Vrije*']
for affiliation in affs:
    query = f'creators.affiliation.name:{affiliation}'
    data=get_records(query, data)

data = get_records('*', data, affiliation_id='https://ror.org/008xxew50')
_store(data, 'datacite.json')
