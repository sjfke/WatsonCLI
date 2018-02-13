#!/usr/bin/env python3
#
import argparse
import codecs
import os
import re
import sys
import json
import yaml
import requests

#===============================================================================
# get_watson_credentials
#===============================================================================


def get_watson_credentials(filename):
    '''
    Return a List of Watson Discovery Environments
    :param filename: Configuration file with Watson credentials
    '''

    if not os.access(filename, os.R_OK):
        print("Error: reading Watson credentials file '{0}: ".format(filename))
        sys.exit(1)

    from configparser import SafeConfigParser

    config = SafeConfigParser()
    config.read(filename)
    result = {}
    result['username'] = config.get('discovery', 'username')
    result['password'] = config.get('discovery', 'password')
    result['version'] = config.get('discovery', 'version')

    return result


#===============================================================================
# print_result
#===============================================================================
def print_result(result, format='JSON', callback=None):
    '''
    Print result (string, list) in JSON, YAML or TEXT (callback) format
    :param result: the result (JSON) string to display
    :param format: JSON, YAML, TEXT (use callback)
    :param callback: custom printing routine
    '''
    if result is None:
        if verbose >= 1:
            print("print_result: 'string' is None")
        return

    if isinstance(result, str) or isinstance(result, unicode):
        values = json.dumps(json.loads(result), sort_keys=True, indent=4, separators=(',', ': '))
    else:
        values = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

    if callback:
        callback(result)
    elif format == 'JSON':
        print(values)
    elif format == 'YAML':
        print(yaml.safe_dump(json.loads(values), default_flow_style=False))
    else:
        print(values)

    return


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
        print("GET: {0}".format(r.url))

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
        if args.verbose >= 1:
            print("List Collections Failed: {0}".format(r.status_code))
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
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    # curl -u "{username}":"{password}"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/configurations?version=2017-11-07"
    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/configurations'
    payload = {}
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print("GET: {}".format(r.url))

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
        print("List Configurations Failed: {0}".format(r.status_code))
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
        print("Invalid envid, '{0}'".format(envid))
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
        print("Invalid envid, '{0}'".format(envid))
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
        print("GET: {0}".format(r.url))

    if r.status_code != requests.codes.ok:
        print("List Collections Failed: {0}".format(r.status_code))
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
        print("Invalid envid, '{0}'".format(envid))
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
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    if colid is None:
        print("Missing collection_id; hint {0} -L configurations --envid {1}".format(sys.argv[0], envid))
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
        print("list_documents: GET: {0}".format(r.url))

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print("List Documents Failed: {0}".format(r.status_code))

        return None
    else:
        # print(r.text)
        return r.text
#         if raw:
#             return r.text
#         else:
#             environment = json.loads(r.text)
#             return yaml.safe_dump(environment, encoding='utf-8', allow_unicode=True)

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
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    if colid is None:
        print("Invalid colid, '{0}'".format(colid))
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
    documents = list_documents(credentials=credentials, envid=envid, colid=colid, count=count)
    if documents is not None:
        document = json.loads(documents)
        for d in document['results']:
            document_ids.append(d['id'])

    return document_ids


def delete_document(credentials, envid, colid, docid):
    '''
    Delete a document from a collection
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: collection_id string
    :param docid: document_id string
    '''
    if envid is None:
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    if colid is None:
        print("Invalid colid, '{0}'".format(colid))
        sys.exit(1)

    if docid is None:
        print("Invalid docid, '{0}'".format(docid))
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
        print("DELETE: {0}".format(r.url))

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print("Delete_document({0},{1},{2},{3})".format('****', envid, colid, docid))
            print("Delete document Failed: {0} ".format(r.status_code))

        return None
    else:
        return r.text


#===============================================================================
# list_environment
#===============================================================================


def list_environment(credentials, envid):
    """
     Return Watson Discovery Environment Details
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param raw: True JSON output, YAML otherwise
    """

    if envid is None:
        print("Invalid envid, '{0}'".format(envid))
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
        print("GET: {0}".format(r.url))

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print("List environment Failed: {0}".format(r.status_code))

        return None
    else:
        return r.text


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
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    if cfgid is None:
        print("Invalid cfgid, '{0}', hint try: {1} -L configurations --envid {2}".format(cfgid, sys.argv[0], envid))
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
        print("GET: {0}".format(r.url))

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print("List configuration Failed: {0}".format(r.status_code))

        return None
    else:
        return r.text


