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
import verify
import menu
import cx_Oracle
import sys
import search


def make(user, row, connection):
    cursor = database.cursor(connection)
    try:
        query = "SELECT name FROM passengers where email='{}'".format(user)
        names = database.read(query, cursor)

        name=""
        while not(verify.char20(name)):
            name = input("Please enter a name: ").strip()
            if not(verify.char20(name)):
                print("Invalid Name Length, Try Again")

        if name.strip().ljust(20) not in names:
            print("Creating passenger...\n")
            country=""

            while not(verify.char10(country)):
                country = input("Please enter a country: ").strip()
                if not(verify.char10(country)):
                    print("Invalid Country Name Length, Try Again")

            query = "INSERT INTO passengers (email, name, country) VALUES  ('{}','{}','{}')".format(user, str(name), str(country))

            cursor.execute(query)

            connection.commit()

        tno = genTicket(cursor)

        if row[7] != "Direct": # not a direct booking multiple tickets needed
            # flight no 1 row[0], fare type f1 row[10]
            # flight no 2 row[1], fare type f2 row[11]
            # dep_date row[12]

            #UPDATE THE VIEWS
            search.create_views(cursor)
            query = "select seats from good_connections WHERE flightno1 = '{}' AND flightno2 = '{}' and  a1_fare = '{}'\
                    and a2_fare = '{}' ".format(str(row[0]),str(row[1]),str(row[10]),str(row[11]))
            seat = database.read(query, cursor)

            if int(seat[0])>0:
                print("Creating booking...\n")

                #generate our ticket
                #price row[8]
                query = "insert into tickets (tno, name, email, paid_price)\
                         VALUES ('{}','{}','{}','{}')".format(tno, name, user, str(row[8]))

                cursor.execute(query)

                # now we can make our bookings
                query = "insert into bookings (tno, flightno, fare, dep_date, seat)\
                        VALUES ('{}','{}','{}','{}','{}')".format(tno, str(row[0]), str(row[10]), str(row[12]), "TBD1")
                cursor.execute(query) #first part of flight

                query = "insert into bookings (tno, flightno, fare, dep_date, seat)\
                        VALUES ('{}','{}','{}','{}','{}')".format(tno, str(row[1]), str(row[11]), str(row[12]), "TBD2")
                cursor.execute(query) #second part of flight

                connection.commit()

                print("Booking created successfully")
                print("Tno:{} under {}".format(tno,name))
                return True


            else:
                print("Booking failed, try again")
                return False


        else: # direct booking, same procedure one less time

            search.create_views(cursor)
            query = "select seats from available_flights WHERE flightno = '{}' AND fare = '{}'".format(str(row[0]),str(row[10]))
            seat = database.read(query, cursor)


            if int(seat[0])>0:
                print("Creating booking...\n")

                #generate our ticket
                #price row[8]
                query = "insert into tickets (tno, name, email, paid_price)\
                         VALUES ('{}','{}','{}','{}')".format(tno, name, user, str(row[8]))

                cursor.execute(query)

                query = "insert into bookings (tno, flightno, fare, dep_date, seat)\
                        VALUES ('{}','{}','{}','{}','{}')".format(tno, str(row[0]), str(row[10]), str(row[12]), "TBD")
                cursor.execute(query)

                connection.commit()

                print("Booking created successfully")
                print("Tno:{} under {}".format(tno,name))
                return True

            else:
                print("Booking failed, try again")
                return False

    except:
        error, = cx_Oracle.DatabaseError.args
        print(sys.stderr, "Oracle code:", error.code)
        print(sys.stderr, "Oracle message:", error.message)
        print("Booking failed, try again")
        return False


