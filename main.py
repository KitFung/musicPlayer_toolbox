#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path, rename
from multiprocessing import Pool
import urllib
import json

from bs4 import BeautifulSoup

THREAD_NUMS = 5
SAVE_FOLDER = './'


def download_audio(id_title):
    id, title = id_title

    test = urllib.FancyURLopener()
    api_url = 'https://tw.streetvoice.com/api/v3/songs/{}/?only_fields=file'

    print('Downloading %s' % id)
    response = urllib.urlopen(api_url.format(id))
    data = json.loads(response.read())

    audio_url = data['file']

    save_name = path.join(SAVE_FOLDER, '%s.mp3' % title)
    test.retrieve(audio_url,
                  save_name)


def find_all_name_and_id(url):
    response = urllib.urlopen(url)
    soup = BeautifulSoup(response.read().decode('utf-8', 'ignore'))
    hrefs = soup.select('tbody h4 a')
    ids = []
    for href in hrefs:
        link = href['href']
        title = href.text
        print link
        link = link.strip('/')
        id = link.split('/')[-1]
        ids.append((id, title))

    print(ids)
    p = Pool(THREAD_NUMS)
    p.map(download_audio, ids)


if __name__ == '__main__':
    global SAVE_FOLDER

    if len(sys.argv) != 3:
        print('Invalid usage. Example: python %s target_url SAVE_FOLDER'
              % sys.argv[0])
        exit()

    target_url = sys.argv[1]
    SAVE_FOLDER = sys.argv[2]

    find_all_name_and_id(target_url)
