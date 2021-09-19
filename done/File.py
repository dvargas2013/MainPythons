"""If I made it and it has to do with files it is here"""

import os.path
from contextlib import contextmanager
from os import renames, remove, walk, makedirs, environ, link as copyfile_hardlink
from os.path import exists, join, splitext, split, relpath, abspath
from shutil import copy2 as copyfile_normal  # preserves metadata
from typing import Dict, List
from urllib.request import urlopen


def same(file1, file2):
    """Checks if the 2 path names are representing the same location
Defaults to False on error"""
    try:
        return os.path.samefile(file1, file2)
    except OSError:
        return False


def getHome():
    """Get the HOME directory. (or USERPROFILE)"""
    return environ.get('HOME', environ.get('USERPROFILE'))


Desktop = join(getHome(), 'Desktop')


@contextmanager
def cwd_as(location):
    """set cwd as location and then set it back to what it was before

    if location doesnt exist or isnt a directory, will make directories as needed
    the directories will not be deleted.
    (it is a context manager over the variable given by os.getcwd nothing else)
    """
    previous = os.getcwd()
    try:
        os.chdir(location)
        yield
    except (FileNotFoundError, NotADirectoryError):
        os.makedirs(location)
        os.chdir(location)
        yield
    finally:
        os.chdir(previous)


def files(directory, relative=True):
    """Yield all files in Directory, relative to the Directory"""
    for rt, ds, fs in walk(directory):
        if relative:
            yield from (relpath(join(rt, f), directory) for f in fs)
        else:
            yield from (join(rt, f) for f in fs)


def folders(directory, relative=True):
    """Yield all folders in Directory (including self), relative to the Directory"""
    yield relpath(directory, directory) if relative else directory
    for rt, ds, fs in walk(directory):
        if relative:
            yield from (relpath(join(rt, d), directory) for d in ds)
        else:
            yield from (join(rt, d) for d in ds)


def listFormats(directory):
    """recursively collects all extensions"""
    lis = set()
    for name in files(directory):
        name, ext = splitext(name)
        if ext and name != ext and ext not in lis:
            lis.add(ext)
            yield ext


def hideInMaze(file, maze_root, depth, size, name_length=7):
    """Hides a file inside {size} directories in each directory for {depth} levels"""
    from done.String.Generators import chain
    from random import choice
    if input('are you sure you want to make ' + str(sum(size ** i for i in range(depth + 1))) + ' folders')[0] in 'Yy':
        paths = [maze_root]
        for d in range(depth):
            new_paths = []
            for base in paths:
                for num in range(size):
                    name_choice = join(base, chain(1, name_length))
                    while name_choice in new_paths: name_choice = join(base, chain(1, name_length))
                    new_paths.append(name_choice)
            paths = new_paths
        for dirs in paths: makedirs(dirs)
        maze_root = choice(paths)
        renames(file, join(maze_root, os.path.basename(file)))
        return maze_root


def linkDirectory(source, destination, symlink=True):
    """Walks through files in source and symlinks to destination. Making directories as needed."""
    link = os.symlink if symlink else os.link
    for d in folders(source, relative=True):
        print('dir:', d)
        d = join(destination, d)
        if not exists(d): os.mkdir(d)
    for f in files(source, relative=True):
        print('f:', join(source, f), join(destination, f))
        try:
            link(join(source, f), join(destination, f))
        except OSError:
            print('cannot:', f)


def Delete(root, file, trash_name="CopyTrash"):
    """Moves file to a 'CopyTrash' directory inside the root directory

Note: On some drives I can't use renames
instead of doing the usual <copy and delete> thing I just straight up delete it
Sorry :c"""
    out = join(trash_name, relpath(file, root))
    if exists(file):
        try:
            renames(file, out)
            print('Delete: %s => %s' % (file, out))
        except OSError:
            remove(file)
            print('HardRemove: %s => the pit' % file)


def Copy(src_file, dst_file, trash_root=Desktop, copyfile=copyfile_normal):
    """delete the dst_file and copy over from the src_file"""

    head, tail = split(dst_file)  # Make sure path exists
    if head and tail and not exists(head): makedirs(head)

    Delete(trash_root, dst_file)
    copyfile(src_file, dst_file)
    print('Copy: %s => %s' % (src_file, dst_file))