def round_trip(user, row, return_date, connection):
    cursor = database.cursor(connection)
    search.create_views(cursor)
    connection.commit()

    try:
        query = "SELECT name FROM passengers where email='{}'".format(user)
        names = database.read(query, cursor)

        name=""
        while not(verify.char20(name)):
            name = input("Please enter a name: ").strip()
            if not(verify.char20(name)):
                print("Invalid Name Length, Try Again")

        if name.strip().ljust(20) not in names:
            print("Creating passenger...\n")
            country=""

            while not(verify.char10(country)):
                country = input("Please enter a country: ").strip()
                if not(verify.char10(country)):
                    print("Invalid Country Name Length, Try Again")

            query = "INSERT INTO passengers (email, name, country) VALUES  ('{}','{}','{}')".format(user, str(name), str(country))

            cursor.execute(query)

            connection.commit()

        tno = genTicket(cursor)

        if row[7] != "Direct": # not a direct booking multiple tickets needed
            # flight no 1 row[0], fare type f1 row[10]
            # flight no 2 row[1], fare type f2 row[11]
            # dep_date row[12]

            #UPDATE THE VIEWS
            search.create_views(cursor)
            query = "select seats from good_connections WHERE flightno1 = '{}' AND flightno2 = '{}' and  a1_fare = '{}'\
                    and a2_fare = '{}' ".format(str(row[0]),str(row[1]),str(row[10]),str(row[11]))
            seat = database.read(query, cursor)

            if int(seat[0])>0:
                print("Creating booking...\n")

                #generate our ticket
                #price row[8]
                query = "insert into tickets (tno, name, email, paid_price)\
                         VALUES ('{}','{}','{}','{}')".format(tno, name, user, str(row[8]))

                cursor.execute(query)

                # now we can make our bookings
                query = "insert into bookings (tno, flightno, fare, dep_date, seat)\
                        VALUES ('{}','{}','{}','{}','{}')".format(tno, str(row[0]), str(row[10]), str(row[12]), "TBD1")
                cursor.execute(query) #first part of flight

                query = "insert into bookings (tno, flightno, fare, dep_date, seat)\
                        VALUES ('{}','{}','{}','{}','{}')".format(tno, str(row[1]), str(row[11]), str(row[12]), "TBD2")
                cursor.execute(query) #second part of flight

                connection.commit()

                print("Booking created successfully")
                print("Tno:{} under {}".format(tno,name))
                return True


            else:
                print("Booking failed, try again")
                return False


        else: # direct booking, same procedure one less time

            search.create_views(cursor)
            query = "select seats from available_flights WHERE flightno = '{}' AND fare = '{}'".format(str(row[0]),str(row[10]))
            seat = database.read(query, cursor)


            if int(seat[0])>0:
                print("Creating booking...\n")

                #generate our ticket
                #price row[8]
                query = "insert into tickets (tno, name, email, paid_price)\
                         VALUES ('{}','{}','{}','{}')".format(tno, name, user, str(row[8]))

                cursor.execute(query)

                query = "insert into bookings (tno, flightno, fare, dep_date, seat)\
                        VALUES ('{}','{}','{}','{}','{}')".format(tno, str(row[0]), str(row[10]), str(row[12]), "TBD")
                cursor.execute(query)

                connection.commit()

                print("Booking created successfully")
                print("Tno:{} under {}".format(tno,name))


                sort = ""
                while sort!="0" and sort!="1":
                    sort = input("Enter 0 to sort by price or 1 to sort by number of connections for return trip: ")

                source = row[3]
                destination = row[2]
                departure_date = return_date

                search_query_gc = "select * from good_connections gc where gc.src='{}' and gc.dst='{}' and \
                                    gc.dep_date = to_date('{}', 'dd-mm-yy')\
                                    order by price asc, layover asc".format(source, destination, departure_date)

                search_query_af = "select * from available_flights af where af.src='{}' and af.dst='{}' and \
                                    af.dep_date = to_date('{}', 'dd-mm-yy') order by price asc".format(source, destination,
                                                                                                       departure_date)

                cursor.execute(search_query_gc)
                search_query_gc_rows = cursor.fetchall()
                cursor.execute(search_query_af)
                search_query_af_rows = cursor.fetchall()

                count = 1

                menu.clearScreen()

                print("Return Trips Found\n\n" + \
                        "Select Row Number to book or press enter to cancel\n\n")

                print(str("Row").ljust(6) + str("Fl no1").ljust(9) + str("Fl no2").ljust(9) + str("Src").ljust(5) + str("Dst").ljust(5) + str("Dep Time").ljust(10)\
                    + str("Arr Time").ljust(10) + str("Stops").ljust(7) + str("Layover(hrs)").ljust(14) + str("Price").ljust(8)\
                    + str("Seats").ljust(7))

                x = "-" * 90
                print(x)

                all_rows = []
                for row in search_query_af_rows:
                    all_rows.append([row[0],"N/A",row[2],row[3],row[4].strftime('%H:%M'),row[5].strftime('%H:%M'),"0","Direct",int(row[8]),row[7],row[6],"N/A", departure_date])

                for row in search_query_gc_rows:
                    all_rows.append([row[3],row[4],row[0],row[1],row[10].strftime('%H:%M'),row[11].strftime('%H:%M'),"1","{0:.2f}".format(row[5]),row[6],row[7],row[8], row[9], departure_date])

                if len(search_query_af_rows) == 0 and len(search_query_gc_rows) == 0:
                    print("No flights found")

                elif sort == "0":
                    all_rows.sort(key=lambda x:x[8])

                    for row in all_rows:
                        print(str(count).ljust(6) + str(row[0]).ljust(9) + str(row[1]).ljust(9) + str(row[2]).ljust(5) + str(row[3]).ljust(5) + str(row[4]).ljust(10)\
                            + str(row[5]).ljust(10) + str(row[6]).ljust(7) + str(row[7]).ljust(14) + str(row[8]).ljust(8)\
                            + str(row[9]).ljust(7))

                        count += 1


                elif sort == "1":
                    all_rows.sort(key=lambda x:x[6])

                    for row in all_rows:
                        print(str(count).ljust(6) + str(row[0]).ljust(9) + str(row[1]).ljust(9) + str(row[2]).ljust(5) + str(row[3]).ljust(5) + str(row[4]).ljust(10)\
                            + str(row[5]).ljust(10) + str(row[6]).ljust(7) + str(row[7]).ljust(14) + str(row[8]).ljust(8)\
                            + str(row[9]).ljust(7))

                        count += 1

                while True:
                    entry = input("\n")

                    if entry == "":
                        break

                    elif verify.rowSelection(entry, len(all_rows)):
                        entry = int(entry)-1 # actual position in list of rows
                        make(user,all_rows[entry], connection)

            else:
                print("Booking failed, try again")
                return False

    except:
            error, = cx_Oracle.DatabaseError.args
            print(sys.stderr, "Oracle code:", error.code)
            print(sys.stderr, "Oracle message:", error.message)
            print("Booking failed, try again")
            return False


