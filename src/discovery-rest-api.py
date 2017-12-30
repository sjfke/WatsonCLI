#!/usr/bin/env python
#
import argparse
import os
import re
import sys
import json
import requests


def get_watson_credentials(filename):
    """ Return a List of Watson Discovery Environments

        Args:
            cfg (str): Configuration file with Watson credentials

        Returns:
            dictionary: (username, password, version)

    """

    if not os.access(filename, os.R_OK):
        print "Error: reading Watson credentials file '{0}: ".format(filename)
        sys.exit(1)

    from ConfigParser import SafeConfigParser

    config = SafeConfigParser()
    config.read(filename)
    result = {}
    result['username'] = config.get('discovery', 'username')
    result['password'] = config.get('discovery', 'password')
    result['version'] = config.get('discovery', 'version')

    return result


def list_environments(credentials, raw=True):
    """ Return Watson Discovery Environments

        Args:
            credentials (dictionary): Watson credentials
            raw (boolean): JSON output

        Returns:
            str: JSON results

    """

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    payload = {}
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print('Request: ' + r.url)

#     {
#       "environments" : [ {
#         "environment_id" : "system",
#         "name" : "Watson System Environment",
#         "description" : "Shared system data sources",
#         "read_only" : true
#       }, {
#         "environment_id" : "71cac327-84eb-4327-81da-24d49f14a445",
#         "name" : "test api",
#         "description" : "why not",
#         "created" : "2017-12-26T19:42:05.004Z",
#         "updated" : "2017-12-26T19:42:05.004Z",
#         "read_only" : false
#       } ]
#     }
    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
    if r.status_code != requests.codes.ok:
        print "List Collections Failed: {0}".format(r.status_code)
        return None
    else:
        if raw:
            return r.text
        else:
            envs = json.loads(r.text)
            environment_list = []
            for e in envs['environments']:
                environment_list.append(e)

            if len(environment_list):
                return environment_list
            else:
                return None


def list_configurations(credentials, envid, raw=True):
    """ Return Watson Discovery Configurations

        Args:
            credentials (dictionary): Watson credentials
            envid (str): Watson environment_id
            raw (boolean): JSON output

        Returns:
            str: JSON results

    """
    if envid == -1:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    # curl -u "{username}":"{password}"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/configurations?version=2017-11-07"
    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/configurations'
    payload = {}
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print('Request: ' + r.url)

    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
#     {
#       "collections" : [ {
#         "collection_id" : "5bbeb90b-08b6-4eb4-b5cf-82b7ed0aada1",
#         "name" : "TestOne",
#         "configuration_id" : "108f7bf9-9c16-43ec-853c-7c877b12b36b",
#         "language" : "en",
#         "status" : "active",
#         "description" : null,
#         "created" : "2017-12-26T19:44:07.225Z",
#         "updated" : "2017-12-26T19:44:07.225Z"
#       } ]
#     }

    if r.status_code != requests.codes.ok:
        print "List Configurations Failed: {0}".format(r.status_code)
        return None
    else:
        if raw:
            return r.text
        else:
            cfgs = json.loads(r.text)
            configuration_list = []
            for e in cfgs['configurations']:
                configuration_list.append(e)

            if len(configuration_list):
                return configuration_list
            else:
                return None


def list_collections(credentials, envid, raw=True):
    """ Return Watson Discovery Collections

        Args:
            credentials (dictionary): Watson credentials
            envid (str): Watson environment_id
            raw (boolean): JSON output

        Returns:
            str: JSON results

    """
    if envid == -1:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    # https://www.ibm.com/watson/developercloud/discovery/api/v1/?curl#create-collection
    # curl \
    # -u "{username}":"{password}" \
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections?version=2017-11-07"
    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections'
    payload = {}
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print('Request: ' + r.url)

    # return "list_collections({0},{1})".format(credentials,envid)
    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
