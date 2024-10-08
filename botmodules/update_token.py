import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
# import logging
import random
import time
from playwright_stealth import stealth_sync
import logging
import re
import sys
import argparse
from subprocess import Popen, check_call
from user_agent import generate_user_agent
import json
import requests
from resy_bot.logging import logging
# from database import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbclass import BotCheckRun, Setting, Account
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

# db = Database("db.sqlite3")
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
CLOSE_MESSAGE = "tes"
PROXY_PL={
  "server": "http://residential-proxy.scrapeops.io:8181",
  "username": "scrapeops",
  "password": "f2d43fe5-5bee-41ab-83f9-da70ae59c60a"
}
PROXY_REQUEST = {
    "http":"http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181",
    "https": "http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181"
}

load_dotenv()

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(os.getenv('DB_USERNAME'), os.getenv('DB_PASS'), os.getenv('DB_PORT'), os.getenv('DB_NAME')) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()

# get proxy for playwright
proxy_helper = session.query(Setting).filter(Setting.key=='PROXY_HELPER').one().value
if len(proxy_helper.split("@")) == 2:
    proxy_server = proxy_helper.split("@")[-1] 
    urlprox = proxy_server.split("//")[-1]
    urlprox = f"{urlprox}"
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

# get proxy for requests
proxytmp = proxy_helper.split("//")[-1]
proxydict2 = {"http":f"http://{proxytmp}",
              "https":f"http://{proxytmp}",
}
# breakpoint()
def login_to_resy(page, email, password):
    """Login to Resy with enhanced stability and error handling."""
    try:
        page.wait_for_selector('.AnnouncementModal__icon-close', timeout=5000)
        page.click('.AnnouncementModal__icon-close')
    except Exception:
        logging.info("No announcement modal to close.")
    # breakpoint()
    page.click("text=Log in", timeout=30000)
    page.click("text=Use Email and Password instead", timeout=30000)

    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    
    page.click('[name="login_form"] button', timeout=10000)
    page.evaluate("() => document.fonts.ready")

def random_delay(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def intercept_request(request, profilename):
    # we can update requests with custom headers
    api_key = ''
    token = ''
    if "https://api.resy.com/2/config" in request.url:
        try:
            token = request.headers['x-resy-auth-token']
            api_key=str(request.headers['authorization']).replace('ResyAPI api_key=', "").replace('"','')
            headers = {
                "Authorization": f'ResyAPI api_key="{api_key}"',
                "X-Resy-Auth-Token": token,
                "X-Resy-Universal-Auth": token,
                "Origin": "https://resy.com",
                "X-origin": "https://resy.com",
                "Referrer": "https://resy.com/",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": generate_user_agent(),
                'Cache-Control': "no-cache",
            }
            response = requests.get('https://api.resy.com/2/user', headers=headers, proxies=proxydict2)
            # response = requests.get('https://api.resy.com/2/user', headers=headers)

            try:
                payment_method_id = response.json()['payment_method_id']
            except:
                payment_method_id = 999999

            if payment_method_id == None:
                payment_method_id = 999999

            session.query(Account).filter(Account.email==profilename).update({"token":token, "api_key":api_key, "payment_method_id": payment_method_id})
            session.flush()
            session.commit()

            logger.info("token Updated Successfully.. ")
            sys.exit()
        except:
            return request
    return request

def main():
    # breakpoint()
    parser = argparse.ArgumentParser(description="Chromium Setup")
    # parser.add_argument('-cp', '--chprofile', type=str,help="Chrome Profile Name")
    parser.add_argument('-em', '--email', type=str,help="Resy Email")
    parser.add_argument('-pw', '--password', type=str,help="Resy Password")
    args = parser.parse_args()
    
    if not args.email or not args.password:
        logger.error(" ".join(['Please add complete parameters, ex: python update_token.py -em [email] -pw [password]', CLOSE_MESSAGE]))
        sys.exit()
    error = True
    logger.info(f"python update_token.py -em {args.email} -pw {args.password}")
    try:
        with sync_playwright() as pr:
            wargs = []
            wargs.append('--v=1')
            wargs.append('--no-sandbox')
            wargs.append('--enable-features=NetworkService,NetworkServiceInProcess')
            wargs.append('--enable-automation')
            wargs.append('--disable-popup-blocking')
            wargs.append('--disable-web-security')
            wargs.append('--start-maximized')
            
            # browser = pr.chromium.launch(headless=False, args=wargs, proxy=PROXY_PL)
            browser =  pr.chromium.launch(headless=True, args=wargs, proxy=proxydict)
            # browser =  pr.chromium.launch(headless=True, args=wargs)

            page = browser.new_page()
            stealth_sync(page)
            trial = 0
            while True:
                trial += 1
                if trial >=3:
                    print("Update token Failed")
                    logger.error("Update token Failed")
                    sys.exit()

                message = "Logged in successfully."
                page.goto("https://resy.com", wait_until="domcontentloaded", timeout=60000)
                random_delay(2,5)
                if page.query_selector('button.Button--login'):
                    login_to_resy(page, args.email, args.password)
                    
                    time.sleep(3)
                    # breakpoint()
                    if page.query_selector('button.Button--login'):
                        time.sleep(5)
                        continue
                    else:
                        break    
            logging.info(message)
            page.on("request", lambda request: intercept_request(request, profilename=args.email))
            page.goto("https://resy.com/cities/orlando-fl", wait_until="domcontentloaded", timeout=60000)
            browser.close()
            error = False
            sys.exit()
            
    except Exception as e:
        if error:
            logger.error("An error occurred.." + str(e))
        sys.exit()
if __name__ == '__main__':
    main()