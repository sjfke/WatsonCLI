#!/usr/bin/env python
#
import argparse
import os
import re
import sys


def get_watson_credentials(cfg):
    """ Return a List of Watson Discovery Environments

        Args:
            cfg (str): Configuration file with Watson credentials

        Returns:
            dictionary: (username, password, version)

    """

    from ConfigParser import SafeConfigParser

    config = SafeConfigParser()
    config.read(cfg)
    result = {}
    result['username'] = config.get('discovery', 'username')
    result['password'] = config.get('discovery', 'password')
    result['version'] = config.get('discovery', 'version')

    return result


def list_environments(cred):
    """ Return Watson Discovery Environments

        Args:
            cred (dictionary): Watson credentials

        Returns:
            str: JSON results

    """

    import json
    import requests
    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    payload = {}
    payload['version'] = cred['version']

    r = requests.get(api, params=payload, auth=(cred['username'], cred['password']))
    if args.verbose >= 1:
        print('Request: ' + r.url)

    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
    return r.text


def list_environments_summary(cred):
    """ Return a List of Watson Discovery Environments Id

        Args:
            cred (dictionary): Watson credentials

        Returns:
            str: <index>: <id>, <name>, <description> 

    """

    import json
    envs = json.loads(list_environments(cred))
    results = []
    for env in envs['environments']:
        result = {'id': env['environment_id'], 'name': env['name'], 'descr': env['description']}
        results.append(result)

    return results


def get_environment_ids(cred):
    """ Return a List of Watson Discovery Environments Id

        Args:
            cred (dictionary): Watson credentials

        Returns:
            list: Watson Environment Ids

    """

    import json
    envs = json.loads(list_environments(cred))
    results = []
    for env in envs['environments']:
        results.append(env['environment_id'])

    return results


def get_environment_summary(cred, envid):
    """ Return Summary of Watson Discovery Environment

        Args:
            cred (dictionary): Watson credentials
            envid (str): Watson environment_id

        Returns:
            str: JSON results

    """

    import json
    import requests

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid
    payload = {}
    payload['version'] = cred['version']

    r = requests.get(api, params=payload, auth=(cred['username'], cred['password']))
    if args.verbose >= 1:
        print('Request: ' + r.url)

    return r.text


def create_discovery_environment(cred, name, descr):
    """ Create Discovery Environment (REST + post)

        Args:
            cred (dictionary): Watson Credentials (username, password, version)
            name (str): mandatory environment name
            descr (str): optional environment description

        Returns:
            str: JSON results

    """
    import json
    import requests

    # TODO: Figure out with this fails; Create Environment Failed: 201
    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '?version=' + cred['version']

    data = {'name': name, 'description': descr}
    r = requests.post(api, json=data, auth=(cred['username'], cred['password']))

    if args.verbose >= 1:
        print('Request: ' + r.url)

    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        print "Create Environment Failed: {0}".format(r.status_code)
        return None


def delete_discovery_environment(cred, envid):
    """ Delete Discovery Environment (REST + post)

        Args:
            cred (dictionary): Watson Credentials (username, password, version)
            envid (str): mandatory environment_id

        Returns:
            str: JSON results

    """
    import json
    import requests

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid
    payload = {}
    payload['version'] = cred['version']

    r = requests.delete(api, params=payload, auth=(cred['username'], cred['password']))
    if args.verbose >= 1:
        print('Request: ' + r.url)

    return r.text

# TODO: add document upload
# https://www.ibm.com/watson/developercloud/discovery/api/v1/
# https://console.bluemix.net/docs/services/discovery/getting-started.html#getting-started-with-the-api

if __name__ == "__main__":
    watson_cfg_file = os.path.join(os.getcwd(), '.watson.cfg')
    parser = argparse.ArgumentParser(description='Discovery REST interface')
    parser.add_argument('-C', '--create-environment', help='Create Discovery environment')
    parser.add_argument('-d', '--description', default=None, help='description for create command')
    parser.add_argument('-D', '--delete', type=int, default=-1, help='environment index')
    parser.add_argument('-c', '--cfg', default='.watson.cfg', help='Watson credentials')
    parser.add_argument('-e', '--environment', type=int, default=-1, help='environment index')
    parser.add_argument('-l', '--list', help='indexed list environments', action='store_true')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    if args.verbose >= 1:
        print "watson-cfg: '{0}'".format(args.cfg)

    credentials = get_watson_credentials(args.cfg)
    envids = get_environment_ids(cred=credentials)

    if args.list:
        # print list_environments(cred=credentials)
        result = list_environments_summary(cred=credentials)
        for i, val in enumerate(result):
            print "{0}: id={1[id]}; name={1[name]}; descr={1[descr]};".format(i, val)

    elif args.environment >= 0:
        if args.environment < len(envids):
            envid = envids[args.environment]
            result = get_environment_summary(cred=credentials, envid=envid)
            print result
        else:
            print "invalid index, '{0:d}' # try: {1} --list".format(args.environment, sys.argv[0])
            sys.exit(1)
    elif args.create:
        create_discovery_environment(cred=credentials, name=args.create, descr=args.description)
    elif args.delete and args.delete >= 0:
        if args.environment < len(envids):
            envid = envids[args.environment]
            result = delete_discovery_environment(cred=credentials, envid=envid)
            print result
        else:
            print "invalid index, '{0:d}' # try: {1} --list".format(args.environment, sys.argv[0])
            sys.exit(1)
        
    else:
        print "bugger"
        result = get_environment_ids(credentials)
        print result

    sys.exit(0)