#     {
#       "collections" : [ {
#         "collection_id" : "5bbeb90b-08b6-4eb4-b5cf-82b7ed0aada1",
#         "name" : "TestOne",
#         "configuration_id" : "108f7bf9-9c16-43ec-853c-7c877b12b36b",
#         "language" : "en",
#         "status" : "active",
#         "description" : null,
#         "created" : "2017-12-26T19:44:07.225Z",
#         "updated" : "2017-12-26T19:44:07.225Z"
#       } ]
#     }

    if r.status_code != requests.codes.ok:
        print "List Collections Failed: {0}".format(r.status_code)
        return None
    else:
        if raw:
            return r.text
        else:
            cols = json.loads(r.text)
            collection_list = []
            for e in cols['collections']:
                collection_list.append(e)

            if len(collection_list):
                return collection_list
            else:
                return None


def get_collections_ids(credentials, envids):
    """ Return Watson Discovery Collections

        Args:
            credentials (dictionary): Watson credentials
            envids (list): Watson environment_id's

        Returns:
            list: collection_ids

    """
    collection_ids = []
    for e in envids:
        collections = list_collection(credentials=credentials, envid=e)
        for c in collections['collections']:
            collection_ids.append(['collection_id'])

    return collection_ids


def list_documents(credentials, envid, colid=None, raw=True):
    """ Return Watson Discovery Documents

        Args:
            credentials (dictionary): Watson credentials
            envid (str): Watson environment_id
            colid (str): Watson collection_id

        Returns:
            str: JSON results

    """
    if envid == -1:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if colid == -1:
        print "Missing collection_id; hint {0} -L configurations --envid <envid>".format(sys.argv[0])
        sys.exit(1)
        
    # GC: 2017.12.30: not sure this is supported...
    # GET /v1/environments/{environment_id}/collections/{collection_id}/documents}
    # curl -u "{username}":"{password}"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections/' + colid + '/documents' 
    payload = {}
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print('Request: ' + r.url)

    if r.status_code != requests.codes.ok:
        print "List Documents Failed: {0}".format(r.status_code)
        return None
    else:
        if raw:
            return r.text
 
    # return "list_collections({0},{1})".format(credentials,envid)
    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
    return "list_documents({0},{1},{2})".format(credentials, envid, colid)


def list_environment(credentials, envid):
    """ Return Watson Discovery Environment Details

        Args:
            credentials (dictionary): Watson credentials
            envid (str): Watson environment_id

        Returns:
            str: JSON results

    """

    return "list_environment({0},{1})".format(credentials, envid)


def list_configuration(credentials, envid, cfgid):
    """ Return Watson Discovery Configuration Details

        Args:
            credentials (dictionary): Watson credentials
            envid (str): Watson environment_id
            cfgid (str): Watson configuration_id

        Returns:
            str: JSON results

    """

    return "list_configuration({0},{1},{2})".format(credentials, envid, cfgid)


def list_collection(credentials, envid, colid):
    """ Return Watson Discovery Collection Details

        Args:
            credentials (dictionary): Watson credentials
            envid (str): Watson environment_id
            colid (str): Watson collection_id

        Returns:
            str: JSON results

    """

    return "list_collection({0},{1},{2})".format(credentials, envid, colid)


