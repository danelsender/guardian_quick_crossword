from tkinter import *
from datetime import datetime, date
import re
import numpy as np
from PIL import ImageTk, Image
from os.path import dirname,abspath
from os import chdir
from crossword_funcs import open_crossword,update_lists,timed_message,get_today

# set working directory to the directory that contains this file
chdir(dirname(abspath(__file__)))

# read in completed crosswords (+partials)
with open("complete.txt") as f_c:
    quicks = f_c.read().splitlines()
with open("partial.txt") as f_p:
    partials = f_p.read().splitlines()

# t deals with christmas day
# will there be an issue if christmass day is on Saturday?
t = []
for i in range(2022,2032+1):
    t.append("{}-12-25".format(i))

current = get_today(t)
quicks_sorted = sorted(quicks)
quicksnotdone = np.arange(9100,current+1,1).tolist()
quicksnotdone = [str(x) for x in quicksnotdone]

for i in quicks_sorted:
    try:
        quicksnotdone.remove(i)
    except ValueError:
        print("unexpected mismatch between all crosswords and completed crosswords") # likely cause is duplicate in completed.txt

# create a tkinter window
root = Tk()
root.geometry('120x120')
root.title('4pm')
# put current in list for pass by reference
current_list = [current]

# Create buttons
image = ImageTk.PhotoImage(Image.open("button_image.png"))  # PIL solution
btn1 = Button(root, image = image, bd = '5', cursor='pirate', command = lambda : open_crossword(quicksnotdone,partials,current_list,t))
btn1.pack(side = 'bottom')   

# keep tkinter window on top of other windows
root.wm_attributes("-topmost", 1)

root.mainloop()
