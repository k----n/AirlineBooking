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
import menu
import time



class User:
    def __init__(self, email = None):
        self.email = email
        self.agent = False

def record_dep(connection):
    while True:
        cursor = database.cursor(connection)

        menu.clearScreen()

        print("Record Depature Time\n\n" + \
              "Select Row Number to Change Departure Time For Scheduled flight or press enter to go back\n\n")

        query = "select s.flightno, to_char(s.dep_date, 'dd-mon-yy') as dep_date \
                from sch_flights s"

        cursor.execute(query)

        rows = cursor.fetchall()

        count = 1

        print(str("Row").ljust(6)+str("Fl No").ljust(8)+str("Dep Date").ljust(12))
        x = "-" * 26
        print(x)

        if len(rows)!= 0:
            for row in rows:
                print(str(count).ljust(6) + str(row[0]).ljust(8) + str(row[1]).ljust(12))
                count += 1

        else:
            print("No Scheduled Flights Currently Exist")

        entry = input("\n")
        if entry == "":
            break

        elif not(entry.isnumeric()):
            print("Invalid entry, Try Again")

        elif 1 <= int(entry) <= len(rows) and len(rows)!=0:
            entry = int(entry)-1
            menu.clearScreen()
            print("Change Departure Time\n\n" + \
                  "Press enter to go back or enter 'hh24:mi' to change departure time\n")
            print("Flight No: " + str(rows[entry][0]))
            print("Dep Date: " + str(rows[entry][1]))

            while True:
                nope = input("\nNew departure time (hh24:mi): ")

                if nope == "":
                    break

                elif not(isTimeFormat(nope)):
                    print("Invalid time format, Try Again")


                elif isTimeFormat(nope):
                    menu.clearScreen()
                    print("Changing Departure Time...")
                    query = "UPDATE sch_flights SET act_dep_time = to_date('{}', 'hh24:mi')\
                             WHERE flightno = '{}' AND dep_date = '{}'".format(str(nope), str(rows[entry][0]),
                                                                               str(rows[entry][1]))
                    cursor.execute(query)

                    connection.commit()

                    break




def record_arr(connection):
    while True:
        cursor = database.cursor(connection)

        menu.clearScreen()

        print("Record Arrival Time\n\n" + \
              "Select Row Number to Change Arrival Time For Scheduled flight or press enter to go back\n\n")

        query = "select s.flightno, to_char(s.dep_date, 'dd-mon-yy') as dep_date \
                from sch_flights s"

        cursor.execute(query)

        rows = cursor.fetchall()

        count = 1

        print(str("Row").ljust(6)+str("Fl No").ljust(8)+str("Dep Date").ljust(12))
        x = "-" * 26
        print(x)

        if len(rows)!= 0:
            for row in rows:
                print(str(count).ljust(6) + str(row[0]).ljust(8) + str(row[1]).ljust(12))
                count += 1

        else:
            print("No Scheduled Flights Currently Exist")

        entry = input("\n")
        if entry == "":
            break

        elif not(entry.isnumeric()):
            print("Invalid entry, Try Again")

        elif 1 <= int(entry) <= len(rows) and len(rows)!=0:
            entry = int(entry)-1
            menu.clearScreen()
            print("Change Arrival Time\n\n" + \
                  "Press enter to go back or enter 'hh24:mi' to change arrival time\n")
            print("Flight No: " + str(rows[entry][0]))
            print("Dep Date: " + str(rows[entry][1]))

            while True:
                nope = input("\nNew arrival time (hh24:mi): ")

                if nope == "":
                    break

                elif not(isTimeFormat(nope)):
                    print("Invalid time format, Try Again")

                elif isTimeFormat(nope):
                    menu.clearScreen()
                    print("Changing Arrival Time...")
                    query = "UPDATE sch_flights SET act_arr_time = to_date('{}', 'hh24:mi')\
                             WHERE flightno = '{}' AND dep_date = '{}'".format(str(nope), str(rows[entry][0]),
                                                                               str(rows[entry][1]))
                    cursor.execute(query)

                    connection.commit()

                    break



def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False