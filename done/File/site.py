from os.path import exists, join
from os import remove
from urllib.request import urlopen

from done.File import Desktop, write


def look(url='', temp=join(Desktop, 'file.html'), browser='Google Chrome'):
    """Save html to desktop and open it with a browser from url given
Moderately safer than directly going to a site"""
    from subprocess import call
    if not url: url = input()
    while url:
        write(read(url), temp)
        try:
            call(['open', '-a', browser, temp])
        except Exception as e:
            print(e)
            print('try again')
        url = input()
    if exists(temp): remove(temp)


def read(url, tries=17):
    """Read url and return string contents"""
    if not url.startswith('http'): url = f'http://{url}'
    for _ in range(tries):
        try:
            return urlopen(url).read().decode()
        except Exception as e:
            print(e)
            from time import sleep
            sleep(1)
            print(f'Retrying: {url}')
