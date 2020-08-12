import os
import csv
import pprint

def generate_header():
    output =\
        """
<html><body>
 <h2>Long list of tools and descriptions</h2>

<!--
 <div id="d_header">
  <p>
DO NOT EDIT THIS TEXT, use the tools and data file in the &quot;tool_descriptions&quot; folder on our <a href="https://github.com/vu-rdm-tech/api-scripts">api-script</a> repository to regenerate this section.<br/>
  </p>
 </div>
-->

 <div id="d_body">
{}
 </div>
 <br/>
</body></html>

        """
    return output

def write_to_file(idata, filename):
    doc = generate_header()
    body = ''
    with open(idata, 'r') as F:
        data = csv.DictReader(F, dialect='excel-tab')
        body += '<p>\n'
        idx = '<ol>\n'
        for row in data:
            idx += ' <li><a href="#tool_{}">{}</a></li>\n'.format(row['Name'].replace(' ', ''), row['Name'])
        idx += '</ol>\n'
        body += idx
        body += '</p>\n'
        F.seek(0)
        data = csv.DictReader(F, dialect='excel-tab')
        for row in data:
            display_uri = row['URI'].replace('https://', '').replace('http://', '')
            display_uri = display_uri.split('/')[0]
            if display_uri.endswith("/"):
                display_uri = display_uri[:-1]
            body += '<h3><a id="tool_{}">{}</a> (<a href="{}">{}</a>)</h3>\n'.format(row['Name'].replace(' ', ''), row['Name'], row['URI'], display_uri)
            keyword = row['Keyword']
            if keyword != '':
                keyword = '({})'.format(keyword)
            body += "<h4>Priority: {} {}</h4>".format(row['Priority'], keyword)
            if row['Description'] == 'Empty':
                body += '<p>\n<strong>TODO:</strong> <a href={}>{}</a>\n</p>\n'.format(row['URI'], row['URI'])
            else:
                body += '<p>\n{} '.format(row['Description'])
                if len(display_uri.split('.')) > 2:
                    src_uri = display_uri.split('.', len(display_uri.split('.'))-2)[-1]
                else:
                    src_uri = display_uri
                body += '<em>This description summarised from {}.</em></p>\n'.format(src_uri)


            body += '<hr/>\n'
    with open(filename, 'w') as F2:
        F2.write(doc.format(body))

if __name__ == '__main__':
    cDir = os.path.dirname(os.path.abspath(os.sys.argv[0]))
    input_data_file = 'tool_data.txt'
    idata = os.path.join(cDir, input_data_file)
    write_to_file(idata, 'doctext.html')

