import requests

def send_to_telegram(message):

    apiToken = '7207865537:AAEyl4_fIWnFjZTnaH9uN6eJeYUF87MfRAk'
    chatID = '-1002402008228'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message, "parse_mode": "MarkdownV2"})
        print(response.text)
    except Exception as e:
        print(e)

send_to_telegram("Hello from Python! [inline URL](http://www.example.com/)")