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

import database
import login

import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it






def search(connection):
    # specifying a case insensitive sort
    cursor.execute("alter session set NLS_COMP=LINGUISTIC")
    cursor.execute("ALTER SESSION SET NLS_SORT=BINARY_CI")
    #cursor = database.cursor(connection)
    source = str(input("Please enter a source: "))
    destination = str(input("Please enter a destination: "))
    #departure_date= input("Please enter a departure date: ")

    #search_query = "select "+source+" "+destination+" "+departure_date+" from airports"
    #search_query = "select "+source+" "+destination+" from airports"

    search_query = "select acode, name, city from airports where acode='"+source+"' or acode='"+destination+"\
    'or name like '%"+source+"%' or name like '%"+destination+"%\
    'or city like '%"+source+"%' or city like '%"+destination+"%'"
    #print (search_query)
    cursor.execute(search_query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# get username
user = input("Username [%s]: " % getpass.getuser())
if not user:
	user=getpass.getuser()

# get password
pw = getpass.getpass()

# The URL we are connnecting to
conString=''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'

# Establish a connection in Python
connection = cx_Oracle.connect(conString)

# create a cursor
cursor= connection.cursor()

search(cursor)