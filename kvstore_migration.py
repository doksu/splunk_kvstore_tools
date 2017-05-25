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
spassword = 'changeme'
dpassword = 'changeme'

# get list of apps
apps_url = ''.join(['https://',shost,':',sport,'/services/apps/local?output_mode=json'])
apps_r = requests.get(apps_url,auth=(suser,spassword),verify=False)
apps = json.loads(apps_r.text)

# for each app
for app in apps['entry']:
    # get a list of collections
    collections_url = ''.join(['https://',shost,':',sport,'/servicesNS/nobody/',app['name'],'/storage/collections/config?output_mode=json'])
    collections_r = requests.get(collections_url,auth=(suser,spassword),verify=False)
    collections = json.loads(collections_r.text)
    try:
        # for each collection
        for collection in collections['entry']:
            # get the collection's records
            scollection_url = ''.join(['https://',shost,':',sport,'/servicesNS/nobody/',app['name'],'/storage/collections/data/',collection['name']])
            scollection_r = requests.get(scollection_url,auth=(suser,spassword),verify=False)
            # if records were returned
            if scollection_r.status_code == 200:
                print app['name'] + " " + collection['name']
                # populate the destination collection
                dcollection_url = ''.join(['https://',dhost,':',dport,'/servicesNS/nobody/',app['name'],'/storage/collections/data/',collection['name'],'/batch_save'])
                dcollection_headers = {'Content-type': 'application/json'}
                try:
                    dcollection_r = requests.post(dcollection_url,auth=(duser,dpassword),verify=False,headers=dcollection_headers,data=scollection_r.text)
                    print dcollection_r.status_code
                except:
                    print dcollection_r.status_code
    except:
        continue
