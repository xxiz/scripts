# You can run this script by running python3 sunsetsunrise.py
import datetime, requests, os
from suntime import Sun
from pytz import timezone

# Enter your city's coordinates here
lat = 49.282730
lon = -123.120735
time_format = "%I:%M %p"

# get id from env
ntfy_id = os.environ['NTFY_ID']

# default value is https://ntfy.sh/
ntfy_server = os.environ['NTFY_SERVER']

sun = Sun(lat, lon)

# Get today's sunrise and sunset in UTC
today_sr = sun.get_local_sunrise_time().astimezone(timezone("US/Pacific")).strftime(time_format)
today_ss = sun.get_local_sunset_time().astimezone(timezone("US/Pacific")).strftime(time_format)

today = datetime.datetime.now().strftime("%A")
requests.post(ntfy_server + ntfy_id,
    data=f"Sunrise: {today_sr} & Sunset: {today_ss}",
    headers={
        "Title": f"{today}'s Sun Times",
        "Tags": "sunrise_over_mountains"
    })
