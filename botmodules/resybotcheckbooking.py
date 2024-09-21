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
from requests.exceptions import SSLError
from requests import Session, HTTPError, ConnectionError
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
from dbclass import BotCheckRun, Setting
from urllib.parse import quote, unquote, quote_plus, unquote_plus

load_dotenv()

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# from settings import CLOSE_MESSAGE, CONTINUE_MESSAGE, TRY_MESSAGE, MIN_IDLE_TIME, MAX_IDLE_TIME
engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(os.getenv('DB_USERNAME'), os.getenv('DB_PASS'), os.getenv('DB_PORT'), os.getenv('DB_NAME')) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()
CLOSE_MESSAGE = ""
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

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
    apiToken = session.query(Setting).filter(Setting.key=='TELEGRAM_TOKEN').one().value
    chatID = session.query(Setting).filter(Setting.key=='TELEGRAM_CHAT_ID').one().value
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message, "parse_mode": "HTML"})
        # print(response.text)
    except Exception as e:
        print(e)

def parse_to_html(slot, url, seats, venue_id, mentionto):
    restaurant_name = str(url).split("/")[-1]
    tokensplit = slot.config.token.split("/")
    mdict = {"venueName":restaurant_name,"featureRecaptcha":False,"badge":None,"colors":{"background":None,"font":None},"isGda":False,"serviceTypeId":2,"templateId":tokensplit[4],"time":f"{tokensplit[6]} {tokensplit[8]}","token":slot.config.token,"type":slot.config.type,"hasAddOns":False,"hasMenus":False,"serviceTypeName":"","serviceTypeKey":""}
    mdictstr = json.dumps(mdict).replace(': ',':').replace(' "','"')
    link = f'{quote_plus(mdictstr)}&date={tokensplit[6]}&seats={seats}&tableConfigId={quote_plus(slot.config.token)}&venueId={venue_id}'
    link = f'https://widgets.resy.com/#/reservation-details?reservation={link}'
    # breakpoint()
    # html = f"Username: <strong>@{username}</strong>\n"
    html = f"Restaurant Name: <strong>{restaurant_name}</strong>\n"
    html += f"Date: <strong>{tokensplit[6]}</strong>\n"
    html += f"Time: <strong>{tokensplit[8][0:-3]}</strong>\n"
    html += f"Seats: <strong>{seats}</strong>\n"
    html += f"Mentions: <strong>{mentionto}</strong>\n"
    html += f'<a href="{link}">Booking</a>'
    return html

def get_api_key():
    proxy_helper = session.query(Setting).filter(Setting.key=='PROXY_HELPER').one().value
    proxy_helper = proxy_helper.replace("http://","")
    if len(proxy_helper.split("@")) == 2:
        proxy_server = proxy_helper.split("@")[-1] 
        urlprox = proxy_server.split("//")[-1]
        urlprox = f"http://{urlprox}"
        username = proxy_helper.split("@")[0].split(":")[0]
        password = proxy_helper.split("@")[0].split(":")[1]
        proxydict = {
            "server": urlprox,
            "username": username,
            "password": password
        }
    else:
        proxy_server = proxy_helper.split("@")[-1] 
        urlprox = proxy_server.split("//")[-1]
        urlprox = f"http://{urlprox}"
        proxydict = {
            "server": urlprox,
            "username": "",
            "password": ""
        }
    with sync_playwright() as pr:
        wargs = []
        wargs.append('--v=1')
        wargs.append('--no-sandbox')
        wargs.append('--enable-features=NetworkService,NetworkServiceInProcess')
        wargs.append('--enable-automation')
        wargs.append('--disable-popup-blocking')
        wargs.append('--disable-web-security')
        wargs.append('--start-maximized')
        
        browser =  pr.chromium.launch(headless=True, args=wargs, proxy=proxydict)

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

