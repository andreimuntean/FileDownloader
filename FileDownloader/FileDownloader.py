#!/usr/bin/python3

"""FileDownloader.py: Downloads all files with a specified extension from a web page."""

__author__ = 'andrei.muntean.dev@gmail.com (Andrei Muntean)'

import re
from os import makedirs, path
from sys import argv
from urllib.request import urlopen, urlretrieve

def get_input_extension():
    if len(argv) == 4:
        return argv[1]
    else:
        print('Please specify an extension.')

        return input('> ')

def get_input_url():
    url = ''

    if len(argv) == 4:
        url = argv[2]
    else:
        print('Please specify a URL.')
        url = input('> ')

    # Defaults to HTTP if no protocol was specified.
    if not '//' in url:
        url = 'http://' + url

    return url

def get_input_destination():
    if len(argv) == 4:
        return argv[3]
    else:
        print('Where would you like to download the files?')
    
        return input('> ')

def get_file_urls(extension, url):
    response = urlopen(url, timeout=5)
    html = str(response.read())
    file_urls = []

    for occurrence in re.finditer('.' + extension, html):
        # Determines whether the URL is contained within a single quote or a double quote.
        delimiter = '\'' if html[occurrence.end()] == '\'' else '"'

        # Gets the starting position of the URL.
        url_start = html[:occurrence.start()].rfind(delimiter) + 1

        # Gets the URL.
        file_url = html[url_start:occurrence.end()]

        if file_url[0] == '/':
            if not file_url[1] == '/':
                # Turns relative paths into absolute paths.
                file_url = url + file_url
            else:
                file_url = file_url[2:]

        # Defaults to HTTP if no protocol was specified.
        if not '//' in file_url:
            file_url = 'http://' + file_url

        # Stores the URL if it hasn't already been stored.
        if not file_url in file_urls:
            file_urls.append(file_url)
            
    return file_urls

def download(file_urls, destination):
    """Downloads the files from the given URLs into the specified destination."""
    
    if not path.exists(destination):
        print('Creating directory \'%s\'.' % destination)
        makedirs(destination)

    for file_url in file_urls:
        # Sets the file name as the string that follows the last '/' in the URL.
        file_name = file_url[file_url.rfind('/') + 1:]

        try:
            # Downloads the file to the specified folder.
            urlretrieve(file_url, path.join(destination, file_name))
            print('Downloaded \'%s\'.' % file_name)
        except:
            pass

def run():
    """Runs the program."""

    extension = get_input_extension()
    url = get_input_url()
    destination = get_input_destination()

    try:
        download(get_file_urls(extension, url), destination)
        print('Download complete.')
    except:
        raise SystemExit('An error has occurred. Could not download files.')

run()