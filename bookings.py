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

def make():
    pass

def list(connection, user):
    while True:
        cursor = database.cursor(connection)

        menu.clearScreen()

        print("Existing Bookings\n\n" + \
              "Select Row Number for more details or press enter to go back\n\n")

        query = "select  t.tno, t.name, to_char(b.dep_date, 'dd-mon-yy') as dep_date, t.paid_price, b.flightno \
                from bookings b, tickets t \
                where b.tno = t.tno and t.email = :user_email"
        query = query.replace(":user_email", "'"+user+"'")

        cursor.execute(query)

        rows = cursor.fetchall()

        count = 1

        print(str("Row").ljust(6) + str("Tno").ljust(6) + str("Passenger Name").ljust(21) + str("Dep Date").ljust(12)\
                  +str("Price").ljust(8)+str("Fl No").ljust(8))
        x = "-" * 61
        print(x)

        if len(rows)!= 0:
            for row in rows:
                print(str(count).ljust(6) + str(row[0]).ljust(6) + str(row[1]).strip().ljust(21) + str(row[2]).ljust(12)\
                      +str(row[3]).ljust(8)+str(row[4]).ljust(8))
                count += 1

        else:
            print("User has no flights")

        entry = input("\n")
        if entry == "":
            break

        elif not(entry.isnumeric()):
            print("Invalid entry, Try Again")

        elif 1 <= int(entry) <= len(rows) and len(rows)!=0:
            entry = int(entry)-1
            menu.clearScreen()
            print("Detailed Booking\n\n" + \
                  "Press enter to go back or enter 'cancel' to cancel flight\n")
            query = "select  f.src, f.dst, b.seat, b.fare\
                    from bookings b, flights f, tickets t\
                    where b.tno = t.tno\
                    and b.flightno = f.flightno\
                    and b.tno = :ticket\
                    and b.flightno = :flight\
                    and b.dep_date = to_date(:depdate, 'dd-mon-yy')"
            query = query.replace(":ticket", "'"+str(rows[entry][0])+"'")
            query = query.replace(":flight", "'"+str(rows[entry][4])+"'")
            query = query.replace(":depdate", "'"+str(rows[entry][2])+"'")

            cursor.execute(query)

            detailed_rows = cursor.fetchall()

            for row in detailed_rows:
                print("Tno: " + str(rows[entry][0]))
                print("Passenger Name: " + str(rows[entry][1]))
                print("Departure Date: " + str(rows[entry][2]))
                print("Price: " + str(rows[entry][3]))
                print("Flight No: " + str(rows[entry][4]))
                print("Flight Source: " + str(row[0]))
                print("Flight Destination: " + str(row[1]))
                print("Seat No: " + str(row[2]))
                print("Fare Type: " + str(row[3]))

            while True:
                nope = input("\n")

                if nope == "" :
                    break

                elif nope == "cancel":
                    menu.clearScreen()
                    print("Canceling booking...")
                    query = "UPDATE flight_fares SET limit = limit + 1\
                             WHERE flightno = '{}' AND fare = '{}'".format(str(row[2]),str(row[3]))
                    cursor.execute(query)
                    query = "DELETE FROM bookings WHERE tno = '{}' and dep_date = to_date('{}', 'dd-mon-yy') \
                             and seat = '{}' and fare = '{}' and flightno = '{}'".format(str(rows[entry][0]),
                                                                                         str(rows[entry][2]),
                                                                                         str(row[2]),
                                                                                         str(row[3]), str(rows[entry][4]))
                    cursor.execute(query)
                    query = "DELETE FROM tickets WHERE tno = '{}' and name = '{}'".format(str(rows[entry][0]),
                                                                                          str(rows[entry][1]))
                    cursor.execute(query)

                    connection.commit()

                    break

        else:
            print("Invalid entry, Try Again")




