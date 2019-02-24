import json 
import requests 
import time  
import datetime
import urllib 
from dbHelper import DBHelper 

db = DBHelper()

def check_commands(text,userId): 
    message = "" 
    status = db.get_status(userId) 
    today = datetime.datetime.now().strftime("%d-%m") 
    if text == "/checkin" and len(status) == 0:
            checkedInTime = datetime.datetime.now() 
            message = "You have checked-in on: " + checkedInTime.strftime("%d-%m-%Y")+ " at " + checkedInTime.strftime("%H:%M")
            
            #add checkin status and time 
            db.checkin_status("checkedin",checkedInTime, userId)     
            
    elif text == "/checkin" and len(status) != 0:
            message = "You are already checked-in!"  
            
    elif text.startswith("/checkout") and len(status) != 0: 
    
                   checkoutText = text.replace('/checkout', '')  
                   checkedOutTime = datetime.datetime.now()   
                   checkedinTimeArray = db.get_checkinTime(userId)  
                   checkedinTime = checkedinTimeArray[0]  
                   checkedinTimeObj = datetime.datetime.strptime(checkedinTime, '%Y-%m-%d %H:%M:%S.%f') 
                   
                   duration = calculate_time(checkedOutTime,checkedinTimeObj)  
                   db.add_item(checkoutText,today,duration,userId)  
                   
                   header = "*You have checked-out on: " + checkedOutTime.strftime("%d-%m-%Y")+ " at " + checkedOutTime.strftime("%H:%M")+".You have done the following: *"
                   message = header + "\n" + checkoutText + "\n" + "You have checked in for " + duration 
                   
                   db.delete_status("checkedin", userId) ##
    elif text.startswith("/checkout") and len(status) == 0:
            message = "You cannot check out without checking in!" 
            
    elif text.startswith("/summary"):
            items = db.get_summary(today) 
            for row in items: 
               item = row[0]  
               date = row[1] 
               duration = row[2] 
               owner = row[3]
               message += "\n"+ item + " " + date + " " + duration + " "+ owner  
               
    elif text.startswith("/"):
            message = "Typo or alien language, or both. Please try again"
    else:
        message = ""
    return message  

def calculate_time(time1,time2):
        diff = time1-time2 
        days,seconds = diff.days,diff.seconds
        hours = round(diff.seconds/3600)
        minutes = round(diff.seconds/60)
        seconds = round(diff.seconds)
        duration = str(hours) + "hours,"+ str(minutes)+"minutes,"+str(seconds)+"seconds." 
        return duration
    