#!/usr/bin/env python
#
import argparse
import sys
import os


def call_watson_nlu(cfg):
    import json
    from ConfigParser import SafeConfigParser
    from watson_developer_cloud import NaturalLanguageUnderstandingV1
    from watson_developer_cloud.natural_language_understanding_v1 import Features, CategoriesOptions
    
    config = SafeConfigParser()
    config.read(cfg)

    natural_language_understanding = NaturalLanguageUnderstandingV1(
      username=config.get('watson', 'username'),
      password=config.get('watson', 'password'),
      version=config.get('watson', 'version'))
    
    response = natural_language_understanding.analyze(
      url='www.ibm.com',
      features=Features(
        categories=CategoriesOptions()))
    
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    watson_cfg_file = os.path.join(os.getcwd(), '.watson.cfg')
    parser = argparse.ArgumentParser(description='NLU SDK interface')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-c', '--cfg', default=watson_cfg_file, help='Watson credentials')
    args = parser.parse_args()
    if args.verbose >= 1 :
        print "watson-cfg: " + args.cfg
        
    call_watson_nlu(cfg=args.cfg)
    
    sys.exit(0)
    
