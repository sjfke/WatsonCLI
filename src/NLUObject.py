#!/usr/bin/env python3
import sys
import json
import yaml
import requests
import os
import logging
from WDSAccess import WDSAccess

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.ERROR)


class NLUObject(WDSAccess):
    '''
    Simplistic access to IBM Watson Natural Language Understanding
    '''

    def __init__(self, filename, url='https://gateway.watsonplatform.net/natural-language-understanding/api/v1', version='2017-02-27'):
        super().__init__(filename)
        super().set_url(url)
        super().set_version(version)

    #===========================================================================
    # analyze
    #===========================================================================
    def analyze(self, query, source='TEXT', format='JSON', verbose=0):
        """
        Watson Natutal Langugage Analyze method
        :param query: JSON format query parameters
        :param source: 'TEXT', 'FILE', 'URL'
        :param format: output result format JSON or YAML
        :param verbose: reporting level
        """
        __valid_source = ['TEXT', 'FILE', 'URL']
        __valid_format = ['JSON', 'YAML']

        if not source in __valid_source:
            logger.critical("{0}: invalid source ({2}), {1}".format('analyze', source, __valid_source))
            return None

        if not format in __valid_format:
            logger.critical("{0}: invalid format ({2}), {1}".format('analyze', format, __valid_format))
            return None

        # api = super().get_url() + '/analyze' + '?version=' + super().get_version()
        api = self.url + '/analyze' + '?version=' + self.version

        if source == 'TEXT':
            logger.critical("{0}: Not Yet Implemented".format(source))
            return None
        elif source == 'URL':
            logger.critical("{0}: Not Yet Implemented".format(source))
            return None
        elif source == 'FILE':
            try:
                data = json.loads(query)
                r = requests.post(api, json=data, auth=(self.username, self.password))

                if verbose >= 1:
                    print("POST: {0}".format(r.url))
                    print("JSON: {0}".format(data))

                logging.debug("POST: {0}".format(r.url))
                logging.debug("JSON: {0}".format(data))

                # https://github.com/requests/requests/blob/master/requests/status_codes.py
                if r.status_code == requests.codes.ok or r.status_code == requests.codes.created:
                    if isinstance(r.text, str):
                        values = json.dumps(json.loads(r.text), sort_keys=True, indent=4, separators=(',', ': '))
                    else:
                        values = json.dumps(r.text, sort_keys=True, indent=4, separators=(',', ': '))

                    if format == 'YAML':
                        return yaml.safe_dump(json.loads(values), default_flow_style=False)
                    else:
                        return values
                else:
                    logging.critical("Analyze query Failed: {0}".format(r.status_code))
                    return None
            except ConnectionError as e:
                logging.critical("DNS failure, or connection refused: '{0}'".format(e.message))
                return None
            except ValueError as e:
                logging.critical("JSON: '{0}' ({1})".format(e.message, query))
                return None
        else:
            return None

    def list_models(self, format='JSON', verbose=0):
        '''
        List all the available models
        :param format: output result format JSON or YAML
        :param verbose: reporting level
        '''
        __valid_format = ['JSON', 'YAML']

        if not format in __valid_format:
            logger.critical("{0}: invalid format ({2}), {1}".format('list_models', format, __valid_format))
            return None

        # curl -G -u "{username}":"{password}" "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/models?version=2017-02-27"
        api = self.url + '/models'
        payload = {}
        payload['version'] = self.version

        try:
            r = requests.get(api, params=payload, auth=(self.username, self.password))
            if verbose >= 1:
                print("GET: {0}".format(r.url))

            logging.debug("GET: {0}".format(r.url))

            if r.status_code != requests.codes.ok:
                logging.error("{0}: {1}".format('list_models', r.status_code))
                return None
            else:
                if isinstance(r.text, str):
                    values = json.dumps(json.loads(r.text), sort_keys=True, indent=4, separators=(',', ': '))
                else:
                    values = json.dumps(r.text, sort_keys=True, indent=4, separators=(',', ': '))

                if format == 'YAML':
                    return yaml.safe_dump(json.loads(values), default_flow_style=False)
                else:
                    return values

        except ConnectionError as e:
            logging.critical("DNS failure, or connection refused: '{0}'".format(e.message))
            return None
