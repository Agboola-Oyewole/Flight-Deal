from twilio.rest import Client
import smtplib
from data_manager import DataManager


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.user_data = DataManager()
        self.my_email = "delmergaldez02@gmail.com"
        self.password = "dayiawcbqfnighpn"
        # Set environment variables for your credentials
        # Read more at http://twil.io/secure
        self.account_sid = "AC41d7974ceb46ee0f9f782a1fc007ba41"
        self.auth_token = "9f87a1e5d956d6e1a4047ce9bf0f70ee"
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, sms_message):
        message = self.client.messages.create(
            body=sms_message,
            from_="+12544337403",
            to="+2348033431111"
        )
        print(message.sid)

    def send_email(self, message):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.password)
            for email in self.user_data.emails:
                connection.sendmail(from_addr=self.my_email,
                                    to_addrs=email,
                                    msg=message)
