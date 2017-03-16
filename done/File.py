#!/usr/bin/env python3
'''If I made it and it has to do with files it is here'''
from os import chdir, renames, getcwd, remove, walk, makedirs
from os.path import exists, join, splitext, split, relpath, abspath
from glob import glob
def getHome():
    from os import environ
    return environ['HOME']
Desktop = join(getHome(),'Desktop')

def files(DIR,relative=True):
    """Yield all files in Directory, relative to the Directory"""
    for rt,ds,fs in walk(DIR):
        if relative: yield from (relpath(join(rt,f),DIR) for f in fs)
        else: yield from (join(rt,f) for f in fs)
def folders(DIR,relative=True):
    """Yield all folders in Directory (including self), relative to the Directory"""
    yield relpath(DIR,DIR) if relative else DIR
    for rt,ds,fs in walk(DIR):
        if relative: yield from (relpath(join(rt,d),DIR) for d in ds)
        else: yield from (join(rt,d) for d in ds)
def listFormats(place):
    """iterator with the extensions of all files under"""
    lis=set()
    for name in files(place):
        name,ext=splitext(name)
        if ext and name!=ext and ext not in lis:
            lis.add(ext)
            yield ext
def hideInMaze(file,mazeRoot,depth,size,dirNameLen=7):
    """Hides a file inside {size} directories in each directory for {depth} levels"""
    from done.String import chain
    from os.path import basename
    from random import randrange
    if input('are you sure you want to make '+str(sum(size**i for i in range(depth+1)))+' folders')[0] in 'Yy':
        paths=[mazeRoot]
        for d in range(depth):
            newpaths=[]
            for base in paths:
                for num in range(size):
                    namechoice = join(base,chain(1,dirNameLen))
                    while namechoice in newpaths: namechoice = join(base,chain(1,dirNameLen))
                    newpaths.append(namechoice)
            paths=newpaths
        for dirs in paths: makedirs(dirs)
        mazeRoot=paths[randrange(len(paths))]
        renames(file,join(mazeRoot,basename(file)))
        return mazeRoot
def linkDirectory(src, dest, symlink=True):
    """Walks through files in src and symlinks to dest. Making directories as needed."""
    from os import mkdir
    if symlink: from os import symlink as link
    else: from os import link
    for d in folders(src,relative=True):
        print('dir:',d)
        d = join(dest,d)
        if not exists(d): mkdir(d)
    for f in files(src,relative=True):
        print('f:',join(src,f),join(dest,f))
        try: link(join(src,f),join(dest,f))
        except: print('cannot:',f)



def Delete(copy,file):
    out = join('CopyTrash',relpath(file,copy))
    if exists(file): 
        try:
            renames(file, out)
            print('Delete: %s => %s'%(file,out))
        except OSError: #On drives I cant use renames. so hard removes take place. srry
            remove(file)
            print('HardRemove: %s => the pit'%file)
def smartBackup(orig, copy, hardlink=False):
    """Checks if a file has been modified and transfers it over as needed"""
    from os.path import getmtime as modT
    if hardlink: from os import link as copyfile
    else: 
        from shutil import copy2
        def copyfile(a,b): copy2(a,b,follow_symlinks=False)
    orig,copy = abspath(orig),abspath(copy)
    def Copy(old,new,copy=copy):
        head, tail = split(new) #Make sure directory exists
        if head and tail and not exists(head): makedirs(head)
        Delete(copy,new)
        copyfile(old,new)
        print('Copy: %s => %s'%(old,new))
        #except OSError: print('CannotCopy: %s => %s'%(old,new))
    
    for file in files(copy,relative=True): 
        file,origFile = join(copy,file), join(orig,file)
        try:
            mO,mC = modT(origFile), modT(file)
            if abs(mO-mC)<10: pass
            elif mO>mC: Copy(origFile,file)
            else: Copy(file,origFile)
        except FileNotFoundError: Delete(copy,file)
    for file in files(orig): 
        copyFile,file = join(copy,file), join(orig,file)
        if not exists(copyFile): Copy(file,copyFile)



