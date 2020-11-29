import matplotlib.pyplot as plt
import csv
import string
import pandas as pd

with open('/Users/josephdixon/Desktop/Data Projects/Setlist NB/dead_setlists.csv') as csvfile:
    setlists = csv.reader(csvfile)

    song_hist = {}
    rebuilt_list = [['Year','Date','Setlist']]
    first_line = True

    # for each setlist, clean strings and build histogram, rebuild cleaned list mapping setlist to year
    for row in setlists:
        if first_line == True:
            first_line = False

        else:
            year = row[1]
            date = row[2]
            setlist = row[3]
            songs_expanded = setlist.split(',')
            for idx,song in enumerate(songs_expanded) :

                # get rid of precursors
                song = song.strip()
                if ":" in song:
                    to_cut_from = song.index(':')
                    songs_expanded[idx] = song[to_cut_from+1:]
                # if "set 2:" in song:
                #     to_cut_from = song.index(':')
                #     songs_expanded[idx] = song[to_cut_from+1:]
                # if "set 3:" in song:
                #     to_cut_from = song.index(':')
                #     songs_expanded[idx] = song[to_cut_from+1:]
                # if "Set 3:" in song:
                #     to_cut_from = song.index(':')
                #     songs_expanded[idx] = song[to_cut_from+1:]
                # if "Encore:" in song:
                #     to_cut_from = song.index(':')
                #     songs_expanded[idx] = song[to_cut_from+1:]

                # normalize songs
                song = song.strip()
                song = song.strip('[')
                song = song.strip(']')
                song = song.strip('\'')
                song = song.strip('\"')
                if song[len(song)-2:] == '\\r':
                    song = song[:len(song)-2]
                song.translate(str.maketrans('', '', string.punctuation))
                song = song.lower()

                songs_expanded[idx] = song #sub cleaned song back into list

                #build hist
                if song not in song_hist.keys():
                    song_hist[song] = 1
                else :
                    song_hist[song] += 1

            # this is redundant, but I don't know why the above section didn't work, so this is staying here for now
            for idx,song in enumerate(songs_expanded):
                if 'set' in song:
                    to_cut_from = song.index(':')
                    songs_expanded[idx] = song[to_cut_from+1:]
                if 'encore' in song:
                    to_cut_from = song.index(':')
                    songs_expanded[idx] = song[to_cut_from+1:]

            song_string = ''
            for song in songs_expanded:
                song_string += str(song) + ':'


            rebuilt_list.append([year,date,song_string])


cleaned_df = pd.DataFrame(rebuilt_list)
cleaned_df.to_csv('/Users/josephdixon/Desktop/Data Projects/Setlist NB/cleaned_dead_setlists.csv',header = False, index = False)
