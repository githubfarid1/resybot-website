import argparse
import json
from resy_bot.logging import logging
import os
import sys
from resy_bot.models import ResyConfig, TimedReservationRequest
from resy_bot.manager import ResyManager
import requests
from user_agent import generate_user_agent
from datetime import datetime, date, timedelta
import random
import time
from requests import Session, HTTPError
from resy_bot.errors import NoSlotsError, ExhaustedRetriesError, Get500Error
from datetime import datetime, timedelta
from prettytable import PrettyTable
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import subprocess
from database import Database

db = Database("db.sqlite3")
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# from settings import CLOSE_MESSAGE, CONTINUE_MESSAGE, TRY_MESSAGE, MIN_IDLE_TIME, MAX_IDLE_TIME

CLOSE_MESSAGE = "TES"
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

def random_delay(min_seconds, max_seconds):
    return random.uniform(min_seconds, max_seconds)

def intercept_request(request):
    if "https://api.resy.com/2/config" in request.url:
        try:
            api_key=str(request.headers['authorization']).replace('ResyAPI api_key=', "").replace('"','')
            f = open("logs/api_key2.log", "w")
            f.write(api_key)
        except:
            return request        
    return request

def convert24(time):
    t = datetime.strptime(time, '%I:%M %p')
    return t.strftime('%H:%M')

def convert24wsecond(time):
    t = datetime.strptime(time, '%I:%M:%S %p')
    return t.strftime('%H:%M:%S')

def get_api_key():
    with sync_playwright() as pr:
        wargs = []
        wargs.append('--v=1')
        wargs.append('--no-sandbox')
        wargs.append('--enable-features=NetworkService,NetworkServiceInProcess')
        wargs.append('--enable-automation')
        wargs.append('--disable-popup-blocking')
        wargs.append('--disable-web-security')
        wargs.append('--start-maximized')
        
        browser =  pr.chromium.launch(headless=True, args=wargs)
        page = browser.new_page()
        stealth_sync(page)
        page.on("request", lambda request: intercept_request(request))

        res = page.goto("https://resy.com", wait_until="domcontentloaded", timeout=20000)
        
def check_now(resy_config: dict, reservation_config: dict) -> str:
    config_data = resy_config
    reservation_data = reservation_config
    config = ResyConfig(**config_data)
    manager = ResyManager.build(config)
    timed_request = TimedReservationRequest(**reservation_data)
    return manager.check_reservation_with_retries(timed_request.reservation_request)

def book_now(resy_config: dict, reservation_config: dict) -> str:
    config_data = resy_config
    reservation_data = reservation_config
    config = ResyConfig(**config_data)
    manager = ResyManager.build(config)
    timed_request = TimedReservationRequest(**reservation_data)
    return manager.make_reservation_with_retries(timed_request.reservation_request)

def get_venue_id(resy_config: dict, urladdress: str) -> str:
    config_data = resy_config
    config = ResyConfig(**config_data)
    manager = ResyManager.build(config)
    return manager.get_venue_id(urladdress)
    
def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days+1):
        yield start_date + timedelta(n)

