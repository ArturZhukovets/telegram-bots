import json

import requests
from config import BOT_TOKEN


REQUEST_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def get_me_req():
    req = requests.get(REQUEST_URL + "getMe")
    response = req.text
    print(response)
    return response

def bot_send_message(chat_id, text):
    req = requests.get(REQUEST_URL + f"SendMessage?chat_id={chat_id}&text={text}")
    response = req.text

    return json.loads(response)



