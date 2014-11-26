import sys
import requests
import pprint
import collections

with open('projectdb.auth') as f:
    credentials = [x.strip().split(':') for x in f.readlines()]


pp = pprint.PrettyPrinter()

if len(sys.argv) == 2:
    gridmapfile = sys.argv[1]
else:
    gridmapfile = None

users = {}

r = requests.post(
    'https://projects.nesi.org.nz:443'
    '/projectdb/rest/advisers/with_properties',
    auth=(credentials[0][0], credentials[0][1]),
    verify=False, data='DN,linuxUsername')

data = r.json()

for full_adviser in data:
    full_name = full_adviser['adviser']['fullName']
    properties = full_adviser['properties']
    dns = []
    usernames = []
    fav_username = ''
    for prop in properties:
        if prop['propname'] == 'DN':
            dns.append(prop['propvalue'])
        elif prop['propname'] == 'linuxUsername':
            usernames.append(prop['propvalue'])
        elif prop['propname'] == 'mainLinuxUsername':
            fav_username = prop['propvalue']

    if not fav_username:
        if len(usernames) == 1:
            fav_username = usernames[0]
        elif len(usernames) > 1:
            fav_username = min(usernames, key=len)
        # random username if 'mainLinuxUsername' is not specified

    if not fav_username:
        continue

    for dn in dns:
        users[dn] = fav_username
        if 'slcs' in dn:
            dn_mpp = dn.replace("/DC=nz/DC=org/DC=bestgrid/DC=slcs/",
                                "/DC=nz/DC=org/DC=nesi/DC=myproxyplus/")
            if 'The University of Auckland' in dn:
                dn_mpp = dn_mpp.replace("The University of Auckland",
                                        "University of Auckland")
            elif 'University of Otago' in dn:
                dn_mpp = dn_mpp.replace("University of Otago",
                                        "The University of Otago")
            users[dn_mpp] = fav_username

r = requests.post(
    'https://projects.nesi.org.nz:443'
    '/projectdb/rest/researchers/with_properties',
    auth=(credentials[0][0], credentials[0][1]),
    verify=False, data='DN,linuxUsername')

data = r.json()

for full_researcher in data:
    full_name = full_researcher['researcher']['fullName']
    properties = full_researcher['properties']
    dns = []
    usernames = []
    fav_username = ''
    for prop in properties:
        if prop['propname'] == 'DN':
            dns.append(prop['propvalue'])
        elif prop['propname'] == 'linuxUsername':
            usernames.append(prop['propvalue'])
        elif prop['propname'] == 'mainLinuxUsername':
            fav_username = prop['propvalue']

    if not fav_username:
        if len(usernames) == 1:
            fav_username = usernames[0]
        elif len(usernames) > 1:
            fav_username = min(usernames, key=len)
        # random username if 'mainLinuxUsername' is not specified

    if not fav_username:
        continue

    for dn in dns:
        users[dn] = fav_username
        if 'slcs' in dn:
            dn_mpp = dn.replace("/DC=nz/DC=org/DC=bestgrid/DC=slcs/",
                                "/DC=nz/DC=org/DC=nesi/DC=myproxyplus/")
            if 'The University of Auckland' in dn:
                dn_mpp = dn_mpp.replace("The University of Auckland",
                                        "University of Auckland")
            elif 'University of Otago' in dn:
                dn_mpp = dn_mpp.replace("University of Otago",
                                        "The University of Otago")
            users[dn_mpp] = fav_username


# sort by dn
sorted_users = collections.OrderedDict()
for dn in sorted(users.keys()):
    sorted_users[dn] = users[dn]

if gridmapfile:
    with open(gridmapfile, "w") as myfile:

        for dn, username in sorted_users.iteritems():
            myfile.write("\""+dn+"\" "+username+"\n")
else:

    for dn, username in sorted_users.iteritems():
        print ("\""+dn+"\" "+username)
