#!/usr/bin/env python

#
# place-all-images-from-dir-into-database.py
#
# Exports a directory full of font awesome icons into database.
#
# Copyright (c) 2014-2014 Andrew Allbright (http://andrewallbright.com)
#
#  - http://andrewallbright.com
#

import sys, argparse, re, mysql.connector, glob, os

# Support Unicode literals with both Python 2 and 3
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]

    def uchr(x):
        return unichr(x)
else:
    def u(x):
        return x

    def uchr(x):
        return chr(x)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description="Puts in all font awesome icons PNGs into database")

    parser.add_argument("--username", type=str, default="",
            help="Database username")
    parser.add_argument("--password", type=str, default="",
            help="Database user password")
    parser.add_argument("--host", type=str, default="localhost",
            help="Connect to host of database (default localhost)")
    parser.add_argument("--database", type=str, default="test",
            help="Connect to database (default test)")
    parser.add_argument("--directory", type=str, default="images",
            help="read this directory (default directory)")
    parser.add_argument("--table", type=str, default="Images",
            help="Table you are injecting the data into (default Images)")
    # parser.add_argument("--table_schema", type=str, default="name, filepath_16, filepath_24, filepath_32, filepath_64",
    parser.add_argument("--table_schema", type=str, default="name, color, 32_filepath, 48_filepath, 64_filepath",
            help="Schema of the table you are inserting into (default )")
    parser.add_argument("--sql", type=str, default="show tables;",
            help="SQL statement")




    args = parser.parse_args()

    username     = args.username
    password     = args.password
    host         = args.host
    database     = args.database
    directory    = args.directory
    table        = args.table
    table_schema = args.table_schema
    sql          = args.sql

    # Inserts into table a table schema (a list) with values to be determined
    cnx = mysql.connector.connect(user     = username, 
                                  password = password,
                                  host     = host,
                                  database = database)
    print("\ndatabase connection established")

    add_image = ("INSERT INTO " + table + " "
                 "(" + table_schema + ") "
                 "VALUES (" + (", ".join(str("'%s' " * len(table_schema.split())).split())) + ")")
    print("\nSQL template: %s" % add_image)
    # OS change directory to target
    os.chdir(directory)
    # Create list of objects with filename and file size
    file_list = []
    for file in glob.glob("*.png"):
        template, filesize, color, filename = file.split("_")
        filename = filename.replace('.png', '')
        found = False
        for data_structure in file_list:
            if data_structure['name'] == filename:
                found = True
                data_structure[filesize+'_filepath'] = directory + '/' + file
        if not found:
            file_list.append({'name'               : filename, 
                              'color'              : color,
                              filesize+'_filepath' : directory + '/' + file})
    
    cursor = cnx.cursor()
    for data_structure in file_list:
        print(add_image % (data_structure['name'], data_structure['color'], data_structure['32_filepath'], data_structure['48_filepath'], data_structure['64_filepath']))
        cursor.execute(add_image % (data_structure['name'], data_structure['color'], data_structure['32_filepath'], data_structure['48_filepath'], data_structure['64_filepath']))
    cnx.commit()
    cursor.close()
    cnx.close()

    print("\n\nScript Complete!")    
