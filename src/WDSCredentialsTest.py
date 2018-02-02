#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from WDSCredentials import WDSCredentials

if __name__ == "__main__":

    wds = WDSCredentials('.gc.watson.json')
    print "JSON:"
    print wds.credentials()
    print "username: {0}".format(wds.username())
    print "password: {0}".format(wds.password())
    print "url: {0}".format(wds.url())
    print "version: {0}".format(wds.version())
    print

    wds = WDSCredentials('.gc.watson.cfg')
    print wds.credentials()
    print "username: {0}".format(wds.username())
    print "password: {0}".format(wds.password())
    print "url: {0}".format(wds.url())
    print "version: {0}".format(wds.version())

    sys.exit(0)
