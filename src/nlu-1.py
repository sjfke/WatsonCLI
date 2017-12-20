#!/usr/bin/env python
#
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, CategoriesOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username=config.get('watson', 'username'),
  password=config.get('watson', 'password'),
  version=config.get('watson', 'version'))

response = natural_language_understanding.analyze(
  url='www.ibm.com',
  features=Features(
    categories=CategoriesOptions()))

print(json.dumps(response, indent=2))
