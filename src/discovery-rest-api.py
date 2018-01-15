#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import argparse
import codecs
import os
import re
import sys
import json
import yaml
import requests
from _bsddb import api

# http://pythonhosted.org/kitchen/unicode-frustrations.html
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

#===============================================================================
# get_watson_credentials
#===============================================================================
def get_watson_credentials(filename):
    '''
    Return a List of Watson Discovery Environments
    :param filename: Configuration file with Watson credentials
    '''

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


#===============================================================================
# list_environments
#===============================================================================
def list_environments(credentials, raw=True):
    """
     Return Watson Discovery Environments
    :param credentials: Watson credentials
    :param raw: JSON output
    """

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    payload = {}
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print "GET: {0}".format(r.url)

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


#===============================================================================
# list_configurations
#===============================================================================
def list_configurations(credentials, envid, raw=True):
    """
     Return Watson Discovery Configurations
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param raw:JSON results
    """
    if envid is None:
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
        print "GET: {}".format(r.url)

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


#===============================================================================
# get_configuration_ids
#===============================================================================
def get_configuration_ids(credentials, envid):
    """
     Return Watson Discovery Configurations
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    """
    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    configuration_ids = []
    configuration = json.loads(list_configurations(credentials=credentials, envid=envid))
    for c in configuration['configurations']:
        configuration_ids.append(c['configuration_id'])

    return configuration_ids


#===============================================================================
# list_collections
#===============================================================================
def list_collections(credentials, envid, raw=True):
    """
     Return Watson Discovery Collections
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param raw: JSON output
    """
    if envid is None:
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
        print "GET: {0}".format(r.url)

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


#===============================================================================
# get_collections_ids
#===============================================================================
def get_collections_ids(credentials, envid):
    """
     Return Watson Discovery Collections
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    """
    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    collection_ids = []
    collections = json.loads(list_collections(credentials=credentials, envid=envid))
    for c in collections['collections']:
        collection_ids.append(c['collection_id'])

    return collection_ids


#===============================================================================
# list_documents
#===============================================================================
def list_documents(credentials, envid, colid=None, count=10, raw=True):
    """
     Return Watson Discovery Documents (broken does not work)
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: Watson collection_id string
    :param count: Number of documents to list
    :param raw: JSON output
    """
    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if colid is None:
        print "Missing collection_id; hint {0} -L configurations --envid {1}".format(sys.argv[0], envid)
        sys.exit(1)

    # GET /v1/environments/{environment_id}/collections/{collection_id}/documents
    # curl -u "{username}":"{password}"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/query?return=extracted_metadata&version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    # api += '/' + envid + '/collections/' + colid + '/documents'
    api += '/' + envid + '/collections/' + colid + '/query'
    payload = {}
    payload['return'] = 'extracted_metadata'
    payload['count'] = count
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print "GET: {0}".format(r.url)

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print "List Documents Failed: {0}".format(r.status_code)

        return None
    else:
        if raw:
            return r.text
        else:
            environment = json.loads(r.text)
            return yaml.safe_dump(environment, encoding='utf-8', allow_unicode=True)

    # return "list_collections({0},{1})".format(credentials,envid)
    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
    return "list_documents({0},{1},{2})".format(credentials, envid, colid)


#===============================================================================
# get_document_ids
#===============================================================================
def get_document_ids(credentials, envid, colid, count=10):
    """
     Return Watson Discovery Documents
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: Watson collection_id string
    :param count: Number of documents to list
    """
    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if colid is None:
        print "Invalid colid, '{0}'".format(colid)
        sys.exit(1)

    # {"matching_results":36,"results":[
    #     { "id":"fcfeba641624af03290105b3d6a93f2b",
    #       "result_metadata":{"score":1},
    #       "extracted_metadata":{
    #           "publicationdate":"2018-01-05",
    #           "sha1":"31f50f9ab95ae4fddadfeeebaea1ddd2f6408f59",
    #           "filename":"LilianeMaibachProfile.pdf",
    #           "file_type":"html",
    #           "title":"no title"
    #         }
    #     },
    #     ...
    #     {}
    # ]}
    document_ids = []
    documents = list_documents(credentials=credentials, envid=envid, colid=colid)
    if documents is not None:
        document = json.loads(documents)
        for d in document['results']:
            document_ids.append(d['id'])

    return document_ids


