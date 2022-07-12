import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "kizzy272727@gmail.com"
MY_PASSWORD = "kfdihxhyynykiruu"
MY_LAT = 6.500180 #my latitue
MY_LONG = 3.302750 #my longitude


def is_iss_overhead():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    # your position is within +5 0r -5 of thw ISS position
    if MY_LAT -5 <= iss_latitude <= MY_LAT + 5 and MY_LONG -5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True



# if the ISS is close to my current position
# and it is currently dark
# then send me an email to look up
# Bonus: run the code every 60 seconds.
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr="kizzy272727@gmail.com",
            to_addrs="kizzy272727@gmail.com",
            msg="Subject: Look up\n\nThe ISS is above you in the sky."
        )