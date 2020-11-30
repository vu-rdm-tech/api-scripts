import json

from pure.config import PURE_APIKEY, PURE_USERNAME, PURE_PASSWORD, PURE_ORGANISATIONALUNITS_URL
import requests
import requests_cache

#https://research.vu.nl/ws/api/518/api-docs/index.html#!/organisational45units/listOrganisationalUnits

requests_cache.install_cache(cache_name='pure_ou_requests_cache', allowable_methods=('GET', 'POST'))

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

    res = requests.post(PURE_ORGANISATIONALUNITS_URL, headers=headers, params=payload, data=data, auth=(PURE_USERNAME, PURE_PASSWORD))
    try:
        cached = res.from_cache
    except:
        cached = False
    if res.status_code == 200:
        return res, cached
    else:
        raise Exception('*** Got: status_code: %s' % res.status_code)


def get_all():
    reqJSON = '{}' # seems to be enough to get all
    res, cached = _do_postrequest(data=reqJSON, size=1, offset=0)
    data = json.loads(res.content)
    count = data['count']

    list={}
    size = 10
    for offset in range(0, count, size):
        res, cached = _do_postrequest(data=reqJSON, size=size, offset=offset)
        data = json.loads(res.content)
        items = data['items']

        for item in items:
            name = item['name']['text'][0]['value']
            print(name)
            term = item['type']['term']['text'][0]['value']

            uuid = item['uuid']
            parents=[]
            if 'parents' in item:
                for parent in item['parents']:
                    parents.append(parent['uuid'])

            list[uuid]={}
            list[uuid]['name']=name
            list[uuid]['term']=term
            list[uuid]['parents']=parents


    return list

list = get_all()

for uuid, v in list.items():
    list[uuid]['parent_names']=[]
    for parent in v['parents']:
        try:
            list[uuid]['parent_names'].append(list[parent]['name'])
        except:
            #print(parent, 'does not exist?')
            pass

_store(list, 'pure_ou.json')




