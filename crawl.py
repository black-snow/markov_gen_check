#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import urllib.parse
import sys
import regex
from pathlib import Path

#
# Crawl lyrics from songtexte.com
# Usage: python crawl.py start_url /path/to/store/lyrics
# Example: python crawl.py 'https://www.songtexte.com/artist/coldplay-3d6bde3.html' ./lyrics/coldplay
#

pages = [sys.argv[1]] #'https://www.songtexte.com/artist/coldplay-3d6bde3.html'
path = Path(sys.argv[2])
path.mkdir(exist_ok = True)
llinks = []

# fetch links
for url in pages:
    with requests.get(url) as f:
        soup = BeautifulSoup(f.content, 'html.parser')
        links = soup.select('.albumDetail.row a.nested[href]')
        llinks += map(lambda x: urllib.parse.urljoin(url, x['href']),links)
        next_page_links = soup.select('a.arrow.next[href*="artist"]')
        pages += map(lambda x: urllib.parse.urljoin(url, x['href']), next_page_links)

for link in llinks:
    with requests.get(link) as f:
        print(link)
        try:
            soup = BeautifulSoup(f.content, 'html.parser')
            text = soup.select('#lyrics').pop().get_text()
            title = soup.select('h2.hidden-print').pop().get_text()
            fname = regex.sub('[^\w _]', '', title).replace(' Songtext', '') + '.txt'

            with open(path / fname, 'w') as file:
                file.write(text)
        except:
            print('failed')
