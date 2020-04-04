import os
import sys
import shutil
from tkinter import *
from tkinter import filedialog

tv_hold = []

#This allows you to select where you store your TV shows, this will be used to see what shows you have.
def tv_folder():
    tv_dest = filedialog.askdirectory()
    tv_hold.append(str(tv_dest))
    tv_folder_entry.delete(0, 'end')
    tv_folder_entry.insert(INSERT, str(tv_dest))

source_hold = []

#This lets the user select a folder they want to move files out of and then appends this to the empty list above called source_hold
def source_folder():
    source_dest = filedialog.askdirectory()
    source_hold.append(str(source_dest))
    source_entry.delete(0, 'end')
    source_entry.insert(INSERT, str(source_dest))

final_hold = []

#Nearly the same as the source_folder function but it used for where the files will end up.
def dest_folder():
    final_dest = filedialog.askdirectory()
    final_hold.append(str(final_dest))
    dest_entry.delete(0, 'end')
    dest_entry.insert(INSERT, str(final_dest))

biggest = ("", -1)

#This function goes through the selected source folder and then go into each folder inside that folder and runs through each file.
#It is looking for the largest file in that particular folder. Once the biggest file in the folder has been found it then moves it to the destination folder.
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
    delete_get = delete_var.get()
    if delete_get == 1:
        try:
            for item in dir_list:
                shutil.rmtree(item)
        except Exception as e:
            print(e)
            pass
    else:
        pass

def mover():
    punc_list = "'"

    name_path = {}

    root = tv_hold[0]

    #Goes into the folder passed into root and finds all the folders and lists makes the folder name a key and the file path a value
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)):
            full_path = root+"/"+item
            if item not in name_path.keys():
                name_path[item] = full_path

    #Checks key in name_path dict has a ' in the dict key, this then deletes that key and replaces it with a key without the '
    for old_key in name_path:
        if punc_list in old_key:
            new_key = old_key.replace(punc_list, "")
            name_path[new_key] = name_path.pop(old_key)


    file_name = []

    #Walks the path given and finds subfolders, and files
    for root, dirs, files in os.walk(source_hold[0], topdown=False):
        for file in files:
            file_name.append(file)

    #Checks if the file names have a full stop in them and then deletes it.
    #This is to help with checking against the dict keys.
    for item in file_name:
        if "." in item:
            new_item = item.replace(".", " ")
            for x in name_path:
                if x.lower() in new_item.lower():
                    shutil.move(f"{source_hold[0]}/{item}", f"{name_path[x]}/{item}")
                    print("Moved")
#This is for starting tkinter GUI
root = Tk()

#Give the program a name and the default size it opens at. Also declares that it is resizable.
root.title("Mass File Mover")
root.geometry("500x300")
root.resizable(width=True, height=True)

#Creates a button that you can click on to point the program to the folder where you store your TV shows
tv_folder = Button(root, text="Select TV Folder", width=15, command=tv_folder)
tv_folder.grid(row=0)

#Creates a button for the user to click on for the source folder.
source_folder = Button(root, text="Source Folder", width=15, command=source_folder)
source_folder.grid(row=1)

#Creates a button for the user to click on for the destination folder.
dest_loca = Button(root, text="Destination Folder", width=15, command=dest_folder)
dest_loca.grid(row=2)

#Creates a button that allows the user to run the program once they have selected both destination and source folder.
run_button = Button(root, text="Move Now", width=15, command=lambda:[main(), mover()])
run_button.grid(row=3)

tv_folder_entry = Entry(root)
tv_folder_entry.grid(row=0, column=1, columnspan=2)

#This shows the user the what source folder they have selected.
source_entry = Entry(root)
source_entry.grid(row=1, column=1, columnspan=2)

#This shows the user what destination folder they have selected
dest_entry = Entry(root)
dest_entry.grid(row=2, column=1, columnspan=2)

delete_var = IntVar()

#This buttons allows users to select if they want the source folders to be deleted after they are finished moving files.
chk = Checkbutton(root,text='Delete Folders After Move', variable=delete_var)
chk.grid(row=0, column=3)

#Allows the user to exit the program with having to click on the x button.
exit_button = Button(root, text="Exit", width=15, command=root.destroy)
exit_button.grid(row=2, column=3)

root.mainloop()
