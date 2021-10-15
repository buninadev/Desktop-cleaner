from tkinter import *
import os
from tkinter.simpledialog import askstring
import shutil
from tkinter.messagebox import askokcancel, askyesno
from tkinter.filedialog import askdirectory

arrangedfiles = []
# Main  conatains all

arranger = Tk()
arranger.minsize(width=200, height=200)
arranger.maxsize(width=1440, height=800)
arranger.title("File arranger")
# All used functions


def changelbl(msg):
    infolbl.config(text=msg)


def fetchpdf(event):  # function to
    print(arrangedfiles)
    file_list.delete(0, END)
    path = os.path.join(os.environ["HOMEPATH"], 'Desktop')
    os.chdir(path)
    files = os.listdir()
    for file in files:
        if ".pdf" in file or ".docx" in file and file[0] != '~':
            if not file in Afiles.get(0, END) and not file in arrangedfiles:
                file_list.insert(END, file)
    changelbl("Good cleaning, We found " + str(len(file_list.get(0, END))
                                               ) + " PDF/DOCX  files on your desktop !")


def passfile(tolist, fromlist):  # passing files from list to list after selection
    items_index = fromlist.curselection()
    if len(items_index) != 0:
        n = 0
        for item in items_index:
            tolist.insert(END, fromlist.get(item - n))
            fromlist.delete(item - n)
            n += 1
        fromlist.select_clear(0, END)
    else:
        return None


'''     fromlist.delete(item)
        fromlist.insert(item, "None")
    i = 0
    while "None" in fromlist.get(0, END) :    
           
        if fromlist.get(i) == "None":
            fromlist.delete(i)
            i = -1
        i += 1
'''


def arrangefile(event):
    files = Afiles.get(0, END)
    if len(files):
        dpath = os.path.join(os.environ["HOMEPATH"], 'Desktop')
        filedir = os.path.dirname(os.path.realpath(__file__))

        os.chdir(filedir)
        foldername = askstring("Folder name", "Enter the foldername")

        folderdir = os.path.join(filedir, "temp/" + foldername)
        try:
            os.makedirs(folderdir)
        except FileExistsError:
            pass
        os.chdir(dpath)
        for file in files:
            arrangedfiles.append(file)
            if file in os.listdir(dpath):
                shutil.copy(file, folderdir)
        Afiles.delete(0, END)
    else:
        changelbl(
            "please fetch files first or move them to the right list to arrange them")
        return None
    changelbl("We arranged " + str(len(arrangedfiles)) + " files.")


def Finish(event):
    print(arrangedfiles)
    dpath = os.path.join(os.environ["HOMEPATH"], 'Desktop')
    filedir = os.path.dirname(os.path.realpath(__file__))
    if askokcancel("Last step", "Do you wanna save your folders?", icon='question'):
        savedir = askdirectory(
            title="Where do you want to save the main folder", initialdir=dpath, mustexist=True)
        namemainfile = askstring(
            "Main folder name", "What do you want to call the main folder ?")
        if askyesno("Last step", "Do you want to proceed saving folders", icon='question'):
            try:
                shutil.move(filedir + "/temp", savedir + '/' + namemainfile)
                if askyesno("Warning! Last step", "Duplicate of your files are on your desktop, do you wanna delete them?", icon='warning'):
                    os.chdir(dpath)
                    for file in arrangedfiles:
                        os.remove(file)
            except FileNotFoundError:
                changelbl("No files have been arranged, Fetch files first")
            except Exception as err:
                changelbl(
                    "Error: {0} lease retry later, or contact developper, if not working, on el_mehdi.benane@ensam.eu".format(err))


def Reset(event):
    filedir = os.path.dirname(os.path.realpath(__file__))
    try:
        os.remove(filedir + "/temp")
    except FileNotFoundError:
        changelbl("No files have been arranged, file lists are cleared")

    arrangedfiles = []
    Afiles.delete(0, END)
    file_list.delete(0, END)


    # File frame containes pdf files
file_frame = Frame(arranger)
file_frame.grid(row=0, rowspan=2, sticky='nw')
file_list = Listbox(file_frame, selectmode=MULTIPLE)
# scrollbar
defily = Scrollbar(arranger, orient="vertical", command=file_list.yview)
defily.grid(row=0, column=0, rowspan=4, sticky='en')
file_list['yscrollcommand'] = defily.set
#
file_list.configure(bd=4)
fileframelabel = Label(file_frame, text="PDF files:")
file_list.grid(row=1)
fileframelabel.grid(row=0)
# button frames contains fetch files frame and arrange files buttons
button_frame = Frame(arranger)
button_frame.grid(row=0, column=2, sticky='e')

# buttons
fbutton = Button(button_frame, text="Fetch files", width=20)
Abutton = Button(button_frame, text="Arrange files", width=20)
fbutton.grid()
fbutton.bind('<Button-1>', fetchpdf)
Abutton.grid()
Abutton.bind('<Button-1>', arrangefile)
# drag frame contains drag and drop folders
drag_frame = Frame(arranger)
drag_frame.grid(row=1, column=2, sticky=E)
manage_file = Label(drag_frame, text="Arranged folder:")
manage_file.grid(row=0)
Afiles = Listbox(drag_frame, selectmode=MULTIPLE)
Afiles.configure(bd=3)
Afiles.grid(row=1)
scA = Scrollbar(master=arranger, orient="vertical", command=Afiles.yview)
scA.grid(row=1, column=3, sticky="ne")
Afiles['yscrollcommand'] = scA.set


# separator between col 0 and col 2  passing button

emptyframe = Frame(arranger)
emptyframe.grid(row=0, column=1, rowspan=4)
pbutton = Button(emptyframe, text=">>", command=lambda tolist=Afiles,
                 fromlist=file_list: passfile(tolist, fromlist))
pbutton.grid()
pbuttonl = Button(emptyframe, text="<<", command=lambda fromlist=Afiles,
                  tolist=file_list: passfile(tolist, fromlist))
pbuttonl.grid()

# info label
infolbl = Label(arranger, text="Select files to arrange in one folder",
                fg="green", font=('gothic', 12, 'bold'))
infolbl.grid(row=2, columnspan=4, sticky="ensw")
# RESET and Finish buttons

lastframe = Frame(arranger)
reset = Button(lastframe, text="Reset")
finish = Button(lastframe, text="Finish")
lastframe.grid(row=4, columnspan=4)
reset.grid(row=0, column=0, sticky='w')
finish.grid(row=0, column=3, sticky='e')
finish.bind('<Button-1>', Finish)
reset.bind('<Button-1>', Reset)
# End
arranger.mainloop()
