import sys
import requests
import pprint
import collections

with open('projectdb.auth') as f:
    credentials = [x.strip().split(':') for x in f.readlines()]


pp = pprint.PrettyPrinter()

users = {}

r = requests.post(
    'https://projects.nesi.org.nz:443'
    '/projectdb/rest/researchers/with_properties',
    auth=(credentials[0][0], credentials[0][1]),
    verify=False, data='linuxUsername')

data = r.json()

for full_researcher in data:
    full_name = full_researcher['researcher']['fullName']
    email = full_researcher['researcher']['email']
    properties = full_researcher['properties']
    dns = []

    for prop in properties:
        if prop['propname'] == 'linuxUsername':
            users[prop['propvalue']] = email


# sort by dn
sorted_users = collections.OrderedDict()
for dn in sorted(users.keys()):
    sorted_users[dn] = users[dn]

for username, email in sorted_users.iteritems():
        print (username + " " + email)
