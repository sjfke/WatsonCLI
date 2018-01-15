#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import argparse
import codecs
import os
import re
import sys
import json

# http://pythonhosted.org/kitchen/unicode-frustrations.html
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


#===============================================================================
# extract_data
#===============================================================================
def extract_data(src):
    '''
    Extract data from discovery JSON
    :param src: source filename
    '''
    # print "SRC: {0}".format(src)
    # print "DST: {0}".format(dst)

    extracted_data = []
    with open(src) as f:
        data = json.loads(f.read())
        count = 0
        for results in data['results']:
            excel_row = {'Person': [], 'JobTitle': [], 'Company': []}
            for entity in results['enriched_text']['entities']:
                # print "Type: {0}".format(entity['type'])
                if entity['type'] in ["JobTitle", "Company", "Person"]:
                    # print '[' + str(count) + ']' + entity['type'] + ": " + entity['text']
                    excel_row[entity['type']].append(entity['text'])
            count += 1
            extracted_data.append(excel_row)

        return extracted_data

    return None


#===============================================================================
# write_excel
#===============================================================================
def write_excel(sheetname, dst, data):
    '''
    Write extracted data to Excel
    :param sheetname: tab description
    :param dst: destination filename
    :param data: data object
    '''
    import xlwt

    wb = xlwt.Workbook()
    sheet = wb.add_sheet(sheetname)

    # https://buxty.com/b/2011/10/widths-heights-with-xlwt-python/
    char_width = 256
    sheet.col(1).width = char_width * 30
    sheet.col(2).width = char_width * 50
    sheet.col(3).width = char_width * 40

    row = 0
    for index, d in enumerate(data):
        minrow = row
        maxrow = row
        sheet.write(minrow, 0, "Person" + str(index))
        if 'Person' in d:
            r = minrow
            for p in d['Person']:
                sheet.write(r, 1, p)
                r += 1
                if r > maxrow:
                    maxrow = r
        else:
            sheet.write(row, 1, '')

        if 'JobTitle' in d:
            r = minrow
            for jt in d['JobTitle']:
                sheet.write(r, 2, jt)
                r += 1
                if r > maxrow:
                    maxrow = r
        else:
            sheet.write(row, 2, '')

        if 'Company' in d:
            r = minrow
            for c in d['Company']:
                sheet.write(r, 3, c)
                r += 1
                if r > maxrow:
                    maxrow = r
        else:
            sheet.write(row, 3, '')

        row = maxrow + 1

    # return json.dumps(data)
    wb.save(dst)
    return None


#===============================================================================
# https://www.ibm.com/watson/developercloud/discovery/api/v1/
# https://console.bluemix.net/docs/services/discovery/getting-started.html#getting-started-with-the-api
# __main__
#===============================================================================
if __name__ == "__main__":
    watson_cfg_file = os.path.join(os.getcwd(), '.watson.cfg')
    parser = argparse.ArgumentParser(description='Mickey Mouse JSON to Excel')
    parser.add_argument("file", help="JSON text file to load")
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()

    src = args.file.lower()
    sheetname = src.replace('.json', '')
    dst = args.file.lower().replace('json', 'xls')
    data = extract_data(src=src)

    result = write_excel(sheetname=sheetname, data=data, dst=dst)
    print result

    sys.exit(0)
