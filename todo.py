import json 
import requests 
import time  
import datetime
import urllib
from dbHelper import DBHelper

db = DBHelper()
TOKEN = "710760209:AAEdFY2udGjdIU7aAgbY6iRkbxx64doRFmM"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)
 
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)
def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items(chat)  ##
        if text == "/done":
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        elif text == "/checkin": 
            currentDT = datetime.datetime.now() 
            message = "You have checked-in on: " + currentDT.strftime("%d-%m-%Y")+ " at " + currentDT.strftime("%H:%M")
            send_message(message, chat)
        elif text.startswith("/checkout"):
                   new_text = text.replace('/checkout', '')
                   db.add_item(new_text, chat) ## 
                   items = db.get_items(chat)  ## 
                   currentDT = datetime.datetime.now() 
                   header = "You have checked-out on: " + currentDT.strftime("%d-%m-%Y")+ " at " + currentDT.strftime("%H:%M")
                   message = header + "\n".join(items)
                   send_message(message, chat)
        elif text.startswith("/"): 
            send_message("Sorry bro, any message starting with / is rejected except /checkin", chat)
            continue
        elif text in items:
            db.delete_item(text, chat)  ##
            items = db.get_items(chat)  ##
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        else:
           ## db.add_item(text, chat)  ##
            ##items = db.get_items(chat)  ##
            ##message = "\n".join(items)
            ##send_message(message, chat) 
            send_message("Currently Disabled", chat)
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def main(): 
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()