def renamer(files, change, 
success=lambda f,n: print("Renamed: "+f+'\n\t'+n+'\n'),
error=lambda f,n: print("Renaming Error: "+f+'\n\t'+n+'\n'),
alreadyExists=lambda f,n: print("Existence Error: "+n+' already exists'),
doesNotExist=lambda f,n: print("Existence Error: "+f+' does not exist'),
noChange=lambda f,n: print("Change function did not change: "+f)):
    """changes file strings in {files} using the {change} function
    
    for each of the files:
        if {change} doesnt change location, {noChange} is called
        if file doesnt exist, {doesNotExist} is called
        if what {change} changes it to already exists, {alreadyExists} is called
        if there is an error trying to rename, {error} is called
        if renaming succeeds, {success} is called
    """
    from os.path import samefile
    def same(a,b):
        try: return samefile(a,b)
        except: return False
    if type(files)==str: files = [files]
    for f in files:
        n = change(f) # apply change function
        if not same(f,n): # might point to same file
            if exists(f): # old name might not exist
                if not exists(n): # new name might exist
                    try: renames(f,n) # renames might fail
                    except: error(f,n) # if failed to rename
                    else: success(f,n) # it succeded the rename
                else: alreadyExists(f,n)
            else: doesNotExist(f,n)
        else: noChange(f,n)
        
def delPyCache(place='/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/'):
    """removes __pycache__ and .pyc recursively"""
    from shutil import rmtree
    for root,directories,files in walk(place):
        for directory in directories:
            if directory=='__pycache__': rmtree(join(root,directory))
        for file in files:
            if file.endswith('.pyc'): remove(join(root,file))
            
def getSizes(DIR,dicti=dict(),gloob='*.*p*g'):
    """Get dimension of images in directory (recursively) -- Depends on sips being on computer"""
    from os import system
    from subprocess import check_output
    for d in folders(DIR,relative=False):
        if not glob(join(d,gloob)): continue
        f = check_output('sips -g pixelHeight -g pixelWidth %s'%join(d,gloob).replace(' ',r'\ '),shell=True).decode().split('\n')
        for name,heit,widf in zip(f[0::3],f[1::3],f[2::3]):
            heit = heit
            widf = widf
            try: dicti[relpath(name)] = (
                int( heit.replace('  pixelHeight: ','') ),
                int( widf.replace('  pixelWidth: ', '') )
            )
            except: pass
    return dicti
def resize(fileDict,types=set(['.jpeg','.jpg','.png']),shrink=1200):
    """Resize .png, .jpg, and .jpeg files in fileDict so biggest dimension is 1200 -- sips dependant"""
    from os import system
    while len(fileDict)>0:
        name,hw = fileDict.popitem()
        if max(hw)>shrink:
            ext = splitext(name)[-1]
            if ext in types: system('sips -Z %s "%s"'%(shrink,name))
            
def siteLook(url='',temp=join(Desktop,'file.html'),browser='Google Chrome'):
    """Save html to desktop and open it with a browser from url given - Moderately safer than directly going to a site"""
    from subprocess import call
    if not url: url=input()
    while url:
        write(siteRead(url),temp)
        try: call(['open','-a',browser,temp])
        except: print('try again')
        url = input()
    if exists(temp): remove(temp)
def siteRead(url,tries=17):
    """Read a url and return string contents"""
    if not url.startswith('http'): url='http://'+url
    try: 
        from urllib.request import urlopen
    except: 
        from urllib import urlopen
    for i in range(tries):
        try: return urlopen(url).read().decode()
        except:
            from time import sleep
            sleep(1)
            print('Retrying: '+url)
def read(file, tag='r', pickled=False):
    """read a file and return its contents"""
    if pickled and 'b' not in tag: tag+='b'
    try: 
        with open(file,tag) as f:
            if pickled: 
                from pickle import load
                return load(f)
            else: return f.read()
    except: 
        with open(file,tag,encoding='latin_1') as f: return f.read()
def write(s, file, tag='w', encoding="utf", onerror=['strict','replace','ignore','xmlcharrefreplace','backslashreplace'][3], pickled=False):
    """write to a file"""
    if pickled:
        from pickle import dumps
        s = dumps(s)
    else:
        if type(s)==dict: s="{\n\t%s\n}"%',\n\t'.join("%s:\t%s"%(repr(i),repr(j)) for i,j in s.items())
        elif type(s)==list: s="[\n\t%s\n]"%',\n\t'.join(repr(i) for i in s)
        elif type(s)==tuple:s="(\n\t%s\n)"%',\n\t'.join(repr(i) for i in s)
        elif type(s)==set:  s="{\n\t%s\n}"%',\n\t'.join(repr(i) for i in s)
    
    if type(s)==str:
        try: 
            with open(file,tag,encoding=encoding) as f: 
                f.write(s)
                return True
        except:
            if encoding: s = s.encode(encoding,onerror)
            else: s = s.encode('utf-8',onerror)
    if type(s)==bytes: 
        if 'b' not in tag: tag+='b'
        with open(file,tag) as f: 
            f.write(s)
            return True
    return False

