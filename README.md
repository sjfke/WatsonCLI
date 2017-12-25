# WatsonCLI
Collection of Python command line utilities for interacting with Watson Bluemix

## Natural Language (REST)
```shell-session
usage: nlu-rest-api.py [-h] [-c CFG] [-f FEATURES] [-F FILENAME] [-u URL]
                       [-j JSON] [-v]

Simple NLU Category example

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

Simple NLU Category example

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose
  -c CFG, --cfg CFG  Watson credentials
```
