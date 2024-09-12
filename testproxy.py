import requests

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
# proxies = {
#   "http": "http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181",
#   "https": "http://scrapeops:f2d43fe5-5bee-41ab-83f9-da70ae59c60a@residential-proxy.scrapeops.io:8181"
# }
proxies = {
  "http": "http://Rf3X-yq_IFA5qRcId7r60A@smartproxy.crawlbase.com:8012",
  "https": "http://Rf3X-yq_IFA5qRcId7r60A@smartproxy.crawlbase.com:8012"
}

response = requests.get('https://quotes.toscrape.com/', proxies=proxies, verify=False)
print(response.text)