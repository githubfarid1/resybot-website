import argparse
import json
import os
import sys
from resy_bot.models import ResyConfig, TimedReservationRequest
from resy_bot.manager import ResyManager
from user_agent import generate_user_agent
from datetime import datetime
import random
import time
from requests import Session, HTTPError
from resy_bot.errors import NoSlotsError, ExhaustedRetriesError
from datetime import datetime, timedelta
from prettytable import PrettyTable
from resy_bot.logging import logging
from database import Database
db = Database("db.sqlite3")

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

CLOSE_MESSAGE = " --> Process Complete..."
TRY_MESSAGE=" --> Bot will try again..."

def random_delay(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

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
    return manager.make_reservation_with_retries(timed_request.reservation_request)

def main():
    parser = argparse.ArgumentParser(description="Resy Bot v5b")
    parser.add_argument('-id', '--id', type=str,help="ID botrun")
    args = parser.parse_args()
    if not args.id:
        sys.exit()
    botrun = db.getBotRunById(args.id)    
    # breakpoint()
    url=botrun[1]
    date=botrun[2]
    stime=botrun[3][:5]
    seats=botrun[5]
    reservation=botrun[14]
    accountemail=botrun[17]
    rdate=botrun[6]
    rtime=botrun[7]
    rhours=botrun[4]
    runnow='Yes' if botrun[8] else 'No' 
    nonstop='Yes' if botrun[9] else 'No'
    duration=botrun[10]
    proxy=botrun[14]
    retry=botrun[11]
    minidle=botrun[12]
    maxidle=botrun[13]
    apikey=botrun[19]
    token=botrun[20]
    payment_method_id = botrun[21]
    password = botrun[18]
    http_proxy= botrun[15] if botrun[15] else ''
    https_proxy=botrun[16] if botrun[16] else ''
    # breakpoint()
    myTable = PrettyTable(["KEY","VALUE"])
    myTable.align ="l"
    myTable.add_row(["Restaurant", url.split("/")[-1]])
    myTable.add_row(["Date Wanted", date])
    myTable.add_row(["Time Wanted", stime])
    myTable.add_row(["Seats", seats])
    myTable.add_row(["Reservation Type", reservation])
    myTable.add_row(["Account", accountemail])
    myTable.add_row(["Bot Run Date", rdate])
    myTable.add_row(["Bot Run Time",rtime])
    myTable.add_row(["Range Hours",rhours])
    myTable.add_row(["Run Immediately", runnow])
    myTable.add_row(["Non Stop Checking", nonstop])
    myTable.add_row(["Bot Duration", f"{duration} Minute"])
    myTable.add_row(["Proxy", proxy])
    myTable.add_row(["Retry Count", retry])
    myTable.add_row(["Min Idle Time", minidle])
    myTable.add_row(["Max Idle Time", maxidle])
    print(myTable)
    headers = {
        "Authorization": 'ResyAPI api_key="{}"'.format(apikey),
        "X-Resy-Auth-Token": token,
        "X-Resy-Universal-Auth": token,
        "Origin": "https://resy.com",
        "X-origin": "https://resy.com",
        "Referrer": "https://resy.com/",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": generate_user_agent(),
        'Cache-Control': "no-cache",
    }
    params = {
        'url_slug': str(url).split("/")[-1],
        'location': str(url).split("/")[-3],
    }
    try:
        session = Session()    
        response = session.get('https://api.resy.com/3/venue', params=params, headers=headers)
        venue_id = response.json()['id']['resy']
        resy_config = {"api_key": apikey, "token": token, "payment_method_id":payment_method_id, "email":accountemail, "password":password, "http_proxy":http_proxy, "https_proxy": https_proxy, "retry_count": int(retry)}
        
        if reservation == '<Not Set>':
            reservation_type = None
        else:
            reservation_type = reservation

        reservation_config = {
        "reservation_request": {
        "party_size": seats,
        "venue_id": venue_id,
        "window_hours": rhours,
        "prefer_early": False,
        "ideal_date": date,
        #   "days_in_advance": 14,
        "ideal_hour": int(stime.split(":")[0]),
        "ideal_minute": int(stime.split(":")[1]),
        "preferred_type": reservation_type
        },
        "expected_drop_hour": int(rtime.split(":")[0]),
        "expected_drop_minute": int(rtime.split(":")[1]), 
        "expected_drop_second": int(rtime.split(":")[2]), 
        "expected_drop_year":str(rdate).split("-")[0],
        "expected_drop_month":str(rdate).split("-")[1],
        "expected_drop_day":str(rdate).split("-")[2],
        }
    except KeyError as e:
        print("KeyError", e)
        print("Error Accurred " + CLOSE_MESSAGE)
        sys.exit()
    except Exception as e:
        print("Exception", e)
        print("Error Accurred " + CLOSE_MESSAGE)
        sys.exit()
    
    if nonstop == 'No':
        try:
            if runnow == "No":
                wait_for_drop_time(resy_config=resy_config, reservation_config=reservation_config)
            else:
                run_now(resy_config=resy_config, reservation_config=reservation_config)
            print("Reservation Success..." + CLOSE_MESSAGE)
        except  (HTTPError, ExhaustedRetriesError, NoSlotsError) as e:
            print("Reservation Failed: " + str(e) + CLOSE_MESSAGE)
        except IndexError as e:
            print("Reservation Error: " + str(e) + CLOSE_MESSAGE)
        except Exception as e:
            print("Application Error: " + str(e) + CLOSE_MESSAGE)

    else:
        if runnow == "No": 
            stoptime = datetime.strptime(f"{rdate} {rtime}", '%Y-%m-%d %H:%M:%S') + timedelta(minutes = int(duration))
        else:
            stoptime = datetime.now() + timedelta(minutes = int(duration))
        # breakpoint() 
        if datetime.strptime(f"{rdate} {rtime}", '%Y-%m-%d %H:%M:%S') < datetime.now():
            stoptime = datetime.now() + timedelta(minutes = int(duration))
        while True:
            # sleeptime = random.uniform(10, 30)
            if int(duration) != 0 and datetime.now() >= stoptime:
                print(f"Duration time reached -> {duration} minutes")
                break
            sleeptime = random.uniform(int(minidle), int(maxidle))
            try:
                if runnow == "No":
                    wait_for_drop_time(resy_config=resy_config, reservation_config=reservation_config)
                else:
                    run_now(resy_config=resy_config, reservation_config=reservation_config)
                print("Reservation Success..." + CLOSE_MESSAGE)
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
