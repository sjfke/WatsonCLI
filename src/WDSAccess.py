#!/usr/bin/env python3
from configparser import SafeConfigParser
import json
import logging
import os

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.ERROR)


class WDSAccess:
    '''
    IBM Watson Discovery Service Access Object
    '''
    #===========================================================================
    # __init__
    #===========================================================================

    def __init__(self, filename):
        self.__username = None
        self.__password = None
        self.__account = 'nobody@nowhere.com'
        self.__instance = 'wds instance'
        self.__version = '2017-11-07'
        self.__url = 'https://gateway.watsonplatform.net/discovery/api/V1'

        with open(filename) as f:
            try:
                data = json.loads(f.read())
                if 'username' in data:
                    self.__username = data['username']
                if 'password' in data:
                    self.__password = data['password']
                if 'account' in data:
                    self.__account = data['account']
                if 'instance' in data:
                    self.__account = data['instance']
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
                    if d[0] == 'account':
                        self.__account = d[1]
                    if d[0] == 'instance':
                        self.__instance = d[1]
                    if d[0] == 'url':
                        self.__url = d[1]
                    if d[0] == 'version':
                        self.__version = d[1]

    #===========================================================================
    # __str__
    #===========================================================================
    def __str__(self):
        '''
        String representation
        '''
        __str = ''
        __str += self.__username + ', '
        __str += self.__password + ', '
        __str += self.__account + ', '
        __str += self.__instance + ', '
        __str += self.__url + ', '
        __str += self.__version
        return __str

    #===========================================================================
    # __repr__
    #===========================================================================
    def __repr__(self):
        '''
        YAML like string representation
        '''
        __str = ''
        __str += "{0:<13s}: {1}".format('username', self.__username) + os.linesep
        __str += "{0:<13s}: {1}".format('password', self.__password) + os.linesep
        __str += "{0:<13s}: {1}".format('account', self.__account) + os.linesep
        __str += "{0:<13s}: {1}".format('instance', self.__instance) + os.linesep
        __str += "{0:<13s}: {1}".format('url', self.__url) + os.linesep
        __str += "{0:<13s}: {1}".format('version', self.__version)
        return __str

    #===========================================================================
    # get_username
    #===========================================================================
    def get_username(self):
        return self.__username

    #===========================================================================
    # get_password
    #===========================================================================
    def get_password(self):
        return self.__password

    #===========================================================================
    # get_account
    #===========================================================================
    def get_account(self):
        return self.__account

    #===========================================================================
    # get_version
    #===========================================================================
    def get_version(self):
        return self.__version

    #===========================================================================
    # get_url
    #===========================================================================
    def get_url(self):
        return self.__url

    #===========================================================================
    # set_version
    #===========================================================================
    def set_version(self, value):
        self.__version = value

    #===========================================================================
    # set_url
    #===========================================================================
    def set_url(self, value):
        self.__url = value

    #===========================================================================
    # get_user
    #===========================================================================
    def get_user(self):
        return {'username': self.__username, 'password': self.__password, 'account': self.__account}

    #===========================================================================
    # credentials
    #===========================================================================
    def get_credentials(self):
        return {'username': self.__username, 'password': self.__password, 'url': self.__url, 'version': self.__version}

    username = property(get_username, None, None, None)
    password = property(get_password, None, None, None)
    account = property(get_account, None, None, None)
    version = property(get_version, set_version, None, None)
    url = property(get_url, set_url, None, None)
    user = property(get_user, None, None, None)
    credentials = property(get_credentials, None, None, None)
