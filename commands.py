import json 
import requests 
import time  
import datetime
import urllib 
from dbHelper import DBHelper 

db = DBHelper()

def check_commands(text,userId,userName): 
    message = "" 
    status = db.get_status(userId) 
    today = datetime.datetime.now().strftime("%d-%m") 
    if text == "/checkin" and len(status) == 0: 
            print("enter checkin:")
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
                   db.add_item(checkoutText,today,duration,userId,userName)  
                   
                   header = "*You have checked-out on: " + checkedOutTime.strftime("%d-%m-%Y")+ " at " + checkedOutTime.strftime("%H:%M")+".You have done the following: *"
                   message = header + "\n" + checkoutText + "\n" + "*You have checked in for " + duration  + "*"
                   db.delete_status("checkedin", userId) ##
    elif text.startswith("/checkout") and len(status) == 0: 
            print("enter checkout start:")
            message = "You cannot check out without checking in!" 
    elif text.startswith("/retrieve"):
            print("Enter retrieve ")
            summaryDate = text.replace('/retrieve ', '')
            print(summaryDate)
            items =[]
            try:  
                summaryDateObj = datetime.datetime.strptime(summaryDate, '%d-%m') 
                summaryDateStr = summaryDateObj.strftime('%d-%m') 
                items = db.get_summary(summaryDateStr)
                header = "*Here's the summary for " + summaryDate + "! *"  
                message= header
                for row in items: 
                    item = row[0]  
                    date = row[1] 
                    duration = row[2] 
                    ownerName = row[4]
                    message += "\n\n"+ "*User:* "+ownerName+"\n"+"*Activity:* "+ item +"\n"+"----------------------------------------------------------"  
                if len(items)== 0:
                    message = "No activities for the listed date"
            except ValueError:
                print("Error. Invalid date") 
                message = "Invalid date brother. Please try again."
    elif text.startswith("/help"): 
            message = "Hi " + userName + ", the following commands are available: "+"\n\n"
            message +="/checkin- Start your checkin session. Timer starts and will end once you checkout."+"\n" 
            message +="/checkout- Any activities listed after checkout will be stored as the activities done for the day."
            message +=" E.g */checkout* Read a book"+"\n" 
            message +="/retrieve- Retrieves a particular session's activity based on date. E.g* /retrieve 02-03*"+"\n"
            message +="/help- You are already here"+"\n"
            message +="/summary- Gives you a summary of what all users have done today"
    elif text.startswith("/summary"):  
            print("Enter Summary")
            items = db.get_summary(today) 
            header = "*Here's the summary for " + today + "! *"  
            message= header
            for row in items: 
               item = row[0]  
               date = row[1]
               date = row[1] 
               duration = row[2] 
               ownerName = row[4]
               message += "\n\n"+ "*User:* "+ownerName+"\n"+"*Activity:* "+ item +"\n"+"----------------------------------------------------------"  
            if len(items)== 0:
               message = "No activities for today"
    elif text.startswith("/"):
            message = "Typo,alien language, or both. Please try again"
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
    