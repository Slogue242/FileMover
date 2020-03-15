import os
import sys
import shutil
from tkinter import *
from tkinter import filedialog

source_hold = []

def source_folder():
    source_dest = filedialog.askdirectory()
    source_hold.append(str(source_dest))

final_hold = []

def dest_folder():
    final_dest = filedialog.askdirectory()
    final_hold.append(str(final_dest))

biggest = ("", -1)

def main():
    global biggest
    def search(dir):
        global biggest
        for item in os.listdir(dir):
            item = dir + "/" + item
            if os.path.isdir(item):
                search(item)
            else:
                itemsize = os.path.getsize(item)
                if itemsize > biggest[1]:
                    biggest = (item, itemsize)

    dir_list = []
    biggest_item = []

    dest_but = final_hold[-1]

    for root, dirs, files in os.walk(source_hold[-1], topdown=False):
       #for name in files:
          #print(os.path.join(root, name))
        for name in dirs:
            name_join = os.path.join(root, name)
            dir_list.append(name_join)
       
    for item in dir_list:
        search(item)
        print(str(biggest[0]))
        biggest_item.append(str(biggest[0]))
        biggest = ("", -1)

    for item in biggest_item:
       shutil.move(item, dest_but)


root = Tk()

root.title("Mass File Mover")
root.geometry("500x300")
root.resizable(width=True, height=True)

source_folder = Button(root, text="Source Folder", width=15, command=source_folder)
source_folder.pack(side="left")

dest_loca = Button(root, text="Destination Folder", width=15, command=dest_folder)
dest_loca.pack(side="left")

run_button = Button(root, text="Move Now", width=15, command=main)
run_button.pack(side="left")

root.mainloop()