import datetime, requests
from suntime import Sun, SunTimeException
from pytz import timezone

lat = 49.282730
lon = -123.120735
time_format = "%I:%M %p"
ntfy_id = "aaeifcaendiwodjwitow2sjeo329sjeo29dkwofjajeifiajq"

sun = Sun(lat, lon)

# Get today's sunrise and sunset in UTC
today_sr = sun.get_local_sunrise_time().astimezone(timezone("US/Pacific")).strftime(time_format)
today_ss = sun.get_local_sunset_time().astimezone(timezone("US/Pacific")).strftime(time_format)

today = datetime.datetime.now().strftime("%A")
requests.post("https://ntfy.sh/" + ntfy_id,
    data=f"Sunrise: {today_sr} & Sunset: {today_ss}",
    headers={
        "Title": f"{today}'s Sun Times",
        "Tags": "sunrise_over_mountains"
    })