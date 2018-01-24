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

    extracted_data = {'entities': [], 'concepts': [], 'keywords': [], 'categories': []}
    with open(src) as f:
        data = json.loads(f.read())
        count = 0
        for results in data['results']:
            for enrichment_type in results['enriched_text']:

                if enrichment_type == 'entities':
                    dict = {}
                    for enrichment in results['enriched_text']['entities']:
                        if enrichment['type'] in dict:
                            dict[enrichment['type']].append((enrichment['text'], enrichment['relevance']))
                        else:
                            dict[enrichment['type']] = [(enrichment['text'], enrichment['relevance'])]

                    if dict:
                        extracted_data['entities'].append(dict)

                elif enrichment_type == 'concepts':
                    dict = {}
                    for enrichment in results['enriched_text']['concepts']:
                        dict[enrichment['text']] = enrichment['relevance']

                    if dict:
                        extracted_data['concepts'].append(dict)

                elif enrichment_type == 'keywords':
                    dict = {}
                    for enrichment in results['enriched_text']['keywords']:
                        dict[enrichment['text']] = enrichment['relevance']

                    if dict:
                        extracted_data['keywords'].append(dict)

                elif enrichment_type == 'categories':
                    dict = {}
                    for enrichment in results['enriched_text']['categories']:
                        dict[enrichment['label']] = enrichment['score']

                    if dict:
                        extracted_data['categories'].append(dict)

        return extracted_data

    return None


#===============================================================================
# write_excel
#===============================================================================
def write_excel(dst, data):
    '''
    Write extracted data to Excel
    :param dst: destination filename
    :param data: data object
    '''
    import xlwt

    wb = xlwt.Workbook()
    sheet = wb.add_sheet('Entities')

    # https://buxty.com/b/2011/10/widths-heights-with-xlwt-python/
    char_width = 256
    col_width = char_width * 25

    row = 0
    col = 1
    column_names = []

    for index, values in enumerate(data['entities']):
        for value in values:
            if not value in column_names:
                column_names.append(value)

    for i in range(0, len(column_names)):
        sheet.col(i).width = col_width

    for index, values in enumerate(data['entities']):

        minrow = row
        maxrow = row
        sheet.write(minrow, 0, "Person" + str(index))

        col = 1
        for column_name in column_names:
            sheet.write(minrow, col, column_name)
            sheet.write(minrow, col + 1, 'Relevance')
            r = minrow + 1
            if column_name in values:
                for v in values[column_name]:
                    sheet.write(r, col, v[0])
                    sheet.write(r, col + 1, v[1])
                    r += 1
                    if r > maxrow:
                        maxrow = r
            col += 2

        row = maxrow + 1
        col = 1

    sheet = wb.add_sheet('Concepts')
    for i in range(0, 2):
        sheet.col(i).width = col_width

    sheet.write(0, 0, "Text")
    sheet.write(0, 1, "Relevance")
    row = 1
    col = 0
    for index, values in enumerate(data['concepts']):
        for key in values:
            sheet.write(row, 0, key)
            sheet.write(row, 1, values[key])
            row += 1

    sheet = wb.add_sheet('Keywords')
    for i in range(0, 2):
        sheet.col(i).width = col_width

    sheet.write(0, 0, "Text")
    sheet.write(0, 1, "Relevance")
    row = 1
    col = 0
    for index, values in enumerate(data['keywords']):
        for key in values:
            sheet.write(row, 0, key)
            sheet.write(row, 1, values[key])
            row += 1

    sheet = wb.add_sheet('Categories')
    for i in range(0, 2):
        sheet.col(i).width = col_width

    sheet.write(0, 0, "Label")
    sheet.write(0, 1, "Score")
    row = 1
    col = 0
    for index, values in enumerate(data['categories']):
        for key in values:
            sheet.write(row, 0, key)
            sheet.write(row, 1, values[key])
            row += 1

    # return json.dumps(data)
    wb.save(dst)


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
    dst = args.file.lower().replace('json', 'xls')
    data = extract_data(src=src)
    # print data
    # sys.exit(0)

    result = write_excel(data=data, dst=dst)
    # print result

    sys.exit(0)