def smartBackup(source, destination, hardlink=False):
    """Checks if a file has been modified and transfers it over as needed

When copying with hardlink active, it will hardlink the files together
"""
    from functools import partial

    src, dst = abspath(source), abspath(destination)
    cp = copyfile_hardlink if hardlink else copyfile_normal
    copy = partial(Copy, trash_root=dst, copyfile=cp)

    for file in files(dst, relative=True):
        # validate files that are already in the backup location need special thought
        dst_file = join(dst, file)
        src_file = join(src, file)

        try:
            time_src = os.path.getmtime(src_file)
            time_dst = os.path.getmtime(dst_file)

            if abs(time_src - time_dst) < 10:
                continue  # negligibly short amount of time

            # copies over the most recently edited file
            if time_src > time_dst:
                copy(src_file, dst_file)
            else:
                copy(dst_file, src_file)

        except FileNotFoundError:
            # if it was deleted from the src delete it from the dst
            Delete(dst, dst_file)

    for file in files(src):  # files that are in the original are easy
        src_file, dst_file = join(src, file), join(dst, file)
        # copy over files that I haven't already gone through in the previous cycle
        if not exists(dst_file): Copy(src_file, dst_file)


def rename_file(file_iterable, change,
                success=lambda f, n: print("Renamed: " + f + '\n\t' + n + '\n'),
                error=lambda f, n, e: print(("Renaming Error %s: " % e) + f + '\n\t' + n + '\n'),
                already_exists=lambda f, n: print("Existence Error: " + n + ' already exists'),
                does_not_exist=lambda f, n: print("Existence Error: " + f + ' does not exist'),
                no_change=lambda f, n: print("Change function did not change: " + f)):
    """changes file strings in {files} using the {change} function
    
for each of the files:
    if {change} doesnt change location, {no_change} is called
    if file doesnt exist, {does_not_exist} is called
    if what {change} changes it to already exists, {already_exists} is called
    if there is an error trying to rename, {error} is called
    if renaming succeeds, {success} is called
"""

    if type(file_iterable) == str: file_iterable = [file_iterable]
    for f in file_iterable:
        n = change(f)  # apply change function
        if not same(f, n):  # might point to same file
            if exists(f):  # old name might not exist
                if not exists(n):  # new name might exist
                    try:
                        renames(f, n)  # renames might fail
                    except OSError as e:
                        error(f, n, e)  # if failed to rename
                    else:
                        success(f, n)  # it succeeded the rename
                else:
                    already_exists(f, n)  # file n already existed
            else:
                does_not_exist(f, n)  # file f does not exist
        else:
            no_change(f, n)  # function change did not change f


renamer = rename_file


def site_look(url='', temp=join(Desktop, 'file.html'), browser='Google Chrome'):
    """Save html to desktop and open it with a browser from url given
Moderately safer than directly going to a site"""
    from subprocess import call
    if not url: url = input()
    while url:
        write(site_read(url), temp)
        try:
            call(['open', '-a', browser, temp])
        except Exception as e:
            print(e)
            print('try again')
        url = input()
    if exists(temp): remove(temp)


def site_read(url, tries=17):
    """Read a url and return string contents"""
    if not url.startswith('http'): url = 'http://' + url
    for i in range(tries):
        try:
            return urlopen(url).read().decode()
        except Exception as e:
            print(e)
            from time import sleep
            sleep(1)
            print('Retrying: ' + url)


def read(file, tag='r', pickled=False):
    """read a file and return its contents"""
    if pickled and 'b' not in tag: tag += 'b'
    try:
        with open(file, tag) as f:
            if pickled:
                from pickle import load
                return load(f)
            else:
                return f.read()
    except Exception as e:
        print(e)
    if "b" in tag:
        with open(file, tag) as f:
            return f.read()
    else:
        with open(file, tag, encoding='latin_1') as f:
            return f.read()


def write_dict_to_tgf(dic: Dict[str, List[str]], file):
    nodes = sorted(set.union(*map(set, dic.values()), set(dic.keys())))
    node_to_tgf_index = {n: i for i, n in enumerate(nodes, start=1)}

    f = []
    for i, n in enumerate(nodes, start=1):
        f.append(f"{i} {n}")
    f.append("#")
    for i, js in dic.items():
        for j in js:
            f.append(f"{node_to_tgf_index[i]} {node_to_tgf_index[j]}")

    return write("\n".join(f), file)


