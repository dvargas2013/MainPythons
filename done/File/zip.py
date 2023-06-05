from os import pardir
from os.path import join, abspath, exists
from tkinter import Tk, Listbox, filedialog, Menu
from zipfile import ZipFile
from random import shuffle

from done.List import applyToGenerator
from done.File.module import add_to_all


def subset(place, master):
    """used to make relative paths out of the master list"""
    return {name.removeprefix(place) for name in master if name.startswith(place)}


@applyToGenerator(set)
def show(place, master):
    """basically runs the ls method by splitting to the first /"""
    for name in subset(place, master):
        a = name.find('/') + 1
        if a > 0:
            yield name[:a]
        elif name != '':
            yield name


class App(Tk):
    """main object class window thing"""

    def __init__(self):
        Tk.__init__(self)
        self.zipfile = self.aim = self.files = None

        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Command-w>", lambda e: self.destroy())
        self.bind("<Command-o>", lambda e: self.openDocument())
        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label="unzip", command=self.unzip)
        self.lists = []
        self.lift()
        self.attributes('-topmost', True)
        self.openDocument()

    def unzip(self):
        """unzip selected file(s)"""
        file_list = self.lists[-1]
        if not file_list.curselection(): file_list = self.lists[-2]
        f = join(file_list.pwd, file_list.get(file_list.curselection()))
        if f.endswith('/'):
            for name in self.files:
                if name.startswith(f) and not name.endswith('/'):
                    self.zipfile.extract(name[2:], self.aim)
        else:
            self.zipfile.extract(f[2:], self.aim)

    def openDocument(self):
        """select a zip file"""
        document = filedialog.askopenfilename(initialdir="~", title="Select ZIP")
        if not document: return
        try:
            self.zipfile = ZipFile(document)
        except Exception as e:
            return self.wm_title(str(e))
        self.aim = abspath(join(document, pardir))
        self.files = {f'./{i}' for i in self.zipfile.namelist()}
        self.popDownTo(0)
        self.wm_title(document)
        FileList(self)

    def popDownTo(self, to):
        """repeatedly call .pop until you have a specific amount of files in the list"""
        for _ in range(len(self.lists) - to - 1):
            self.pop()

    def pop(self):
        """pop and destroy the last item in the file list"""
        if len(self.lists) < 1: return
        self.lists.pop().destroy()
        self.columnconfigure(len(self.lists), weight=0)


class FileList(Listbox):
    """the vertical file selector thing"""

    def __init__(self, master: App, place='./'):
        Listbox.__init__(self, master, selectmode="SINGLE")
        self.grid(row=0, column=len(master.lists), sticky="NSWE")
        master.columnconfigure(len(master.lists), weight=1)
        master.rowconfigure(0, weight=1)
        self.master: App = master
        self.pwd = place
        master.lists.append(self)
        for i in sorted(show(place, master.files), key=lambda z: f'!{z}' if z.endswith('/') else z):
            self.insert("end", i)
        self.bind("<Button-1>", lambda e: self.click())
        self.bind("<Button-2>", lambda e: self.master.menu.post(e.x_root, e.y_root))

    def click(self, retry=1):
        """something to register the clicks and selections"""
        if retry: return self.after(20, lambda: self.click(retry - 1))
        sel = self.curselection()
        self.master.popDownTo(int(self.grid_info().get('column', 0)))
        FileList(self.master, self.pwd + self.get(sel))


@add_to_all
def ZipGui():
    """Creates a nice gui for zip files"""
    App().mainloop()


@add_to_all
def unzip(file, aim='', file_iterable=None):
    """unzip a file: file by file. return a set of files that were unable to be extracted"""
    zip_file = ZipFile(file)
    if not aim:
        aim = abspath(join(file, pardir))
    if not file_iterable: file_iterable = zip_file.namelist()
    shuffle(file_iterable)
    failed = set()
    while len(file_iterable) != 0:
        extract = file_iterable.pop()
        if not exists(join(aim, extract)):
            try:
                print(f'Doing: {extract}')
                zip_file.extract(extract, aim)
            except Exception as e:
                failed.add(extract)
                print(f'Failed: {extract}')
                print(e)
    return failed
