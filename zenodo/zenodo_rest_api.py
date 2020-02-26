"""
Title: Access Zenodo's API 
Author: Brett G. Olivier

Usage::

 - Define an environment variable ZENODO_API_KEY that contains your  API key.
 - Define your queries in the queries list.
 - Run the file.


(C) Brett G. Olivier, VU Amsterdam, 2020. Licenced for use under the GNU GPL 3.0

"""

import os, requests, json, time, random, pprint

def testAPI(token, url):
    """
    Simple API test to see if we can connect to Zenodo

    """
    r = requests.get(url, params={'access_token' : token})
    print(r.status_code)
    print(r.json())

def recordsGet(token, query):
    """
    Get request, searches records for query string and returns json formatted results

    """
    time.sleep(random.randint(1, 4))
    params = {'access_token' : token,
              'q' : query
              }

    r = requests.get("https://zenodo.org/api/records", params=params)
    print('{}: {}'.format(query, r.status_code))
    return r.json()

def writeRecords(records, filename):
    """
    Write records to filename.json

    """
    if not filename.endswith('.json'):
        filename += '.json'
    with open(filename, 'w') as F:
        json.dump(records, F, indent=1)

if __name__ == '__main__':
    # Set an environmental variable ZENODO_API_KEY that contains your ZENODO API key
    if 'ZENODO_API_KEY' in os.environ:
        ZENODO_API_KEY = os.environ['ZENODO_API_KEY']
    else:
        print('\n\nNo ZENODO_API_KEY defined! Set an environmental variable ZENODO_API_KEY that contains your ZENODO API key.\n')
        os.sys.exit(-1)

    # first test the API
    testAPI(ZENODO_API_KEY, "https://zenodo.org/api/deposit/depositions")

    # define some queries
    queries = ["Vrije Universiteit Amsterdam", "VU University Amsterdam", "VU Amsterdam"]

    # and hit Zenodo exporting results per query
    for query in queries:
        res = recordsGet(ZENODO_API_KEY, query)
        writeRecords(res, query.replace(' ', '_').strip())
        




















'''
def pretty_print_POST(req):
    """
    https://stackoverflow.com/questions/20658572/python-requests-print-entire-http-request-raw/23816211#23816211

    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

# interesting for debugging
#req = requests.Request('POST','http://stackoverflow.com',headers={'X-Custom':'Test'},data='a=1&b=2')
#prepared = req.prepare()
#pretty_print_POST(prepared)
'''
