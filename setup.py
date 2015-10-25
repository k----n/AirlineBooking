#
#   Copyright 2015 Kyrylo Shegeda, Kalvin Eng
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import sys

import cx_Oracle  # the package used for accessing Oracle in Python

import database
import menu


def execSQL(sqlFile, cursor):
    f = open(sqlFile)
    full_sql = f.read()
    sql_commands = full_sql.split(';')

    for x in range(0, len(sql_commands)-1):
        cursor.execute(sql_commands[x])


def checkTable(dropTablesfile, cursor):
    '''
    Checks if there are any existing tables that need to be dropped for fresh setup

    '''
    f = open(dropTablesfile)
    sql_commands = f.read()
    sql_commands = sql_commands.split(';')
    table_names = [x.strip() for x in sql_commands]
    table_names = [x.replace("drop table ","").upper() for x in table_names].pop()
    print(table_names)

    count = 0

    cursor.execute("SELECT TABLE_NAME FROM USER_TABLES")
    output_rows = cursor.fetchall()
    output_rows = [''.join(i) for i in output_rows]

    for line in output_rows:
        if line in table_names:
            count +=1

    if count == len(table_names):
        for x in range(0, len(sql_commands)-1):
            cursor.execute(sql_commands[x])


def createTable(mode = 0, connection = None, database_spec = None, drop_tables = None):
    if mode == 1:
        menu.clearScreen()
        print("\nAirline Booking Setup")

        # connect to database
        curs = database.cursor(connection)

        try:
                # drop pre-existing tables
                checkTable(drop_tables, curs)

                # create tables
                execSQL(database_spec, curs)

                connection.commit()

                database.close(None,curs)

                print("Setup Complete\n")

        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print(sys.stderr, "Oracle code:", error.code)
            print(sys.stderr, "Oracle message:", error.message)