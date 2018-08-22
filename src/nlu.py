#!/usr/bin/env python3
#
import argparse
import json
import os
import sys

import yaml

from NLUObject import NLUObject


#===============================================================================
# delete_model
#===============================================================================
def delete_model(nlu, model, yaml_format=False, verbose=0):
    '''
    Delete the specified Model
    :param nlu: NLU Object
    :param model: Model to delete
    :param yaml_format: YAML rather than JSON
    :param verbose: messages
    '''
    logging.critical("{0}: not yet implemented".format('delete_model'))
    return None

#===============================================================================
# list_models
#===============================================================================


def list_models(nlu, yaml_format, verbose):
    '''
    List the Available Models
    :param nlu: NLU Object
    :param yaml_format: YAML rather than JSON
    :param verbose: messages
    '''
    format = 'JSON'
    if yaml_format:
        format = 'YAML'

    return nlu.list_models(format=format, verbose=verbose)

    logging.critical("{0}: not yet implemented".format('list_models'))
    return None

#===============================================================================
# analyze_url
#===============================================================================


def analyze_url(nlu, query, url, yaml_format, verbose):
    '''
    Perform POST Analyze
    :param nlu: NLU Object
    :param query: JSON request filename
    :param url: insert or replace URL in JSON query
    :param yaml_format: YAML rather than JSON
    :param verbose: messages
    '''
    format = 'JSON'
    if yaml_format:
        format = 'YAML'

    with open(query) as f:
        try:
            data = json.loads(f.read())
            if url:
                data['url'] = str(url)

            if verbose >= 2:
                print(data)

            result = nlu.analyze(query=json.dumps(data), source='FILE', format=format, verbose=verbose)
            return result
        except ValueError as e:
            logging.critical("JSON: '{0}' ({1})".format(e.message, query))
            return None

    logging.critical("{0}: not yet implemented".format('post_analyze'))
    return None

#===============================================================================
# analyze_text
#===============================================================================


def analyze_text(nlu, query, text, yaml_format, verbose):
    '''
    Perform GET Analyze on the Supplied text
    :param nlu: NLU Object
    :param query: JSON request filename
    :param text: String to analyze
    :param yaml_format: YAML rather than JSON
    :param verbose: messages
    '''
    format = 'JSON'
    if yaml_format:
        format = 'YAML'

    with open(query) as f:
        try:
            data = json.loads(f.read())
            if 'url' in data:
                del data['url']

            data['text'] = str(text)

            if verbose >= 2:
                print(data)

            result = nlu.analyze(query=json.dumps(data), source='FILE', format=format, verbose=verbose)
            return result
        except ValueError as e:
            logging.critical("JSON: '{0}' ({1})".format(e.message, query))
            return None
    logging.critical("{0}: not yet implemented".format('analyze_text'))
    return None


#===============================================================================
# https://www.ibm.com/watson/developercloud/natural-language-understanding/api/v1/
# https://console.bluemix.net/docs/services/natural-language-understanding/getting-started.html#getting-started-tutorial
# https://console.bluemix.net/docs/services/natural-language-understanding/categories.html#categories-hierarchy
# https://console.bluemix.net/docs/services/natural-language-understanding/detectable-languages.html#detectable-languages
# __main__
#===============================================================================
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='NLU Simplistic CLI interface')
    parser.add_argument('-F', '--file-mode', help='Local file', default=False, action='store_true')
    parser.add_argument('-D', '--delete-model', help='Delete Custom Model')
    parser.add_argument('-L', '--list-models', help='List Custom Model(s)', default=False, action='store_true')
    parser.add_argument('-a', '--auth', default=None, help='Watson credentials file')
    parser.add_argument('-q', '--query', default='parameter.json', help='NLU Query (JSON format)')
    parser.add_argument('-u', '--url', help='supercede URL in query', default=None)
    parser.add_argument('-y', '--yaml', help='YAML output', default=False, action='store_true')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    # https://docs.python.org/dev/library/argparse.html#nargs
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()

    if args.verbose >= 1:
        print("args: {0}".format(args.__str__()))

    cfg_file = os.path.join(os.getcwd(), '.watson.json')
    if args.auth:
        cfg_file = args.auth

    try:
        nlu = NLUObject(cfg_file)
    except FileNotFoundError as e:
        print("{0}".format(e))
        sys.exit(1)

    if args.delete_model:
        result = delete_model(nlu=nlu, model=args.delete_model, yaml_format=args.yaml, verbose=args.verbose)
        print(result)
    elif args.list_models:
        result = list_models(nlu=nlu, yaml_format=args.yaml, verbose=args.verbose)
        print(result)
    elif args.file_mode:
        data = args.infile.read()
        result = analyze_text(nlu=nlu, query=args.query, text=data, yaml_format=args.yaml, verbose=args.verbose)
        print(result)
    else:
        result = analyze_url(nlu=nlu, query=args.query, url=args.url, yaml_format=args.yaml, verbose=args.verbose)
        print(result)

    sys.exit(0)
