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
import datetime
import menu

def create_views(cursor):
    f = open('sql/drop_views.sql')
    sql_commands = f.read()
    sql_commands = sql_commands.split(';')
    view_names = [x.strip() for x in sql_commands]
    view_names = [x.replace("drop view ","").upper() for x in view_names].pop()
    print(view_names)

    count = 0

    cursor.execute("select view_name from user_views")
    output_rows = cursor.fetchall()
    output_rows = [''.join(i) for i in output_rows]

    for line in output_rows:
        if line in view_names:
            count +=1

    if count == len(view_names):
        for x in range(0, len(sql_commands)-1):
            cursor.execute(sql_commands[x])

    query = "create view available_flights(flightno,dep_date, src,dst,dep_time,arr_time,fare,seats,\
            price, a1_name, a2_name, a1_city, a2_city) as select f.flightno, sf.dep_date, f.src, f.dst,\
            f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)), \
            f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24, \
            fa.fare, fa.limit-count(tno), fa.price, a1.name, a2.name, a1.city, a2.city\
            from flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2\
            where f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and\
            f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and\
            sf.dep_date=b.dep_date(+)\
            group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone,\
            a1.tzone, fa.fare, fa.limit, fa.price, a1.name, a2.name, a1.city, a2.city\
            having fa.limit-count(tno) > 0"

    cursor.execute(query)

    query = "create view good_connections (src,dst,dep_date,flightno1,flightno2, layover,price, seats,\
            a1_fare, a2_fare, dep_time, arr_time, a1_name, a2_name, a1_city, a2_city) as\
            select a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, (a2.dep_time-a1.arr_time)*24,\
            (a1.price+a2.price),case when a1.seats <= a2.seats then a1.seats else a2.seats end,\
            a1.fare, a2.fare, a1.dep_time, a2.arr_time, a1.a1_name, a2.a2_name, a1.a1_city, a2.a2_city\
            from available_flights a1, available_flights a2 where a1.dst=a2.src and a1.src!=a2.dst and  \
            a1.arr_time<=a2.dep_time group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time, \
            a1.arr_time, (a1.price+a2.price), case when a1.seats <= a2.seats then a1.seats else a2.seats end, \
            a1.fare, a2.fare, a1.dep_time, a2.arr_time, a1.a1_name, a2.a2_name, a1.a1_city, a2.a2_city"

    cursor.execute(query)


