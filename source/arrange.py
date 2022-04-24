from tkinter import *
from tkinter import filedialog
import os ,stat
from tkinter.simpledialog import askstring
import shutil
from tkinter.messagebox import askokcancel, askyesno
from tkinter.filedialog import askdirectory

class Arranger:


    def __init__(self):
        self.arrangedfiles = []
        self.construct()

    def changelbl(self,msg):
        self.infolbl.config(text=msg)


    def fetchpdf(self,event):  # function to
        print(self.arrangedfiles)
        self.file_list.delete(0, END)
        os.chdir(self.desktop)
        files = os.listdir()
        for file in files:
            if ".pdf" in file or ".docx" in file and file[0] != '~':
                if not file in self.Afiles.get(0, END) and not file in self.arrangedfiles:
                    self.file_list.insert(END, file)
        self.changelbl("Good cleaning, We found " + str(len(self.file_list.get(0, END))
                                                ) + " PDF/DOCX  files on your desktop !")
        print(self.file_list.get(0,END))


    def passfile(self, tolist, fromlist):  # passing files from list to list after selection
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
    while "None" in fromlist.get(0, END) :    
        while "None" in fromlist.get(0, END) :    
            
            if fromlist.get(i) == "None":
                fromlist.delete(i)
                i = -1
            i += 1
    '''


    def arrangefile(self, event):
        files = self.Afiles.get(0, END)
        if len(files):
            filedir = os.path.dirname(os.path.realpath(__file__))
            os.chdir(filedir)
            foldername = askstring("Folder name", "Enter the foldername")

            folderdir = os.path.join(filedir, "temp/" + foldername)
            try:
                os.makedirs(folderdir)
            except FileExistsError:
                pass
            os.chdir(self.desktop)
            for file in files:
                self.arrangedfiles.append(file)
                if file in os.listdir(self.desktop):
                    shutil.copy(file, folderdir)
            self.Afiles.delete(0, END)
        else:
            self.changelbl(
                "please fetch files first or move them to the right list to arrange them")
            return None
        self.changelbl("We arranged " + str(len(self.arrangedfiles)) + " files.")


    def Finish(self, event):
        print(self.arrangedfiles)
        filedir = os.path.dirname(os.path.realpath(__file__))
        if askokcancel("Last step", "Do you wanna save your folders?", icon='question'):
            savedir = askdirectory(
            title="Where do you want to save the main folder", initialdir=self.desktop, mustexist=True)
        namemainfile = askstring(
            "Main folder name", "What do you want to call the main folder ?")
        if askyesno("Last step", "Do you want to proceed saving folders", icon='question'):
            try:
                shutil.move(filedir + "/temp", savedir + '/' + namemainfile)
                if askyesno("Warning! Last step", "Duplicate of your files are on your desktop, do you wanna delete them?", icon='warning'):
                        os.chdir(filedir)
                        for file in self.arrangedfiles:
                            os.remove(file)
            except FileNotFoundError:
                    self.changelbl("No files have been arranged, Fetch files first")
            except Exception as err:
                    self.changelbl(
                        "Error: {0} lease retry later, or contact developper, if not working, on el_mehdi.benane@ensam.eu".format(err))


    def Reset(self, event):
        filedir = os.path.dirname(os.path.realpath(__file__))
        temp = filedir + "/temp"
        try:
            shutil.rmtree(temp)
        except FileNotFoundError:
            self.changelbl("No files have been arranged, file lists are cleared")

        self.arrangedfiles = []
        self.Afiles.delete(0, END)
        self.file_list.delete(0, END)

    def DeleteAll(self,event):
        files  = self.file_list.get(0,END)
        if askyesno("Warning!", "Do you wanna delete the doc files on your folder?", icon='warning'):
            os.chdir(self.desktop)
            for file in files:
                os.remove(file)
                print("deleted {}".format(file))
            self.Reset("")
        

    def construct(self):
        arranger = Tk()
        self.desktop = filedialog.askdirectory(title="Select the folder that you wanna clean", mustexist=True)
        arranger.minsize(width=1260, height=600)
        arranger.maxsize(width=1440, height=800)
        arranger.title("File arranger")
            # File frame containes pdf files
        file_frame = Frame(arranger)
        file_frame.grid(row=0, rowspan=2, sticky='nw')
        self.file_list = Listbox(file_frame, selectmode=MULTIPLE,width=100)
        # scrollbar
        defily = Scrollbar(arranger, orient="vertical", command=self.file_list.yview)
        defily.grid(row=0, column=0, rowspan=4, sticky='en')
        self.file_list['yscrollcommand'] = defily.set
        #
        self.file_list.configure(bd=4)
        fileframelabel = Label(file_frame, text="PDF files:")
        self.file_list.grid(row=1)
        fileframelabel.grid(row=2)
        # button frames contains fetch files frame and arrange files buttons
        button_frame = Frame(arranger)
        button_frame.grid(row=0, column=2, sticky='e')

        # buttons
        fbutton = Button(button_frame, text="Fetch files", width=20)
        Abutton = Button(button_frame, text="Arrange files", width=20)
        fbutton.grid()
        fbutton.bind('<Button-1>', self.fetchpdf)
        Abutton.grid()
        Abutton.bind('<Button-1>', self.arrangefile)
        # drag frame contains drag and drop folders
        drag_frame = Frame(arranger)
        drag_frame.grid(row=1, column=2, sticky=E)
        manage_file = Label(drag_frame, text="Arranged folder:")
        manage_file.grid(row=0)
        self.Afiles = Listbox(drag_frame, selectmode=MULTIPLE,width=100)
        self.Afiles.configure(bd=3)
        self.Afiles.grid(row=1)
        scA = Scrollbar(master=arranger, orient="vertical", command=self.Afiles.yview)
        scA.grid(row=1, column=3, sticky="ne")
        self.Afiles['yscrollcommand'] = scA.set


        # separator between col 0 and col 2  passing button

        emptyframe = Frame(arranger)
        emptyframe.grid(row=0, column=1, rowspan=4)
        pbutton = Button(emptyframe, text=">>", command=lambda tolist=self.Afiles,
                        fromlist=self.file_list: self.passfile(tolist, fromlist))
        pbutton.grid()
        pbuttonl = Button(emptyframe, text="<<", command=lambda fromlist=self.Afiles,
                        tolist=self.file_list: self.passfile(tolist, fromlist))
        pbuttonl.grid()

        # info label
        self.infolbl = Label(arranger, text="Select files to arrange in one folder",
                        fg="green", font=('gothic', 12, 'bold'))
        self.infolbl.grid(row=2, columnspan=4, sticky="ensw")
        # RESET and Finish buttons
        lastframe = Frame(arranger,width=100)
        reset = Button(lastframe, text="Reset")
        finish = Button(lastframe, text="Finish")
        DeleteAll = Button(lastframe, text="Delete All PDF files",background="red")

        lastframe.grid(row=4, columnspan=4)
        reset.grid(row=0, column=0, sticky='w')
        finish.grid(row=0, column=3, sticky='e')
        DeleteAll.grid(row=1,column=2)
        finish.bind('<Button-1>', self.Finish)
        reset.bind('<Button-1>', self.Reset)
        DeleteAll.bind('<Button-1>', self.DeleteAll)
        # End
        arranger.mainloop()


Arranger()