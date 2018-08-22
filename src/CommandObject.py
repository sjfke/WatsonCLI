#!/usr/bin/env python3
import logging
import os
from WDSObject import WDSObject

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.ERROR)


class CommandObject:
    '''
    WDS Command Line Object, use to validate commands, sub-commands and store arguments
    '''
    #===========================================================================
    # __init__
    #===========================================================================

    def __init__(self, args):
        '''
        Commmand object used to store validated command, its arguments etc.
        :param args: arguments dictionary from ArgumentParser
        '''
        self.__auth = args.auth
        self.__command = None
        self.__subcommand = None
        self.__command_name = None
        self.__envid = args.envid
        self.__envid_str = None
        self.__cfgid = args.cfgid
        self.__cfgid_str = None
        self.__colid = args.colid
        self.__colid_str = None
        self.__docid = args.docid
        self.__docid_str = None
        self.__count = args.count
        self.__name = args.name
        self.__description = args.description
        self.__json = args.json
        self.__yaml = args.yaml
        self.__output_format = 'TEXT'
        self.__validated = False

        __sub_commands = {}
        __sub_commands['create'] = ['environment', 'collection']
        __sub_commands['delete'] = ['environment', 'configuration', 'collection', 'document']
        __sub_commands['list'] = ['environments', 'configurations', 'collections', 'documents', 'environment', 'configuration', 'collection', 'document']
        __sub_commands['delete'] = ['environment', 'configuration', 'collection', 'document']
        __sub_commands['query'] = ['collection', 'document']

        if args.list:
            self.__command = 'list'
            if not (args.list.lower() in __sub_commands[self.__command]):
                logging.critical("{0}: invalid sub-command, '{1}'".format(self.__command, args.list))
                return None
            else:
                self.__subcommand = args.list.lower()

        elif args.add:
            self.__command = 'add'
            self.__name = args.add
            if self.__envid is None or self.__colid is None:
                logging.critical("{0}: envid = '{1}'; colid ='{2}'".format(self.__command, self.__envid, self.__colid))
                return None

        elif args.create:
            self.__command = 'create'
            if not (args.create.lower() in __sub_commands[self.__command]):
                logging.critical("{0}: invalid sub-command, '{1}'".format(self.__command, args.create))
                return None
            else:
                self.__subcommand = args.create.lower()
                self.__name = args.name
                if self.__envid is None or self.__cfgid is None:
                    logging.critical("{0}: envid = '{1}'; colid ='{2}'".format(self.__command, self.__envid, self.__cfgid))

        elif args.delete:
            self.__command = 'delete'
            if not (args.delete.lower() in __sub_commqnds[self.__command]):
                logging.critical("{0}: invalid sub-command, '{1}'".format(self.__command, args.delete))
                return None
            else:
                self.__subcommand = args.delete.lower()

        elif args.query:
            self.__command = 'query'
            if not (args.query.lower() in __sub_commands[self.__command]):
                logging.critical("{0}: invalid sub-command, '{1}'".format(self.__command, args.query))
                return None
            else:
                self.__subcommand = args.query.lower()

        else:
            logging.critical("Unknown command")
            return None

        if self.__subcommand is None:
            self.__command_name = self.__command
        else:
            self.__command_name = self.__command + '_' + self.__subcommand

        if args.json:
            self.__output_format = 'JSON'

        if args.yaml:
            self.__output_format = 'YAML'

    #===========================================================================
    # get_auth
    #===========================================================================
    def get_auth(self):
        return self.__auth

    #===========================================================================
    # get_command
    #===========================================================================
    def get_command(self):
        return self.__command

    #===========================================================================
    # get_subcommand
    #===========================================================================
    def get_subcommand(self):
        return self.__subcommand

    #===========================================================================
    # get_command_name
    #===========================================================================
    def get_command_name(self):
        return self.__command_name

    #===========================================================================
    # get_envid
    #===========================================================================
    def get_envid(self):
        return self.__envid

    #===========================================================================
    # get_envid_str
    #===========================================================================
    def get_envid_str(self):
        return self.__envid_str

    #===========================================================================
    # get_cfgid
    #===========================================================================
    def get_cfgid(self):
        return self.__cfgid

    #===========================================================================
    # get_cfgid_str
    #===========================================================================
    def get_cfgid_str(self):
        return self.__cfgid_str

    #===========================================================================
    # get_colid
    #===========================================================================
    def get_colid(self):
        return self.__colid

    #===========================================================================
    # get_colid_str
    #===========================================================================
    def get_colid_str(self):
        return self.__colid_str

    #===========================================================================
    # get_docid
    #===========================================================================
    def get_docid(self):
        return self.__docid

    #===========================================================================
    # get_docid_str
    #===========================================================================
    def get_docid_str(self):
        return self.__docid_str

    #===========================================================================
    # get_count
    #===========================================================================
    def get_count(self):
        return self.__count

    #===========================================================================
    # get_name
    #===========================================================================
    def get_name(self):
        return self.__name

    #===========================================================================
    # get_description
    #===========================================================================
    def get_description(self):
        return self.__description

    #===========================================================================
    # get_json
    #===========================================================================
    def get_json(self):
        return self.__json

    #===========================================================================
    # get_yaml
    #===========================================================================
    def get_yaml(self):
        return self.__yaml

    #===========================================================================
    # get_output_format
    #===========================================================================
    def get_output_format(self):
        return self.__output_format

    #===========================================================================
    # get_validated
    #===========================================================================
    def get_validated(self):
        return self.__validated

    #===========================================================================
    # set_auth
    #===========================================================================
    def set_auth(self, value):
        self.__auth = value

    #===========================================================================
    # set_count
    #===========================================================================
    def set_count(self, value):
        self.__count = value

    #===========================================================================
    # set_name
    #===========================================================================
    def set_name(self, value):
        self.__name = value

    #===========================================================================
    # set_description
    #===========================================================================
    def set_description(self, value):
        self.__description = value

    auth = property(get_auth, set_auth, None, None)
    command = property(get_command, None, None, None)
    subcommand = property(get_subcommand, None, None, None)
    command_name = property(get_command_name, None, None, None)
    envid = property(get_envid, None, None, None)
    envid_str = property(get_envid_str, None, None, None)
    cfgid = property(get_cfgid, None, None, None)
    cfgid_str = property(get_cfgid_str, None, None, None)
    colid = property(get_colid, None, None, None)
    colid_str = property(get_colid_str, None, None, None)
    docid = property(get_docid, None, None, None)
    docid_str = property(get_docid_str, None, None, None)
    count = property(get_count, set_count, None, None)
    name = property(get_name, set_name, None, None)
    description = property(get_description, set_description, None, None)
    json = property(get_json, None, None, "json's docstring")
    yaml = property(get_yaml, None, None, None)
    output_format = property(get_output_format, None, None, None)
    validated = property(get_validated, None, None, None)

    #===========================================================================
    # __repr__
    #===========================================================================
    def __repr__(self):
        '''
        Return a sring representation of the object
        '''
        str = ''
        str += "{0:13s}: {1}".format('auth', self.__auth) + os.linesep
        str += "{0:13s}: {1}".format('command', self.__command) + os.linesep
        str += "{0:13s}: {1}".format('subcommand', self.__subcommand) + os.linesep
        str += "{0:13s}: {1}".format('command_name', self.__command_name) + os.linesep
        str += "{0:13s}: {1}".format('envid', self.__envid) + os.linesep
        str += "{0:13s}: {1}".format('envid_str', self.__envid_str) + os.linesep
        str += "{0:13s}: {1}".format('cfgid', self.__cfgid) + os.linesep
        str += "{0:13s}: {1}".format('cfgid_str', self.__cfgid_str) + os.linesep
        str += "{0:13s}: {1}".format('colid', self.__colid) + os.linesep
        str += "{0:13s}: {1}".format('colid_str', self.__colid_str) + os.linesep
        str += "{0:13s}: {1}".format('docid', self.__docid) + os.linesep
        str += "{0:13s}: {1}".format('docid_str', self.__docid_str) + os.linesep
        str += "{0:13s}: {1}".format('count', self.__count) + os.linesep
        str += "{0:13s}: {1}".format('name', self.__name) + os.linesep
        str += "{0:13s}: {1}".format('description', self.__description) + os.linesep
        str += "{0:13s}: {1}".format('json', self.__json) + os.linesep
        str += "{0:13s}: {1}".format('yaml', self.__yaml) + os.linesep
        str += "{0:13s}: {1}".format('output_format', self.__output_format) + os.linesep
        str += "{0:13s}: {1}".format('validated', self.__validated)
        return str

    #===========================================================================
    # validate
    #===========================================================================
    def validate(self, wds):
        '''
        Validate the WDS identifiers, return True of False
        :param wds: WDSObject
        '''
        if self.__validated:
            return self.__validated
        elif self.__command == 'list' and self.__subcommand == 'environments':
            self.__validated = True
            return self.__validated
        else:
            __id_str = wds.get_valid_id_string(self.__envid, wds.get_environment_ids())
            if __id_str is None:
                logging.critical("{0}: invalid environment_id, {1}".format(self.__command_name, self.__envid))
                return False
            else:
                self.__envid_str = __id_str

            if self.__cfgid is not None:
                __id_str = wds.get_valid_id_string(self.__cfgid, wds.get_configuration_ids(self.__envid_str))
                if __id_str is None:
                    logging.critical("{0}: invalid configuration_id, {1}".format(self.__command_name, self.__cfgid))
                    return False
                else:
                    self.__cfgid_str = __id_str

            if self.__colid is not None:
                __id_str = wds.get_valid_id_string(self.__colid, wds.get_collections_ids(self.__envid_str))
                if __id_str is None:
                    logging.critical("{0}: invalid collection_id, {1}".format(self.__command_name, self.__colid))
                    return False
                else:
                    self.__colid_str = __id_str

            if self.__docid is not None:
                if self.__count is None:
                    logging.warning("{0}: setting count to, {1}".format(self.__command_name, 10))
                    self.__count = 10

                __id_str = wds.get_valid_id_string(self.__colid, wds.get_document_ids(self.__envid_str, self.__colid_str, self.__count))
                if __id_str is None:
                    logging.critical("{0}: invalid document_id, {1}".format(self.__command_name, self.__docid))
                    return False
                else:
                    self.__docid_str = __id_str

            if self.__command_name == 'list_documents' and self.__colid is None:
                logging.critical("{0}: missing collection_id, {1}".format(self.__command_name, self.__colid_str))
                return False
            elif self.__command_name == 'list_configuration' and self.__cfgid is None:
                logging.critical("{0}: missing configuration_id, {1}".format(self.__command_name, self.__cfgid_str))
                return False
            elif self.__command_name == 'list_collection' and self.__colid is None:
                logging.critical("{0}: missing collection_id, {1}".format(self.__command_name, self.__colid_str))
                return False
            elif self.__command_name == 'list_document' and (self.__colid is None or self.__docid is None):
                logging.critical("{0}: missing collection_id, {1} or document_id, {2}".format(self.__command_name, self.__colid_str, self.__docid_str))
                return False
            elif self.__command_name == 'add' and (self.__colid is None or self.__name is None):
                logging.critical("{0}: missing collection_id, {1} or document name, {2}".format(self.__command_name, self.__colid_str, self.__name))
                return False
            elif self.__command_name == 'create_environment' and self.__name is None:
                logging.critical("{0}: missing environment name, {1}".format(self.__command_name, self.__name))
                return False
            elif self.__command_name == 'create_collection' and (self.__name is None or self.__cfgid is None):
                logging.critical("{0}: missing collection name, {1} or configuration_id, {2}".format(self.__command_name, self.__name, self.__cfgid_str))
                return False
            elif self.__command_name == 'delete_collection' and self.__colid is None:
                logging.critical("{0}: missing collection_id, {1}".format(self.__command_name, self.__colid_str))
                return False
            elif self.__command_name == 'delete_document' and (self.__colid is None or self.__docid is None):
                logging.critical("{0}: missing collection_id, {1} or document_id, {2}".format(self.__command_name, self.__colid_str, self.__docid_str))
                return False
            elif self.__command_name == 'query_collection' and self.__colid is None:
                logging.critical("{0}: missing collection_id, {1}".format(self.__command_name, self.__colid_str))
                return False
            elif self.__command_name == 'query_document' and (self.__colid is None or self.__docid is None):
                logging.critical("{0}: missing collection_id, {1} or document_id, {2}".format(self.__command_name, self.__colid_str, self.__docid_str))
                return False

            if self.__json:
                self.__output_format = 'JSON'
            if self.__yaml:
                self.__output_format = 'YAML'

            self.__validated = True
            return self.__validated

    #===========================================================================
    # execute
    #===========================================================================
    def execute(self, wds):
        '''
        Execute a validated command, validate() must be called first.
        :param wds: WDSObject
        '''
        if not self.__validated:
            logging.critical("{0}: command object is not validated".format(self.__command_name))
            return None

        if self.__command_name == 'list_environments':
            return wds.get_environments()
        elif self.__command_name == 'list_configurations':
            return wds.get_configurations(envid=self.__envid_str)
        elif self.__command_name == 'list_collections':
            return wds.get_collections(envid=self.__envid_str)
        elif self.__command_name == 'list_documents':
            return wds.get_documents(envid=self.__envid_str, colid=self.__colid_str, count=self.__count)
        elif self.__command_name == 'list_environment':
            return wds.get_environment(envid=self.__envid_str)
        elif self.__command_name == 'list_configuration':
            return wds.get_configuration(envid=self.__envid_str, cfgid=self.__cfgid_str)
        elif self.__command_name == 'list_collection':
            return wds.get_collection(envid=self.__envid_str, colid=self.__colid_str)
        elif self.__command_name == 'list_document':
            return wds.get_document(envid=self.__envid_str, colid=self.__colid_str, docid=self.__docid_str)
        elif self.__command_name == 'add':
            return wds.upload_document(envid=self.__envid_str, colid=self.__colid_str, file_name=self.__name)
        elif self.__command_name == 'create_environment':
            return wds.create_environment(name=self.__name, descr=self.__description)
        elif self.__command_name == 'create_collection':
            return wds.create_collection(envid=self.__envid_str, name=self.__name, cfgid=self.__cfgid_str, description=self.__description)
        elif self.__command_name == 'delete_environment':
            return wds.delete_environment(envid=self.__envid_str)
        elif self.__command_name == 'delete_collection':
            return wds.delete_collection(envid=self.__envid_str, colid=self.__colid_str)
        elif self.__command_name == 'delete_document':
            return wds.delete_document(envid=self.__envid_str, colid=self.__colid_str, docid=self.__docid_str)
        elif self.__command_name == 'query_collection':
            return wds.query_collection(envid=self.__envid_str, colid=self.__colid_str, count=self.__count)
        elif self.__command_name == 'query_document':
            return wds.query_document(envid=self.__envid_str, colid=self.__colid_str, docid=self.__docid_str)
        else:
            logging.critical("{0}: unknown command, {1}".format('execute', self.__command_name))
            return None
