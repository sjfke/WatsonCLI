#!/usr/bin/env python3
#
import argparse
import os
import re
import sys


def nlu_get_analyze(cfg, features, url=None, text_file=None):
    """ Perform NLU Analysis based on CLI options (REST + get)

        Args:
            cfg (str): Configuration file with Watson credentials
            url (str): URL to analyze
            text_file (str): File to analyze.

        Returns:
            str: JSON results

    """

    import json
    import requests
    from ConfigParser import SafeConfigParser

    config = SafeConfigParser()
    config.read(cfg)

    if not url and not text_file:
        print('Missing url of text_file')
        sys.exit(1)

    payload = {'version': config.get('nlu', 'version'), 'features': features}

    if text_file:
        # TODO - load file and add to 'text'
        with open(text_file, 'r') as f:
            text_str = f.read()

        if text_str and re.match('DOCTYPE', text_str, re.IGNORECASE):
            payload['html'] = text_str
        elif text_str:
            payload['text'] = text_str

    if url:
        # url and (html|text) are mutually exclusive
        payload['url'] = url
        if 'text' in payload:
            del payload['text']
        if 'html' in payload:
            del payload['html']

    # curl --user "watson-user":"watson-password"\
    # "https://gateway.watsonplatform.net/natural-languag-understanding/api/v1/analyze?version=2017-02-27&url=www.ibm.com&features=sentiment,keywords"
    # request.get('https://api.github.com/user/', auth=('user', 'pass'))
    api = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze"
    wuser = config.get('nlu', 'username')
    wpass = config.get('nlu', 'password')

    r = requests.get(api, params=payload, auth=(wuser, wpass))
    if args.verbose >= 1:
        if text_file is None:
            print('URL: ' + url)
        else:
            print('File: ' + text_file)

        print('Request: ' + r.url)

    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
    return r.text


def cleanse_features(feature_str):
    """ Return only valid Watson features

        Args:
            feature_str (str): feature string to check

        Returns:
            str: a cleansed or default string
    """

    allowed = set(['entities', 'keywords', 'concepts', 'emotion', 'metadata', 'relations', 'semantic_roles', 'sentiment'])
    result_str = 'sentiment,keywords'

    if feature_str:
        features = feature_str.split(',')
        matched = []

        for feature in features:
            if feature.lower in allowed:
                matched.append(feature.lower)

        if len(matched) >= 1:
            result_str = ','.join(matched)
        else:
            print("Warning: Using Default Features '{0}'".format(result_str))

    if args.verbose >= 1:
        print('result_str: ' + result_str)

    return result_str


def nlu_post_analyze_json(cfg, url=None, json_file=None, text_file=None):
    """ Perform NLU Analysis based on JSON file (REST + post)

        Args:
            cfg (str): Configuration file with Watson credentials
            url (str): URL to analyze (over-rides JSON file)
            json_file (str): Analysis Query in JSON format
            text_file (str): Text file to analyze (over-ride JSON file)

        Returns:
            str: JSON results

    """
    import json
    import requests
    from ConfigParser import SafeConfigParser

    config = SafeConfigParser()
    config.read(cfg)

    if json_file is None:
        print('Missing JSON file')
        sys.exit(1)

    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except ValueError as e:
            print("{0}:".format(json_file))
            print("   ValueError: {0}".format(e))
            sys.exit(1)
        except:
            print("{0}:".format(json_file))
            print("   Unexpected error: ", sys.exc_info()[0])
            sys.exit(1)

    if not data:
        print("{0}:".format(json_file))
        print("   File has no JSON content")
        sys.exit(1)

    if text_file:
        # TODO - load file and add to 'text'
        with open(text_file, 'r') as f:
            text_str = f.read()

        if text_str and re.match('DOCTYPE', text_str, re.IGNORECASE):
            data['html'] = text_str
            if 'text' in data:
                del data['text']
        elif text_str:
            data['text'] = text_str
            if 'html' in data:
                del data['html']

        # url and (html|text) are mutually exclusive
        if 'url' in data:
            del data['url']

    if url:
        # url and (html|text) are mutually exclusive
        data['url'] = url
        if 'text' in data:
            del data['text']
        if 'html' in data:
            del data['html']

    api = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze"
    wuser = config.get('nlu', 'username')
    wpass = config.get('nlu', 'password')
    data['version'] = config.get('nlu', 'version')

    r = requests.post(api, json=data, auth=(wuser, wpass))
    if args.verbose >= 1:
        print('File: ' + json_file)
        print('Request: ' + r.url)

    # print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    # print(r.text)
    return r.text


if __name__ == "__main__":
    watson_cfg_file = os.path.join(os.getcwd(), '.watson.cfg')
    parser = argparse.ArgumentParser(description='NLU REST interface')
    parser.add_argument('-c', '--cfg', default=watson_cfg_file, help='Watson credentials')
    parser.add_argument('-f', '--features', default='sentiment,keywords', help='Watson features')
    parser.add_argument('-F', '--filename', default=None, help='text file to analyze')
    parser.add_argument('-u', '--url', default=None, help="URL to analyze")
    parser.add_argument('-j', '--json', default=None, help="JSON parameters")
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    if args.verbose >= 1:
        print("watson-cfg: '{0}'".format(args.cfg))

    if args.json:
        result = nlu_post_analyze_json(cfg=args.cfg, url=args.url, json_file=args.json, text_file=args.filename)
        print(result)
    else:
        features = cleanse_features(args.features)  # may enforce default 'sentiment,keywords'
        result = nlu_get_analyze(cfg=args.cfg, url=args.url, text_file=args.filename, features=features)
        print(result)

    sys.exit(0)
