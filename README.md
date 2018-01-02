# WatsonCLI
Collection of Python command line utilities for interacting with Watson Bluemix

## Discovery (REST)
```shell-session
usage: discovery-rest-api.py [-h] [-C CREATE] [-D DELETE] [-L LIST]
                             [-U UPDATE] [-d DESCRIPTION] [-n NAME]
                             [--envid ENVID] [--cfgid CFGID] [--colid COLID]
                             [--docid DOCID] [-a AUTH] [--raw] [-s SEPARATOR]
                             [-v]

Discovery REST interface

optional arguments:
  -h, --help            show this help message and exit
  -C CREATE, --create CREATE
                        (environment|collection)
  -D DELETE, --delete DELETE
                        (environment|configuration|collection|document)
  -L LIST, --list LIST  (environment[s]|configuration[s]|collection[s]|documen
                        t[s])
  -U UPDATE, --update UPDATE
                        (environment|configuration|collection|document)
  -d DESCRIPTION, --description DESCRIPTION
                        description for create command
  -n NAME, --name NAME  name for create command
  --envid ENVID         environment index
  --cfgid CFGID         configuration index
  --colid COLID         collection index
  --docid DOCID         document index
  -a AUTH, --auth AUTH  Watson credentials file
  --raw                 JSON output
  -s SEPARATOR, --separator SEPARATOR
                        field delimiter
  -v, --verbose
```
## Natural Language (REST)
```shell-session
usage: nlu-rest-api.py [-h] [-c CFG] [-f FEATURES] [-F FILENAME] [-u URL]
                       [-j JSON] [-v]

NLU REST interface

optional arguments:
  -h, --help            show this help message and exit
  -c CFG, --cfg CFG     Watson credentials
  -f FEATURES, --features FEATURES
                        Watson features
  -F FILENAME, --filename FILENAME
                        text file to analyze
  -u URL, --url URL     URL to analyze
  -j JSON, --json JSON  JSON parameters
  -v, --verbose
```
## Natural Language (SDK)
```shell-session
usage: nlu-sdk.py [-h] [-v] [-c CFG]

NLU SDK interface

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose
  -c CFG, --cfg CFG  Watson credentials
[osboxes@osboxes src]$ ./nlu-sdk.py -h
usage: nlu-sdk.py [-h] [-v] [-c CFG]

NLU SDK interface

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose
  -c CFG, --cfg CFG  Watson credentials
```
