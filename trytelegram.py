import requests

def send_to_telegram(message):

    apiToken = '7047922582:AAETkQ2FgOZtebsxobTWqZCBX90HvebN_30'
    chatID = '838609217'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

send_to_telegram("Hello from Python!")