def genTicket(cursor):
    query = "SELECT tno FROM tickets"
    tickets = database.read(query, cursor)

    return max(tickets)+1


def list(connection, user):
    while True:
        cursor = database.cursor(connection)
        search.create_views(cursor)

        menu.clearScreen()

        print("Existing Bookings\n\n" + \
              "Select Row Number for more details or press enter to go back\n\n")

        query = "select  t.tno, t.name, to_char(b.dep_date, 'dd-mon-yy') as dep_date, t.paid_price, b.flightno \
                 from bookings b, tickets t where b.tno = t.tno and t.email = '{}'".format(user)

        cursor.execute(query)

        rows = cursor.fetchall()

        count_view = 1

        print(str("Row").ljust(6) + str("Tno").ljust(6) + str("Passenger Name").ljust(21) + str("Dep Date").ljust(12)\
                   +str("Price").ljust(8))
        x = "-" * 61
        print(x)

        already_seen = []
        if len(rows)!= 0:
            for row in rows:
                entry_string = [row[0],row[1], row[2],row[3]]
                if entry_string not in already_seen:
                    print(str(count_view).ljust(6) + str(entry_string[0]).ljust(6) + str(entry_string[1]).strip().ljust(21) + str(entry_string[2]).ljust(12) + str(entry_string[3]).ljust(8))
                    already_seen.append(entry_string)
                    count_view+=1

        else:
            print("User has no flights")

        entry = input("\n")
        if entry == "":
            break

        elif not(verify.rowSelection(entry, count_view)):
            print("Invalid entry, Try Again")

        elif verify.rowSelection(entry, len(rows)):
            entry = int(count_view)-2 # actual position in list of rows

            menu.clearScreen()

            print("Detailed Booking\n\n" + \
                  "Press enter to go back or enter 'cancel' to cancel flight\n")

            query = "select count(tno) from bookings where tno = '{}'".format(str(already_seen[entry][0]))

            cursor.execute(query)

            ticket_count = database.read(query, cursor)

            if int(ticket_count[0])>1: # non-direct flight choose from good_connections
                query = "select  t.tno, to_char(b.dep_date, 'dd-mon-yy') as dep_date, t.paid_price, b.flightno, t.name \
                 from bookings b, tickets t where b.tno = t.tno and t.tno='{}' and t.email = '{}'".format(str(already_seen[entry][0]),user)

                cursor.execute(query)

                rows = cursor.fetchall()

                query = "select * from good_connections where flightno1 = '{}' or flightno1 = '{}' or flightno2 = '{}'\
                        or flightno2 = '{}' and price = '{}' \
                        and dep_date = to_date('{}', 'dd-mon-yy')".format(str(rows[0][3]),str(rows[1][3]),str(rows[1][3]),\
                                                                          str(rows[0][3]), str(rows[0][2]),str(rows[0][1]))

                cursor.execute(query)

                result = cursor.fetchall()

                #tno is str(already_seen[entry][0])

                for x in result:
                    if x[6] == str(rows[0][1]):
                        break

                print("Tno: " + str(already_seen[entry][0]))
                print("Passenger Name: " + str(rows[0][4]))
                print("Departure Date: " + str(rows[0][1]))
                print("Price: " + str(result[0][6]))
                print("Flight No1: " + str(x[3]))
                print("Flight No2: " + str(x[4]))
                print("Flight Source: " +str(x[0]))
                print("Flight Destination: " + str(x[1]))
                print("Fare Type1: " + str(x[8]))
                print("Fare Type2: " + str(x[9]))

                query = "select f.descr, ff.bag_allow from flight_fares ff, fares f where ff.flightno = '{}'\
                        and ff.fare = '{}' and ff.fare = f.fare".format(str(x[3]), str(x[8]))

                cursor.execute(query)

                additional_rows = cursor.fetchall()

                for add_row in additional_rows:
                    print("Fare Type1 Description: " + str(add_row[0]))
                    print("Bags Type1 Allowed: " + str(add_row[1]))

                query = "select f.descr, ff.bag_allow from flight_fares ff, fares f where ff.flightno = '{}'\
                        and ff.fare = '{}' and ff.fare = f.fare".format(str(x[4]), str(x[9]))

                cursor.execute(query)

                additional_rows = cursor.fetchall()

                for add_row in additional_rows:
                    print("Fare Type2 Description: " + str(add_row[0]))
                    print("Bags Type2 Allowed: " + str(add_row[1]))

                while True:
                    nope = input("\n")

                    if nope == "" :
                        break

                    elif nope == "cancel":
                        menu.clearScreen()
                        print("Canceling booking...")

                        query = "DELETE FROM bookings WHERE tno = '{}' and \
                                dep_date = to_date('{}', 'dd-mon-yy')".format(str(already_seen[entry][0]), str(rows[0][1]))

                        cursor.execute(query)

                        query = "SELECT email FROM tickets"
                        users = database.read(query, cursor)


                        if user.ljust(20) not in users:
                            query = "DELETE FROM passengers WHERE email = '{}' and name = '{}'".format(user,
                                                                                                  str(rows[0][4]))
                            cursor.execute(query)

                        connection.commit()

                        break

            else: # direct flight
                query = "select  f.src, f.dst, b.seat, b.fare from bookings b, flights f, tickets t where b.tno = t.tno\
                    and b.flightno = f.flightno and b.tno = '{}' and b.flightno = '{}'\
                    and b.dep_date = to_date('{}', 'dd-mon-yy')".format(str(rows[entry][0]), str(rows[entry][4]),
                                                                        str(rows[entry][2]))

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

                query = "select f.descr, ff.bag_allow from flight_fares ff, fares f where ff.flightno = '{}'\
                        and ff.fare = '{}' and ff.fare = f.fare".format(str(rows[entry][4]), str(row[3]))

                cursor.execute(query)

                additional_rows = cursor.fetchall()

                for add_row in additional_rows:
                    print("Fare Description: " + str(add_row[0]))
                    print("Bags Allowed: " + str(add_row[1]))


                while True:
                    nope = input("\n")

                    if nope == "" :
                        break

                    elif nope == "cancel":
                        menu.clearScreen()
                        print("Canceling booking...")

                        query = "DELETE FROM bookings WHERE tno = '{}' and \
                                dep_date = to_date('{}', 'dd-mon-yy')".format(str(rows[entry][0]), str(rows[entry][2]))

                        cursor.execute(query)

                        query = "SELECT email FROM tickets"
                        users = database.read(query, cursor)


                        if user.ljust(20) not in users:
                            query = "DELETE FROM passengers WHERE email = '{}' and name = '{}'".format(user,
                                                                                                  str(rows[entry][1]))
                            cursor.execute(query)

                        connection.commit()

                        break

        else:
            print("Invalid entry, Try Again")