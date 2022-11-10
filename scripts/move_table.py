import sqlite3
import random


US_CITIES = {
    1: "Atlanta",
    4: "Los Angeles",
    5: "Chicago",
    22: "New York",
    24: "San Francisco",
    27: "Las Vegas",
    39: "Orlando",
    40: "Miami",
    43: "Newark",
    48: "Houston",
    53: "Minneapolis",
    55: "Boston",
    59: "Detroit",
    63: "Orlando",
    68: "New York",
    69: "Philadelphia",
    79: "Baltimore",
    91: "Salt Lake City",
    93: "Washington",
}

US_AIRLINES = {"Delta Airlines": "DL", "American Airlines": "AA", "United Airlines": "UA", "Jet Blue": "B6"}

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
        query = "update flight set economy_fare = ROUND(economy_fare, 2)"
        cursor1.execute(query)
        query = "update flight set business_fare = ROUND(business_fare, 2)"
        cursor1.execute(query)
        query = "update flight set first_fare = ROUND(first_fare, 2)"
        cursor1.execute(query)

def insert_domestic_flights():
    with sqlite3.connect("../instance/test.db") as conn:
        cursor = conn.cursor()
        statement = "UPDATE flight SET origin_id=?, destination_id=?, plane=?, airline=? WHERE id=?"
        place_ids = list(US_CITIES.keys())
        airlines = list(US_AIRLINES.keys())
        for i in range(1, 101):
            origin_id = random.choice(place_ids)
            destination_id = choose_random_place(origin_id, place_ids)
            airline = random.choice(airlines)
            plane = US_AIRLINES[airline] + str(random.randint(100, 2000))
            cursor.execute(statement, (origin_id, destination_id, plane, airline, i))

def choose_random_place(id, ids):
    result = random.choice(ids)
    while result == id:
        result = random.choice(ids)
    return result

if __name__ == "__main__":
    price()
