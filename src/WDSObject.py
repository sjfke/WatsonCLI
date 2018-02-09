#!/usr/bin/env python3
import sys
import json
import yaml
import requests
import os
import logging
from configparser import SafeConfigParser

logging.basicConfig(format='%(asctime) %(message)s')


class WDSObject:
    '''
    Simplistic access to IBM Watson Discovery Service
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

    #===============================================================================
    # get_environments
    #===============================================================================
    def get_environments(self, raw=True):
        """
         Return Watson Discovery Environments
        :param raw: unformatted JSON result
        """
        api = self.__url + '/v1/environments'
        payload = {}
        payload['version'] = self.__version

        r = requests.get(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("GET: {0}".format(r.url))

        if r.status_code != requests.codes.ok:
            logging.debug("List Collections Failed: {0}".format(r.status_code))
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
    # get_configurations
    #===============================================================================
    def get_configurations(self, envid, raw=True):
        """
         Return Watson Discovery Configurations
        :param envid: Watson environment_id string
        :param raw: unformatted JSON result
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        # curl -u "{username}":"{password}"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/configurations?version=2017-11-07"
        api = self.__url + '/v1/environments/' + envid + '/configurations'
        payload = {}
        payload['version'] = self.__version

        r = requests.get(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("GET: {}".format(r.url))

        if r.status_code != requests.codes.ok:
            logging.debug("List Configurations Failed: {0}".format(r.status_code))
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
    def get_configuration_ids(self, envid):
        """
        Return Watson Discovery Configuration IDs
        :param envid: Watson environment_id string
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        id_list = []
        configuration = json.loads(self.get_configurations(envid=envid))
        for c in configuration['configurations']:
            id_list.append(c['configuration_id'])

        return id_list

    #===============================================================================
    # get_collections
    #===============================================================================
    def get_collections(self, envid, raw=True):
        """
         Return Watson Discovery Collections
        :param envid: Watson environment_id string
        :param raw: JSON output
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        # https://www.ibm.com/watson/developercloud/discovery/api/v1/?curl#create-collection
        # curl -u "{username}":"{password}" \
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections?version=2017-11-07"
        api = self.__url + '/v1/environments/' + envid + '/collections'
        payload = {}
        payload['version'] = self.__version

        r = requests.get(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("GET: {0}".format(r.url))

        if r.status_code != requests.codes.ok:
            logging.error("List Collections Failed: {0}".format(r.status_code))
            return None
        else:
            if raw:
                return r.text
            else:
                cols = json.loads(r.text)
                collection_list = []
                for c in cols['collections']:
                    collection_list.append(c)

                if len(collection_list):
                    return collection_list
                else:
                    return None

    #===============================================================================
    # get_collections_ids
    #===============================================================================
    def get_collections_ids(self, envid):
        """
         Return a list of Watson Discovery Collections
        :param envid: Watson environment_id string
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        id_list = []
        collections = json.loads(self.get_collections(envid=envid))
        for c in collections['collections']:
            id_list.append(c['collection_id'])

        return id_list

    #===============================================================================
    # get_documents
    #===============================================================================
    def get_documents(self, envid, colid=None, count=10):
        """
        Return a list of Watson Discovery Documents
        :param envid: Watson environment_id string
        :param colid: Watson collection_id string
        :param count: Number of documents to list
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if colid is None:
            logging.critical("Missing collection_id; hint {0} -L configurations --envid {1}".format(sys.argv[0], envid))
            return None

        # GET /v1/environments/{environment_id}/collections/{collection_id}/documents
        # curl -u "{username}":"{password}"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/query?return=extracted_metadata&version=2017-11-07"

        api = self.__url + '/v1/environments/' + envid + '/collections/' + colid + '/query'
        payload = {}
        payload['return'] = 'extracted_metadata'
        payload['count'] = count
        payload['version'] = self.__version

        r = requests.get(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("list_documents: GET: {0}".format(r.url))

        if r.status_code != requests.codes.ok:
            logging.error("List Documents Failed: {0}".format(r.status_code))
            return None
        else:
            return r.text

    #===============================================================================
    # get_document_ids
    #===============================================================================
    def get_document_ids(self, envid, colid, count=10):
        """
        Return a list of Watson Discovery Document IDs
        :param envid: Watson environment_id string
        :param colid: Watson collection_id string
        :param count: Number of documents to list
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if colid is None:
            logging.critical("Invalid colid, '{0}'".format(colid))
            return None

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
        id_list = []
        documents = self.get_documents(envid=envid, colid=colid, count=count)
        if documents is not None:
            document = json.loads(documents)
            if documents["matching_results"] > count:
                logging.warning("Only {0} out of {1} document ids returned".format(count, documents["matching_results"]))

            for d in document['results']:
                id_list.append(d['id'])

        if len(id_list):
            return id_list
        else:
            return None

    #===============================================================================
    # delete_document
    #===============================================================================
    def delete_document(self, envid, colid, docid):
        '''
        Delete a document from a collection
        :param envid: Watson environment_id string
        :param colid: collection_id string
        :param docid: document_id string
        '''
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if colid is None:
            logging.critical("Invalid colid, '{0}'".format(colid))
            return None

        if docid is None:
            logging.critical("Invalid docid, '{0}'".format(docid))
            return None

        # DELETE /v1/environments/{environment_id}/collections/{collection_id}/documents/{document_id}
        # curl -X DELETE -u "{username}":"{password}"
        #  "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents/{document_id}?version=2017-11-07"

        api = self.__url + '/v1/environments/' + envid + '/collections/' + colid + '/documents/' + docid
        payload = {}
        payload['version'] = self.__version

        r = requests.delete(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("DELETE: {0}".format(r.url))

        if r.status_code != requests.codes.ok:
            if args.verbose >= 1:
                logging.error("Delete_document({0},{1},{2},{3})".format('****', envid, colid, docid))
                logging.error("Delete document Failed: {0} ".format(r.status_code))

            return None
        else:
            return r.text

    #===============================================================================
    # get_environment
    #===============================================================================
    def get_environment(self, envid):
        """
        Return Watson Discovery Environment Details
        :param envid: Watson environment_id string
        :param raw: True JSON output, YAML otherwise
        """

        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        # GET /v1/environments/{environment_id}
        # curl -u "{username}":"{password}"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}?version=2017-11-07"
        api = self.__url + '/v1/environments/' + envid
        payload = {}
        payload['version'] = self.__version

        r = requests.get(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("GET: {0}".format(r.url))

        if r.status_code != requests.codes.ok:
            logging.error("List environment Failed: {0}".format(r.status_code))
            return None
        else:
            return r.text

    #===============================================================================
    # get_configuration
    #===============================================================================
    def get_configuration(self, envid, cfgid):
        """
         Return Watson Discovery Configuration Details
        :param envid: Watson environment_id string
        :param cfgid: Watson configuration_id string
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if cfgid is None:
            logging.critical("Invalid cfgid, '{0}'".format(cfgid))
            return None

        # GET /v1/environments/{environment_id}/configurations/{configuration_id}
        # curl -u "{username}":"{password}"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/configurations/{configuration_id}?version=2017-11-07"
        api = self.__url + '/v1/environments/' + envid + '/configurations/' + cfgid
        payload = {}
        payload['version'] = self.__version

        r = requests.get(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("GET: {0}".format(r.url))

        if r.status_code != requests.codes.ok:
            logging.error("List configuration Failed: {0}".format(r.status_code))
            return None
        else:
            return r.text

    #===============================================================================
    # get_collection
    #===============================================================================
    def get_collection(self, envid, colid):
        """
         Return Watson Discovery Collection Details
        :param envid: Watson environment_id string
        :param colid: Watson collection_id string
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if colid is None:
            logging.critical("Invalid colid, '{0}'".format(colid))
            return None

        # GET /v1/environments/{environment_id}/collections/{collection_id}
        # curl -u "{username}":"{password}"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}?version=2017-11-07"
        api = self.__url + '/v1/environments/' + envid + '/collections/' + colid
        payload = {}
        payload['version'] = self.__version

        r = requests.get(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("GET: {0}".format(r.url))

        if r.status_code != requests.codes.ok:
            logging.error("List collection Failed: {0}".format(r.status_code))
            return None
        else:
            return r.text

    #===============================================================================
    # get_document
    #===============================================================================
    def get_document(self, envid, colid, docid):
        """
         Return Watson Discovery Document Details
        :param envid: Watson environment_id string
        :param colid: Watson collection_id string
        :param docid: Watson document_id string
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if colid is None:
            logging.critical("Invalid colid, '{0}'".format(colid))
            return None

        if docid is None:
            logging.critical("Invalid docid, '{0}'".format(docid))
            return None

        # GET /v1/environments/{environment_id}/collections/{collection_id}/documents/{document_id}
        # curl -u "{username}":"{password}"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents/{document_id}?version=2017-11-07"
        api = self.__url + '/v1/environments/' + envid + '/collections/' + colid + '/documents/' + docid
        payload = {}
        payload['version'] = self.__version

        r = requests.get(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("GET: {0}".format(r.url))

        if r.status_code != requests.codes.ok:
            logging.error("List document Failed: {0}".format(r.status_code))
            return None
        else:
            return r.text

    #===============================================================================
    # get_environment_ids
    #===============================================================================
    def get_environment_ids(self):
        """
        Return a List of Watson Discovery Environment Identifiers
        """
        environment_list = self.get_environments()
        results = None
        if environment_list:
            results = []
            envs = json.loads(environment_list)
            for env in envs['environments']:
                results.append(env['environment_id'])

        return results

    #===============================================================================
    # create_environment
    #===============================================================================
    def create_environment(self, name, descr):
        """
        Create Discovery Environment
        :param name: mandatory environment name
        :param descr: optional environment description
        """
        api = self.__url + '/v1/environments/' + '?version=' + self.__version

        if name is None:
            logging.critical("Environment needs a name, {0}".format(name))
            return None

        data = {'name': name, 'description': descr}
        r = requests.post(api, json=data, auth=(self.__username, sel.__password))

        logging.debug("POST: {0}".format(r.url))
        logging.debug("JSON: {0}".format(data))

        if r.status_code == requests.codes.ok or r.status_code == requests.codes.created:
            return r.text
        else:
            logging.critical("Create Environment Failed: {0}".format(r.status_code))
            return None

    #===============================================================================
    # delete_environment
    #===============================================================================
    def delete_environment(self, envid):
        """
         Delete Discovery Environment (REST + post)
        :param envid: mandatory environment_id string
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        api = self.__url + '/v1/environments/' + envid
        payload = {}
        payload['version'] = self.__version

        r = requests.delete(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("DELETE: {0}".format(r.url))

        return r.text

    #===============================================================================
    # create_collection
    #===============================================================================
    def create_collection(self, envid, name, cfgid, description=None, language='en'):
        '''
        Create Watson collection in the environment
        :param envid: mandatory environment_id string
        :param cfgid: mandatory configuration_id string
        :param description: optional description
        :param language: defaults to 'en'
        '''
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if name is None:
            logging.critical("Environment needs a name, {0}".format(name))
            return None

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

        api = self.__url + '/v1/environments/' + envid + '/collections'
        api += '?version=' + self.__version

        data = {'name': name, 'description': description, 'configuration_id': cfgid, 'language': language}
        r = requests.post(api, json=data, auth=(self.__username, self.__password))

        logging.debug("POST: {0}".format(r.url))
        logging.debug("DATA: {0}".format(data))

        if r.status_code == requests.codes.ok or r.status_code == requests.codes.created:
            logging.debug("{0}: Create Collection succeeded".format(r.status_code))
            return r.text
        else:
            logging.error("Create Collection Failed: {0}".format(r.status_code))
            return None

    #===============================================================================
    # delete_collection
    #===============================================================================
    def delete_collection(self, envid, colid):
        '''
        Delete collection in Watson environment
        :param envid: mandatory environment_id string
        :param colid: mandatory collection_id string
        '''
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if colid is None:
            logging.critical("Invalid colid, '{0}'".format(colid))
            return None

        # DELETE /v1/environments/{environment_id}/collections/{collection_id}
        # curl -u "{username}":"{password}" -X DELETE
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}?version=2017-11-07"
        api = self.__url + '/v1/environments/' + envid + '/collections/' + colid
        payload = {}
        payload['version'] = self.__version

        r = requests.delete(api, params=payload, auth=(credentials['username'], credentials['password']))
        logging.debug("DELETE {0}".format(r.url))
        return r.text

    #===============================================================================
    # upload_document
    #===============================================================================
    def upload_document(self, envid, colid, file_name):
        '''
        Upload a document into a collection in the environment
        :param envid: mandatory environment_id string
        :param colid: mandatory collection_id string
        :param file_name: file to upload
        '''
        import magic

        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if colid is None:
            logging.critical("Invalid colid, '{0}',; envid '{1}'".format(colid, envid))
            return None

        if not (os.path.isfile(file_name) and os.access(file_name, os.R_OK)):
            logging.critical("Filename not readable, '{0}'".format(file_name))
            return None

        # POST /v1/environments/{environment_id}/collections/{collection_id}/documents
        # curl -X POST -u "{username}":"{password}" \
        # -F file=@sample1.html
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
        logging.debug("upload: envid={0}; colid={1}; fname={2}".format(envid, colid, file_name))

        api = self.__url + '/v1/environments/' + envid + '/collections/' + colid + '/documents'
        api += '?version=' + self.__version

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

        logging.debug("POST: {0}".format(r.url))
        logging.debug("FILE: {0}".format(file_name))

        # 200 OK - Successful request
        # 202 Accepted - index progressing.
        # 400 Bad Request - Invalid request if the request is incorrectly formatted.
        # 404 Not Found - The request specified a resource that was not found
        if r.status_code == requests.codes.ok or r.status_code == requests.codes.accepted:
            return r.text
        else:
            logging.error("Upload File Failed: {0}".format(r.status_code))
            return None

    #===============================================================================
    # query_document
    #===============================================================================
    def query_document(self, envid, colid=None, docid=None, query=None, filtered=True):
        """
        Query a single document
        :param envid: Watson environment_id string
        :param colid: Watson collection_id string
        :param docid: Watson document id string
        :param query: JSON string query
        :param filtered: return only enriched_text.(concepts,keywords,entities,categories)
        :param count: Number of documents to list
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if colid is None:
            logging.critical("Invalid colid, '{0}'".format(colid))
            return None

        if docid is None:
            logging.critical("Invalid docid, '{0}'".format(docid))
            return None

        # GET /v1/environments/{environment_id}/collections/{collection_id}/documents
        # curl -u "{username}":"{password}"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/query?return=extracted_metadata&version=2017-11-07"
        api = self.__url + '/v1/environments/' + envid + '/collections/' + colid + '/query'
        payload = {}
        payload['filter'] = '_id:"' + docid + '"'
        if filtered:
            payload['return'] = 'enriched_text.concepts,enriched_text.keywords,enriched_text.entities,enriched_text.categories'

        payload['version'] = self.__version

        r = requests.get(api, params=payload, auth=(credentials['username'], credentials['password']))
        logging.debug("GET: {0}".format(r.url))

        if r.status_code != requests.codes.ok:
            logging.error("Query Document Failed: {0}".format(r.status_code))
            return None
        else:
            return r.text

    #===============================================================================
    # query_collection
    #===============================================================================
    def query_collection(self, envid, colid=None, query=None, count=10):
        """
        Query a single document
        :param envid: Watson environment_id string
        :param colid: Watson collection_id string
        :param query: JSON string query
        :param count: Number of documents to list
        """
        if envid is None:
            logging.critical("Invalid envid, '{0}'".format(envid))
            return None

        if colid is None:
            logging.critical("Invalid colid, '{0}'".format(colid))
            return None

        # GET /v1/environments/{environment_id}/collections/{collection_id}/documents
        # curl -u "{username}":"{password}"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/documents?version=2017-11-07"
        # "https://gateway.watsonplatform.net/discovery/api/v1/environments/{environment_id}/collections/{collection_id}/query?return=extracted_metadata&version=2017-11-07"
        api = self.__url + '/v1/environments/' + envid + '/collections/' + colid + '/query'
        payload = {}
        payload['filter'] = 'enriched_text.entities.type::"Company"'
        payload['return'] = 'enriched_text.concepts,enriched_text.keywords,enriched_text.entities,enriched_text.categories'
        payload['count'] = count
        payload['version'] = self.__version

        r = requests.get(api, params=payload, auth=(self.__username, self.__password))
        logging.debug("GET: {0}".format(r.url))

        if r.status_code != requests.codes.ok:
            logging.error("Query Collection Failed: {0}".format(r.status_code))
            return None
        else:
            return r.text

    #===============================================================================
    # get_valid_id_string
    #===============================================================================
    @staticmethod
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
                logging.critical("get_valid_id_string: Invalid Index; hint try {0} -L collections --envid <envid>".format(sys.argv[0]))
                logging.critical("  index={0}(>= {2}); id_list={1}".format(index, id_list, len(id_list)))
                sys.exit(1)
            else:
                return None
        except TypeError as e:
            if strict:
                logging.critical("get_valid_id_string: Invalid Index; hint try {0} -L collections --envid <envid>".format(sys.argv[0]))
                logging.critical("  index={1}(>= {3}); id_list={2}".format(e, index, id_list, len(id_list)))
                sys.exit(1)
            else:
                return None
