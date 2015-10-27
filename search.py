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
import setup
import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it






def search(connection):
    # specifying a case insensitive sort
    cursor.execute("alter session set NLS_COMP=LINGUISTIC")
    cursor.execute("ALTER SESSION SET NLS_SORT=BINARY_CI")
    source = str(input("Please enter a source: "))
    destination = str(input("Please enter a destination: "))
    departure_date= str(input("Please enter a departure date (DD/MM/YYYY): "))

    get_existing_view_query = "select view_name from user_views"
    cursor.execute(get_existing_view_query)
    existing_queries = cursor.fetchall()
    if len(existing_queries) == 0:
        #queries sourced from assignment 2 solutions
        available_flights_query = "create view available_flights(flightno,dep_date, src,dst,dep_time,arr_time,fare,seats,price) as\
            select f.flightno, sf.dep_date, f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)),\
            f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24,\
            fa.fare, fa.limit-count(tno), fa.price\
            from flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2\
            where f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and\
            f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and sf.dep_date=b.dep_date(+)\
            group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone, a1.tzone, fa.fare, fa.limit, fa.price\
            having fa.limit-count(tno) > 0"
        cursor.execute(available_flights_query)

        good_connections_query = "create view good_connections (src,dst,dep_date,flightno1,flightno2, layover,price, seats) as\
        select a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, (a2.dep_time-a1.arr_time),\
	    (a1.price+a2.price),case when a1.seats <= a2.seats then a1.seats else a2.seats end\
        from available_flights a1, available_flights a2\
        where a1.dst=a2.src and  a1.arr_time <=a2.dep_time \
        group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time, a1.arr_time, (a1.price+a2.price), case when a1.seats <= a2.seats then a1.seats else a2.seats end"
        cursor.execute(good_connections_query)
        '''
        good_connections_query ="create view good_connections (src,dst,dep_date,flightno1,flightno2, dep_time, arr_time, layover,price, seats) as\
            select a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a1.dep_time, a2.arr_time, a2.dep_time-a1.arr_time,\
            min(a1.price+a2.price), min(both.seats)\
            from available_flights a1, available_flights a2, ((select ff1.limit from available_flights af1, flight_fares ff1 where ff1.flightno = af1.flightno) union (select ff2.limit from available_flihts af2, flight_fare ff2 where ff2.flightno = af2.flightno)) both\
            where a1.dst=a2.src and a1.arr_time +1.5/24 <=a2.dep_time and a1.arr_time +5/24 >=a2.dep_time\
            group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a1.dep_time, a2.arr_time, a2.dep_time, a1.arr_time"
        cursor.execute(good_connections_query)
        '''
        good_flights_query = "create view good_flights as select flightno1, flightno2, layover, price, src, dst, dep_date, seats, dep_time, arr_time\
                                from ((select flightno as flightno1, NULL as flightno2, NULL as layover, dep_date, dst, src, price, seats, dep_time, arr_time\
                                        from available_flights) union\
                                    (select flightno1, flightno2, layover, dep_date, dst, src, price, NULL as seats, NULL as dep_time,NULL as arr_time\
                                    from good_connections))"

        cursor.execute(good_flights_query)


    get_acodes_query = "select acode from airports"
    cursor.execute(get_acodes_query)
    rows = cursor.fetchall()
    valid_acodes = list()
    for row in rows:
        for acode in row:
            valid_acodes.append(acode)
    if (source.upper() and destination.upper() in valid_acodes):
        search_query= "select flightno1, src, dst, price, gf.layover*24, seats, to_char(dep_time,'HH24:MI'), to_char(arr_time,'HH24:MI') from good_flights gf, airports a1, airports a2\
        where gf.src='"+source+"' and gf.dst='"+destination+"' and to_char(dep_date, 'DD/MM/YYYY')='"+departure_date+"' order by price asc, layover asc"
    else:
        search_query = "select flightno1, a1.acode, a2.acode, price, gf.layover*24, seats, to_char(dep_time,'HH24:MI'), to_char(arr_time,'HH24:MI') from good_flights gf, airports a1, airports a2\
        where (a1.name like '%"+source+"%' or a1.city like '%"+source+"%' and gf.src = a1.acode) and\
        (a2.name like '%"+destination+"%' or a2.city like '%"+destination+"%' and gf.dst = a2.acode) and to_char(dep_date, 'DD/MM/YYYY') = '"+departure_date+"' order by price asc, layover asc"

    cursor.execute(search_query)
    rows = cursor.fetchall()
    for row in rows:
        print("Flight number:", row[0])
        print("Source airport code:", row[1])
        print("Destination airport code:", row[2])
        print("Departure Time: ",row[6])
        print("Arrival Time: ",row[7])
        print("Price: $", row[3])

        if type(row[4]) == type(None):
            print("Number of seats:", row[5])
            print ("Number of connections: 0    DIRECT FLIGHT")
            print ("No layover time")
        else:
            print("Number of seats:", row[5])
            print("Number of connections: 1")
            print("Layover time:", row[4], "hours")
        print("\n")

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