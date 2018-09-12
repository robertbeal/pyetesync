#!/usr/bin/env python

import sys
import etesync as api
import json

class Collection:    
    def __init__(self, collection, journal):
        content = json.loads(collection.content)
        self.id = collection.uid
        self.version = collection.version       
        self.name = content['displayName']
        self.type = content['type']
        self.journal = [Entry(entry) for entry in journal.list()]

class Entry:
    def __init__(self, entry):
        content = json.loads(entry.content)
        self.id = entry.uid
        self.action = content['action']
        self.item = content['content']     

email = sys.argv[1]
password = sys.argv[2]
passphrase = sys.argv[3]
remote = sys.argv[4]

token = api.Authenticator(remote).get_auth_token(email, password)
etesync = api.EteSync(email, token, remote)
etesync.derive_key(passphrase)
etesync.sync()

collections = []
for entry in etesync.list():
    journal = etesync.get(entry.uid)
    collections.append(Collection(entry, journal))

print(json.dumps(collections, default=lambda o: o.__dict__))

