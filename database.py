#
#   Copyright 2015 Kalvin Eng
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
import getpass
import cx_Oracle  # the package used for accessing Oracle in Python
import login
import menu
import bookings
import user
import search


def connect(connection_url):
    menu.clearScreen()
    print("Connect to Airline Booking Database\n")

    # get username
    user = input("Oracle Username: ")
    if not user:
        user = getpass.getuser()

    # get password
    pw = getpass.getpass()

    # The URL we are connnecting to
    conString = '' + user + '/' + pw + connection_url

    print("\nConnecting...\n")

    try:
            # Establish a connection in Python
            connection = cx_Oracle.connect(conString)

            print("Connected!")

            return connection

    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)


def process(option, connection, current_user):
    if option == 0:
        search.search_flights(connection,str(current_user.email))
    if option == 1:
        bookings.list(connection,str(current_user.email))
    if option == 2:
        login.logout(connection, str(current_user.email))
    if option == 3:
        user.record_dep(connection)
    if option == 4:
        user.record_arr(connection)


def cursor(connection = None):
    return connection.cursor()


def close(connection = None, cursor = None):
        # close the connection
        if cursor != None:
            cursor.close()

        if connection !=None:
            connection.close()


def read(query = None, cursor = None):
    if query != None and cursor!= None:
        # read from a table
        cursor.execute(query)
        # get all data and print it
        rows = cursor.fetchall()
        result = list()
        for row in rows:
            for x in row:
                result.append(x)

        return result