#===============================================================================
# list_collection
#===============================================================================
def list_collection(credentials, envid, colid):
    """
     Return Watson Discovery Collection Details
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: Watson collection_id string
    """
    if envid is None:
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    if colid is None:
        print("Invalid colid, '{0}', hint try: {1} -L collections --envid {2}".format(colid, sys.argv[0], envid))
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
        print("GET: {0}".format(r.url))

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print("List collection Failed: {0}".format(r.status_code))

        return None
    else:
        return r.text


#===============================================================================
# list_document
#===============================================================================
def list_document(credentials, envid, colid, docid):
    """
     Return Watson Discovery Document Details
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: Watson collection_id string
    :param docid: Watson document_id string
    """
    if envid is None:
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    if colid is None:
        print("Invalid colid, '{0}', hint try: {1} -L collections --envid {2}".format(colid, sys.argv[0], '<envid>'))
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
        print("GET: {0}".format(r.url))

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print("List document Failed: {0}".format(r.status_code))

        return None
    else:
        return r.text


#===============================================================================
# get_environment_ids
#===============================================================================
def get_environment_ids(credentials):
    """
     Return a List of Watson Discovery Environments Id
    :param credentials: Watson credentials
    """

    import json
    environment_list = list_environments(credentials)
    results = None
    if environment_list:
        results = []
        envs = json.loads(environment_list)
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
        print("GET: {0}".format(r.url))

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
        print("POST: {0}".format(r.url))
        print("JSON: {0}".format(data))

    if r.status_code == requests.codes.ok or r.status_code == requests.codes.created:
        return r.text
    else:
        print("Create Environment Failed: {0}".format(r.status_code))
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
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid
    payload = {}
    payload['version'] = cred['version']

    r = requests.delete(api, params=payload, auth=(cred['username'], cred['password']))
    if args.verbose >= 1:
        print("DELETE: {0}".format(r.url))

    return r.text


