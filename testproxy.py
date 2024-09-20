import requests
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import sys
# proxies = {
#   "http": "http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181",
#   "https": "http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181"
# }
# response = requests.get('https://quotes.toscrape.com/', proxies=proxies, verify=False)
# print(response.text)

# proxies = {
#   "http": "http://sp90lzhoej:2vQ_jk6cpTF98ujLyj@gate.smartproxy.com:7000",
#   "https": "http://sp90lzhoej:2vQ_jk6cpTF98ujLyj@gate.smartproxy.com:7000"
# }
proxies = {
  "http": "http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181",
  "https": "http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181"
}
response = requests.get('https://quotes.toscrape.com/', proxies=proxies)
print(response.text)
sys.exit()
proxies = {
  "http": "http://14af2bc2a24d2:c85279a73c@198.143.4.8:10323",
  "https": "http://14af2bc2a24d2:c85279a73c@198.143.4.8:10323"
}
proxy_helper = "14af2bc2a24d2:c85279a73c@198.143.4.8:10323"
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
    browser =  pr.chromium.launch(headless=True, args=wargs, proxy=proxydict)

    # browser =  pr.chromium.launch(headless=True, args=wargs)

    page = browser.new_page()
    stealth_sync(page)
    
    page.goto("https://resy.com", wait_until="domcontentloaded", timeout=60000)
    breakpoint()
    page.inner_html()

