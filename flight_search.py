import requests
from flight_data import FlightData
from data_manager import DataManager


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.header = {
            "apikey": "FfKoeF_JUo5zL5RbTDj2vhHbt6m9HWOo",
            "Content-Type": "application/json"
        }
        self.data = DataManager()
        self.list_of_iata_codes = []
        for city in self.data.list_of_cities():
            self.flight_endpoint = f"https://api.tequila.kiwi.com/locations/query?term={city}"
            self.response = requests.get(url=self.flight_endpoint, headers=self.header)
            data = self.response.json()
            self.list_of_iata_codes.append(data['locations'][0]['code'])

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = self.header
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(
            url="https://api.tequila.kiwi.com/v2/search",
            headers=headers,
            params=query,
        )

        try:
            data = response.json()["data"][0]
        except IndexError:
            query['max_stopovers'] = 1
            response = requests.get(
                url="https://api.tequila.kiwi.com/v2/search",
                headers=headers,
                params=query,
            )
            if len(response.json()["data"]) == 0:
                print(f"No flights found for {destination_city_code}.")
                return None
            else:
                if len(response.json()["data"]) > 0:
                    data = response.json()["data"][0]

                    flight_data = FlightData(
                        price=data["price"],
                        origin_city=data["route"][0]["cityFrom"],
                        origin_airport=data["route"][0]["flyFrom"],
                        destination_city=data["route"][1]["cityTo"],
                        destination_airport=data["route"][1]["flyTo"],
                        out_date=data["route"][0]["local_departure"].split("T")[0],
                        return_date=data["route"][2]["local_departure"].split("T")[0],
                        stop_overs=1,
                        via_city=data["route"][0]["cityTo"]
                    )
                    return flight_data

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data

