from tkinter import *
from datetime import datetime, date
import webbrowser
import re
import numpy as np
import random
from PIL import ImageTk, Image
from os.path import dirname,abspath
from os import chdir

def open_crossword(clist,ctype,current_list,t):
    # compare today with last time a crossword was opened
    oldcurrent = current_list[0]
    current = get_today(t)
    # change current_list by reference so value changes in main
    current_list[0] = current
    # if new day
    if (current != oldcurrent):
        # append new days to list
        for i in range(1,current-oldcurrent+1):
            clist.append(str(oldcurrent+i))
    nextcross = clist[-1]
    # if first crossword of the day
    if (int(nextcross) == current):
        webbrowser.open('https://www.theguardian.com/crosswords/'+ctype+"/"+nextcross)
        update_lists(clist,nextcross,ctype)
        if (datetime.today().weekday() == 0):
            satcross = str(int(nextcross) - 1)
            webbrowser.open('https://www.theguardian.com/crosswords/'+ctype+"/"+satcross)
            monday_message = "Hooray it's Monday, opened Saturday's as well"
            monday_title = 'Mondays Rock'
            monday_time = 5 # time in seconds
            timed_message(monday_message,monday_title,monday_time)
            update_lists(clist,satcross,ctype)
    # if second or higher crossword today
    else:
        nextcross = random.choice(tuple(clist))
        webbrowser.open('https://www.theguardian.com/crosswords/'+ctype+"/"+nextcross)
        update_lists(clist,nextcross,ctype)
    
def update_lists(clist,nextcross,ctype):
    # remove from list of available crosswords
    clist.remove(nextcross)
    # add to file list of completed crosswords
    with open("numbers_with_type.txt","a") as f:
        f.write(nextcross+" "+ctype+"\n")

# this would be improved by passing the message content and duration as arguments        
def timed_message(message,title,time):
    message = Tk()
    ws = message.winfo_screenwidth() # width of the screen
    hs = message.winfo_screenheight() # height of the screen
    w = 1000
    h = 100
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    message.wm_attributes("-topmost", 1)
    message.geometry('%dx%d+%d+%d' % (w, h, x, y))
    message.title(title)
    label = Label(message, text = message,font=("System",40))
    label.pack(ipadx=10, ipady=10)
    message.after(time*1000, lambda: message.destroy()) # Destroy after 3 seconds

# calculate what todays quick crossword number will be
# 16381 is todays crossword, at time of writing (2022-11-07)
# append to list
def get_today(t):
    d1 = date.today().strftime('%Y-%m-%d')
    diff = np.busday_count('2022-11-07',d1,weekmask=[1,1,1,1,1,1,0],holidays=t)
    return 16381 + diff

# begin program    
speedies = []
quicks = []
quiptics = []

# set working directory to the directory that contains this file
chdir(dirname(abspath(__file__)))
with open("numbers_with_type.txt") as f:
    print("reading completed crosswords file")
    while (True):
        line = f.readline().split()
        if (len(line) < 2):
            print('end of file')
            break
        if (line[1] == 'quick'):
            quicks.append(line[0])
        elif (line[1] == 'speedy'):
            speedies.append(line[0])
        elif (line[1] == 'quiptic'):
            quiptics.append(line[0])
        else:
            print("unknown crossword type",line[1])

# t deals with christmas day
# will there be an issue if christmass day is on Saturday?
t = []
for i in range(2022,2032+1):
    t.append("{}-12-25".format(i))

current = get_today(t)
quicks_sorted = sorted(quicks)
allquicks = np.arange(9100,current+1,1).tolist()
allquicks = [str(x) for x in allquicks]

quicks_set = set(quicks_sorted)
allquicks_set = set(allquicks)

quicksnotdone = sorted(allquicks_set.difference(quicks_set))
quicksnotdone = [str(x) for x in quicksnotdone]

# create a tkinter window
root = Tk()

# Open window having dimension 100x100
root.geometry('120x120')

#current in list for pass by reference
current_list = [current]

# Create buttons
image = ImageTk.PhotoImage(Image.open("button_image.png"))  # PIL solution
btn1 = Button(root, image = image, bd = '5', cursor='pirate', command = lambda : open_crossword(quicksnotdone,'quick',current_list,t))
#btn2 = Button(root, text = 'Todays', bd = '5', command = lambda : open_crossword(quicksnotdone,'quick'))
#btn3 = Button(root, text = 'Quiptic', bd = '5' ,command = lambda : open_crossword(quiptics,'quiptic'))

# Label tkinter window
#label = Label(root, text = 'Crosswords')
#label.pack(ipadx=10, ipady=10)

# Organise buttons from the bottom up 
btn1.pack(side = 'bottom')   
#btn2.pack(side = 'bottom')   
#btn3.pack(side = 'top')   

# keep tkinter window on top of other windows
root.wm_attributes("-topmost", 1)

root.title('4pm')
root.mainloop()
