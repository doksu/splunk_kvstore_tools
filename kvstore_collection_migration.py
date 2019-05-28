#!/usr/bin/python

import sys
import json
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

shost = ''
sport = '8089'
dhost = ''
dport = '8089'
suser = 'admin'
spassword = ''
duser = 'admin'
dpassword = ''
app = str(sys.argv[1])
collection = str(sys.argv[2])

print "Starting migration of collection " + collection + " in app " + app

scollection_url = ''.join(['https://',shost,':',sport,'/servicesNS/nobody/',app,'/storage/collections/data/',collection])
scollection_r = requests.get(scollection_url,auth=(suser,spassword),verify=False)
collection_json = json.loads(scollection_r.text)

print "Received " + str(len(collection_json)) + " records"

dcollection_headers = {'Content-type': 'application/json'}
dcollection_url = ''.join(['https://',dhost,':',dport,'/servicesNS/nobody/',app,'/storage/collections/data/',collection,'/batch_save'])
array_index = 0
end_record = len(collection_json)

while array_index < end_record:

    if array_index + 1000 < end_record:
        pass_end = array_index + 1000
    else:
        pass_end = end_record
   
    data = json.dumps(collection_json[array_index:pass_end])
    print "Sending records " + str(array_index) + " to " + str(pass_end)
    dcollection_r = requests.post(dcollection_url,auth=(duser,dpassword),verify=False,headers=dcollection_headers,data=data)

    if dcollection_r.status_code != 200:
        print dcollection_r.text
        break

    array_index = pass_end
    time.sleep(5)
