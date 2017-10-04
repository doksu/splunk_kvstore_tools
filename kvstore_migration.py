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

    print "Looking for collections in app: " + app['name']

    # get a list of collections
    collections_url = ''.join(['https://',shost,':',sport,'/servicesNS/nobody/',app['name'],'/storage/collections/config?output_mode=json'])
    collections_r = requests.get(collections_url,auth=(suser,spassword),verify=False)
    collections = json.loads(collections_r.text)

    for collection in collections['entry']:

        # if the collection belongs to the app
        if collection['acl']['app'] == app['name']:

            print "Found collection: " + collection['name']
        
            # get the collection's records
            scollection_url = ''.join(['https://',shost,':',sport,'/servicesNS/nobody/',app['name'],'/storage/collections/data/',collection['name']])
            scollection_r = requests.get(scollection_url,auth=(suser,spassword),verify=False)
        
            # if the collection isn't empty
            if scollection_r.text != '[ ]':

                collection_json = json.loads(scollection_r.text)
                collection_size = len(collection_json)
                print "Collection size: " + str(collection_size)
                dcollection_headers = {'Content-type': 'application/json'}
                dcollection_url = ''.join(['https://',dhost,':',dport,'/servicesNS/nobody/',app['name'],'/storage/collections/data/',collection['name'],'/batch_save'])

                if collection_size < 1000:
                    # populate the destination collection
                    dcollection_r = requests.post(dcollection_url,auth=(duser,dpassword),verify=False,headers=dcollection_headers,data=scollection_r.text.encode('utf-8'))
                    if dcollection_r.status_code != 200:
                        print dcollection_r.text
                else:
                    start_record = 0
                    end_record = 1000
                    passes = (len(collection_json)/1000)+1
                    print "Performing " + str(passes) + " passes"
                    p = 1
                    while p <= passes:
                        data = json.dumps(collection_json[start_record:end_record])
                        dcollection_r = requests.post(dcollection_url,auth=(duser,dpassword),verify=False,headers=dcollection_headers,data=data)
                        if dcollection_r.status_code != 200:
                            print dcollection_r.text
                            p = passes + 1
                        start_record = end_record
                        end_record += 1000
                        p += 1
            else:
                print "Collection is empty"
