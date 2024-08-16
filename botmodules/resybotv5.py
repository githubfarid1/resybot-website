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
from requests import Session, HTTPError
from resy_bot.errors import NoSlotsError, ExhaustedRetriesError
from datetime import datetime, timedelta
from prettytable import PrettyTable

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import CLOSE_MESSAGE, CONTINUE_MESSAGE, TRY_MESSAGE, MIN_IDLE_TIME, MAX_IDLE_TIME

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

def random_delay(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def convert24(time):
    t = datetime.strptime(time, '%I:%M %p')
    return t.strftime('%H:%M')

def convert24wsecond(time):
    t = datetime.strptime(time, '%I:%M:%S %p')
    return t.strftime('%H:%M:%S')

def wait_for_drop_time(resy_config: dict, reservation_config: dict) -> str:
    logger.info("waiting for drop time!")
    config_data = resy_config
    reservation_data = reservation_config
    config = ResyConfig(**config_data)
    manager = ResyManager.build(config)
    timed_request = TimedReservationRequest(**reservation_data)
    return manager.make_reservation_at_opening_time(timed_request)

def run_now(resy_config: dict, reservation_config: dict) -> str:
    config_data = resy_config
    reservation_data = reservation_config
    config = ResyConfig(**config_data)
    manager = ResyManager.build(config)
    timed_request = TimedReservationRequest(**reservation_data)
    # breakpoint()
    return manager.make_reservation_with_retries(timed_request.reservation_request)

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
    parser.add_argument('-rh', '--rhours', type=str,help="Range Hours")
    parser.add_argument('-rn', '--runnow', type=str,help="Run Now")
    parser.add_argument('-ns', '--nonstop', type=str,help="Non Stop Checking")
    parser.add_argument('-dr', '--duration', type=str,help="Duration time")
    parser.add_argument('-up', '--proxy', type=str,help="Use Proxy")
    parser.add_argument('-re', '--retry', type=str,help="Retry Count")
    parser.add_argument('-mn', '--minidle', type=str,help="Min Idle Time")
    parser.add_argument('-mx', '--maxidle', type=str,help="Max Idle Time")

    args = parser.parse_args()
    if not args.url or not args.date or not args.time or not args.seats or not args.reservation or not args.chprofile or not args.rdate or not args.rtime or not args.rhours or not args.runnow or not args.nonstop or not args.duration or not args.duration or not args.proxy or not args.retry or not args.minidle or not args.maxidle:
        input(" ".join(['Please add complete parameters, ex: python resybotv4b -u [url] -d [dd-mm-yyyy] -t [h:m am/pm] -s [seats_count] -p [period] -r [reservation_type] -cp [chrome_profile] -rd [rdate] -rt [rtime] -rh [rhours] -rn [runnow] -ns [nonstop] -dr [duration] -up [proxy] -re [retry] -mn [minidle] -mx [maxidle]', CLOSE_MESSAGE]))
        sys.exit()
    # breakpoint()
    
    file = open("profilelist.json", "r")
    profilelist = json.load(file)
    for profile in profilelist:
        if profile['email'] == args.chprofile:
            break
    myTable = PrettyTable(["KEY","VALUE"])
    myTable.align ="l"
    myTable.add_row(["Restaurant", args.url.split("/")[-1]])
    myTable.add_row(["Date Wanted", args.date])
    myTable.add_row(["Time Wanted", args.time])
    myTable.add_row(["Seats", args.seats])
    myTable.add_row(["Reservation Type", args.reservation])
    myTable.add_row(["Account", profile['email']])
    myTable.add_row(["Bot Run Date", args.rdate])
    myTable.add_row(["Bot Run Time",args.rtime])
    myTable.add_row(["Range Hours",args.rhours])
    myTable.add_row(["Run Immediately", args.runnow])
    myTable.add_row(["Non Stop Checking", args.nonstop])
    myTable.add_row(["Bot Duration", f"{args.duration} Minute"])
    myTable.add_row(["Proxy", args.proxy])
    myTable.add_row(["Retry Count", args.retry])
    myTable.add_row(["Min Idle Time", args.minidle])
    myTable.add_row(["Max Idle Time", args.maxidle])
    # myTable.add_row(["URL", args.url])
    print(myTable)
    # breakpoint()
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
    try:
        session = Session()    
        response = session.get('https://api.resy.com/3/venue', params=params, headers=headers)
        venue_id = response.json()['id']['resy']
        https_proxy = ''
        http_proxy = ''
        if args.proxy != '<Not Set>':
            file = open("proxylist.json", "r")
            listvalue = json.load(file)
            proxy = [prof for prof in listvalue if prof['profilename']==args.proxy]
            http_proxy = proxy[0]['http_proxy']
            https_proxy = proxy[0]['https_proxy']
        resy_config = {"api_key": profile['api_key'], "token": profile["token"], "payment_method_id":profile["payment_method_id"], "email":profile["email"], "password":profile["password"], "http_proxy":http_proxy, "https_proxy": https_proxy, "retry_count": int(args.retry)}
        
        if args.reservation == '<Not Set>':
            reservation_type = None
        else:
            reservation_type = args.reservation
        # breakpoint()
        reservation_config = {
        "reservation_request": {
        "party_size": args.seats,
        "venue_id": venue_id,
        "window_hours": args.rhours,
        "prefer_early": False,
        "ideal_date": args.date,
        #   "days_in_advance": 14,
        "ideal_hour": int(convert24(args.time).split(":")[0]),
        "ideal_minute": int(convert24(args.time).split(":")[1]),
        "preferred_type": reservation_type
        },
        "expected_drop_hour": int(convert24wsecond(args.rtime).split(":")[0]),
        "expected_drop_minute": int(convert24wsecond(args.rtime).split(":")[1]), 
        "expected_drop_second": int(convert24wsecond(args.rtime).split(":")[2]), 
        "expected_drop_year":str(args.rdate).split("-")[0],
        "expected_drop_month":str(args.rdate).split("-")[1],
        "expected_drop_day":str(args.rdate).split("-")[2],
        }
    except KeyError as e:
        print("KeyError", e)
        input("Error Accurred " + CLOSE_MESSAGE)
        sys.exit()
    except Exception as e:
        print("Exception", e)
        input("Error Accurred " + CLOSE_MESSAGE)
        sys.exit()
    
    if args.nonstop == 'No':
        try:
            if args.runnow == "No":
                wait_for_drop_time(resy_config=resy_config, reservation_config=reservation_config)
            else:
                run_now(resy_config=resy_config, reservation_config=reservation_config)
            input("Reservation Success..." + CLOSE_MESSAGE)
        except  (HTTPError, ExhaustedRetriesError, NoSlotsError) as e:
            input("Reservation Failed: " + str(e) + CLOSE_MESSAGE)
        except IndexError as e:
            input("Reservation Error: " + str(e) + CLOSE_MESSAGE)
        except Exception as e:
            input("Application Error: " + str(e) + CLOSE_MESSAGE)

    else:
        if args.runnow == "No": 
            stoptime = datetime.strptime(f"{args.rdate} {args.rtime}", '%Y-%m-%d %I:%M:%S %p') + timedelta(minutes = int(args.duration))
        else:
            stoptime = datetime.now() + timedelta(minutes = int(args.duration))

        if datetime.strptime(f"{args.rdate} {args.rtime}", '%Y-%m-%d %I:%M:%S %p') < datetime.now():
            stoptime = datetime.now() + timedelta(minutes = int(args.duration))
        while True:
            # sleeptime = random.uniform(10, 30)
            if int(args.duration) != 0 and datetime.now() >= stoptime:
                input(f"Duration time reached -> {args.duration} minutes")
                break
            sleeptime = random.uniform(int(args.minidle), int(args.maxidle))
            try:
                if args.runnow == "No":
                    wait_for_drop_time(resy_config=resy_config, reservation_config=reservation_config)
                else:
                    run_now(resy_config=resy_config, reservation_config=reservation_config)
                input("Reservation Success..." + CLOSE_MESSAGE)
                break
            except  (HTTPError, ExhaustedRetriesError, NoSlotsError) as e:
                print("Reservation Failed: " + str(e) + TRY_MESSAGE)
                print("idle time", int(sleeptime), "seconds")
                time.sleep(sleeptime)
                continue
            except IndexError as e:
                print("Reservation Error: " + str(e) + TRY_MESSAGE)
                print("idle time", int(sleeptime), "seconds")
                time.sleep(sleeptime)
                continue
            except Exception as e:
                print("Application Error: " + str(e) + TRY_MESSAGE)
                print("idle time", int(sleeptime), "seconds")
                time.sleep(sleeptime)
                continue

if __name__ == "__main__":
    main()
