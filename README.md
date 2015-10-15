# AirlineBooking
A simple airline booking system implemented in Python using Oracle SQL.

## To Be Implemented
### User Functions
1. Login Screen
2. Searching for flights
3. Making a booking
4. List existing bookings
5. Cancel bookings
6. Logout

### Airline Agent Functions
1. Record flight departure
2. Record flight arrival

### Booking Functions (at least 2)
1. Search and book round trips
2. Search and book with upto 3 connecting flights
3. Search and book for parties larger than 1

## Relational Schema of Database
* airports(acode, name, city, country, tzone)
* flights(flightno, src, dst, dep_time, est_dur)
* sch_flights(flightno, dep_date, act_dep_time, act_arr_time)
* fares(fare, descr)
* flight_fares(flightno, fare, limit, price, bag_allow)
* users(email, pass, last_login)
* passengers(email, name, country)
* tickets(tno, name, email, paid_price)
* bookings(tno, flightno, fare, dep_date, seat)
* airline_agents(email, name)

## Documentation
System documentation can be found in the [wiki](https://github.com/k----n/AirlineBooking/wiki).

## License
Licensed under Apache 2.0 License.
