#!/usr/bin/env python3
#
import argparse
import json
import os

import sys

import yaml

from CommandObject import CommandObject
from WDSObject import WDSObject


#===============================================================================
# print_result
#===============================================================================
def print_result(result, format='JSON', title=None, callback=None):
    '''
    Print result (string, list) in JSON, YAML or TEXT (callback) format
    :param result: the result (JSON) string to display
    :param format: JSON, YAML, TEXT (use callback)
    :param title: text heading
    :param callback: custom printing routine
    '''
    if result is None:
        if verbose >= 1:
            print("print_result: 'string' is None")
        return

    if title:
        print(title)

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
# list_environments
#===============================================================================
def list_environments(result, title="Environments:"):
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
# list_configurations
#===============================================================================
def list_configurations(result, title="Configurations:"):
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
# list_collections
#===============================================================================
def list_collections(result, title="Collections:"):
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
# list_documents
#===============================================================================
def list_documents(result, title="Documents:"):
    '''
    Print Documents List
    :param result: Configurations text or object to print
    :param title: Title string
    '''

    values = result
    if isinstance(result, str):
        values = json.loads(result)

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
                print("  filename: ", end='')
                print(val['extracted_metadata']['filename'])
            if 'file_type' in val['extracted_metadata']:
                print("  file_type: ", end='')
                print(val['extracted_metadata']['file_type'])
            if 'publicationdate' in val['extracted_metadata']:
                print("  publicationdate: ", end='')
                print(val['extracted_metadata']['publicationdate'])
            if 'sha1' in val['extracted_metadata']:
                print("  sha1: ", end='')
                print(val['extracted_metadata']['sha1'])

        if 'result_metadata' in val:
            if 'score' in val['result_metadata']:
                print("  score: {0[score]}".format(val['result_metadata']))

        print

    print("Showing {0} out of {1} documents".format(len(values['results']), document_count))

    return None


#===============================================================================
# list_environment
#===============================================================================
def list_environment(result, title="Environment:"):
    '''
    Print the Environment
    :param result: Configurations text or object to print
    :param title: Title string
    '''
    print(title + os.linesep + ("=" * len(title)))

    # simple Wrapper YAML output
    print_result(result=result, format='YAML')


#===============================================================================
# list_configuration
#===============================================================================
def list_configuration(result, title="Configuration:"):
    '''
    Print the Configuration
    :param result: Configurations text or object to print
    :param title: Title string
    '''
    print(title + os.linesep + ("=" * len(title)))

    # simple Wrapper YAML output
    print_result(result=result, format='YAML')


#===============================================================================
# list_collection
#===============================================================================
def list_collection(result, title="Collection:"):
    '''
    Print the Collection
    :param result: Configurations text or object to print
    :param title: Title string
    '''
    print(title + os.linesep + ("=" * len(title)))

    # simple Wrapper YAML output
    print_result(result=result, format='YAML')


#===============================================================================
# list_document
#===============================================================================
def list_document(result, title="Document:"):
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

    cmd = CommandObject(args)
    if not cmd.validate(wds=wds):
        print("ERROR: failed to execute '{0}'".format(cmd.command_name))
        sys.exit(1)

    result = cmd.execute(wds=wds)
    title = None
    if cmd.output_format == 'TEXT':
        if cmd.envid_str:
            title = "EnvID: {0}".format(cmd.envid_str)

        if cmd.command_name in {'create_environment', 'create_collection', 'delete_collection', 'delete_document', 'query_collection', 'query_document'}:
            print_result(result=result, title=title, format='YAML')
        else:
            print_result(result=result, title=title, callback=eval(cmd.command_name))
    else:
        print_result(result=result, title=title, format=cmd.output_format)

    sys.exit(0)
