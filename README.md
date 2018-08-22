# WDS Simple CLI
Simple Python command line utility for interacting with Watson Bluemix

## Simplistic CLI to Watson Discovery
```shell-session
usage: wds.py [-h] [-A ADD] [-C CREATE] [-D DELETE] [-L LIST] [-U UPDATE]
              [-Q QUERY] [-c COUNT] [-d DESCRIPTION] [-n NAME] [--envid ENVID]
              [--cfgid CFGID] [--colid COLID] [--docid DOCID] [-a AUTH]
              [--raw] [-j] [-y] [-v]

WDS Simplistic CLI interface

optional arguments:
  -h, --help            show this help message and exit
  -A ADD, --add ADD     upload document
  -C CREATE, --create CREATE
                        (environment|collection)
  -D DELETE, --delete DELETE
                        (environment|configuration|collection|document)
  -L LIST, --list LIST  (environment[s]|configuration[s]|collection[s]|documen
                        t[s])
  -U UPDATE, --update UPDATE
                        (environment|configuration|collection|document)
  -Q QUERY, --query QUERY
                        (collection|document)
  -c COUNT, --count COUNT
                        number of documents
  -d DESCRIPTION, --description DESCRIPTION
                        description for create command
  -n NAME, --name NAME  name for create command
  --envid ENVID         environment index
  --cfgid CFGID         configuration index
  --colid COLID         collection index
  --docid DOCID         document index
  -a AUTH, --auth AUTH  Watson credentials file
  --raw                 JSON output
  -j, --json            JSON output
  -y, --yaml            YAML output
  -v, --verbose
