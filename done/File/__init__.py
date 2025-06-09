"""If I made it, and it has to do with files it is here"""

from contextlib import contextmanager
from os import walk, environ, renames
from os.path import join, relpath, samefile, exists

from done.File.module import submodules, filter_off_modules_and_dunder

def same(file1, file2):
    """Checks if the 2 path names are representing the same location
Defaults to False on error"""
    try:
        return samefile(file1, file2)
    except OSError:
        return False


def getHome():
    """Get the HOME directory. (or USERPROFILE)"""
    return environ.get('HOME', environ.get('USERPROFILE'))


Desktop = join(getHome(), 'Desktop')


@contextmanager
def cwd_as(location):
    """set cwd as location and then set it back to what it was before

    if location doesn't exist or isn't a directory, will make directories as needed
    the directories will not be deleted.
    (it is a context manager over the variable given by os.getcwd nothing else)
    """
    import os
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


def read(file, tag='r', pickled=False):
    """read a file and return its contents"""
    if pickled and 'b' not in tag: tag += 'b'
    try:
        with open(file, tag) as f:
            if not pickled:
                return f.read()

            from pickle import load
            return load(f)
    except Exception as e:
        print(e)
    if "b" in tag:
        with open(file, tag) as f:
            return f.read()
    else:
        with open(file, tag, encoding='latin_1') as f:
            return f.read()


def write(s, file, tag='w', encoding="utf",
          onerror=['strict', 'replace', 'ignore', 'xmlcharrefreplace', 'backslashreplace'][3], pickled=False):
    """write to a file"""
    if pickled:
        from pickle import dumps
        s = dumps(s)
    else:
        from done.File.pretty import stringify
        s = stringify(s)

    if type(s) == str:
        try:
            with open(file, tag, encoding=encoding) as f:
                f.write(s)
                return True
        except Exception as e:
            print(e)
            s = s.encode(encoding or "utf-8", onerror)
    if type(s) == bytes:
        if 'b' not in tag: tag += 'b'
        with open(file, tag) as f:
            f.write(s)
            return True
    return False


def rename_files(file_iterable, change,
                 success=lambda f, n: print(f"Renamed: {f}\n\t{n}\n"),
                 error=lambda f, n, e: print(f"Renaming Error {e}: {f}\n\t{n}\n"),
                 already_exists=lambda f, n: print(f"Existence Error: {n} already exists"),
                 does_not_exist=lambda f, n: print(f"Existence Error: {f} does not exist"),
                 no_change=lambda f, n: print(f"Change function did not change: {f}")):
    """changes file strings in {files} using the {change} function

for each of the files:
    if {change} doesn't change location, {no_change} is called
    if file doesn't exist, {does_not_exist} is called
    if what {change} changes it to already exists, {already_exists} is called
    if there is an error trying to rename, {error} is called
    if renaming succeeds, {success} is called
"""

    if type(file_iterable) == str: file_iterable = [file_iterable]
    for f in file_iterable:
        n = change(f)  # apply change function

        if same(f, n):
            return no_change(f, n)

        if not exists(f):  # old name doesn't exist
            return does_not_exist(f, n)

        if exists(n):  # new name taken
            return already_exists(f, n)

        try:
            renames(f, n)
        except OSError as e:
            error(f, n, e)
        else:
            success(f, n)


renamer = rename_files


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


__all__ = filter_off_modules_and_dunder(dir(), globals()) if __name__ != "__main__" else []
__all__.extend(submodules(__file__))