def delete_document(credentials, envid, colid, docid, raw):
    '''
    Delete a document from a collection
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: collection_id string
    :param docid: document_id string
    :param raw: True JSON output, YAML otherwise 
    '''
    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if colid is None:
        print "Invalid colid, '{0}'".format(colid)
        sys.exit(1)

    if docid is None:
        print "Invalid docid, '{0}'".format(docid)
        sys.exit(1)

    # DELETE /v1/environments/{environment_id}/collections/{collection_id}/documents/{document_id}
    # curl -X DELETE -u "{username}":"{password}"
    #  "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents/{document_id}?version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections/' + colid + '/documents/' + docid
    payload = {}
    payload['version'] = credentials['version']

    r = requests.delete(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print "DELETE: {0}".format(r.url)

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print "Delete_document({0},{1},{2},{3})".format('****', envid, colid, docid)
            print "Delete document Failed: {0} ".format(r.status_code)

        return None
    else:
        if raw:
            return r.text
        else:
            environment = json.loads(r.text)
            return yaml.safe_dump(environment, encoding='utf-8', allow_unicode=True)

    # print(r.text)
    return "delete_documents({0},{1},{2},{3})".format(credentials, envid, colid, docid)

#===============================================================================
# list_environment
#===============================================================================


def list_environment(credentials, envid, raw=True):
    """
     Return Watson Discovery Environment Details
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param raw: True JSON output, YAML otherwise 
    """

    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

#     GET /v1/environments/{environment_id}
#     curl -u "{username}":"{password}"
#      "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}?version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid
    payload = {}
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print "GET: {0}".format(r.url)

#     {
#       "environment_id" : "71cac327-84eb-4327-81da-24d49f14a445",
#       "name" : "test api",
#       "description" : "why not",
#       "created" : "2017-12-26T19:42:05.004Z",
#       "updated" : "2017-12-26T19:42:05.004Z",
#       "status" : "active",
#       "read_only" : false,
#       "index_capacity" : {
#         "documents" : {
#           "available" : 0,
#           "maximum_allowed" : 2000
#         },
#         "disk_usage" : {
#           "used_bytes" : 162,
#           "maximum_allowed_bytes" : 200000000
#         },
#         "collections" : {
#           "available" : 1,
#           "maximum_allowed" : 2
#         }
#       }
#     }

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print "List environment Failed: {0}".format(r.status_code)

        return None
    else:
        if raw:
            return r.text
        else:
            environment = json.loads(r.text)
            return yaml.safe_dump(environment, encoding='utf-8', allow_unicode=True)

    return "Unknown Error: list_environment({0})".format(envid)


#===============================================================================
# list_configuration
#===============================================================================
def list_configuration(credentials, envid, cfgid, raw=True):
    """
     Return Watson Discovery Configuration Details
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param cfgid: Watson configuration_id string
    :param raw: JSON output (True), YAML otherwise
    """

    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if cfgid is None:
        print "Invalid cfgid, '{0}', hint try: {1} -L configurations --envid {2}".format(cfgid, sys.argv[0], envid)
        sys.exit(1)

#     GET /v1/environments/{environment_id}/configurations/{configuration_id}
#     curl -u "{username}":"{password}"
#      "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/configurations/{configuration_id}?version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/configurations/' + cfgid
    payload = {}
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print "GET: {0}".format(r.url)

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print "List configuration Failed: {0}".format(r.status_code)

        return None
    else:
        if raw:
            return r.text
        else:
            configuration = json.loads(r.text)
            return yaml.safe_dump(configuration, encoding='utf-8', allow_unicode=True)

    return "Unknown Error: list_configuration({0})".format(envid)


#===============================================================================
# list_collection
#===============================================================================
def list_collection(credentials, envid, colid, raw=True):
    """
     Return Watson Discovery Collection Details
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: Watson collection_id string
    :param raw: JSON or YAML output
    """
    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if colid is None:
        print "Invalid colid, '{0}', hint try: {1} -L collections --envid {2}".format(colid, sys.argv[0], envid)
        sys.exit(1)

#     GET /v1/environments/{environment_id}/collections/{collection_id}
#     curl -u "{username}":"{password}"
#      "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}?version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections/' + colid
    payload = {}
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print "GET: {0}".format(r.url)

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print "List collection Failed: {0}".format(r.status_code)

        return None
    else:
        if raw:
            return r.text
        else:
            collection = json.loads(r.text)
            return yaml.safe_dump(collection, encoding='utf-8', allow_unicode=True)

    return "Unknown Error: list_collecation({0})".format(envid)


#===============================================================================
# list_document
#===============================================================================
def list_document(credentials, envid, colid, docid, raw=True):
    """
     Return Watson Discovery Document Details
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: Watson collection_id string
    :param docid: Watson document_id string
    :param raw: JSON or YAML output
    """
    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if colid is None:
        print "Invalid colid, '{0}', hint try: {1} -L collections --envid {2}".format(colid, sys.argv[0], '<envid>')
        sys.exit(1)

#     GET /v1/environments/{environment_id}/collections/{collection_id}/documents/{document_id}
#     curl -u "{username}":"{password}"
#      "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents/{document_id}?version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections/' + colid + '/documents/' + docid
    payload = {}
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print "GET: {0}".format(r.url)

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print "List document Failed: {0}".format(r.status_code)

        return None
    else:
        if raw:
            return r.text
        else:
            document = json.loads(r.text)
            return yaml.safe_dump(document, encoding='utf-8', allow_unicode=True)

    return "Unknown Error: list document({0})".format(envid)


#===============================================================================
# get_environment_ids
#===============================================================================
def get_environment_ids(credentials):
    """
     Return a List of Watson Discovery Environments Id
    :param credentials: Watson credentials
    """

    import json
    envs = json.loads(list_environments(credentials))
    results = []
    for env in envs['environments']:
        results.append(env['environment_id'])

    return results


#===============================================================================
# get_environment_summary
#===============================================================================
def get_environment_summary(cred, envid):
    """
     Return Summary of Watson Discovery Environment
    :param cred: Watson credentials string
    :param envid: Watson environment_id string
    """

    import json
    import requests

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid
    payload = {}
    payload['version'] = cred['version']

    r = requests.get(api, params=payload, auth=(cred['username'], cred['password']))
    if args.verbose >= 1:
        print "GET: {0}".format(r.url)

    return r.text


#===============================================================================
# create_environment
#===============================================================================
def create_environment(cred, name, descr):
    """
     Create Discovery Environment (REST + post)
    :param cred: Watson Credentials (username, password, version)
    :param name: mandatory environment name
    :param descr: optional environment description
    """
    import json
    import requests

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '?version=' + cred['version']

    data = {'name': name, 'description': descr}
    r = requests.post(api, json=data, auth=(cred['username'], cred['password']))

    if args.verbose >= 1:
        print "POST: {0}".format(r.url)
        print "JSON: {0}".format(data)

    if r.status_code == requests.codes.ok or r.status_code == requests.codes.created:
        return r.text
    else:
        print "Create Environment Failed: {0}".format(r.status_code)
        return None


#===============================================================================
# delete_environment
#===============================================================================
def delete_environment(cred, envid):
    """
     Delete Discovery Environment (REST + post)
    :param cred: Watson Credentials (username, password, version)
    :param envid: mandatory environment_id string
    """
    import json
    import requests

    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid
    payload = {}
    payload['version'] = cred['version']

    r = requests.delete(api, params=payload, auth=(cred['username'], cred['password']))
    if args.verbose >= 1:
        print "DELETE: {0}".format(r.url)

    return r.text


#===============================================================================
# create_collection
#===============================================================================
def create_collection(credentials, envid, name, cfgid, description=None, language='en', raw=True):
    '''
    Create Watson collection in the environment
    :param credentials: Watson Credentials (username, password, version)
    :param envid: mandatory environment_id string
    :param cfgid: mandatory configuration_id string
    :param description: optional description
    :param language: defaults to 'en'
    :param raw: True (JSON), False (YAML)
    '''

    # POST /v1/environments/{environment_id}/collections
    # curl -X POST  -u "{username}":"{password}" -H "Content-Type: application/json" \
    # -d '{
    #   "name": "test_collection",
    #   "description": "My test collection",
    #   "configuration_id": "{configuration_id}",
    #   "language": "en"
    # }' "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections?version=2017-11-07"

    # Example JSON body
    # {
    #   "name": "{collection_name}",
    #   "description": "{description}",
    #   "configuration_id": "{configuration_id}",
    #   "language": "en"
    # }

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections'
    api += '?version=' + credentials['version']

    data = {'name': name, 'description': description, 'configuration_id': cfgid, 'language': language}
    r = requests.post(api, json=data, auth=(credentials['username'], credentials['password']))

    if args.verbose >= 1:
        print "POST: {0}".format(r.url)
        print "DATA: {0}".format(data)

    if r.status_code == requests.codes.ok or r.status_code == requests.codes.created:
        if args.verbose >= 1:
            print "{0}: Create Collection succeeded".format(r.status_code)

        if raw:
            return r.text
        else:
            document = json.loads(r.text)
            return yaml.safe_dump(document, encoding='utf-8', allow_unicode=True)
    else:
        if args.verbose >= 1:
            print "Create Collection Failed: {0}".format(r.status_code)

        return None

    print "Unknown Error: Create Collection({0})".format(envid)
    sys.exit(1)


#===============================================================================
# delete_collection
#===============================================================================
def delete_collection(credentials, envid, colid, raw=True):
    '''
    Delete collection in Watson environment
    :param credentials: Watson Credentials (username, password, version)
    :param envid: mandatory environment_id string
    :param colid: mandatory collection_id string
    :param raw: True (JSON), False (YAML)
    '''

    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if colid is None:
        print "Invalid colid, '{0}', hint try: {1} -L collections --envid {2}".format(colid, sys.argv[0], envid)
        sys.exit(1)

    # DELETE /v1/environments/{environment_id}/collections/{collection_id}
    # curl -u "{username}":"{password}" -X DELETE
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}?version=2017-11-07"
    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections/' + colid
    payload = {}
    payload['version'] = credentials['version']

    r = requests.delete(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print "DELETE {0}".format(r.url)

    if raw:
        return r.text
    else:
        document = json.loads(r.text)
        return yaml.safe_dump(document, encoding='utf-8', allow_unicode=True)

    print "Unknown Error: delete_collection(envid={0}; cfgid={1})".format(envid, colid)
    sys.exit(1)


#===============================================================================
# upload_document
#===============================================================================
def upload_document(credentials, envid, colid, file_name, raw=True):
    '''
    Upload a document into a collection in the environment
    :param credentials: Watson Credentials (username, password, version)
    :param envid: mandatory environment_id string
    :param colid: mandatory collection_id string
    :param file_name: file to upload
    :param raw: True (JSON), False (YAML)
    '''
    import magic

    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if colid is None:
        print "Invalid colid, '{0}', hint try: {1} -L collections --envid {2}".format(colid, sys.argv[0], envid)
        sys.exit(1)

    if not (os.path.isfile(file_name) and os.access(file_name, os.R_OK)):
        print "Filename not readable, '{0}'".format(file_name)
        sys.exit(1)

#     POST /v1/environments/{environment_id}/collections/{collection_id}/documents
#     curl -X POST -u "{username}":"{password}" \
#      -F file=@sample1.html
#      "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
    if args.verbose:
        print "upload: envid={0}; colid={1}; fname={2}".format(envid, colid, file_name)

    api = "https://gateway.watsonplatform.net/discovery/api/v1"
    api += '/environments/' + envid + '/collections/' + colid + '/documents'
    api += '?version=' + credentials['version']

    # Supported formats (50 MB max).
    # application/json,
    # application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document,
    # application/pdf,
    # text/html, and application/xhtml+xml
    #
    # magic.from_file("../examples/file.txt", mime=True) >>> 'text/plain'
    # magic.from_file("../examples/LinkedIn_Ella_Salzmann.pdf", mime=True) >>> 'application/pdf'
    # magic.from_file("../examples/parameters.json", mime=True) >>>'text/plain'
    # magic.from_file("../examples/missing-file.txt", mime=True)
    #   IOError: [Errno 2] No such file or directory: '../examples/missing-file.txt'
    mime_type = magic.from_file(file_name, mime=True)
    if mime_type == 'text/html':
        try:
            json.loads(file_name)
            mime_type = "application/json"
        except ValueError:
            pass

    files = {'file': (os.path.basename(file_name), open(file_name, 'rb'), mime_type, {'Expires': 0})}
    r = requests.post(api, files=files, auth=(credentials['username'], credentials['password']))

    if args.verbose >= 1:
        print "POST: {0}".format(r.url)
        print "FILE: {0}".format(file_name)

    # 200 OK - Successful request
    # 202 Accepted - index progressing.
    # 400 Bad Request - Invalid request if the request is incorrectly formatted.
    # 404 Not Found - The request specified a resource that was not found
    if r.status_code == requests.codes.ok or r.status_code == requests.codes.accepted:
        return r.text
    else:
        print "Upload File Failed: {0}".format(r.status_code)
        return None


#===============================================================================
# query_document
#===============================================================================
def query_document(credentials, envid, colid=None, docid=None, query=None, raw=True):
    """
    Query a single document
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: Watson collection_id string
    :param docid: Watson document id string
    :param query: JSON string query
    :param count: Number of documents to list
    :param raw: JSON output
    """
    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if colid is None:
        print "Missing collection_id; hint {0} -L configurations --envid {1}".format(sys.argv[0], envid)
        sys.exit(1)

    # GET /v1/environments/{environment_id}/collections/{collection_id}/documents
    # curl -u "{username}":"{password}"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/query?return=extracted_metadata&version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections/' + colid + '/query'
    payload = {}
    payload['filter'] = '_id:"' + docid + '"'
    payload['return'] = 'enriched_text.entities'
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print "GET: {0}".format(r.url)

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print "Query Document Failed: {0}".format(r.status_code)

        return None
    else:
        if raw:
            return r.text
        else:
            environment = json.loads(r.text)
            return yaml.safe_dump(environment, encoding='utf-8', allow_unicode=True)

    # return "list_collections({0},{1})".format(credentials,envid)
    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
    return "query_document({0},{1},{2})".format(credentials, envid, colid)


#===============================================================================
# query_collection
#===============================================================================
def query_collection(credentials, envid, colid=None, query=None, count=10, raw=True):
    """
    Query a single document
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: Watson collection_id string
    :param query: JSON string query
    :param count: Number of documents to list
    :param raw: JSON output
    """
    if envid is None:
        print "Invalid envid, '{0}'".format(envid)
        sys.exit(1)

    if colid is None:
        print "Missing collection_id; hint {0} -L configurations --envid {1}".format(sys.argv[0], envid)
        sys.exit(1)

    # GET /v1/environments/{environment_id}/collections/{collection_id}/documents
    # curl -u "{username}":"{password}"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/query?return=extracted_metadata&version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections/' + colid + '/query'
    payload = {}
    payload['filter'] = 'enriched_text.entities.type::"Company"'
    payload['return'] = 'enriched_text.entities'
    payload['count'] = count
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print "GET: {0}".format(r.url)

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print "Query Collection Failed: {0}".format(r.status_code)

        return None
    else:
        if raw:
            return r.text
        else:
            #environment = json.loads(r.text)
            return yaml.safe_dump(json.loads(r.text), encoding='utf-8', allow_unicode=True)

    # return "list_collections({0},{1})".format(credentials,envid)
    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
    return "query_collection({0},{1},{2})".format(credentials, envid, colid)


#===============================================================================
# https://www.ibm.com/watson/developercloud/discovery/api/v1/
# https://console.bluemix.net/docs/services/discovery/getting-started.html#getting-started-with-the-api
# __main__
#===============================================================================
if __name__ == "__main__":
    watson_cfg_file = os.path.join(os.getcwd(), '.watson.cfg')
    parser = argparse.ArgumentParser(description='Discovery REST interface')
    parser.add_argument('-A', '--add', help='upload document')
    parser.add_argument('-C', '--create', help='(environment|collection)')
    parser.add_argument('-D', '--delete', help='(environment|configuration|collection|document)')
    parser.add_argument('-L', '--list', help='(environment[s]|configuration[s]|collection[s]|document[s])')
    parser.add_argument('-U', '--update', help='(environment|configuration|collection|document)')
    parser.add_argument('-Q', '--query', help='(collection|document)')
    parser.add_argument('-c', '--count', type=int, default=None, help='number of documents')
    parser.add_argument('-d', '--description', default=None, help='description for create command')
    parser.add_argument('-n', '--name', default=None, help='name for create command')
    parser.add_argument('--envid', type=int, default=None, help='environment index')
    parser.add_argument('--cfgid', type=int, default=None, help='configuration index')
    parser.add_argument('--colid', type=int, default=None, help='collection index')
    parser.add_argument('--docid', type=int, default=None, help='document index')
    parser.add_argument('-a', '--auth', default='.watson.cfg', help='Watson credentials file')
    parser.add_argument('--raw', help='JSON output', default=False, action='store_true')
    parser.add_argument('-s', '--separator', help='field delimiter', default='\n  ')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    if args.verbose >= 1:
        print "watson-cfg: '{0}'".format(args.auth)

    credentials = get_watson_credentials(args.auth)
    envids = get_environment_ids(credentials=credentials)

    create_allowed = ['environment', 'collection']
    delete_allowed = ['environment', 'configuration', 'collection', 'document']
    list_allowed = ['environments', 'configurations', 'collections', 'documents', 'environment', 'configuration', 'collection', 'document']
    delete_allowed = ['environment', 'configuration', 'collection', 'document']
    query_allowed = ['collection', 'document']

    if args.list:
        if not (args.list.lower() in list_allowed):
            print"{0}: invalid argument, '{1}'".format(sys.argv[0], args.list)
            sys.exit(1)

        command = args.list.lower()

        if args.envid is not None:
            try:
                envid = envids[args.envid]
            except IndexError:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={0}".format(args.envid)
                sys.exit(1)
            except TypeError as e:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={1}; {0}".format(e, args.envid)
                sys.exit(1)
        elif command == 'environments':
            pass
        else:
            print "Error: invalid envid='{0}'; try {1} -L environments".format(args.envid, sys.argv[0])
            sys.exit(1)

        if command == 'environments':
            result = list_environments(credentials=credentials, raw=args.raw)
            if result is None:
                print "No Environments?"
                sys.exit(1)
            elif args.raw:
                print result
            else:
                title = "Environments:"
                print title + os.linesep + ("=" * len(title))
                for i, val in enumerate(result):
                    print "{0:d}:{2}configuration_id: {1[environment_id]}{2}name: {1[name]}{2}description: {1[description]}".format(i, val, args.separator),
                    if 'created' in val:
                        print "{1}created: {0[created]}".format(val, args.separator),
                    if 'updated' in val:
                        print "{1}updated: {0[updated]}".format(val, args.separator),
                    print

        elif command == 'configurations':
            result = list_configurations(credentials=credentials, envid=envid, raw=args.raw)
            if result is None:
                print "No configurations for, '{0}'".format(envid)
            elif args.raw:
                print result
            else:
                title = "Configurations (EnvID: {0}):".format(envid)
                print title + os.linesep + ("=" * len(title))
                for i, val in enumerate(result):
                    print "{0:d}:{2}configuration_id: {1[configuration_id]}{2}name: {1[name]}{2}description: {1[description]}".format(i, val, args.separator),
                    if 'created' in val:
                        print "{1}created: {0[created]}".format(val, args.separator),
                    if 'updated' in val:
                        print "{1}updated: {0[updated]}".format(val, args.separator),
                    print

        elif command == 'collections':
            result = list_collections(credentials=credentials, envid=envid, raw=args.raw)
            if result is None:
                print "No collections for, '{0}'".format(envid)
            elif args.raw:
                print result
            else:
                title = "Collections (EnvID: {0}):".format(envid)
                print title + os.linesep + ("=" * len(title))
                for i, val in enumerate(result):
                    print "{0:d}:{2}collection_id: {1[collection_id]}{2}name: {1[name]}{2}description: {1[description]}".format(i, val, args.separator),
                    print "{1}lang: {0[language]}{1}status: {0[status]}".format(val, args.separator),
                    if 'configuration_id' in val:
                        print "{1}configuration_id: {0[configuration_id]}".format(val, args.separator),
                    if 'created' in val:
                        print "{1}created: {0[created]}".format(val, args.separator),
                    if 'updated' in val:
                        print "{1}updated: {0[updated]}".format(val, args.separator),

                    print

        elif command == 'documents':
            try:
                colids = get_collections_ids(credentials, envid)
                colid = colids[args.colid]
            except IndexError:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={0}; colid={1}".format(args.envid, args.colid)
                sys.exit(1)
            except TypeError as e:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={1}; colid={2}; {0}".format(e, args.envid, args.colid)
                sys.exit(1)

            result = list_documents(credentials=credentials, envid=envid, colid=colid, count=args.count, raw=args.raw)
            if result is None:
                title = "Documents (EnvID: {0}):".format(envid)
                print title + os.linesep + ("=" * len(title)),
                print "{1}Collection: '{0}'".format(colid, args.separator),
                print "{0}No documents found".format(args.separator),
                print
            elif args.raw:
                print result
            else:
                print result
        elif command == 'environment':
            result = list_environment(credentials=credentials, envid=envid, raw=args.raw)
            title = "Environment: {0}".format(envid)
            print title + os.linesep + ("=" * len(title))
            print result
        elif command == 'configuration':
            try:
                cfgids = get_configuration_ids(credentials, envid)
                cfgid = cfgids[args.cfgid]
                result = list_configuration(credentials=credentials, envid=envid, cfgid=cfgid, raw=args.raw)
                title = "Configuration: {0}".format(cfgid)
                print title + os.linesep + ("=" * len(title))
                print result
            except IndexError:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={0}; cfgid={1}".format(args.envid, args.cfgid)
                sys.exit(1)
            except TypeError as e:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={1}; cfgid={2}; {0}".format(e, args.envid, args.cfgid)
                sys.exit(1)

        elif command == 'collection':
            colids = get_collections_ids(credentials, envid)
            try:
                colid = colids[args.colid]
                result = list_collection(credentials=credentials, envid=envid, colid=colid, raw=args.raw)
                title = "Collection: {0}".format(colid)
                print title + os.linesep + ("=" * len(title))
                print result
            except IndexError:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={0}; colid={1}".format(args.envid, args.colid)
                sys.exit(1)
            except TypeError as e:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={1}; colid={2}; {0}".format(e, args.envid, args.colid)
                sys.exit(1)

        elif command == 'document':
            colids = get_collections_ids(credentials, envid)
            try:
                colid = colids[args.colid]
                docids = get_document_ids(credentials=credentials, envid=envid, colid=colid)
                docid = docids[args.docid]
                result = list_document(credentials=credentials, envid=envid, colid=colid, docid=docid, raw=args.raw)
                title = "Document: {0}".format(docid)
                print title + os.linesep + ("=" * len(title))
                print result
            except IndexError:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={0}; colid={1}; docid={2}".format(args.envid, args.colid, args.docid)
                sys.exit(1)
            except TypeError as e:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={1}; colid={2}; docid={3}; {0}".format(e, args.envid, args.colid, args.docid)
                sys.exit(1)

        else:
            print "Error: invalid List option, '{0}'".format(args.list)
            sys.exit(1)

    elif args.add:
        try:
            envid = envids[args.envid]
            colids = get_collections_ids(credentials, envid)
            colid = colids[args.colid]
            result = upload_document(credentials=credentials, envid=envid, colid=colid, file_name=args.add, raw=args.raw)
            title = "Add Document: '{0}' (ColID {1})".format(args.add, colid)
            print title + os.linesep + ("=" * len(title))
            print result
        except IndexError:
            print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
            print " envid={0}; colid={1}".format(args.envid, args.colid)
            sys.exit(1)
        except TypeError as e:
            print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
            print " envid={1}; colid={2}; {0}".format(e, args.envid, args.colid)
            sys.exit(1)

    elif args.create:
        if not (args.create.lower() in create_allowed):
            print"{0}: invalid argument, '{1}'".format(sys.argv[0], args.list)
            sys.exit(1)

        command = args.create.lower()
        if args.envid is not None:
            try:
                envid = envids[args.envid]
                if command == 'environment':
                    create_environment(credentials=credentials, name=args.create, descr=args.description)
                elif command == 'collection':
                    cfgids = get_configuration_ids(credentials, envid)
                    cfgid = cfgids[args.cfgid]
                    result = create_collection(credentials=credentials, envid=envid, name=args.name, cfgid=cfgid, description=args.description, raw=args.raw)
                    print result
            except IndexError:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={0}; cfgid={1}".format(args.envid, args.cfgid)
                sys.exit(1)
            except TypeError as e:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={1}; cfgid={2}; {0}".format(e, args.envid, args.cfgid)
                sys.exit(1)
        else:
            print "Error: invalid envid='{0}'; try {1} -L environments".format(args.envid, sys.argv[0])
            sys.exit(1)

    elif args.delete:
        if not (args.delete.lower() in delete_allowed):
            print"{0}: invalid argument, '{1}'".format(sys.argv[0], args.delete)
            sys.exit(1)

        command = args.delete.lower()
        if args.envid is not None:
            try:
                envid = envids[args.envid]
                if command == 'environment':
                    result = delete_environment(credentials=credentials, envid=envid)
                    print result
                    sys.exit(0)
                elif command == 'collection':
                    colids = get_collections_ids(credentials=credentials, envid=envid)
                    if colids:
                        colid = colids[args.colid]
                        result = delete_collection(credentials=credentials, envid=envid, colid=colid, raw=args.raw)
                        print result
                        sys.exit(0)
                    else:
                        print "No collections found?"
                        sys.exit(1)
                elif command == 'document':
                    colids = get_collections_ids(credentials=credentials, envid=envid)
                    if colids:
                        colid = colids[args.colid]
                        docids = get_document_ids(credentials=credentials, envid=envid, colid=colid, count=args.count)

                        if docids:
                            docid = docids[args.docid]
                            result = delete_document(credentials=credentials, envid=envid, colid=colid, docid=docid, raw=args.raw)
                            print result
                            sys.exit(0)
                        else:
                            print "No documents found?"
                            sys.exit(1)
                    else:
                        print "No collections found?"
                        sys.exit(1)

            except IndexError:
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={0}; colid={1}; cfgid={2}".format(args.envid, args.colid, args.cfgid)
                sys.exit(1)
            except TypeError as e:
                print "Delete:"
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={1}; colid={2}; cfgid={3}; {0}".format(e, args.envid, args.colid, args.cfgid)
                sys.exit(1)

    elif args.query:
        if not (args.query.lower() in query_allowed):
            print"{0}: invalid argument, '{1}'".format(sys.argv[0], args.query)
            sys.exit(1)

        command = args.query.lower()
        if args.envid is not None:
            try:
                envid = envids[args.envid]
                if command == 'collection':
                    colids = get_collections_ids(credentials=credentials, envid=envid)
                    if colids:
                        colid = colids[args.colid]
                        result = query_collection(credentials=credentials, envid=envid, colid=colid, count=args.count, raw=args.raw)
                        print result
                        sys.exit(0)
                    else:
                        print "No collections found?"
                        sys.exit(1)
                elif command == 'document':
                    colids = get_collections_ids(credentials=credentials, envid=envid)
                    if colids:
                        colid = colids[args.colid]
                        docids = get_document_ids(credentials=credentials, envid=envid, colid=colid, count=args.count)

                        if docids:
                            docid = docids[args.docid]
                            result = query_document(credentials=credentials, envid=envid, colid=colid, docid=docid, raw=args.raw)
                            print result
                            sys.exit(0)
                        else:
                            print "No documents found?"
                            sys.exit(1)
                    else:
                        print "No collections found?"
                        sys.exit(1)

            except IndexError:
                print "Query:"
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={0}; colid={1}; cfgid={2}".format(args.envid, args.colid, args.cfgid)
                sys.exit(1)
            except TypeError as e:
                print "Query:"
                print "Invalid {1}; hint try {0} -L environments".format(sys.argv[0], 'index')
                print " envid={1}; colid={2}; cfgid={3}; {0}".format(e, args.envid, args.colid, args.cfgid)
                sys.exit(1)

    else:
        print "Unknown command"
        print parser.print_usage()
        sys.exit(1)

    sys.exit(0)
