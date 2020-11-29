import pandas as pd
import requests
from requests import get
from bs4 import BeautifulSoup
import re


setlists = []

index = 1
for n in range(2400):
    url = 'http://www.setlists.net/?show_id=' + str(index)
    index += 1
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "html.parser")

    if '0 Shows Found' in soup.text or 'The setlist for this show is unknown.' in soup.text:
        continue

    else:
        try:
            date_re = '(\d+\/\d+\/\d+)'
            songs_re = 'Set [1|2|3]:([\s\S]*)Download\/Listen'
            date_object = re.search(date_re,soup.text)
            date = date_object[1]
            year = '19' + str(date.split('/')[2])
            songs_object = re.search(songs_re,soup.text)
            songs = songs_object[1].split('\n')
            for idx, song in enumerate(songs):
                if ":" in song:
                    song_split = song.split(':')
                    songs[idx] = song_split[1]
                if song == '':
                    songs.pop(idx)

            to_add = (year, date, songs)
            setlists.append(to_add)
            print('Adding setlist from '+str(date))
        except:
            continue


df = pd.DataFrame(setlists)
df.to_csv('/Users/josephdixon/Desktop/dead_setlists.csv')
