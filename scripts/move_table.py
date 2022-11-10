import sqlite3


def move_place():
    with sqlite3.connect("../instance/test.db") as conn1:
        with sqlite3.connect("../instance/db.sqlite3") as conn2:
            cursor2 = conn2.cursor()
            query = "SELECT * FROM flight_place"
            cursor2.execute(query)
            result = cursor2.fetchall()
            # print(result)

            cursor1 = conn1.cursor()
            insertion = "INSERT INTO place (id, city, airport, code, country) VALUES (?, ?, ?, ?, ?)"
            cursor1.executemany(insertion, result)


def move_week():
    with sqlite3.connect("../instance/test.db") as conn1:
        with sqlite3.connect("../instance/db.sqlite3") as conn2:
            cursor2 = conn2.cursor()
            query = "SELECT * FROM flight_week"
            cursor2.execute(query)
            result = cursor2.fetchall()

            cursor1 = conn1.cursor()
            insertion = "INSERT INTO week (id, number, name) VALUES (?, ?, ?)"
            cursor1.executemany(insertion, result)

def move_flight():
    with sqlite3.connect("../instance/test.db") as conn1:
        with sqlite3.connect("../instance/db.sqlite3") as conn2:
            cursor2 = conn2.cursor()
            query = "SELECT * FROM flight_flight"
            cursor2.execute(query)
            result = cursor2.fetchall()

            cursor1 = conn1.cursor()
            insertion = "INSERT INTO flight (id, depart_time, duration, arrival_time, plane, airline, economy_fare, business_fare, first_fare, destination_id, origin_id)" + \
                        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor1.executemany(insertion, result)

def price():
    with sqlite3.connect("../instance/test.db") as conn1:
        cursor1 = conn1.cursor()
        # query = "update flight set economy_fare = economy_fare + 100"
        # cursor1.execute(query)
        query = "update flight set business_fare = business_fare * 3"
        cursor1.execute(query)
        query = "update flight set first_fare = first_fare * 5"
        cursor1.execute(query)

if __name__ == "__main__":
    price()
