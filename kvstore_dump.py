#!/usr/bin/python

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Thanks https://github.com/georgestarcher/Splunk-createkvstore/blob/master/makekvstore.py for providing an example that helped me to create this tool

shost = ''
dhost = ''
sport = '8089'
dport = '8089'
suser = 'admin'
duser = 'admin'
spassword = ''
dpassword = ''

# get list of apps
apps_url = ''.join(['https://',shost,':',sport,'/servicesNS/nobody?output_mode=json'])
apps_r = requests.get(apps_url,auth=(suser,spassword),verify=False)
apps = json.loads(apps_r.text)

# for each app
for app in apps['entry']:

    # get a list of collections
    collections_url = ''.join(['https://',shost,':',sport,'/servicesNS/nobody/',app['name'],'/storage/collections/config?output_mode=json'])
    collections_r = requests.get(collections_url,auth=(suser,spassword),verify=False)
    collections = json.loads(collections_r.text)

    for collection in collections['entry']:

        # if the collection belongs to the app
        if collection['acl']['app'] == app['name']:

            # get the collection's records
            scollection_url = ''.join(['https://',shost,':',sport,'/servicesNS/nobody/',app['name'],'/storage/collections/data/',collection['name']])
            scollection_r = requests.get(scollection_url,auth=(suser,spassword),verify=False)
        
            # if the collection isn't empty
            if scollection_r.text != '[ ]':
                print "app=" + app['name'] + " collection=" + collection['name']
                print scollection_r.text
