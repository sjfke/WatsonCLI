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
            # excel_row = {'Person': [], 'JobTitle': [], 'Company': []}
            excel_row = {}
            for entity in results['enriched_text']['entities']:
                # print "Type: {0}".format(entity['type'])
                # print '[' + str(count) + ']' + entity['type'] + ": " + entity['text']
                if entity['type'] in excel_row:
                    excel_row[entity['type']].append(entity['text'])
                else:   
                    excel_row[entity['type']] = [entity['text']]
                
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
    col_width = char_width * 25

    row = 0
    col = 1
    column_names = []
    
    for index, values in enumerate(data):
        for value in values:
            if not value in column_names:
                column_names.append(value)
   
    for i in range(0, len(column_names)):             
        sheet.col(i).width = col_width
                
    for index, values in enumerate(data):
        
        minrow = row
        maxrow = row
        sheet.write(minrow, 0, "Person" + str(index))
        
        for column_name in column_names:
            col = column_names.index(column_name) + 1
            sheet.write(minrow, col, column_name)
            r = minrow + 1
            if column_name in values:
                for v in values[column_name]:
                    sheet.write(r, col, v)
                    r += 1
                    if r > maxrow:
                        maxrow = r
            else:
                sheet.write(r, col, '')             
                
        row = maxrow + 1
        col = 1

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
    sheetname = src.replace('.json', '')
    dst = args.file.lower().replace('json', 'xls')
    data = extract_data(src=src)
    # print data

    result = write_excel(sheetname=sheetname, data=data, dst=dst)
    # print result

    sys.exit(0)
