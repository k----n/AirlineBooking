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
import sys

import database
import user
import verify
import menu


#TODO comment

def login(connection):
    cursor = database.cursor(connection)

    current_user = user.User()

    menu.clearScreen()
    print(
        "Login to Airline Booking System\n" +
        "-------------------------\n" +
        "Select an option:\n\n" +
        "0 - Login\n" +
        "1 - Create Account\n" +
        "2 - Exit\n" +
        "-------------------------"
        )

    entries = [x for x in range(3)]
    while True:
        option = input("\nOption: ")

        if option == "0":
            email = ""
            password = ""
            while not(verify.char20(email)):
                email = input("\nEmail: ").strip().lower()
                if not(verify.char20(email)):
                    print("Invalid Email Length, Try Again")

            while not(verify.char4(password)):
                password = getpass.getpass("Password: ")
                if not(verify.char4(password)):
                    print("Invalid Password length, Try Again")

            query = "SELECT count(*) from users where email = '{}' and pass = '{}'".format(email,password)

            valid = database.read(query, cursor)

            if valid[0]:
                current_user.email = email
                break
            else:
                print("Incorrect email/pass!")

        elif option == "1":
            query = "SELECT email FROM USERS"
            users = database.read(query, cursor)

            email = ""
            password = ""
            while True:
                email = input("\nNew Email: ").strip().lower()
                if not(verify.char20(email)):
                    print("Invalid Email Length, Try Again")

                elif email.ljust(20) in users:
                    print("User already exists, Try Again")

                else:
                    break

            while not(verify.char4(password)):
                password = getpass.getpass("New Password: ")
                if not(verify.char4(password)):
                    print("Invalid Password length, Try Again")

            createUser(email, password, cursor)

            connection.commit()

            current_user.email = email
            break

        elif option == "2":
            menu.clearScreen()
            sys.exit()

        elif option not in entries:
            print("Invalid input, try again")

    # check if airline agent
    query = "SELECT email FROM airline_agents"
    agents = database.read(query, cursor)

    if str(current_user.email).ljust(20) in agents:
        current_user.agent = True

    database.close(cursor)
    return current_user



def logout(connection, user):
    cursor = database.cursor(connection)

    update = "Update users set last_login = sysdate where email = '{}'".format(user)
    cursor.execute(update)

    connection.commit()
    database.close(cursor)


def createUser(email, password, cursInsert):
    data = [(email, password)]
    cursInsert.bindarraysize = 1
    cursInsert.setinputsizes(20,4)
    cursInsert.executemany("INSERT INTO USERS(email, pass) "
                                       "VALUES (:1, :2)", data)