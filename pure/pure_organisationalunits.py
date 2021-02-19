"""
Title:
Author: Brett G. Olivier

Usage::


(C) Brett G. Olivier, VU Amsterdam, 2021. Licenced for use under the GNU GPL 3.0

"""

import json

from pure.config import (
    PURE_APIKEY,
    PURE_USERNAME,
    PURE_PASSWORD,
    PURE_ORGANISATIONALUNITS_URL,
)
import requests
import requests_cache

# https://research.vu.nl/ws/api/518/api-docs/index.html#!/organisational45units/listOrganisationalUnits

requests_cache.install_cache(
    cache_name='pure_ou_requests_cache', allowable_methods=('GET', 'POST')
)


def _store(data, filename):
    '''
    Store the data dict as a json file

    :param data: dict
    :param filename: string
    :return:
    '''
    with open(filename, 'w') as f:
        json.dump(data, f, indent=1)


def _do_postrequest(data, size=10, offset=0):
    headers = {"Content-Type": "application/json", 'Accept': 'application/json'}
    payload = {'apiKey': PURE_APIKEY, 'size': size, 'offset': offset}

    res = requests.post(
        PURE_ORGANISATIONALUNITS_URL,
        headers=headers,
        params=payload,
        data=data,
        auth=(PURE_USERNAME, PURE_PASSWORD),
    )
    try:
        cached = res.from_cache
    except:
        cached = False
    if res.status_code == 200:
        return res, cached
    else:
        raise Exception('*** Got: status_code: %s' % res.status_code)


def get_all():
    reqJSON = '{}'  # seems to be enough to get all
    res, cached = _do_postrequest(data=reqJSON, size=1, offset=0)
    data = json.loads(res.content)
    count = data['count']

    list = {}
    size = 10
    for offset in range(0, count, size):
        res, cached = _do_postrequest(data=reqJSON, size=size, offset=offset)
        data = json.loads(res.content)
        items = data['items']

        # "period": {
        #         "startDate": "1970-01-01T11:00:00.000+0000",
        #         "endDate": "2015-05-31T10:00:00.000+0000"
        #       },

        for item in items:
            if 'endDate' not in item['period']:  # ou no longer exists
                name = item['name']['text'][0]['value']
                term = item['type']['term']['text'][0]['value']
                uuid = item['uuid']
                parents = []
                if 'parents' in item:
                    for parent in item['parents']:
                        parents.append(parent['uuid'])
                list[uuid] = {}
                list[uuid]['name'] = name
                list[uuid]['term'] = term
                list[uuid]['parents'] = parents

    return list


def find_children(list, uuid):
    children = []
    for cuuid, v in list.items():
        if uuid in v['parents']:
            children.append(
                {
                    'uuid': cuuid,
                    'name': list[cuuid]['name'],
                    'term': list[cuuid]['term'],
                }
            )
    return children


def get_children2(uuid, level):
    level = level + 1
    tmpstr = (
        ("\t" * level) + " " + list[uuid]['name'] + " (" + list[uuid]['term'] + ")\n"
    )
    tmpstr = tmpstr + ("").join(
        [get_children2(child['uuid'], level) for child in list[uuid]['children']]
    )
    return tmpstr


def get_children(uuid):
    tmp = {}
    tmp['uuid'] = uuid
    tmp['name'] = list[uuid]['name']
    tmp['term'] = list[uuid]['term']
    tmp['children'] = [get_children(child['uuid']) for child in list[uuid]['children']]
    return tmp


list = get_all()
for uuid, v in list.items():
    list[uuid]['children'] = find_children(list, uuid)

tree = get_children('971a8f57-d401-4e8b-9b1a-a1b97e46e0ea')
text = get_children2('971a8f57-d401-4e8b-9b1a-a1b97e46e0ea', -1)
print(text)
_store(tree, 'pure_ou.json')
with open('pure_list.txt', 'w') as f:
    f.write(text)