def write(s, file, tag='w', encoding="utf",
          onerror=['strict', 'replace', 'ignore', 'xmlcharrefreplace', 'backslashreplace'][3], pickled=False):
    """write to a file"""
    if pickled:
        from pickle import dumps
        s = dumps(s)
    else:
        if type(s) == dict:
            s = "{\n\t%s\n}" % ',\n\t'.join("%s:\t%s" % (repr(i), repr(j)) for i, j in s.items())
        elif type(s) == list:
            s = "[\n\t%s\n]" % ',\n\t'.join(repr(i) for i in s)
        elif type(s) == tuple:
            s = "(\n\t%s\n)" % ',\n\t'.join(repr(i) for i in s)
        elif type(s) == set:
            s = "{\n\t%s\n}" % ',\n\t'.join(repr(i) for i in s)

    if type(s) == str:
        try:
            with open(file, tag, encoding=encoding) as f:
                f.write(s)
                return True
        except Exception as e:
            print(e)
            if encoding:
                s = s.encode(encoding, onerror)
            else:
                s = s.encode('utf-8', onerror)
    if type(s) == bytes:
        if 'b' not in tag: tag += 'b'
        with open(file, tag) as f:
            f.write(s)
            return True
    return False


def repeatTillValid(validation_func):
    """When given a validation function, returns a decorator

The decorator runs `validationFn(decoratedFn(...))`
until validationFn returns true

It then returns the value passed into decoratedFn

EXAMPLE USAGE:
@repeatTillValid(str.islower)
def getInput(): return input()

will repeatedly execute input() until the input is lowercase"""
    from functools import wraps

    def decoratorWithParameter(decorated_func):
        @wraps(decorated_func)
        def wrapper(*args, **kwargs):
            x = decorated_func(*args, **kwargs)
            while not validation_func(x):
                x = decorated_func(*args, **kwargs)
            return x

        return wrapper

    return decoratorWithParameter


def reImport(module):
    """imports and returns a {module} object. Automatically save itself in the global"""
    import importlib
    return importlib.reload(module)


def subset(place, master):
    """used to make relative paths out of the master list"""
    return {name.lstrip(place) for name in master if name.startswith(place)}


def show(place, master):
    """basically runs the ls method by splitting to the first /"""

    def generator():
        for name in subset(place, master):
            a = name.find('/') + 1
            if a > 0:
                yield name[:a]
            elif name != '':
                yield name

    return set(generator())


def ZipGui():
    """Creates a nice gui for zip files"""
    from tkinter import Tk, Listbox, filedialog, Menu
    from zipfile import ZipFile

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
                return self.wm_title(e)
            self.aim = abspath(join(document, os.pardir))
            self.files = set('./' + i for i in self.zipfile.namelist())
            self.popDownTo(0)
            self.wm_title(document)
            FileList(self)

        def popDownTo(self, to):
            """repeatedly call .pop until you have a specific amount of files in the list"""
            for i in range(len(self.lists) - to - 1): self.pop()

        def pop(self):
            """pop and destroy the last item in the file list"""
            if len(self.lists) < 1: return
            self.lists.pop().destroy()
            self.columnconfigure(len(self.lists), weight=0)

    class FileList(Listbox):
        """the vertical file selector thing"""

        def __init__(self, master, place='./'):
            Listbox.__init__(self, master, selectmode="SINGLE")
            self.grid(row=0, column=len(master.lists), sticky="NSWE")
            master.columnconfigure(len(master.lists), weight=1)
            master.rowconfigure(0, weight=1)
            self.master = master
            self.pwd = place
            master.lists.append(self)
            for i in sorted(show(place, master.files), key=lambda z: '!' + z if z.endswith('/') else z): self.insert(
                "end", i)
            self.bind("<Button-1>", lambda e: self.click())
            self.bind("<Button-2>", lambda e: self.master.menu.post(e.x_root, e.y_root))

        def click(self, retry=1):
            """something to register the clicks and selections"""
            if retry: return self.after(20, lambda: self.click(retry - 1))
            sel = self.curselection()
            self.master.popDownTo(int(self.grid_info().get('column', 0)))
            FileList(self.master, self.pwd + self.get(sel))

    app = App()
    app.mainloop()


def unzip(file, aim='', file_iterable=None):
    """unzip a file file by file. return a set of files that were unable to be extracted"""
    from zipfile import ZipFile
    from random import shuffle
    zip_file = ZipFile(file)
    if not aim:
        aim = abspath(join(file, os.pardir))
    if not file_iterable: file_iterable = zip_file.namelist()
    shuffle(file_iterable)
    failed = set()
    while len(file_iterable) != 0:
        extract = file_iterable.pop()
        if not exists(join(aim, extract)):
            try:
                print('Doing: %s' % extract)
                zip_file.extract(extract, aim)
            except Exception as e:
                failed.add(extract)
                print('Failed: %s' % extract)
                print(e)
    return failed
