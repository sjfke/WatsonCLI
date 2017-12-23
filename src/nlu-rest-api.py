#!/usr/bin/env python
#
import argparse
import sys
import os


def call_watson_nlu(cfg):
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
    payload = {'version': '2017-02-27', 'url': 'www.ibm.com', 'features': 'sentiment,keywords'}
    r = requests.get(api, params=payload, auth=(wuser, wpass))
    if args.verbose >= 1:
        print(r.url)
            
    print(json.dumps(r.text, indent=2))


if __name__ == "__main__":
    watson_cfg_file = os.path.join(os.getcwd(), '.watson.cfg')
    parser = argparse.ArgumentParser(description='Simple NLU Category example')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-c', '--cfg', default=watson_cfg_file, help='Watson credentials')
    args = parser.parse_args()
    if args.verbose >= 1 :
        print "watson-cfg: " + args.cfg
        
    call_watson_nlu(cfg=args.cfg)
    
    sys.exit(0)
    
