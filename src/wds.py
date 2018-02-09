#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import argparse
import codecs
import os
import re
import sys
import json
import yaml

from WDSObject import WDSObject

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

    # TODO: This is overly complex and needs to be redone, values needs to be a sane JSON string thats all.
    if isinstance(result, str):
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
    if isinstance(result, str):
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
    if isinstance(result, str):
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
    if isinstance(result, str):
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

        print

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
    wds_cfg_file = os.path.join(os.getcwd(), '.watson.cfg')

    parser = argparse.ArgumentParser(description='WDS Simplistic CLI interface')
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
    parser.add_argument('-a', '--auth', default=None, help='Watson credentials file')
    parser.add_argument('--raw', help='JSON output', default=False, action='store_true')
    parser.add_argument('-j', '--json', help='JSON output', default=False, action='store_true')
    parser.add_argument('-y', '--yaml', help='YAML output', default=False, action='store_true')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()

    if args.auth:
        wds_cfg_file = args.auth

    if args.verbose >= 1:
        print("wds-cfg: '{0}'".format(wds_cfg_file))

    wds = WDSObject(wds_cfg_file)

    if wds is None:
        print("Failed to create Watson Discovery Object")
        sys.exit(1)

    envids = wds.get_environment_ids()

    sub_commands = {}
    sub_commands['create'] = ['environment', 'collection']
    sub_commands['delete'] = ['environment', 'configuration', 'collection', 'document']
    sub_commands['list'] = ['environments', 'configurations', 'collections', 'documents', 'environment', 'configuration', 'collection', 'document']
    sub_commands['delete'] = ['environment', 'configuration', 'collection', 'document']
    sub_commands['query'] = ['collection', 'document']

    output_format = 'TEXT'
    if args.json:
        output_format = 'JSON'
    if args.yaml:
        output_format = 'YAML'

    if args.list:
        if not (args.list.lower() in sub_commands['list']):
            print("{0}: invalid argument, '{1}'".format(sys.argv[0], args.list))
            sys.exit(1)

        command = args.list.lower()

        if command != 'environments':
            envid = wds.get_valid_id_string(args.envid, envids, strict=True)

        if command == 'environments':
            result = wds.get_environments()
            if result is None:
                print("No Environments?")
                sys.exit(1)
            elif output_format == 'TEXT':
                print_result(result=result, callback=print_environments_list)
            else:
                print_result(result=result, format=output_format)

        elif command == 'configurations':
            result = wds.get_configurations(envid=envid, raw=args.raw)
            if result is None:
                print("No configurations for, '{0}'".format(envid))
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_configurations_list)
            else:
                print_result(result=result, format=output_format)

        elif command == 'collections':
            result = wds.get_collections(envid=envid, raw=args.raw)
            if result is None:
                print("No collections for, '{0}'".format(envid))
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_collections_list)
            else:
                print_result(result=result, format=output_format)

        elif command == 'documents':
            colids = wds.get_collections_ids(envid)
            colid = wds.get_valid_id_string(args.colid, colids, strict=True)
            result = wds.get_documents(envid=envid, colid=colid, count=args.count)

            if result is None:
                print("Collection: '{0}'".format(colid),)
                print("  No documents found".format(),)
                print()
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_documents_list)
            else:
                print_result(result=result, format=output_format)

        elif command == 'environment':
            result = wds.get_environment(envid=envid)
            if result is None:
                print("EnvID: {0}".format(envid))
                print("  No documents found")
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_environment)
            else:
                print_result(result=result, format=output_format)

        elif command == 'configuration':
            cfgids = wds.get_configuration_ids(envid)
            cfgid = wds.get_valid_id_string(args.cfgid, cfgids, strict=True)
            result = wds.get_configuration(envid=envid, cfgid=cfgid)
            if result is None:
                print("EnvID: {0}".format(envid))
                print("  No configurations found")
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_configuration)
            else:
                print_result(result=result, format=output_format)

        elif command == 'collection':
            colids = wds.get_collections_ids(envid)
            colid = wds.get_valid_id_string(args.colid, colids, strict=True)
            result = wds.get_collection(envid=envid, colid=colid)
            if result is None:
                print("EnvID: {0}".format(envid))
                print("  No collection found")
            elif output_format == 'TEXT':
                print("EnvID: {0}".format(envid))
                print_result(result=result, callback=print_collection)
            else:
                print_result(result=result, format=output_format)

        elif command == 'document':
            colids = wds.get_collections_ids(envid)
            colid = wds.get_valid_id_string(args.colid, colids, strict=True)
            docids = wds.get_document_ids(envid=envid, colid=colid, count=args.count)
            docid = wds.get_valid_id_string(args.docid, docids, strict=True)
            result = wds.get_document(envid=envid, colid=colid, docid=docid)
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
        envid = wds.get_valid_id_string(args.envid, envids, strict=True)
        colids = wds.get_collections_ids(envid=envid)
        colid = wds.get_valid_id_string(args.colid, colids, strict=True)
        result = wds.upload_document(envid=envid, colid=colid, file_name=args.add)
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
        if not (args.create.lower() in sub_commqnds['create']):
            print("{0}: invalid argument, '{1}'".format(sys.argv[0], args.list))
            sys.exit(1)

        command = args.create.lower()
        if args.envid is not None:
            envid = envids[args.envid]
            if command == 'environment':
                result = wds.create_environment(name=args.create, descr=args.description)
            elif command == 'collection':
                cfgids = wds.get_configuration_ids(envid=envid)
                cfgid = wds.get_valid_id_string(args.cfgid, cfgids, strict=True)
                result = wds.create_collection(envid=envid, name=args.name, cfgid=cfgid, description=args.description)
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
        if not (args.delete.lower() in sub_commqnds['delete']):
            print("{0}: invalid argument, '{1}'".format(sys.argv[0], args.delete))
            sys.exit(1)

        command = args.delete.lower()
        if args.envid is not None:
            envid = wds.get_valid_id_string(args.envid, envids, strict=True)
            if command == 'environment':
                result = wds.delete_environment(envid=envid)
            elif command == 'collection':
                colids = wds.get_collections_ids(envid=envid)
                if colids:
                    colid = wds.get_valid_id_string(args.colid, colids, strict=True)
                    result = wds.delete_collection(envid=envid, colid=colid)
                else:
                    print("DELETE: {0}, No collections found?".format(command))
                    sys.exit(1)
            elif command == 'document':
                colids = wds.get_collections_ids(envid=envid)
                if colids:
                    colid = wds.get_valid_id_string(args.colid, colids, strict=True)
                    docids = wds.get_document_ids(envid=envid, colid=colid, count=args.count)

                    if docids:
                        docid = wds.get_valid_id_string(args.docid, docids, strict=True)
                        result = wds.delete_document(envid=envid, colid=colid, docid=docid)
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
        if not (args.query.lower() in sub_commands['query']):
            print("{0}: invalid argument, '{1}'".format(sys.argv[0], args.query))
            sys.exit(1)

        command = args.query.lower()
        if args.envid is not None:
            envid = envids[args.envid]
            if command == 'collection':
                colids = wds.get_collections_ids(envid=envid)
                if colids:
                    colid = wds.get_valid_id_string(args.colid, colids, strict=True)
                    result = wds.query_collection(envid=envid, colid=colid, count=args.count)
                else:
                    print("QUERY: {0}, No collections found?".format(command))
                    sys.exit(1)
            elif command == 'document':
                colids = wds.get_collections_ids(envid=envid)
                if colids:
                    colid = wds.get_valid_id_string(args.colid, colids, strict=True)
                    docids = wds.get_document_ids(envid=envid, colid=colid, count=args.count)

                    if docids:
                        docid = wds.get_valid_id_string(args.docid, docids, strict=True)
                        result = wds.query_document(envid=envid, colid=colid, docid=docid)
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
