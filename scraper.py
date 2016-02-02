import re
import time
import sys
import requests
from bs4 import BeautifulSoup
#from SECRETS import *

def getLyricsFromURL(url, regex, keepchars = '.+-'):
    soup = BeautifulSoup(requests.get(url).content, 'lxml')

    title_raw = soup.h1.get_text()
    title = ''.join(c if c.isalnum() or c in keepchars
                    else '_' for c in title_raw).rstrip()

    # get lyrics with song section breaks
    lyrics_raw = ''.join(lyr.get_text() for lyr in soup.lyrics.find_all(['b','p']))
    lyrics = re.sub(regex, '', lyrics_raw).strip() + '\n' # rm leading \n only

    with open(title, 'w') as f:
        f.write(lyrics)


def doWork(file_in):
    # regex to remove `[HEADERS]`
    to_remove = re.compile('\[[^\]]*\]')
    with open(file_in, 'r') as f:
        for url in f.xreadlines():
            getLyricsFromURL(url.rstrip(), to_remove)
            time.sleep(5)


if __name__ == "__main__":
    try:
        FILE = sys.argv[1]
    except(IndexError):
        print "Where's the file of URLs to scrape ?"
        raise
    doWork(FILE)