def search_flights(connection):
    cursor = database.cursor(connection)
    create_views(cursor)
    connection.commit()

    # specifying a case insensitive sort
    cursor.execute("ALTER SESSION SET NLS_COMP=LINGUISTIC")
    cursor.execute("ALTER SESSION SET NLS_SORT=BINARY_CI")


    source = ""
    destination = ""
    departure_date = ""
    sort=""
    while not(verify.char30(source)):
        source = input("Please enter a source: ").strip()
        if not(verify.char30(source)):
            print("Invalid Source Length, Try Again")

    while not(verify.char30(destination)):
        destination = input("Please enter a destination: ").strip()
        if not(verify.char30(destination)):
            print("Invalid Destination Length, Try Again")

    while not(verify.isDateFormat(departure_date)):
        departure_date= input("Please enter a departure date (DD-MON-YYYY): ").strip()
        if not(verify.isDateFormat(departure_date)):
            print("Invalid Date Format, Try Again")

    while sort!="0" and sort!="1":
        sort = input("Enter 0 to sort by price or 1 to sort by number of connections: ")


    get_acodes_query = "select acode from airports"

    valid_acodes = database.read(get_acodes_query,cursor)

    if source.upper() and destination.upper() in valid_acodes:
        search_query_gc = "select * from good_connections gc where gc.src='{}' and gc.dst='{}' and \
                        gc.dep_date = to_date('{}', 'dd-mm-yy')\
                        order by price asc, layover asc".format(source, destination, departure_date)
        search_query_af = "select * from available_flights af where af.src='{}' and af.dst='{}' and \
                        af.dep_date = to_date('{}', 'dd-mm-yy') order by price asc".format(source, destination,
                                                                                           departure_date)
    else:
        search_query_gc = "select * from good_connections gc where gc.a1_name like '%{}%' or gc.a1_city like '%{}%'\
                        or gc.src  like '%{}%' and gc.a2_name like '%{}%' or gc.a1_city like '%{}%' or\
                        gc.src like '%{}%' and gc.dep_date = to_date('{}', 'dd-mon-yy') order by price asc,\
                        layover asc".format(source,source,source,destination,destination,destination,departure_date)
        search_query_af = "select * from available_flights af where af.a1_name like '%{}%' or af.a1_city like '%{}%'\
                        or af.src  like '%{}%' and af.a2_name like '%{}%' or af.a2_city like '%{}%' or\
                        af.dst like '%{}%' and af.dep_date = to_date('{}', 'dd-mon-yy')\
                        order by price asc".format(source,source,source,destination,destination,
                                            destination,departure_date)

    cursor.execute(search_query_gc)
    search_query_gc_rows = cursor.fetchall()
    cursor.execute(search_query_af)
    search_query_af_rows = cursor.fetchall()

    count = 1

    menu.clearScreen()

    print("Flights Found\n\n" + \
            "Select Row Number to book or press enter to go back\n\n")


    print(str("Row").ljust(6) + str("Fl no1").ljust(9) + str("Fl no2").ljust(9) + str("Src").ljust(5) + str("Dst").ljust(5) + str("Dep Time").ljust(10)\
        + str("Arr Time").ljust(10) + str("Stops").ljust(7) + str("Layover (hrs)").ljust(14) + str("Price").ljust(8)\
        + str("Seats").ljust(7))

    x = "-" * 90
    print(x)

    if len(search_query_af_rows) == 0 and len(search_query_gc_rows) == 0:
        print("No flights found")

    elif sort == "0":
        price_rows = list()
        for row in search_query_af_rows:
            price_rows.append([row[0],"N/A",row[2],row[3],row[4].strftime('%H:%M'),row[5].strftime('%H:%M'),"0","Direct",int(row[8]),row[7]])

        for row in search_query_gc_rows:
            price_rows.append([row[3],row[4],row[0],row[1],row[10].strftime('%H:%M'),row[11].strftime('%H:%M'),"1",row[5],row[6],row[7]])

        price_rows.sort(key=lambda x:x[8])

        for row in price_rows:
            print(str(count).ljust(6) + str(row[0]).ljust(9) + str(row[1]).ljust(9) + str(row[2]).ljust(5) + str(row[3]).ljust(5) + str(row[4]).ljust(10)\
                + str(row[5]).ljust(10) + str(row[6]).ljust(7) + str(row[7]).ljust(14) + str(row[8]).ljust(8)\
                + str(row[9]).ljust(7))


    elif sort == "1":
        for row in search_query_af_rows:
            print(str(count).ljust(6) + str(row[0]).ljust(9) + str("N/A").ljust(9) + str(row[2]).ljust(5) + str(row[3]).ljust(5) + str(row[4].strftime('%H:%M')).ljust(10)\
                + str(row[5].strftime('%H:%M')).ljust(10) + "0".ljust(7) + str("Direct").ljust(14) + str(int(row[8])).ljust(8)\
                + str(row[7]).ljust(7))
            count+=1

        for row in search_query_gc_rows:
            print(str(count).ljust(6) + str(row[3]).ljust(9) + str(row[4]).ljust(9) + str(row[0]).ljust(5) + str(row[1]).ljust(5) + str(row[10].strftime('%H:%M')).ljust(10)\
                + str(row[11].strftime('%H:%M')).ljust(10) + "1".ljust(7) + str(row[5]).ljust(14) + str(row[6]).ljust(8)\
                + str(row[7]).ljust(7))
            count += 1

    while True:
        entry = input("\n")
        if entry == "":
            break