import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import logging
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

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import CLOSE_MESSAGE, CHROME_USER_DATA, CHROME_EXE
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
    # print(request.url, "tes")
    # we can update requests with custom headers
    api_key = ''
    token = ''
    if "https://api.resy.com/2/config" in request.url:
        # print(request.url)
        try:
            token = request.headers['x-resy-auth-token']
            api_key=str(request.headers['authorization']).replace('ResyAPI api_key=', "").replace('"','')
            # print(token, api_key)
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
            response = requests.get('https://api.resy.com/2/user', headers=headers)
            try:
                payment_method_id = response.json()['payment_method_id']
            except:
                payment_method_id = 999999

            if payment_method_id == None:
                payment_method_id = 999999

            file = open("profilelist.json", "r")
            profilelist = json.load(file)
            tmplist = []
            for dl in profilelist:
                if dl['profilename'] == profilename:
                    tmplist.append({"profilename": profilename, "email":dl['email'], "password": dl['password'], "api_key": api_key, "token":token, "payment_method_id": payment_method_id})
                else:
                    tmplist.append(dl)
            with open("profilelist.json", "w") as final:
                json.dump(tmplist, final)
            input("token Updated.. " + CLOSE_MESSAGE)
            sys.exit()
        except:
            return request        
    return request

def main():
    # breakpoint()
    parser = argparse.ArgumentParser(description="Chromium Setup")
    parser.add_argument('-cp', '--chprofile', type=str,help="Chrome Profile Name")
    parser.add_argument('-em', '--email', type=str,help="Resy Email")
    parser.add_argument('-pw', '--password', type=str,help="Resy Password")
    args = parser.parse_args()
        
    if not args.chprofile or not args.email or not args.password:
        input(" ".join(['Please add complete parameters, ex: python chromium_setup.py -cp [chrome_profile] -em [email] -pw [password]', CLOSE_MESSAGE]))
        sys.exit()
    error = True
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
            
            browser =  pr.chromium.launch(headless=True, args=wargs)
            page = browser.new_page()
            stealth_sync(page)
            page.on("request", lambda request: intercept_request(request, profilename=args.chprofile))

            page.goto("https://resy.com", wait_until="domcontentloaded", timeout=20000)
            random_delay(2,5)
            
            if page.query_selector('button.Button--login'):
                login_to_resy(page, args.email, args.password)
                message = "Logged in successfully."
                time.sleep(3)
                if page.query_selector('button.Button--login'):
                    message = "Logged in Failed."
                    raise Exception(message)    
                
                logging.info(message)
                print(message)
                # time.sleep(1)
                page.goto("https://resy.com/cities/orlando-fl", wait_until="domcontentloaded", timeout=60000)
                browser.close()
            error = False
            sys.exit()
            
    except Exception as e:
        if error:
            print(e)
            input("An error occurred..," + CLOSE_MESSAGE)
        sys.exit()
if __name__ == '__main__':
    main()