import json 
import requests 
import time  
import datetime
import urllib 
from commands import check_commands
from dbHelper import DBHelper

db = DBHelper()
TOKEN = "710760209:AAEdFY2udGjdIU7aAgbY6iRkbxx64doRFmM"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#downloads the content from a url and returns a string
def get_url(url):
    response = requests.get(url)
    #decode("utf8") is added for extra compatibility for some python versions
    content = response.content.decode("utf8")
    return content 
    
#gets string response from url and parse into json
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js
 
#calls the API command and retrieve updates (messages sent to bot)
#offset is for indicating which messages have been seen
def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids) 
    
#takes the text and ID, calls sendMessage api to display chat made by bot
def send_message(text, chat_id, reply_markup=None): 
    #urlLib helps encode special characters
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url) 

#loop through each update and grab text and userID
def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        userId = update["message"]["chat"]["id"] 
        status = db.get_status(userId)
        today = datetime.datetime.now().strftime("%d-%m")
        message = check_commands(text,userId) 
        send_message(message,userId) 

def main(): 
    db.setup()
    last_update_id = None 
    while True: 
        #check for new updates
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()