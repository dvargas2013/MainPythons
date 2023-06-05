from os import renames, remove, makedirs, mkdir, link as copyfile_hardlink
from os.path import exists, join, splitext, split, relpath, abspath, getmtime, basename
from shutil import copy2 as copyfile_normal  # preserves metadata

from done.File import files, folders, Desktop


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
    if input(f'are you sure you want to make {sum(size ** i for i in range(depth + 1))} folders')[0] in 'Yy':
        paths = [maze_root]
        for _ in range(depth):
            new_paths = []
            for base in paths:
                for _ in range(size):
                    name_choice = join(base, chain(1, name_length))
                    while name_choice in new_paths: name_choice = join(base, chain(1, name_length))
                    new_paths.append(name_choice)
            paths = new_paths
        for dirs in paths: makedirs(dirs)
        maze_root = choice(paths)
        renames(file, join(maze_root, basename(file)))
        return maze_root


def linkDirectory(source, destination, symlink=True):
    """Walks through files in source and symlinks to destination. Making directories as needed."""
    import os
    link = os.symlink if symlink else os.link
    for d in folders(source, relative=True):
        print('dir:', d)
        d = join(destination, d)
        if not exists(d): mkdir(d)
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
            print(f'Delete: {file} => {out}')
        except OSError:
            remove(file)
            print(f'HardRemove: {file} => the pit')


def Copy(src_file, dst_file, trash_root=Desktop, copyfile=copyfile_normal):
    """delete the dst_file and copy over from the src_file"""

    head, tail = split(dst_file)  # Make sure path exists
    if head and tail and not exists(head): makedirs(head)

    Delete(trash_root, dst_file)
    copyfile(src_file, dst_file)
    print(f'Copy: {src_file} => {dst_file}')


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
            time_src = getmtime(src_file)
            time_dst = getmtime(dst_file)

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
