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
import menu
import sys

def login(connection):
    cursor = database.cursor(connection)

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
            while len(email) > 20 or len(email) == 0:
                email = input("\nEmail: ").strip().lower()
                if len(email) > 20 or len(email) == 0:
                    print("Invalid Email Length, Try Again")

            users = database.read("SELECT email FROM USERS", cursor)
            if email not in users:
                print("User does not exist!")

            else:
                while len(password) > 4 or len(password) == 0:
                    password = getpass.getpass("Password: ")
                    if len(password) > 4 or len(password) == 0:
                        print("Invalid Password length, Try Again")

                users_pass = database.read("SELECT pass FROM USERS", cursor)

                if password != users_pass[users.index(email)]:
                    print("Incorrect password!")

                elif password == users_pass[users.index(email)]:
                    break

        elif option == "1":
            email = ""
            password = ""
            while len(email) > 20 or len(email) == 0:
                email = input("\nNew Email: ").strip().lower()
                if len(email) > 20 or len(email) == 0:
                    print("Invalid Email Length, Try Again")

            while len(password) > 4 or len(password) == 0:
                password = getpass.getpass("New Password: ")
                if len(password) > 4 or len(password) == 0:
                    print("Invalid Password length, Try Again")

            createUser(email, password, cursor)

            connection.commit()

            break

        elif option == "2":
            menu.clearScreen()
            sys.exit()

        elif option not in entries:
            print("Invalid input, try again")

    database.close(cursor)
    return email

def logout(connection, user):
    cursor = database.cursor(connection)

    update = "Update users set last_login = sysdate where email = :user_email"
    update = update.replace(":user_email", "'"+user+"'")

    cursor.execute(update)

    connection.commit()
    database.close(cursor)


def createUser(email, password, cursInsert):
    data = [(email, password)]
    cursInsert.bindarraysize = 1
    cursInsert.setinputsizes(20,4)
    cursInsert.executemany("INSERT INTO USERS(email, pass) "
                                       "VALUES (:1, :2)", data)