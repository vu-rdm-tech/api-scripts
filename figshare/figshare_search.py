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
import copy
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
    db2 = copy.deepcopy(db)

    for r in db:
        try:
            if db[r]['url_public_html'].startswith('https://figshare.com'):
                real_res += 1
            else:
                fake_res += 1
                fake_results.append(r)
                null = db2.pop(r)
        except:
            fail_res += 1
            fail_results.append(r)
    print('***\nReal {}\nFake {}\nFail {}\n***\n'.format(real_res, fake_res, fail_res))
    return db2


def addToDB(db, res):
    for r in res:
        if r['id'] not in db:
            db[r['id']] = r
        else:
            print('Duplicate id: {}'.format(db['id']))
    return db

def printDB(db):
    for r in db:
        try:
            public_url = db[r]['url_public_html']
            url = db[r]['url']
        except:
            public_url = url = db[r]['url']

        print('{}\n{}\n{}\n'.format(db[r]['title'], url, public_url))

def getAuthorsFromRecords(db):
    output = {}
    for r in db:
        print(r)
        try:
            public_url = db[r]['url_public_html']
            url = db[r]['url']
        except:
            public_url = url = db[r]['url']

        print('{}\n{}\n{}\n'.format(db[r]['title'], url, public_url))
        output[r] = {'title' : db[r]['title'],
                     'url' : url,
                     'public_url' : public_url,
                     'authors' : [],
                     'citation' : '',
                     'categories' : [],
                     'description' : '',
                     'date' : '',
                     'json' : ''

        }
        params = {'access_token' : FIGSHARE_API_KEY}
        res2 = requests.get(url, params)
        print(res2.status_code)
        rec = res2.json()
        del res2
        output[r]['citation'] = rec['citation']
        output[r]['categories'] = [a['title'] for a in rec['categories']]
        output[r]['description'] = rec['description']
        output[r]['date'] = rec['created_date']
        for aut in rec['authors']:
            output[r]['authors'].append((aut['full_name'], aut['orcid_id']))
        #output[r]['json'] = rec
        output[r]['json'] = {}
    return output


def writeToExcel(db, filename):
    """
    Write authors to Excel spreadsheet

    """
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'
    xls = xlsxwriter.Workbook(filename)
    xls.nan_inf_to_errors = True
    fmt_head = xls.add_format({'bold': True, 'align': 'center'})
    fmt_date = xls.add_format({'num_format': 'yyyy-m-d'})

    xldat = xls.add_worksheet('authors')
    xldat.write_string(0, 0, 'Name', fmt_head)
    xldat.write_string(0, 1, 'Orcid', fmt_head)
    xldat.write_string(0, 2, 'Email', fmt_head)
    xldat.write_string(0, 3, 'Id', fmt_head)
    xldat.write_string(0, 4, 'Title', fmt_head)
    xldat.write_string(0, 5, 'Citation', fmt_head)
    xldat.write_string(0, 6, 'Description', fmt_head)
    xldat.write_string(0, 7, 'Categories', fmt_head)
    xldat.write_string(0, 8, 'Date', fmt_head)

    row = 1
    for d in data:
        print('\n{}'.format(data[d]['title']))
        for a in data[d]['authors']:
            print('\t{}, {}'.format(a[0], a[1]))
            xldat.write_string(row, 0, a[0])
            xldat.write_string(row, 1, a[1])
            xldat.write_string(row, 3, str(d))
            xldat.write_string(row, 4, data[d]['title'])
            xldat.write_string(row, 5, data[d]['citation'])
            xldat.write_string(row, 6, data[d]['description'])
            xldat.write_string(row, 7, ','.join(data[d]['categories']))
            xldat.write_string(row, 8, data[d]['date'])
            row += 1
    xls.close()


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


    printDB(db)
    print('\nNumber of results: {}\n'.format(len(db)))

    printDB(res)
    print('\nNumber of real results: {}\n'.format(len(res)))

    data = getAuthorsFromRecords(res)
    pprint.pprint(data)

    with open(os.path.join(raw_data_path, 'raw_data.json'), 'w') as F:
        json.dump(data, F, indent=1)


    writeToExcel(data, 'figshare_data.xlsx')