def main():
    parser = argparse.ArgumentParser(description="Resy Bot Check")

    parser.add_argument('-id', '--id', type=str,help="Record ID")

    args = parser.parse_args()
    data = db.getCheckBooking(id=args.id)

    id = data[0]
    url = data[1]
    startdate = data[2]
    enddate = data[3]
    seats = data[4]
    account = data[5]
    timewanted = data[6]
    hoursba = data[7]
    breservation = data[8]
    nonstop = data[9]
    proxyname = data[10]
    minidle = data[11]
    maxidle = data[12]
    retsecs = data[13]
    if breservation == '<Not Set>':
        reservation_type = None
    else:
        reservation_type = breservation

    start_date = datetime.strptime(startdate, '%Y-%m-%d').date()
    end_date = datetime.strptime(enddate, '%Y-%m-%d').date()
    get_api_key()
    file = open("logs/api_key.log", "r")
    # breakpoint()
    api_key = file.read()
    https_proxy = ''
    http_proxy = ''
    proxies = []
    if  proxyname != '<Not Set>':
        proxy = db.getMultiproxy(proxyname)
        proxies = proxy[2].split("\n")
        http_proxy = proxies[0]
        https_proxy = proxies[0]
    
    resy_config = {"api_key": api_key, "token": '', "payment_method_id": 999999, "email":'', "password":'', "http_proxy": http_proxy, "https_proxy": https_proxy, "retry_count": 1, "seconds_retry": float(retsecs)}
    venue_id = get_venue_id(resy_config=resy_config, urladdress=url)
    
    accountdata = db.getAccount(email=account)
    password = accountdata[2]
    token = accountdata[3]
    api_key = accountdata[4]
    payment_method_id = accountdata[5]
    resy_config_booking = {"api_key": api_key, "token": token, "payment_method_id": payment_method_id, "email":account, "password":password, "http_proxy": http_proxy, "https_proxy": https_proxy, "retry_count": 3, "seconds_retry": float(retsecs)}
    strdateyesterday = datetime.strftime(datetime.now()-timedelta(days=1), '%Y-%m-%d')
    flog = open(f"logs/checkbooking_{id}.log", "w")
    stoptime = datetime.now() + timedelta(minutes = 5)
    proxyidx = 1
    try:
        while True:
            if len(proxies) > 0:
                if datetime.now() >= stoptime:
                    stoptime = datetime.now() + timedelta(minutes = 5)
                    resy_config['http_proxy'] = proxies[proxyidx]
                    resy_config['https_proxy'] = proxies[proxyidx]
                    tmpstr = f"IP Proxy updated: {resy_config['http_proxy']}"
                    print(tmpstr)
                    flog.write(tmpstr + "\n")
                    proxyidx += 1
                    if proxyidx == len(proxies):
                        proxyidx = 0

            myTable = PrettyTable(["KEY","VALUE"])
            myTable.align ="l"
            myTable.add_row(["Restaurant URL", url])
            myTable.add_row(["Range Date", f"{startdate} - {enddate}"])
            myTable.add_row(["Seats Wanted", seats])
            print(myTable)
            flog.write(str(myTable))
            print("")
            flog.write("\n")
            for single_date in daterange(start_date, end_date):
                searchdate = single_date.strftime("%Y-%m-%d")
                tmpstr = f"Date Searching: {searchdate}"
                print(tmpstr)
                flog.write(tmpstr + "\n")
                reservation_config = {
                "reservation_request": {
                "party_size": int(seats),
                "venue_id": venue_id,
                "window_hours": int(hoursba),
                "prefer_early": False,
                "ideal_date": searchdate,
                #   "days_in_advance": 14,
                "ideal_hour": int(convert24(timewanted).split(":")[0]),
                "ideal_minute": int(convert24(timewanted).split(":")[1]),
                "preferred_type": reservation_type
                },
                "expected_drop_hour": 9,
                "expected_drop_minute": 0, 
                "expected_drop_second": 0, 
                "expected_drop_year":strdateyesterday.split("-")[0],
                "expected_drop_month":strdateyesterday.split("-")[1],
                "expected_drop_day":strdateyesterday.split("-")[2],
                }
                try:
                    myTable = PrettyTable(["TIME","RESER. TYPE"])
                    myTable.align ="l"
                    slots = check_now(resy_config=resy_config, reservation_config=reservation_config)
                    if len(slots) != 0:
                        print(searchdate)
                        flog.write(searchdate + "\n")
                        tmpstr = f"Found {len(slots)} Slots"
                        print(tmpstr)
                        flog.write(tmpstr + "\n")
                        for slot in slots:
                            dtime = str(slot.config.token).split("/")[-3][:5]
                            reservation = str(slot.config.token).split("/")[-1]
                            myTable.add_row([dtime, reservation])
                        print(myTable)
                        flog.write(str(myTable))
                        # breakpoint()
                        if account != "<Not Set>":
                            try:
                                tmpstr = "Trying to Book.."
                                print(tmpstr)
                                flog.write(tmpstr + "\n")
                                # breakpoint()
                                book_now(resy_config=resy_config_booking, reservation_config=reservation_config)
                                input("Reservation Success..." + CLOSE_MESSAGE)
                                sys.exit()
                            except (ExhaustedRetriesError, NoSlotsError) as e:
                                tmpstr = str(e)
                                print(tmpstr)
                                flog.write(tmpstr + "\n")
                                continue
                except (HTTPError, ExhaustedRetriesError, NoSlotsError) as e:
                    tmpstr = str(e)
                    print(tmpstr)
                    flog.write(tmpstr + "\n")
                except Get500Error as e:
                    tmpstr = str(e)
                    print(tmpstr)
                    flog.write(tmpstr + "\n")

                except Exception as e:
                    print("Bot Error:", str(e))
                print(datetime.now())
                flog.write("\n" + str(datetime.now()) +"\n")
                print("")
                flog.write("\n")
            if nonstop == "No":
                break
            else:
                tmpstr = "____________________________Repeat________________________________"
                print(tmpstr)
                flog.write(tmpstr + "\n\n")
                sleeptime = random_delay(int(minidle), int(maxidle))
                print("Idle Time", int(sleeptime), "seconds")
                time.sleep(sleeptime)
        tmpstr = "Process Finished..."
        flog.write(tmpstr+"\n")
        flog.close()
        input(tmpstr)
    except:
        flog.close()
    
    sys.exit()

if __name__ == "__main__":
    main()
