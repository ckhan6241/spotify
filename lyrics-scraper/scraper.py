from bs4 import BeautifulSoup
import json
import os
from os import path
import re
import threading
import time
from urllib import parse, request
from urllib.error import URLError

GENIUS_BASE_URL = "https://genius.com"
GENIUS_QUERY_BASE_URL = "https://genius.com/api/search/song"

THREAD_INTERVAL = 0.05
MAX_THREAD = 100

def scrape(song_name, artist_name, output_directory):
    """Scrape genius.com for the lyrics, it will create a file with name [song_name]_[artist_name].txt with spaces replaced by '-' in lower
    :param song_name: the song's name
    :param artist_name: the artist's name
    :param output_directory: the output directory where the file will be written
    :return: None
    """
    __handle_output_directory(output_directory)
    try:
        lyrics = __get_lyrics(song_name, artist_name) # elaborated song names will not be found, have to extract the song name
    except:
        extracted_song_name = re.search("([\s\w]+)", song_name).group(0).strip()
        lyrics = __get_lyrics(extracted_song_name, artist_name)
    filename = '_'.join((song_name.lower().replace(' ', '-'), artist_name.lower().replace(' ', '-'))) + '.txt'
    filename = filename.replace("/", "").replace("\\", "") # filename cannot contains slashes
    with open(path.join(output_directory, filename), 'w') as f:
        f.write(lyrics)

def scrape_multi(song_names, artist_names, output_directory):
    """Scrape multiple songs' lyrics using scrape function above
    :param song_names: song names
    :type song_names: a sequence of string
    :param artist_names: artist names
    :type artist_names: a sequence of string
    :param output_directory: the directory where the files will be written
    :return: None
    """
    exitFlag = False
    queueLock = threading.Lock()
    queue = list(zip(song_names, artist_names))
    class ScrapeThread(threading.Thread):
        def __init__(self, q):
            threading.Thread.__init__(self)
            self.q = q

        def run(self):
            while not exitFlag:
                with queueLock:
                    if len(queue) > 0:
                        song_name, artist_name = self.q.pop()
                    else:
                        break
                try:
                    scrape(song_name, artist_name, output_directory)
                    print("scraped %s by %s" % (song_name, artist_name))
                except Exception as e:
                    print(e)
                    print("ERROR!!!!!!!!!!! %s by %s" % (song_name, artist_name))
    thread_count = min(len(song_names), MAX_THREAD)
    threads = [ScrapeThread(queue) for i in range(thread_count)]
    for thread in threads:
        thread.daemon = True
        thread.start()
        time.sleep(THREAD_INTERVAL)
    while len(queue) > 0:
        pass
    exitFlag = True
    for t in threads:
        t.join()

def __handle_output_directory(output_directory):
    if not path.isdir(output_directory):
        try:
            os.makedirs(output_directory)
        except os.error:
            raise Exception("Error creating directory: {}".format(output_directory))

def __get_lyrics(song_name, artist_name):
    query_url = __prepare_url(song_name, artist_name)
    try:
        req = request.Request(query_url, headers=__get_spoof_headers())
        response = request.urlopen(req)
    except URLError:
        raise Exception("Unable to query via url: {}".format(query_url))
    lyrics_url = __process_query_response(response.read().decode('utf-8'))
    lyrics = __scrape_lyrics(lyrics_url)
    return lyrics

def __prepare_url(song_name, artist_name):
    param = parse.quote("{} {}".format(song_name, artist_name))
    url = "?q=".join((GENIUS_QUERY_BASE_URL, param))
    return url

def __get_spoof_headers():
    """Headers copied from chrome browser request"""
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

def __process_query_response(raw_response):
    data = json.loads(raw_response)
    if data["meta"]["status"] != 200:
        raise Exception("Error returned from query endpoint: {}".format(raw_response))
    results = data["response"]["sections"]
    assert len(results) == 1 and results[0]["type"] == "song", "Return json not recognized: {}".format(results)
    try:
        url = results[0]["hits"][0]["result"]["path"]
    except IndexError:
        raise Exception("No results")
    return GENIUS_BASE_URL + url

def __scrape_lyrics(url):
    try:
        req = request.Request(url, headers=__get_spoof_headers())
        response = request.urlopen(req)
    except URLError:
        raise Exception("Unable to open url: {}".format(url()))
    soup = BeautifulSoup(response.read(), "html.parser")
    lyrics_div = soup.find_all("div", class_="lyrics")[0]
    lyrics = lyrics_div.get_text()
    return lyrics.strip()

if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("./datasets/featuresdf.csv")
    song_names = data["name"]
    artist_names = data["artists"]
    # song = "look what you made me do"
    # artist = "taylor swift"
    directory = "lyrics-data"
    # scrape(song, artist, directory)
    scrape_multi(song_names, artist_names, directory)
