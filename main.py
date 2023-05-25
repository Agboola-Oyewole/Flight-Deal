from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

data = DataManager()
search = FlightSearch()
notify = NotificationManager()
iata_codes = search.list_of_iata_codes
today = datetime.date(datetime.now()) + timedelta(days=1)
date = datetime.date(datetime.now()) + timedelta(6 * 30)
from_time = today.strftime("%d/%m/%Y")
to_time = date.strftime("%d/%m/%Y")


id_row = 2
sheet_row = 0
for code in iata_codes:
    data.write_to_sheets(id_row=id_row, iata_codes=code)
    details = search.check_flights(origin_city_code="LON", destination_city_code=code, from_time=from_time,
                                   to_time=to_time)
    if details is None:
        continue
    else:
        if details.price < data.data['prices'][sheet_row]['lowestPrice']:
            print("Yes its low")
            message = f"Subject:Low Price Alert! \n\nOnly £{details.price} to fly from {details.origin_city}-" \
                      f"{details.origin_airport} to {details.destination_city}-{details.destination_airport}" \
                      f" from {details.out_date} to {details.return_date}".encode('utf-8')
            notify.send_email(message)
            notify.send_sms(message)

            if details.stop_overs > 0:
                print(f"Flight has {details.stop_overs}")

    id_row += 1
    sheet_row += 1

