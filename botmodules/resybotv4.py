import argparse
import json
from resy_bot.logging import logging
import os
import sys
from resy_bot.models import ResyConfig, TimedReservationRequest
from resy_bot.manager import ResyManager
import requests
from user_agent import generate_user_agent
from datetime import datetime
import random
import time
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import CLOSE_MESSAGE, CHROME_USER_DATA, CONTINUE_MESSAGE

logger = logging.getLogger(__name__)
logger.setLevel("ERROR")

def random_delay(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def convert24(time):
    t = datetime.strptime(time, '%I:%M %p')
    return t.strftime('%H:%M')

def wait_for_drop_time(resy_config: dict, reservation_config: dict) -> str:
    logger.info("waiting for drop time!")

    config_data = resy_config

    reservation_data = reservation_config

    config = ResyConfig(**config_data)
    manager = ResyManager.build(config)

    timed_request = TimedReservationRequest(**reservation_data)

    return manager.make_reservation_at_opening_time(timed_request)

def main():
    parser = argparse.ArgumentParser(description="Resy Bot v4")
    parser.add_argument('-u', '--url', type=str,help="Base URL")
    parser.add_argument('-d', '--date', type=str,help="Date wanted")
    parser.add_argument('-t', '--time', type=str,help="Time wanted")
    parser.add_argument('-s', '--seats', type=str,help="Seats count")
    parser.add_argument('-r', '--reservation', type=str,help="Reservation type")
    parser.add_argument('-cp', '--chprofile', type=str,help="Chrome Profile Name")
    parser.add_argument('-rd', '--rdate', type=str,help="Run Date")
    parser.add_argument('-rt', '--rtime', type=str,help="Run Time")

    args = parser.parse_args()
    if not args.url or not args.date or not args.time or not args.seats or not args.reservation or not args.chprofile or not args.rdate or not args.rtime:
        input(" ".join(['Please add complete parameters, ex: python resybotv4 -u [url] -d [dd-mm-yyyy] -t [h:m am/pm] -s [seats_count] -p [period] -r [reservation_type] -cp [chrome_profile] -rd [rdate] -rt [rtime]', CLOSE_MESSAGE]))
        sys.exit()
    file = open("profilelist.json", "r")
    profilelist = json.load(file)
    for profile in profilelist:
        if profile['profilename'] == args.chprofile:
            break
    
    headers = {
        "Authorization": 'ResyAPI api_key="{}"'.format(profile['api_key']),
        "X-Resy-Auth-Token": profile['token'],
        "X-Resy-Universal-Auth": profile['token'],
        "Origin": "https://resy.com",
        "X-origin": "https://resy.com",
        "Referrer": "https://resy.com/",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": generate_user_agent(),
        'Cache-Control': "no-cache",
    }
    params = {
        'url_slug': str(args.url).split("/")[-1],
        'location': str(args.url).split("/")[-3],
    }    
    response = requests.get('https://api.resy.com/3/venue', params=params, headers=headers)
    venue_id = response.json()['id']['resy']

    # resy_config = {"api_key": profile['api_key'], "token": profile["token"], "payment_method_id":profile["payment_method_id"], "email":profile["email"], "password":profile["password"]}
    resy_config = {"api_key": profile['api_key'], "token": profile["token"], "payment_method_id":99999999, "email":profile["email"], "password":profile["password"]}
    
    if args.reservation == '<Not Set>':
        reservation_type = None
    else:
        reservation_type = args.reservation
    
    reservation_config = {
    "reservation_request": {
      "party_size": args.seats,
      "venue_id": venue_id,
      "window_hours": 1,
      "prefer_early": False,
      "ideal_date": args.date,
    #   "days_in_advance": 14,
      "ideal_hour": int(convert24(args.time).split(":")[0]),
      "ideal_minute": int(convert24(args.time).split(":")[1]),
      "preferred_type": reservation_type
    },
      "expected_drop_hour": int(convert24(args.rtime).split(":")[0]),
      "expected_drop_minute": int(convert24(args.rtime).split(":")[1]), 
      "expected_drop_year":str(args.rdate).split("-")[0],
      "expected_drop_month":str(args.rdate).split("-")[1],
      "expected_drop_day":str(args.rdate).split("-")[2],
    }
    try:
        wait_for_drop_time(resy_config=resy_config, reservation_config=reservation_config)
        input("Reservation Success..." + CLOSE_MESSAGE)
    except Exception as e:
        input(e)
    # while True:
    #     try:
    #         wait_for_drop_time(resy_config=resy_config, reservation_config=reservation_config)
    #         input("Reservation Success..." + CLOSE_MESSAGE)
    #         break
    #     except:
    #         tsleep = random.uniform(1, 5)
    #         # print("The Booking seat not Found, Bot sleep", int(tsleep), "seconds")
    #         time.sleep(tsleep)
    #         continue

if __name__ == "__main__":
    main()
