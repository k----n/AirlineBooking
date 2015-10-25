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

import getpass  # the package for getting password from user without displaying it
import database
import cx_Oracle

def login(connection):
    cursor = database.cursor(connection)
    check = "n"

    print("Login to Airline Booking System\n")

    email = input("Email: ")

    data = database.read("SELECT email FROM USERS", cursor)

    if email not in data:
        check = input("User does not exist...\nEnter 'y' to create user: ")

    while True:
        if check == "y":
            password = getpass.getpass()
            createUser(email, password, cursor)
            break

    #database.read("SELECT email FROM USERS", cursor)

    database.close(cursor)


def createUser(email, password, cursInsert):
    data = [(email, password)]
    cursInsert.bindarraysize = 1
    cursInsert.setinputsizes(20,4)
    cursInsert.executemany("INSERT INTO USERS(email, pass) "
                                       "VALUES (:1, :2)", data)