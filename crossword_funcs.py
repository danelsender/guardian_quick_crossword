from tkinter import *
from datetime import datetime, date
import webbrowser
import numpy as np
import random

def open_crossword(clist,plist,current_list,t):
    # compare today with last time a crossword was opened
    oldcurrent = current_list[0]
    current = get_today(t)
    # if new day
    if (current != oldcurrent):
        # change current_list by reference so value changes in main
        current_list[0] = current
        # append new days to list
        for i in range(1,current-oldcurrent+1):
            clist.append(str(oldcurrent+i))
    # if first crossword of the day
    if (int(clist[-1]) == current):
        webbrowser.open('https://www.theguardian.com/crosswords/quick/'+str(current))
        update_lists(clist,str(current))
        # if Monday
        if (datetime.today().weekday() == 0):
            satcross = str(current - 1)
            webbrowser.open('https://www.theguardian.com/crosswords/quick/'+satcross)
            monday_message = "Hooray it's Monday, opened Saturday's crossword as well"
            monday_title = 'Mondays Rock'
            monday_time = 8 # time in seconds
            timed_message(monday_message,monday_title,monday_time)
            update_lists(clist,satcross)
    # open a partially completed crossword 1 in 200 times
    elif (random.random() < 1./200.):
        nextcross = plist[-1]
        webbrowser.open('https://www.theguardian.com/crosswords/quick/'+satcross)
        partial_message = "Congratulations, you have been selected to fix someone elses mess"
        partial_title = 'Incomplete crossword'
        partial_time = 8
        timed_message(partial_message,partial_title,partial_time)
        plist.remove(nextcross)
        with open('partial.txt','w') as f_p:
            f_p.writelines(plist)
    else:
        nextcross = random.choice(tuple(clist))
        webbrowser.open('https://www.theguardian.com/crosswords/quick/'+nextcross)
        update_lists(clist,nextcross)
    
def update_lists(clist,nextcross):
    # remove from list of available crosswords
    clist.remove(nextcross)
    # add to file list of completed crosswords
    with open("complete.txt","a") as f:
        f.write(nextcross+"\n")

def timed_message(text,title,time):
    message = Tk()
    ws = message.winfo_screenwidth()
    hs = message.winfo_screenheight()
    w = 1300
    h = 100
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    message.wm_attributes("-topmost", 1)
    message.geometry('%dx%d+%d+%d' % (w, h, x, y))
    message.title(title)
    label = Label(message, text = text,font=("System",40))
    label.pack(ipadx=10, ipady=10)
    message.after(time*1000, lambda: message.destroy())

# calculate what todays quick crossword number will be
# 16381 is todays crossword, at time of writing (2022-11-07)
def get_today(t):
    d1 = date.today().strftime('%Y-%m-%d')
    diff = np.busday_count('2022-11-07',d1,weekmask=[1,1,1,1,1,1,0],holidays=t)
    return 16381 + diff
