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

def recordsGet(token, query, hits=100):
    """
    Get request, searches records for query string and returns json formatted results. Don't go insane
    on the hits or Zenodo might start getting twitchy.

    - **token** Zenodo API token
    - **query** the institution query string
    - **hits** the number of hits to return (Zenodo API size)

    """
    time.sleep(random.randint(1, 4))
    params = {'access_token' : token,
              'q' : query,
              'size' : hits
              }

    r = requests.get("https://zenodo.org/api/records", params=params)
    print('{}: {}'.format(query, r.status_code))
    return r.json()

def writeRecordsToFile(records, filename):
    """
    Write records to filename.json

    """
    if not filename.endswith('.json'):
        filename += '.json'
    with open(filename, 'w') as F:
        json.dump(records, F, indent=1)

def extractMetadata(res, db, query):
    """
    Extract the metadata we need, Author, PubDate from search results and place them in doi keyed dict. Extracts VU names
    based on query and reformats names into Name Surname (if necessary).

    - **res** a results dict from a getRecords call
    - **db** doi keyed metadata dict
    - **query** the institution query string

    """
    #dbnew = {}

    print('\nProcessing metadata for {} potential hits for query: \"{}\"!'.format(len(res['hits']['hits']), query))
    for r_ in res['hits']['hits']:
        VALID = False
        auth_list = r_['metadata']['creators']
        vu_auth_list = []
        for a in auth_list:
            if 'affiliation' in a and a['affiliation'] == query:
                VALID = True
                name = a['name']
                if ',' in name:
                    sname = name.split(',')
                    name = '{} {}'.format(sname[1].strip(), sname[0].strip())
                vu_auth_list.append(name)
        if VALID:
            if r_['metadata']['doi'] in db:
                print('Duplicate DOI detected: {} overwriting.'.format(r_['metadata']['doi']))

            db[r_['metadata']['doi']] = {'pubdate' : r_['metadata']['publication_date'],
                                         'authors' : vu_auth_list,
                                         'type' : r_['metadata']['resource_type']['type'],
                                         'query' : query
                                         }
    #db[query] = dbnew
    return db

if __name__ == '__main__':
    cDir = os.path.dirname(os.path.abspath(os.sys.argv[0]))
    raw_data_path = os.path.join(cDir, 'raw_json')
    if not os.path.exists(raw_data_path):
        os.makedirs(raw_data_path)

    # Set an environmental variable ZENODO_API_KEY that contains your ZENODO API key
    if 'ZENODO_API_KEY' in os.environ:
        ZENODO_API_KEY = os.environ['ZENODO_API_KEY']
    else:
        print('\n\nNo ZENODO_API_KEY defined! Set an environmental variable ZENODO_API_KEY that contains your ZENODO API key.\n')
        os.sys.exit(-1)

    # first test the API
    #testAPI(ZENODO_API_KEY, "https://zenodo.org/api/deposit/depositions")

    metadata = {}
    timing = []

    # define some queries
    queries = ["Vrije Universiteit Amsterdam", "VU University Amsterdam", "VU Amsterdam"]
    #queries = ["Vrije Universiteit Amsterdam"]

    # and hit Zenodo exporting results per query, seems to be no advantage to use more than 500 hits.
    for query in queries:
        time0 = time.time()
        res = recordsGet(ZENODO_API_KEY, query, hits=500)
        timeGet = time.time()
        metadata = extractMetadata(res, metadata, query)
        timeExt = time.time()
        writeRecordsToFile(res, os.path.join(raw_data_path, query.replace(' ', '_').strip()))
        timeWrite = time.time()
        timing.append('Query: {}\n Get: {:03.2f}s\n Extract: {:03.2f}s\n Write: {:03.2f}s\n'.format(query,\
                                                                    timeGet-time0, timeExt-timeGet, timeWrite-timeExt))


    # dump metadata as a json dict
    with open('zenodo_search_results.json', 'w') as F:
        json.dump(metadata, F, indent=1)

    #pprint.pprint(metadata)
    print('')
    for t in timing:
        print(t)

    print('\n\nZenodo returned {} results from the requested search queries: \"{}\".'.format(len(metadata), queries))





















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
