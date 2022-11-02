from dbm import dumb
from typing import Dict, List


def convert_flight_info(flight_info: List[Dict]) -> Dict:
    result = []
    for flight in flight_info:
        # numberOfBookableSeats=flight["numberOfBookableSeats"]
        numberOfBookableSeats=1
        price_label = flight["price"]["total"] + " " + flight["price"]["currency"]
        itineraries=[]
        depart_trip = itineraries[0]
        arrival_trip = itineraries[1]
        depart_trip_info = {
            "duration": depart_trip["duration"],
            "trip": depart_trip["segments"][0]["departure"]["iataCode"]+"->"+depart_trip["segments"][-1]["arrival"]["iataCode"],
            "numberOfStops": len(depart_trip["segments"])
        }
        arrival_trip_info = {
            "duration": arrival_trip["duration"],
            "trip": depart_trip["segments"][0]["departure"]["iataCode"]+"->"+depart_trip["segments"][-1]["arrival"]["iataCode"],
            "numberOfStops": len(arrival_trip["segments"])
        }

        result.append(
            {
                "numberOfBookableSeats": numberOfBookableSeats,
                "price": price_label,
                "departTrip": depart_trip_info,
                "arrivalTrip": arrival_trip_info,
            }
        )
    
    return result
                

        