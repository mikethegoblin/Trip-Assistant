from dbm import dumb
from typing import Dict, List

TRAVEL_CLASS_MAP = {
    "Economy Class": "ECONOMY",
    "FIRST Class": "FIRST",
    "Business Class": "BUSINESS"
}

def convert_flight_info(flight_info: List[Dict], multi=False) -> Dict:
    result = []
    for flight in flight_info:
        numberOfBookableSeats=flight["numberOfBookableSeats"]
        price_label = flight["price"]["total"] + " " + flight["price"]["currency"]
        itineraries=flight["itineraries"]
        depart_trip = itineraries[0]
        depart_trip_info = {
            "duration": depart_trip["duration"],
            "trip": depart_trip["segments"][0]["departure"]["iataCode"]+"->"+depart_trip["segments"][-1]["arrival"]["iataCode"],
            "numberOfStops": len(depart_trip["segments"])
        }

        trip_info = {
                "numberOfBookableSeats": numberOfBookableSeats,
                "price": price_label,
                "departTrip": depart_trip_info,
        }
        if multi: 
            arrival_trip = itineraries[1]
            arrival_trip_info = {
            "duration": arrival_trip["duration"],
            "trip": depart_trip["segments"][0]["departure"]["iataCode"]+"->"+depart_trip["segments"][-1]["arrival"]["iataCode"],
            "numberOfStops": len(arrival_trip["segments"])
            }
            trip_info.update(
                {"arrivalTrip": arrival_trip_info}
            )

        result.append(trip_info)
    print(result[0])
    return result


def parse_class(travel_class):
    return TRAVEL_CLASS_MAP[travel_class]
                

        