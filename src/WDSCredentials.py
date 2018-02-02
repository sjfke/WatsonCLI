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

    #===========================================================================
    # __init__
    #===========================================================================
    def __init__(self, filename):
        self.__username = None
        self.__password = None
        self.__version = '2017-11-07'
        self.__url = 'https://gateway.watsonplatform.net/discovery/api'

        with open(filename) as f:
            try:
                data = json.loads(f.read())
                if 'username' in data:
                    self.__username = data['username']
                if 'password' in data:
                    self.__password = data['password']
                if 'url' in data:
                    self.__url = data['url']
                if 'version' in data:
                    self.__version = data['version']

            except ValueError:
                config = SafeConfigParser()
                config.read(filename)
                data = config.items('discovery')
                for d in data:
                    if d[0] == 'username':
                        self.__username = d[1]
                    if d[0] == 'password':
                        self.__password = d[1]
                    if d[0] == 'url':
                        self.__url = d[1]
                    if d[0] == 'version':
                        self.__version = d[1]

    #===========================================================================
    # credentials
    #===========================================================================
    def credentials(self):
        '''
        Return Watson Discovery Service Credentials
        '''
        return {'username': self.__username, 'password': self.__password, 'url': self.__url, 'version': self.__version}

    #===========================================================================
    # username
    #===========================================================================
    def username(self):
        '''
        Return Watson Discovery Service username
        '''
        return self.__username

    #===========================================================================
    # password
    #===========================================================================
    def password(self):
        '''
        Return Watson Discovery Service Password
        '''
        return self.__password

    #===========================================================================
    # url
    #===========================================================================
    def url(self):
        '''
        Return Watson Discovery Service API URL
        '''
        return self.__url

    #===========================================================================
    # version
    #===========================================================================
    def version(self):
        '''
        Return Watson Discovery Service Version
        '''
        return self.__version


if __name__ == "__main__":

    wds = WDSCredentials('.gc.watson.json')
    print "JSON:"
    print wds.credentials()
    print "username: {0}".format(wds.username())
    print "password: {0}".format(wds.password())
    print "url: {0}".format(wds.url())
    print "version: {0}".format(wds.version())
    print

    wds = WDSCredentials('.gc.watson.cfg')
    print wds.credentials()
    print "username: {0}".format(wds.username())
    print "password: {0}".format(wds.password())
    print "url: {0}".format(wds.url())
    print "version: {0}".format(wds.version())

    sys.exit(0)