def reImport(module="done.File",value="File"):
    """import a {module} and overwrite the global {value}"""
    from importlib import import_module 
    globals()[value] = import_module(module)

def dARename(*files):
    """rename files in a specific way to make deviantart downloaded content filenames better"""
    def newName(f):
        f,e=splitext(f) #extension
        b,f=split(f) #base folders
        s,a=f,f.rfind('-') 
        if a!=-1: s = f[:a] # $-dasdfnk
        s = s.split('_by_') # half_by_half
        if len(s)==2: return join(b,'_'.join(''.join(i for i in half.title() if i.isalnum()) for half in s))+e
        return join(b,s[0])+e
    for f in files:
        new = newName(f)
        if exists(f) and not exists(new): renames(f,new)


def subset(place,ZipFiles): return set(name.replace(place,'') for name in ZipFiles if name.startswith(place))
def show(place,ZipFiles):
    scan = set()
    for name in subset(place,ZipFiles):
        a = name.find('/')+1
        if a>0: scan.add(name[:a])
        elif name!='': scan.add(name)
    return scan
def ZipGui():
    from tkinter import Tk,Listbox,filedialog,Menu
    from zipfile import ZipFile
    from os import pardir
    class App(Tk):
        def __init__(self):
            Tk.__init__(self)
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
            l = self.lists[-1]
            if not l.curselection(): l = self.lists[-2]
            f = join(l.pwd,l.get(l.curselection()))
            if f.endswith('/'):
                for name in self.files:
                    if name.startswith(f) and not name.endswith('/'): self.zipfile.extract(name[2:],self.aim)
            else: self.zipfile.extract(f[2:],self.aim)
        def openDocument(self):
            self.document = filedialog.askopenfilename(initialdir = "~",title = "Select ZIP")
            if not self.document: return
            try: self.zipfile = ZipFile(self.document)
            except Exception as e:return self.wm_title(e)
            self.aim = abspath(join(self.document,pardir))
            self.files = set('./'+i for i in self.zipfile.namelist())
            self.popDownTo(0)
            self.wm_title(self.document)
            FileList(self)
        def popDownTo(self,to):
            n = len(self.lists)-to-1
            for i in range(n): self.pop()
        def pop(self):
            if len(self.lists) < 1: return
            self.lists.pop().destroy()
            self.columnconfigure(len(self.lists),weight=0)
    class FileList(Listbox):
        def __init__(self,master,place='./'):
            Listbox.__init__(self, master,selectmode="SINGLE")
            self.grid(row=0,column=len(master.lists),sticky="NSWE")
            master.columnconfigure(len(master.lists),weight=1)
            master.rowconfigure(0,weight=1)
            self.master = master
            self.pwd = place
            master.lists.append(self)
            for i in sorted(show(place,master.files),key=lambda z: '!'+z if z.endswith('/') else z): self.insert("end",i)
            self.bind("<Button-1>",lambda e: self.click())
            self.bind("<Button-2>",lambda e: self.master.menu.post(e.x_root,e.y_root))
        def click(self,retry=1):
            if retry: return self.after(20,lambda: self.click(retry-1))
            sel = self.curselection()
            self.master.popDownTo(int(self.grid_info().get('column',0)))
            FileList(self.master,self.pwd+self.get(sel))
    app = App()
    app.mainloop()



def unzip(file, aim='', files=None):
    """unzip a file file by file. return a set of files that were unable to be extracted"""
    from zipfile import ZipFile
    from random import shuffle
    ZIP = ZipFile(file)
    if not aim:
        from os import pardir
        aim = abspath(join(file, pardir))
    if not files: files = ZIP.namelist()
    shuffle(files)
    failed = set()
    while len(files) != 0:
        extract = files.pop()
        if not exists(join(aim,extract)):
            try: 
                print('Doing: %s'%extract)
                ZIP.extract(extract, aim)
            except:
                failed.add(extract)
                print('Failed: %s'%extract)
    return failed