def list_document(credentials, envid, colid, docid):
    """ Return Watson Discovery Document Details

        Args:
            credentials (dictionary): Watson credentials
            envid (str): Watson environment_id
            colid (str): Watson collection_id
            docid (str): Watson document_id

        Returns:
            str: JSON results

    """

    return "list_document({0},{1},{2},{3})".format(credentials, envid, colid, docid)


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
    parser.add_argument('-C', '--create', help='(environment|collection)')
    parser.add_argument('-D', '--delete', help='(environment|configuration|collection|document)')
    parser.add_argument('-L', '--list', help='(environment[s]|configuration[s]|collection[s]|document[s])')
    parser.add_argument('-U', '--update', help='(environment|configuration|collection|document)')
    parser.add_argument('-d', '--description', default=None, help='description for create command')
    parser.add_argument('-n', '--name', default=None, help='name for create command')
    parser.add_argument('--envid', type=int, default=-1, help='environment index')
    parser.add_argument('--cfgid', type=int, default=-1, help='configuration index')
    parser.add_argument('--colid', type=int, default=-1, help='collection index')
    parser.add_argument('--docid', type=int, default=-1, help='document index')
    parser.add_argument('-a', '--auth', default='.watson.cfg', help='Watson credentials')
    parser.add_argument('--raw', help='JSON output', default=False, action='store_true')
    parser.add_argument('-s', '--separator', help='delimited', default='\n  ')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    if args.verbose >= 1:
        print "watson-cfg: '{0}'".format(args.auth)

    credentials = get_watson_credentials(args.auth)
    envids = get_environment_ids(cred=credentials)

    create_allowed = ['environment', 'collection']
    delete_allowed = ['environment', 'configuration', 'collection', 'document']
    list_allowed = ['environments', 'configurations', 'collections', 'documents', 'environment', 'configuration', 'collection', 'document']
    delete_allowed = ['environment', 'configuration', 'collection', 'document']

    if args.list:
        if not (args.list.lower() in list_allowed):
            print"{0}: invalid argument, '{1}'".format(sys.argv[0], args.list)
            sys.exit(1)

        list_lower = args.list.lower()

        if list_lower == 'environments':
            pass
        elif args.envid < len(envids) and args.envid >= 0:
            envid = envids[args.envid]
        else:
            print "Error: invalid envid='{0}'; try {1} -L environments".format(args.envid, sys.argv[0])
            sys.exit(1)

        if list_lower == 'environments':
            result = list_environments(credentials=credentials, raw=args.debug)
            if result is None:
                print "No Environments?"
                sys.exit(1)
            elif args.raw:
                print result
            else:
                for i, val in enumerate(result):
                    print "{0}: id={1[environment_id]}{2}name={1[name]}{2}descr={1[description]}{2}".format(i, val, args.separator)

        elif list_lower == 'configurations':
            result = list_configurations(credentials=credentials, envid=envid, raw=args.raw)
            if result is None:
                print "No configurations for, '{0}'".format(envid)
            elif args.raw:
                print result
            else:
                for i, val in enumerate(result):
                    print "{0}: id={1[configuration_id]}{2}name={1[name]}{2}descr={1[description]}{2}created={1[created]}{2}updated={1[updated]}".format(i, val, args.separator)

        elif list_lower == 'collections':
            result = list_collections(credentials=credentials, envid=envid, raw=args.raw)
            if result is None:
                print "No collections for, '{0}'".format(envid)
            elif args.raw:
                print result
            else:
                for i, val in enumerate(result):
                    print "{0}: id={1[collection_id]}{2}name={1[name]}{2}descr={1[description]}{2}lang={1[language]}{2}status={1[status]}".format(i, val, args.separator),
                    if 'configuration_id' in val:
                        print "{1}cfgid={0[configuration_id]}".format(val, args.separator),
                    if 'created' in val:
                        print "{1}created={0[created]}".format(val, args.separator),                        
                    if 'updated' in val:
                        print "{1}updated={0[updated]}".format(val, args.separator),
                        
                    print                        

        elif list_lower == 'documents':
            colids = get_collections_ids(credentials, envids)
            result = list_documents(credentials=credentials, envid=envid, colid=args.colid, raw=args.raw)
            print result
        elif list_lower == 'environment':
            result = list_environment(credentials=credentials, envid=envid)
            print result
        elif list_lower == 'configuration':
            result = list_configuration(credentials=credentials, envid=envid, cfgid=args.cfgid)
            print result
        elif list_lower == 'collection':
            result = list_collection(credentials=credentials, envid=envid, colid=args.colid)
            print result
        elif list_lower == 'document':
            result = list_document(credentials=credentials, envid=envid, colid=args.colid, docid=args.docid)
            print result
        else:
            print "Error: invalid List option, '{0}'".format(args.list)
            sys.exit(1)

        sys.exit(0)

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
    elif args.create_environment:
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