def check_static_proxy(proxies):
    for proxy in proxies:
        if proxy['status']:
            return True
    return False

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
    proxy_value2 = data.multiproxy_value2
    reservation_name = data.reservation_name
    account_email = data.account_email
    account_password = data.account_password
    account_token = data.account_token
    account_api_key = data.account_api_key
    account_payment_method_id = data.account_payment_method_id
    sendmessage = data.sendmessage
    mentionto = data.mentionto
    minproxy = data.minproxy
    maxproxy = data.maxproxy
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
    proxies = []
    if  proxy_name != '<Not Set>':
        for proxy in proxy_value.split("\n"):
            urlprox = proxy.split("//")[-1]
            proxies.append({'proxy': f"http://{urlprox}", 'status': True})
    
    proxy_helper = session.query(Setting).filter(Setting.key=='PROXY_HELPER').one().value
    
    if "http://" not in proxy_helper:
        proxy_helper = f"http://{proxy_helper}"
    resy_config_venue = {"api_key": api_key, "token": '', "payment_method_id": 999999, "email":'', "password":'', "http_proxy": proxy_helper, "https_proxy": proxy_helper, "retry_count": 3, "seconds_retry": float(retsecs)}

    resy_config_checker = {"api_key": api_key, "token": '', "payment_method_id": 999999, "email":'', "password":'', "http_proxy": proxies[0]['proxy'], "https_proxy": proxies[0]['proxy'], "retry_count": 1, "seconds_retry": float(retsecs)}

    venue_id = get_venue_id(resy_config=resy_config_venue, urladdress=url)
    if not venue_id:
        print("Proxy error or venue_id not found")
        sys.exit()
    # venue_id = '64869'
    if account_email != "<Not Set>":
        resy_config_booking = {"api_key": account_api_key, "token": account_token, "payment_method_id": account_payment_method_id, "email":account_email, "password":account_password, "http_proxy": proxy_helper, "https_proxy": proxy_helper, "retry_count": 3, "seconds_retry": float(retsecs)}
    
    strdateyesterday = datetime.strftime(datetime.now()-timedelta(days=1), '%Y-%m-%d')
    flog = open(f"{os.getenv('BASE_FOLDER')}logs/checkbookrun_terminal_{id}.log", "w")
    

    # stoptime = datetime.now() + timedelta(minutes = random_delay(minproxy, maxproxy))
    
    reservation_config = {
    "reservation_request": {
    "party_size": int(seats),
    "venue_id": venue_id,
    "window_hours": int(hoursba),
    "prefer_early": False,
    "ideal_date": None,
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



    def check_availability(resy_config, datewanted):
        reservation_config["reservation_request"]["ideal_date"] = datewanted
        # breakpoint()
        slots = check_now(resy_config=resy_config, reservation_config=reservation_config)
        return slots        
    
    
    myTable = PrettyTable(["KEY","VALUE"])
    myTable.align ="l"
    myTable.add_row(["Restaurant URL", url])
    myTable.add_row(["Range Date", f"{startdate} - {enddate}"])
    myTable.add_row(["Time wanted", timewanted.strftime("%H:%M")])
    myTable.add_row(["Hours before and After", hoursba])

    myTable.add_row(["Seats Wanted", seats])
    print(myTable)
    flog.write(str(myTable))
    print("")
    flog.write("\n")
    proxyidx = 0
    excount = int(random_delay(minproxy, maxproxy))
    usecount = 0
    booklist = []
    while True:
        for single_date in daterange(start_date, end_date):
            searchdate = single_date.strftime("%Y-%m-%d")
            bookable = False
            while True:
                try:
                    if len(proxies) > 1:
                        # if not check_static_proxy(proxies):
                        #     print("All proxies malfunction")
                        #     sys.exit()
                        if proxyidx > len(proxies)-1:
                            proxyidx = 0
                        if proxies[proxyidx]['status']:
                            resy_config_checker['http_proxy'] = proxies[proxyidx]['proxy']
                            resy_config_checker['https_proxy'] = proxies[proxyidx]['proxy']
                        else:
                            raise Get500Error
                    
                    myTable = PrettyTable(["KEY","VALUE"])
                    myTable.align ="l"
                    slots = check_availability(resy_config=resy_config_checker, datewanted=searchdate)
                    if len(slots) != 0:
                        bookable = True
                        print(searchdate)
                        flog.write(searchdate + "\n")
                        tmpstr = f"Found {len(slots)} Slots"
                        flog.write(tmpstr + "\n")
                        htmllist = []
                        for slot in slots:
                            dtime = str(slot.config.token).split("/")[-3][:5]
                            reservation = str(slot.config.token).split("/")[-1]
                            html = parse_to_html(slot=slot, url=url, seats=seats, venue_id=venue_id, mentionto=mentionto)
                            myTable.add_row([dtime, reservation])
                            htmllist.append(html)
                        print(myTable)
                        if sendmessage == True:
                            for html in htmllist:
                                send_to_telegram(html)
                    usecount += 1
                    if usecount >= excount:
                        usecount = 0
                        print("Proxy use count reach limit", excount)
                        excount = int(random_delay(minproxy, maxproxy))
                        proxyidx += 1
                        break
                    break
                except (Get500Error, SSLError, ConnectionError) as e:
                    # proxies[proxyidx]['status'] = False
                    proxyidx += 1
                    print("Proxy Error, go to next proxy")
                    continue
                except (ExhaustedRetriesError, NoSlotsError, IndexError) as e:
                    print(searchdate)
                    print(str(e))
                    bookable = False
                    break
                except Exception as e:
                    print("Bot Error:", str(e))
                    sys.exit()
            # sleeptime = random_delay(int(minidle), int(maxidle))
            # print("Idle Time", int(sleeptime), "seconds")
            # time.sleep(sleeptime)
            # breakpoint()            
            if account_email != "<Not Set>" and bookable and reservation_config["reservation_request"]["ideal_date"] not in booklist:
                try:
                    # breakpoint()
                    tmpstr = "Trying to Book.."
                    print(tmpstr)
                    flog.write(tmpstr + "\n")
                    resy_book_token = book_now(resy_config=resy_config_booking, reservation_config=reservation_config)
                    # breakpoint()
                    booklist.append(reservation_config["reservation_request"]["ideal_date"])
                    print("Reservation Success..." + CLOSE_MESSAGE)
                    # sys.exit()
                except (ExhaustedRetriesError, NoSlotsError) as e:
                    tmpstr = str(e)
                    print(tmpstr)
                    flog.write(tmpstr + "\n")
                    continue
                except (Get500Error, SSLError, ConnectionError) as e:
                    print("Proxy Error, Booking Failed")
                    continue

        if not nonstop:
            break


if __name__ == "__main__":
    main()
