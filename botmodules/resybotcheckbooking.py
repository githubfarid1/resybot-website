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
# from database import Database
from dotenv import load_dotenv
from telegram_text import PlainText, Bold, Italic, Underline
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbclass import Account, Multiproxy, ReservationType, BotCheck, BotCheckRun


load_dotenv()
PROXY_PL={
  "server": "http://residential-proxy.scrapeops.io:8181",
  "username": "scrapeops",
  "password": "f2d43fe5-5bee-41ab-83f9-da70ae59c60a"
}
PROXY_REQUEST = {
    "http":"http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181",
    "https": "http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181"
}


# db = Database(os.getenv('BASE_FOLDER') + "db.sqlite3")
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# from settings import CLOSE_MESSAGE, CONTINUE_MESSAGE, TRY_MESSAGE, MIN_IDLE_TIME, MAX_IDLE_TIME
engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(os.getenv('DB_USERNAME'), os.getenv('DB_PASS'), os.getenv('DB_PORT'), os.getenv('DB_NAME')) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()
CLOSE_MESSAGE = ""
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

def random_delay(min_seconds, max_seconds):
    return random.uniform(min_seconds, max_seconds)

def intercept_request(request):
    if "https://api.resy.com/2/config" in request.url:
        try:
            api_key=str(request.headers['authorization']).replace('ResyAPI api_key=', "").replace('"','')
            f = open(f"{os.getenv('BASE_FOLDER')}logs/api_key.log", "w")
            f.write(api_key)
        except:
            return request        
    return request

def send_to_telegram(message):

    apiToken = os.getenv('TELEGRAM_TOKEN')
    chatID = os.getenv('TELEGRAM_CHAT_ID')
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message, "parse_mode": "MarkdownV2"})
        print(response.text)
    except Exception as e:
        print(e)

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
        
        # browser =  pr.chromium.launch(headless=True, args=wargs, proxy=PROXY_PL)
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
    parser.add_argument('-apikey', '--apikey', type=str,help="Resy Apikey")

    args = parser.parse_args()
    # data = db.getCheckBookingRun(id=args.id)
     
    data = session.query(BotCheckRun).filter(BotCheckRun.id==args.id).one()
    id = data.id
    url = data.url
    startdate = data.startdate
    enddate = data.enddate
    seats = data.seats
    timewanted = data.timewanted
    hoursba = data.hoursba
    nonstop = data.nonstop
    minidle = data.minidle
    maxidle = data.maxidle
    retsecs = data.retrysec
    proxy_name = data.multiproxy_name
    proxy_value = data.multiproxy_value
    reservation_name = data.reservation_name
    account_email = data.account_email
    account_password = data.account_password
    account_token = data.account_token
    account_api_key = data.account_api_key
    account_payment_method_id = data.account_payment_method_id
    sendmessage = data.sendmessage
    if reservation_name == '<Not Set>':
        reservation_name = None

    # start_date = datetime.strptime(startdate, '%Y-%m-%d').date()
    # end_date = datetime.strptime(enddate, '%Y-%m-%d').date()
    start_date = startdate
    end_date = enddate
    if not args.apikey:
        get_api_key()
        file = open(f"{os.getenv('BASE_FOLDER')}logs/api_key.log", "r")
        api_key = file.read()
    else:
        api_key = args.apikey
    https_proxy = ''
    http_proxy = ''
    # multiproxy = db.getMultiproxy(id=multiproxy_id)
    proxies = []
    if  proxy_name != '<Not Set>':
        # proxy = db.getMultiproxy(proxyname)
        # breakpoint()
        proxies = proxy_value.split("\n")
        http_proxy = proxies[0]
        https_proxy = proxies[0]
    
    resy_config = {"api_key": api_key, "token": '', "payment_method_id": 999999, "email":'', "password":'', "http_proxy": http_proxy, "https_proxy": https_proxy, "retry_count": 1, "seconds_retry": float(retsecs)}
    # resy_config = {"api_key": api_key, "token": '', "payment_method_id": 999999, "email":'', "password":'', "http_proxy": '', "https_proxy": '', "retry_count": 1, "seconds_retry": float(retsecs)}

    venue_id = get_venue_id(resy_config=resy_config, urladdress=url)
    # breakpoint()
    # accountdata = db.getAccount(id=account_id)

    if account_email != "<Not Set>":
        resy_config_booking = {"api_key": account_api_key, "token": account_token, "payment_method_id": account_payment_method_id, "email":account_email, "password":account_password, "http_proxy": http_proxy, "https_proxy": https_proxy, "retry_count": 3, "seconds_retry": float(retsecs)}
    
    strdateyesterday = datetime.strftime(datetime.now()-timedelta(days=1), '%Y-%m-%d')
    flog = open(f"{os.getenv('BASE_FOLDER')}logs/checkbookrun_terminal_{id}.log", "w")
    stoptime = datetime.now() + timedelta(minutes = 5)
    proxyidx = 1
    try:
        while True:
            if len(proxies) > 1:
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
                "ideal_hour": int(timewanted.strftime("%H:%M:%S").split(":")[0]),
                "ideal_minute": int(timewanted.strftime("%H:%M:%S").split(":")[1]),
                "preferred_type": reservation_name,
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
                            breakpoint()
                            dtime = str(slot.config.token).split("/")[-3][:5]
                            reservation = str(slot.config.token).split("/")[-1]
                            myTable.add_row([dtime, reservation])
                        print(myTable)
                        flog.write(str(myTable))
                        if sendmessage == True:
                            dsearch = single_date.strftime("%Y-%m-%d")
                            urlstr = f"{url}?{dsearch}&seats={seats}" 
                            tmpstr = PlainText(f"Found slot at {dsearch}\n{str(myTable)}") 
                            send_to_telegram(tmpstr.to_markdown() + f"\n[Go To Resy]({urlstr})")
                        if account_email != "<Not Set>":
                            try:
                                tmpstr = "Trying to Book.."
                                print(tmpstr)
                                flog.write(tmpstr + "\n")
                                book_now(resy_config=resy_config_booking, reservation_config=reservation_config)
                                print("Reservation Success..." + CLOSE_MESSAGE)
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
                    if len(proxies) > 1:
                        # go to next proxy
                        stoptime = datetime.now() + timedelta(minutes = 5)
                        resy_config['http_proxy'] = proxies[proxyidx]
                        resy_config['https_proxy'] = proxies[proxyidx]
                        tmpstr = f"IP Proxy updated: {resy_config['http_proxy']}"
                        print(tmpstr)
                        flog.write(tmpstr + "\n")
                        proxyidx += 1
                        if proxyidx == len(proxies):
                            proxyidx = 0

                except Exception as e:
                    print("Bot Error:", str(e))
                print(datetime.now())
                flog.write("\n" + str(datetime.now()) +"\n")
                print("")
                flog.write("\n")
            if nonstop == False:
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
        print(tmpstr)
    except:
        flog.close()
    
    sys.exit()

if __name__ == "__main__":
    main()
