import requests
import getpass
from requests.auth import HTTPBasicAuth
import time
import tkinter as tk
from tkinter import ttk
timedelay = 10
loctime = time.localtime()
year = loctime[0]
month = loctime[1]
day = loctime[2]
nm = 0
hour = loctime[3]
pp = 0
def get_userPass():
    global username
    global password
    username = user_entry.get()
    password = pass_entry.get()
    global reqf
    reqf = requests.get(api, auth=(username, password))
    
api = "https://ion.tjhsst.edu/api/blocks"
window = tk.Tk()
window.title("ION Club Signup")
window.geometry("500x500")
window.resizable(False, False)
user_entry = ttk.Entry(window)
user_entry.pack()
pass_entry = ttk.Entry(window, show="*")
pass_entry.pack()
enter = ttk.Button(window, command=get_userPass()).pack()
if reqf.status_code == 201 or reqf.status_code == 200:
    print("Successfully Signed In!: ")
    date = input("what date would you like? Format: YYYY-MM-DD: ")
    name = input("Name of Activity: ")
    blockAorB = input("Block A or B?: ")
    api = "https://ion.tjhsst.edu/api/blocks?date=" + date
    ion_sch = requests.get(api, auth=(username, password)).json()
    pp = 1

elif reqf.status_code == 401 or reqf.status_code == 400:
    print("Could not successfully sign in, please try again... ")

if pp == 1:
    for i in ion_sch:
        if i == 'results':
            if blockAorB in 'Bb':
                newurl = ion_sch['results'][1]['url']
                print('found URL: step one complete:', newurl)
                digits = newurl[34:]
                print(digits)
            elif blockAorB in 'Aa':
                newurl = ion_sch['results'][0]['url']
                print('found URL: step  complete:', newurl)
                digits = newurl[34:]
                print(digits)
            else:
                print('invalid block: You typed somethimg other than A or B: ')
    newapi = requests.get(newurl, auth=(username, password)).json() 
    for x in newapi['activities']:
        if newapi['activities'][x]['name'] == name:
            blockID = newapi['activities'][x]['id']
            print('successfully found Activity and blockID: step two complete:', blockID)
            scheduleActivity = newapi['activities'][x]['scheduled_activity']['id']
            print('Scheduled_Activity_ID:', newapi['activities'][x]['scheduled_activity']['id'])
            nm = 1
            break
        else:
            print("Could not find Activity Name: ")
    if nm == 0:
        print("Could not find activity or BlockID: ")
    if nm == 1:
        o = requests.post("https://ion.tjhsst.edu/api/signups/user", json={"block": digits ,"activity": blockID, "scheduled_activity": scheduleActivity}, auth=HTTPBasicAuth(username, password))
    if o.status_code == 201:
        print(f"Success!: you have successfully signed up for {name}!")
        if o.status_code == 400 or o.status_code == 401:
            print("Unsuccessful attempt at signing up for block: please run program and try again... ")
            print('if any error pops up, the block most likely is not on that date, sorry... ')
window.mainloop()