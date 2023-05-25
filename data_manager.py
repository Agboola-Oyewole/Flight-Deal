import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.sheet_endpoint = "https://api.sheety.co/a83c073483bc6d9b44bf73768cafd6e9/myFlightDeals/prices"
        self.response = requests.get(url=self.sheet_endpoint)
        self.data = self.response.json()

        self.user_sheet_endpoint = "https://api.sheety.co/a83c073483bc6d9b44bf73768cafd6e9/myFlightDeals/users"
        self.response = requests.get(url=self.user_sheet_endpoint)
        self.customer_data = self.response.json()
        self.emails = [row['email'] for row in self.customer_data['users']]
        self.users = [row['firstName'] for row in self.customer_data['users']]

    def write_to_sheets(self, id_row, iata_codes):
        if self.data['prices'][0]['iataCode'] == "":
            sheet_param = {
                "price": {
                    "iataCode": iata_codes
                }
            }
            requests.put(url=f"{self.sheet_endpoint}/{str(id_row)}", json=sheet_param)
        else:
            pass

    @staticmethod
    def write_to_users_sheet():
        print("Welcome to Ola's Flight Club.")
        print("We find the best flight deals and email you.")
        first_name = input("What is your first name?\n").title()
        last_name = input("What is your last name?\n").title()
        email = input("What is your email?\n").lower()
        confirmed_email = input("Type your email again please.\n").lower()

        if email == confirmed_email:
            sheet_param = {
                "user": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": confirmed_email
                }
            }
            requests.post(url="https://api.sheety.co/a83c073483bc6d9b44bf73768cafd6e9/myFlightDeals/users",
                          json=sheet_param)
            print("Success!, your email has been added.")
            print("You're in the Club!")
        else:
            print("Please check that the emails are the same!")

    def list_of_cities(self):
        data_list = [self.data['prices'][num]['city'] for num in range(len(self.data['prices']))]
        return data_list
