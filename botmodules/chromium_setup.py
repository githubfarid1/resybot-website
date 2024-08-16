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
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        # More user agents can be added here
    ]
    
    chrome_user_data = f"{CHROME_USER_DATA}\\{args.chprofile}"
    error = True
    try:
        user_agent = random.choice(user_agents)
        with sync_playwright() as pr:
            wargs = []
            wargs.append('--v=1')
            wargs.append('--no-sandbox')
            wargs.append('--enable-features=NetworkService,NetworkServiceInProcess')
            wargs.append('--enable-automation')
            wargs.append('--disable-popup-blocking')
            wargs.append('--disable-web-security')
            wargs.append('--start-maximized')
            # wargs.append('--disable-infobars')
            # wargs.append('--disable-blink-features=AutomationControlled')
            # breakpoint()
            # browser =  pr.chromium.launch(args=wargs)
            browser =  pr.chromium.launch_persistent_context(user_data_dir=chrome_user_data, 
                    headless=False, 
                    args=wargs, 
                    user_agent=user_agent,
                    permissions=['geolocation', 'notifications'],
                    java_script_enabled=True,
                    no_viewport=True
                    )
            # context = browser.new_context(
            #     user_agent=user_agent,
            #     # viewport={'width': random.randint(1200, 1920), 'height': random.randint(900, 1080)},
            #     # viewport={'width': 1920, 'height': 1080},
            #     permissions=['geolocation', 'notifications'],
            #     java_script_enabled=True,
            #     no_viewport=True,
            #     # bypass_csp=True,
            #     # locale='US_en',
            #     # geolocation=False,
            #     #proxy = {
            #         #'server': proxy_server
            #     #}
            # )
            # page = context.new_page()
            page = browser.pages[0]
            stealth_sync(page)
            page.goto("https://resy.com", wait_until='domcontentloaded', timeout=20000)
            random_delay(2, 5)
            # breakpoint()
            if  page.query_selector('button.Button--login'):
                login_to_resy(page, args.email, args.password)
                message = "Logged in successfully."
                logging.info(message)
                print(message)
                time.sleep(3)
                browser.close()
            # breakpoint()
            # Popen([CHROME_EXE, "https://resy.com","--user-data-dir={}".format(chrome_user_data), "--profile-directory=Default"])
            # input("Press any key when finished setting up Browser..")
            error = False
            sys.exit()
            
    except:
        if error:
            input("An error occurred..," + CLOSE_MESSAGE)
        sys.exit()
if __name__ == '__main__':
    main()