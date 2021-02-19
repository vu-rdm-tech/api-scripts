"""
Title:
Author: Brett G. Olivier

Usage:

(C) Brett G. Olivier, VU Amsterdam, 2021. Licenced for use under the GNU GPL 3.0

# These need to be defined and passed into the module methods

expressions = ['Department', 'Research Institute']
searchkey = 'term'

output = {'Department' : {},
          'Research Institute' : {},
          'Acronymns' : [],
          }

# custom replacements, can be empty
custom_repl = collections.OrderedDict({})

# needs to be loaded from Peter's org data file
orgdata = None

"""

import os, json, pprint, collections

# These need to be defined and passed into the module methods
# using my current defaults - bgoli

expressions = ['Department', 'Research Institute']
searchkey = 'term'

# store output here, keys must include expressions as dictionaries and
# and a single 'Acronymns' list.
output = {
    'Department': {},
    'Research Institute': {},
    'Acronymns': [],
}

# custom replacements, can be empty
custom_repl = collections.OrderedDict(
    {
        'Mathematics': 'Math',
        'Philosophy': 'Phil',
        'Sociology': 'Socio',
        'Accounting': 'Acc',
        'Finance': 'Fin',
        'Marketing': 'Mrk',
        'Economics': 'Econ',
        'LaserLaB': 'Laser',
        '!': '',
        '-': '',
        '_': '',
        '(': '',
        ')': '',
        '+': '',
        '&': 'and',
        ' (WHO) ': ' ',
        ' for ': ' ',
        ' of ': ' ',
        ' and ': ' ',
    }
)

# print(custom_repl.items())


def find_all(branch, expr, key, acro_repl, out):
    for e in branch:
        if e == key and branch[key] in expr:
            acro = acronize(branch['name'], acro_repl)
            if acro in out['Acronymns']:
                print('Duplicate acronym', acro)
                # out['Acronymns'].insert(0, (acro, branch['name']))
                acro = acronize(branch['name'], acro_repl, duplicate=True)
            out['Acronymns'].append(acro)
            out[branch[key]][branch['name']] = acro
        elif e == 'children':
            for c in branch['children']:
                find_all(c, expr, key, acro_repl, out)


def acronize(words, replacements, duplicate=False):
    # single word names treated as Acronymns, shorten if needed.
    # words0 = words

    # clean phrase
    for r in replacements:
        words = words.replace(r, replacements[r])

    if len(words.split()) == 1:
        if not duplicate:
            words = words.upper()
        else:
            print('\nWARNING: not sure what to do with a duplicate single name:', words)
            raise (RuntimeWarning(), words)
    else:
        if not duplicate:
            words = ''.join(w[0] for w in words.split())
        else:
            # words = words.replace('and', ' ')
            words = ''.join(w[:2].upper() for w in words.split())

    # print(words0, ' --> ', words)
    return words


if __name__ == '__main__':
    cDir = os.path.dirname(os.path.abspath(os.sys.argv[0]))

    data_file = ''
    # data_path = os.path.join(cDir, 'data')
    # if not os.path.exists(data_path):
    # os.makedirs(data_path)

    with open(os.path.join(cDir, 'pure_ou.json'), 'r') as F:
        orgdata = json.load(F)

    find_all(orgdata, expressions, searchkey, custom_repl, output)

    pprint.pprint(output)
    with open('abbreviations.json', 'w') as F:
        json.dump(output, F, indent=' ')
