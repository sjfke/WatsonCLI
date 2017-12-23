#!/usr/bin/env python
#
import argparse
import sys
import os


def simple_nlu_analyse(cfg, url='www.ibm.com', filename=None):
    import json
    import requests
    from ConfigParser import SafeConfigParser

    config = SafeConfigParser()
    config.read(cfg)

    # curl --user "watson-user":"watson-password"\
    # "https://gateway.watsonplatform.net/natural-languag-understanding/api/v1/analyze?version=2017-02-27&url=www.ibm.com&features=sentiment,keywords"
    # request.get('https://api.github.com/user/', auth=('user', 'pass'))
    api = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze"
    wuser = config.get('watson', 'username')
    wpass = config.get('watson', 'password')
    payload = {'version': '2017-02-27', 'url': url, 'features': 'sentiment,keywords'}
    r = requests.get(api, params=payload, auth=(wuser, wpass))
    if args.verbose >= 1:
        if filename is None:
            print('URL: ' + url)
        else:
            print('File: ' + filename)
            
        print('Request: ' + r.url)

    #print(json.dumps(r.text, sort_keys=True, indent=2, separators=(',', ': ')))
    print(r.text)



def nlu_json_analyse(cfg, url='www.ibm.com', filename=None):
    import json
    import requests
    from ConfigParser import SafeConfigParser

    config = SafeConfigParser()
    config.read(cfg)

    pass


if __name__ == "__main__":
    watson_cfg_file = os.path.join(os.getcwd(), '.watson.cfg')
    parser = argparse.ArgumentParser(description='Simple NLU Category example')
    parser.add_argument('-c', '--cfg', default=watson_cfg_file, help='Watson credentials')
    parser.add_argument('-f', '--filename', default=None, help='text file to analyze')
    parser.add_argument('-u', '--url', default='www.ibm.com', help="URL to analyze")
    parser.add_argument('-j', '--json', default=None, help="JSON parameters")
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    if args.verbose >= 1:
        print "watson-cfg: " + args.cfg

    if args.json:
        nlu_json_analyse(cfg=args.cfg, url=args.url, filename=args.filename)
    else:
        simple_nlu_analyse(cfg=args.cfg, url=args.url, filename=args.filename)

    sys.exit(0)
