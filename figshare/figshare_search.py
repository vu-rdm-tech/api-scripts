# From fugshare
"""
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ArticlesApi()
search =  {
  "order": "published_date",
  "search_for": "(:description: VU OR :description: Vrije) AND :description: Amsterdam",
  "order_direction": "desc"
}

try:
    # Public Articles Search
    api_response = api_instance.articles_search(search=search)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ArticlesApi->articlesSearch: %s\n" % e)
"""


# Sanity prevails


import os
import requests
import json
import time
import random
import xlsxwriter
import datetime
import pprint


def fugshareSearch(token, url, params={}):
    """
    Fugshare article search, returns some JSON

    - *token* access token
    - *params* parameters

    """
    params['access_token'] = token
    r = requests.post(url, params=params)
    #print(r.status_code)
    #pprint.pprint(r.json())
    return r.json()

def fugshareFilterCopiedResults(db):
    """
    Filter out non-figshare results taken from other databases.
    - *db* results of a fugshareSearch

    """
    fake_results = []
    fail_results = []
    real_res = 0
    fake_res = 0
    fail_res = 0
    for r in db:
        try:
            if db[r]['url_public_html'].startswith('https://figshare.com'):
                real_res += 1
            else:
                fake_res += 1
                fake_results.append(r)
        except:
            fail_res += 1
            fail_results.append(r)
        print('***\nReal {}\nFake {}\n***\n'.format(real_res, fake_res))
    print(fake_results)
    for id in fake_results:
        a = db.pop(id)
    return db

def addToDB(db, res):
    for r in res:
        if r['id'] not in db:
            db[r['id']] = r
        else:
            print('Duplicate id: {}'.format(db['id']))
    return db



if __name__ == '__main__':
    cDir = os.path.dirname(os.path.abspath(os.sys.argv[0]))
    raw_data_path = os.path.join(cDir, 'raw_json')
    if not os.path.exists(raw_data_path):
        os.makedirs(raw_data_path)

    # Set an environmental variable FIGSHARE_API_KEY that contains your ZENODO API key
    if 'FIGSHARE_API_KEY' in os.environ:
        FIGSHARE_API_KEY = os.environ['FIGSHARE_API_KEY']
    else:
        print('\n\nNo FIGSHARE_API_KEY defined! Set an environmental variable FIGSHARE_API_KEY that contains your ZENODO API key.\n')
        os.sys.exit(-1)


    search_par = {"search_for": '(:description: "VU" OR :description: "Vrije") AND :description: "Amsterdam"',
                  "published_since" : '2010-01-01'
                  }

    # get some data
    db = {}

    url = "https://api.figshare.com/v2/articles/search"
    addToDB(db, fugshareSearch(FIGSHARE_API_KEY, url, search_par))

    url = "https://api.figshare.com/v2/collections/search"
    addToDB(db, fugshareSearch(FIGSHARE_API_KEY, url, search_par))

    url = "https://api.figshare.com/v2/projects/search"
    addToDB(db, fugshareSearch(FIGSHARE_API_KEY, url, search_par))

    res = fugshareFilterCopiedResults(db)


    pprint.pprint(res)
    print('\nNumber of real results: {}\n'.format(len(res)))


    for r in db:
        try:
            public_url = db[r]['url_public_html']
            url = db[r]['url']
        except:
            public_url = url = db[r]['url']

        print('{}\n{}\n{}\n'.format(db[r]['title'], url, public_url))


    url = "https://api.figshare.com/v2/articles/5106808"
    requests.get(url, params={})