#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import os
from ConfigParser import SafeConfigParser


class WDSCredentials:
    '''
    IBM Watson Discovery Login Credentials
    '''

    def __init__(self, filename):
        self.username = None
        self.password = None
        self.version = '2017-11-07'
        self.url = 'https://gateway.watsonplatform.net/discovery/api'

        with open(filename) as f:
            try:
                data = json.loads(f.read())
                if 'username' in data:
                    self.username = data['username']
                if 'password' in data:
                    self.password = data['password']
                if 'url' in data:
                    self.url = data['url']
                if 'version' in data:
                    self.version = data['version']

            except ValueError:
                config = SafeConfigParser()
                config.read(filename)
                data = config.items('discovery')
                for d in data:
                    if d[0] == 'username':
                        self.username = d[1]
                    if d[0] == 'password':
                        self.password = d[1]
                    if d[0] == 'url':
                        self.url = d[1]
                    if d[0] == 'version':
                        self.version = d[1]

if __name__ == "__main__":

    wds = WDSCredentials('.gc.watson.json')
    print "JSON:"
    print "username: {0}".format(wds.username)
    print "password: {0}".format(wds.password)
    print "url: {0}".format(wds.url)
    print "version: {0}".format(wds.version)

    wds = WDSCredentials('.gc.watson.cfg')
    print "Configuration:"
    print "username: {0}".format(wds.username)
    print "password: {0}".format(wds.password)
    print "url: {0}".format(wds.url)
    print "version: {0}".format(wds.version)

    sys.exit(0)