#===============================================================================
# create_collection
#===============================================================================
def create_collection(credentials, envid, name, cfgid, description=None, language='en'):
    '''
    Create Watson collection in the environment
    :param credentials: Watson Credentials (username, password, version)
    :param envid: mandatory environment_id string
    :param cfgid: mandatory configuration_id string
    :param description: optional description
    :param language: defaults to 'en'
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
        print("POST: {0}".format(r.url))
        print("DATA: {0}".format(data))

    if r.status_code == requests.codes.ok or r.status_code == requests.codes.created:
        if args.verbose >= 1:
            print("{0}: Create Collection succeeded".format(r.status_code))

        return r.text
    else:
        if args.verbose >= 1:
            print("Create Collection Failed: {0}".format(r.status_code))

        return None

    print("Unknown Error: Create Collection({0})".format(envid))
    sys.exit(1)


#===============================================================================
# delete_collection
#===============================================================================
def delete_collection(credentials, envid, colid):
    '''
    Delete collection in Watson environment
    :param credentials: Watson Credentials (username, password, version)
    :param envid: mandatory environment_id string
    :param colid: mandatory collection_id string
    '''

    if envid is None:
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    if colid is None:
        print("Invalid colid, '{0}', hint try: {1} -L collections --envid {2}".format(colid, sys.argv[0], envid))
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
        print("DELETE {0}".format(r.url))

    return r.text


#===============================================================================
# get_valid_id_string
#===============================================================================
def get_valid_id_string(index, id_list, strict=False):
    '''
    Return a valid collection_id string, trapping any list index errors
    :param index: index
    :param id_list: list of valid id_strings
    :param strict: return None or exit if no match
    '''
    try:
        return id_list[index]
    except IndexError:
        if strict:
            print("get_valid_id_string: Invalid Index; hint try {0} -L collections --envid <envid>".format(sys.argv[0]))
            print("  index={0}(>= {2}); id_list={1}".format(index, id_list, len(id_list)))
            sys.exit(1)
        else:
            return None
    except TypeError as e:
        if strict:
            print("get_valid_id_string: Invalid Index; hint try {0} -L collections --envid <envid>".format(sys.argv[0]))
            print("  index={1}(>= {3}); id_list={2}".format(e, index, id_list, len(id_list)))
            sys.exit(1)
        else:
            return None


#===============================================================================
# upload_document
#===============================================================================
def upload_document(credentials, envid, colid, file_name):
    '''
    Upload a document into a collection in the environment
    :param credentials: Watson Credentials (username, password, version)
    :param envid: mandatory environment_id string
    :param colid: mandatory collection_id string
    :param file_name: file to upload
    '''
    import magic

    if envid is None:
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    if colid is None:
        print("Invalid colid, '{0}', hint try: {1} -L collections --envid {2}".format(colid, sys.argv[0], envid))
        sys.exit(1)

    if not (os.path.isfile(file_name) and os.access(file_name, os.R_OK)):
        print("Filename not readable, '{0}'".format(file_name))
        sys.exit(1)

#     POST /v1/environments/{environment_id}/collections/{collection_id}/documents
#     curl -X POST -u "{username}":"{password}" \
#      -F file=@sample1.html
#      "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
    if args.verbose:
        print("upload: envid={0}; colid={1}; fname={2}".format(envid, colid, file_name))

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
        print("POST: {0}".format(r.url))
        print("FILE: {0}".format(file_name))

    # 200 OK - Successful request
    # 202 Accepted - index progressing.
    # 400 Bad Request - Invalid request if the request is incorrectly formatted.
    # 404 Not Found - The request specified a resource that was not found
    if r.status_code == requests.codes.ok or r.status_code == requests.codes.accepted:
        return r.text
    else:
        if args.verbose >= 1:
            print("Upload File Failed: {0}".format(r.status_code))
        return None


#===============================================================================
# query_document
#===============================================================================
def query_document(credentials, envid, colid=None, docid=None, query=None, filtered=True):
    """
    Query a single document
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: Watson collection_id string
    :param docid: Watson document id string
    :param query: JSON string query
    :param filtered: return only enriched_text.(concepts,keywords,entities,categories)
    :param count: Number of documents to list
    """
    if envid is None:
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    if colid is None:
        print("Missing collection_id; hint {0} -L configurations --envid {1}".format(sys.argv[0], envid))
        sys.exit(1)

    # GET /v1/environments/{environment_id}/collections/{collection_id}/documents
    # curl -u "{username}":"{password}"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/query?return=extracted_metadata&version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections/' + colid + '/query'
    payload = {}
    payload['filter'] = '_id:"' + docid + '"'
    if filtered:
        payload['return'] = 'enriched_text.concepts,enriched_text.keywords,enriched_text.entities,enriched_text.categories'

    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print("GET: {0}".format(r.url))

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print("Query Document Failed: {0}".format(r.status_code))

        return None
    else:
        return r.text


#===============================================================================
# query_collection
#===============================================================================
def query_collection(credentials, envid, colid=None, query=None, count=10):
    """
    Query a single document
    :param credentials: Watson credentials
    :param envid: Watson environment_id string
    :param colid: Watson collection_id string
    :param query: JSON string query
    :param count: Number of documents to list
    """
    if envid is None:
        print("Invalid envid, '{0}'".format(envid))
        sys.exit(1)

    if colid is None:
        print("Missing collection_id; hint {0} -L configurations --envid {1}".format(sys.argv[0], envid))
        sys.exit(1)

    # GET /v1/environments/{environment_id}/collections/{collection_id}/documents
    # curl -u "{username}":"{password}"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
    # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/query?return=extracted_metadata&version=2017-11-07"

    api = "https://gateway.watsonplatform.net/discovery/api/v1/environments"
    api += '/' + envid + '/collections/' + colid + '/query'
    payload = {}
    payload['filter'] = 'enriched_text.entities.type::"Company"'
    # payload['return'] = 'enriched_text.entities'
    payload['return'] = 'enriched_text.concepts,enriched_text.keywords,enriched_text.entities,enriched_text.categories'
    payload['count'] = count
    payload['version'] = credentials['version']

    r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
    if args.verbose >= 1:
        print("GET: {0}".format(r.url))

    if r.status_code != requests.codes.ok:
        if args.verbose >= 1:
            print("Query Collection Failed: {0}".format(r.status_code))

        return None
    else:
        return r.text


#===============================================================================
# print_environments_list
#===============================================================================
def print_environments_list(result, title="Environments:"):
    '''
    Print Environments List in Human Format
    :param result: Environments text or object to print
    :param title: Title string
    '''

    print(title + os.linesep + ("=" * len(title)))

    values = result
    if isinstance(result, str) or isinstance(result, unicode):
        values = json.loads(result)

    for i, val in enumerate(values["environments"]):
        if 'environment_id' in val:
            print("[{0}]: {1[environment_id]}".format(i, val))
            print("  environment_id: {0[environment_id]}".format(val))
        else:
            print("[{0}]:".format(i))

        if 'name' in val:
            print("  name: {0[name]}".format(val))
        if 'description' in val:
            print("  description: {0[description]}".format(val))
        if 'read_only' in val:
            print("  read_only: {0[read_only]}".format(val))
        if 'created' in val:
            print("  created: {0[created]}".format(val))
        if 'updated' in val:
            print("  updated: {0[updated]}".format(val))
        print()

    return None


#===============================================================================
# print_configurations_list
#===============================================================================
def print_configurations_list(result, title="Configurations:"):
    '''
    Print Configurations List in Human Format
    :param result: Configurations text or object to print
    :param title: Title string
    '''

    print(title + os.linesep + ("=" * len(title)))

    values = result
    if isinstance(result, str) or isinstance(result, unicode):
        values = json.loads(result)

    for i, val in enumerate(values):
        if 'configuration_id' in val:
            print("{0:d}: {1[configuration_id]}".format(i, val))
            print("  configuration_id: {0[configuration_id]}".format(val))
        else:
            print("{0:d}:".format(i))

        if 'name' in val:
            print("  name: {0[name]}".format(val))
        if 'description' in val:
            print("  description: {0[description]}".format(val))
        if 'read_only' in val:
            print("  read_only: {0[read_only]}".format(val))
        if 'created' in val:
            print("  created: {0[created]}".format(val))
        if 'updated' in val:
            print("  updated: {0[updated]}".format(val))
        print()

    return None


#===============================================================================
# print_collections_list
#===============================================================================
def print_collections_list(result, title="Collections:"):
    '''
    Print Collections List
    :param result: Configurations text or object to print
    :param title: Title string
    '''
    print(title + os.linesep + ("=" * len(title)))

    values = result
    if isinstance(result, str) or isinstance(result, unicode):
        values = json.loads(result)

    for i, val in enumerate(values):
        if 'collection_id' in val:
            print("{0:d}: {1[collection_id]}".format(i, val))
            print("  collection_id: {0[collection_id]}".format(val))
        else:
            print("{0:d}:".format(i))

        if 'configuration_id' in val:
            print("  configuration_id: {0[configuration_id]}".format(val))
        if 'name' in val:
            print("  name: {0[name]}".format(val))
        if 'status' in val:
            print("  status: {0[status]}".format(val))
        if 'language' in val:
            print("  language: {0[language]}".format(val))
        if 'created' in val:
            print("  created: {0[created]}".format(val))
        if 'updated' in val:
            print("  updated: {0[updated]}".format(val))

        print()

    return None


#===============================================================================
# print_documents_list
#===============================================================================
def print_documents_list(result, title="Documents:"):
    '''
    Print Documents List
    :param result: Configurations text or object to print
    :param title: Title string
    '''

    values = result
    if isinstance(result, str):
        values = json.loads(result)

    if isinstance(result, unicode):
        values = json.loads(result)
        # http://pythonhosted.org/kitchen/unicode-frustrations.html
        # https://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
        UTF8Writer = codecs.getwriter('utf8')
        sys.stdout = UTF8Writer(sys.stdout)

    document_count = values['matching_results']
    newtitle = title + "(" + str(document_count) + ")"
    print(newtitle + os.linesep + ("=" * len(newtitle)))

    for i, val in enumerate(values['results']):

        if 'id' in val:
            print("{0:d}: {1[id]}".format(i, val))
            print("  id: {0[id]}".format(val))
        else:
            print("{0:d}:".format(i))

        if 'extracted_metadata' in val:
            if 'filename' in val['extracted_metadata']:
                print("  filename: ",)
                print(val['extracted_metadata']['filename'])
            if 'file_type' in val['extracted_metadata']:
                print("  file_type: ",)
                print(val['extracted_metadata']['file_type'])
            if 'publicationdate' in val['extracted_metadata']:
                print("  publicationdate: ",)
                print(val['extracted_metadata']['publicationdate'])
            if 'sha1' in val['extracted_metadata']:
                print("  sha1: ",)
                print(val['extracted_metadata']['sha1'])

        if 'result_metadata' in val:
            if 'score' in val['result_metadata']:
                print("  score: {0[score]}".format(val['result_metadata']))

        print()

    print("Showing {0} out of {1} documents".format(len(values['results']), document_count))

    return None


#===============================================================================
# print_environment
#===============================================================================
def print_environment(result, title="Environment:"):
    '''
    Print the Environment
    :param result: Configurations text or object to print
    :param title: Title string
    '''
    print(title + os.linesep + ("=" * len(title)))

    # simple Wrapper YAML output
    print_result(result=result, format='YAML')


#===============================================================================
# print_configuration
#===============================================================================
def print_configuration(result, title="Configuration:"):
    '''
    Print the Configuration
    :param result: Configurations text or object to print
    :param title: Title string
    '''
    print(title + os.linesep + ("=" * len(title)))

    # simple Wrapper YAML output
    print_result(result=result, format='YAML')


#===============================================================================
# print_collection
#===============================================================================
def print_collection(result, title="Collection:"):
    '''
    Print the Collection
    :param result: Configurations text or object to print
    :param title: Title string
    '''
    print(title + os.linesep + ("=" * len(title)))

    # simple Wrapper YAML output
    print_result(result=result, format='YAML')


#===============================================================================
# print_document
#===============================================================================
def print_document(result, title="Document:"):
    '''
    Print the Document
    :param result: Configurations text or object to print
    :param title: Title string
    '''
    print(title + os.linesep + ("=" * len(title)))

    # simple Wrapper YAML output
    print_result(result=result, format='YAML')


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
    parser.add_argument('-j', '--json', help='JSON output', default=False, action='store_true')
    parser.add_argument('-y', '--yaml', help='YAML output', default=False, action='store_true')
    parser.add_argument('-s', '--separator', help='field delimiter', default='\n  ')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    if args.verbose >= 1:
        print("watson-cfg: '{0}'".format(args.auth))

    credentials = get_watson_credentials(args.auth)
    envids = get_environment_ids(credentials=credentials)

    create_allowed = ['environment', 'collection']
    delete_allowed = ['environment', 'configuration', 'collection', 'document']
    list_allowed = ['environments', 'configurations', 'collections', 'documents', 'environment', 'configuration', 'collection', 'document']
    delete_allowed = ['environment', 'configuration', 'collection', 'document']
    query_allowed = ['collection', 'document']

    output_format = 'TEXT'
    if args.json:
        output_format = 'JSON'
    if args.yaml:
        output_format = 'YAML'

    if args.list:
        if not (args.list.lower() in list_allowed):
            print("{0}: invalid argument, '{1}'".format(sys.argv[0], args.list))
            sys.exit(1)

        command = args.list.lower()

        if command != 'environments':
            envid = get_valid_id_string(args.envid, envids, strict=True)

        if command == 'environments':
            result = list_environments(credentials=credentials)
            if result is None:
                print("No Environments?")
                sys.exit(1)
            elif output_format == 'TEXT':
                print_result(result=result, callback=print_environments_list)
            else:
                print_result(result=result, format=output_format)

        elif command == 'configurations':
            result = list_configurations(credentials=credentials, envid=envid, raw=args.raw)
            if result is None:
                print("No configurations for, '{0}'".format(envid))
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_configurations_list)
            else:
                print_result(result=result, format=output_format)

        elif command == 'collections':
            result = list_collections(credentials=credentials, envid=envid, raw=args.raw)
            if result is None:
                print("No collections for, '{0}'".format(envid))
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_collections_list)
            else:
                print_result(result=result, format=output_format)

        elif command == 'documents':
            colids = get_collections_ids(credentials, envid)
            colid = get_valid_id_string(args.colid, colids, strict=True)
            result = list_documents(credentials=credentials, envid=envid, colid=colid, count=args.count, raw=args.raw)

            if result is None:
                print("{1}Collection: '{0}'".format(colid, args.separator),)
                print("{0}No documents found".format(args.separator),)
                print()
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_documents_list)
            else:
                print_result(result=result, format=output_format)

        elif command == 'environment':
            result = list_environment(credentials=credentials, envid=envid)
            if result is None:
                print("EnvID: {0}".format(envid))
                print("  No documents found")
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_environment)
            else:
                print_result(result=result, format=output_format)

        elif command == 'configuration':
            cfgids = get_configuration_ids(credentials, envid)
            cfgid = get_valid_id_string(args.cfgid, cfgids, strict=True)
            result = list_configuration(credentials=credentials, envid=envid, cfgid=cfgid, raw=args.raw)
            if result is None:
                print("EnvID: {0}".format(envid))
                print("  No configurations found")
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_configuration)
            else:
                print_result(result=result, format=output_format)

        elif command == 'collection':
            colids = get_collections_ids(credentials, envid)
            colid = get_valid_id_string(args.colid, colids, strict=True)
            result = list_collection(credentials=credentials, envid=envid, colid=colid)
            if result is None:
                print("EnvID: {0}".format(envid))
                print("  No collection found")
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_collection)
            else:
                print_result(result=result, format=output_format)

        elif command == 'document':
            colids = get_collections_ids(credentials, envid)
            colid = get_valid_id_string(args.colid, colids, strict=True)
            docids = get_document_ids(credentials=credentials, envid=envid, colid=colid, count=args.count)
            docid = get_valid_id_string(args.docid, docids, strict=True)
            result = list_document(credentials=credentials, envid=envid, colid=colid, docid=docid)
            if result is None:
                print("EnvID: {0}".format(envid))
                print("  No document found")
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_document)
            else:
                print_result(result=result, format=output_format)

        else:
            print("Error: invalid List option, '{0}'".format(args.list))
            sys.exit(1)

    elif args.add:
        envid = get_valid_id_string(args.envid, envids, strict=True)
        colids = get_collections_ids(credentials, envid)
        colid = get_valid_id_string(args.colid, colids, strict=True)
        result = upload_document(credentials=credentials, envid=envid, colid=colid, file_name=args.add)
        if result is None:
            print("EnvID: {0}".format(envid))
            print("  No document found")
        elif output_format == 'TEXT':
            print("EnvID: {0}".format(envid))
            title = "Add Document: '{0}' (ColID {1})".format(args.add, colid)
            print(title + os.linesep + ("=" * len(title)))
            print_result(result=result, format="YAML")
        else:
            print_result(result=result, format=output_format)

    elif args.create:
        if not (args.create.lower() in create_allowed):
            print("{0}: invalid argument, '{1}'".format(sys.argv[0], args.list))
            sys.exit(1)

        command = args.create.lower()
        if args.envid is not None:
            envid = envids[args.envid]
            if command == 'environment':
                result = create_environment(credentials=credentials, name=args.create, descr=args.description)
            elif command == 'collection':
                cfgids = get_configuration_ids(credentials, envid)
                cfgid = get_valid_id_string(args.cfgid, cfgids, strict=True)
                result = create_collection(credentials=credentials, envid=envid, name=args.name, cfgid=cfgid, description=args.description)
            else:
                print("Invalid {1} '{2}'; hint try {0} -h".format(sys.argv[0], 'create command', command))
                print(" envid={0}; name={1}; cfgid={2}".format(args.envid, args.name, args.cfgid))
                sys.exit(1)

            if result is None:
                print("EnvID: {0}".format(envid))
                print("Create {0} '{1}' failed".format(command, args.name))
                sys.exit(1)
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                title = "Create {0} '{1}' succeeded".format(command, args.name)
                print(title + os.linesep + ("=" * len(title)))
                print_result(result=result, format="YAML")
            else:
                print_result(result=result, format=output_format)

        else:
            print("Error: invalid envid='{0}'; try {1} -L environments".format(args.envid, sys.argv[0]))
            sys.exit(1)

    elif args.delete:
        if not (args.delete.lower() in delete_allowed):
            print("{0}: invalid argument, '{1}'".format(sys.argv[0], args.delete))
            sys.exit(1)

        command = args.delete.lower()
        if args.envid is not None:
            envid = get_valid_id_string(args.envid, envids, strict=True)
            if command == 'environment':
                result = delete_environment(credentials=credentials, envid=envid)
            elif command == 'collection':
                colids = get_collections_ids(credentials=credentials, envid=envid)
                if colids:
                    colid = get_valid_id_string(args.colid, colids, strict=True)
                    result = delete_collection(credentials=credentials, envid=envid, colid=colid)
                else:
                    print("DELETE: {0}, No collections found?".format(command))
                    sys.exit(1)
            elif command == 'document':
                colids = get_collections_ids(credentials=credentials, envid=envid)
                if colids:
                    colid = get_valid_id_string(args.colid, colids, strict=True)
                    docids = get_document_ids(credentials=credentials, envid=envid, colid=colid, count=args.count)

                    if docids:
                        docid = get_valid_id_string(args.docid, docids, strict=True)
                        result = delete_document(credentials=credentials, envid=envid, colid=colid, docid=docid)
                    else:
                        print("DELETE: No document found?")
                        sys.exit(1)
                else:
                    print("DELETE: {0}, No collections found?".format(command))
                    sys.exit(1)

            if result is None:
                print("EnvID: {0}".format(envid))
                print("Delete {0} failed".format(command))
                sys.exit(1)
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                title = "Delete {0} succeeded".format(command)
                print(title + os.linesep + ("=" * len(title)))
                print_result(result=result, format="YAML")
            else:
                print_result(result=result, format=output_format)

    elif args.query:
        if not (args.query.lower() in query_allowed):
            print("{0}: invalid argument, '{1}'".format(sys.argv[0], args.query))
            sys.exit(1)

        command = args.query.lower()
        if args.envid is not None:
            envid = envids[args.envid]
            if command == 'collection':
                colids = get_collections_ids(credentials=credentials, envid=envid)
                if colids:
                    colid = get_valid_id_string(args.colid, colids, strict=True)
                    result = query_collection(credentials=credentials, envid=envid, colid=colid, count=args.count)
                else:
                    print("QUERY: {0}, No collections found?".format(command))
                    sys.exit(1)
            elif command == 'document':
                colids = get_collections_ids(credentials=credentials, envid=envid)
                if colids:
                    colid = get_valid_id_string(args.colid, colids, strict=True)
                    docids = get_document_ids(credentials=credentials, envid=envid, colid=colid, count=args.count)

                    if docids:
                        docid = get_valid_id_string(args.docid, docids, strict=True)
                        result = query_document(credentials=credentials, envid=envid, colid=colid, docid=docid)
                    else:
                        print("QUERY: {0}, No documents found?".format(command))
                        sys.exit(1)
                else:
                    print("QUERY: {0}, No collections found?".format(command))
                    sys.exit(1)

            if result is None:
                print("EnvID: {0}".format(envid))
                print("Query {0} failed".format(command))
                sys.exit(1)
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                title = "Query {0} succeeded".format(command)
                print(title + os.linesep + ("=" * len(title)))
                print_result(result=result, format="YAML")
            else:
                print_result(result=result, format=output_format)

    else:
        print("Unknown command")
        print(parser.print_usage())
        sys.exit(1)

    sys.exit(0)
