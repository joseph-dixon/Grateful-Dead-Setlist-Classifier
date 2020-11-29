#adapted from https://github.com/Midvel/medium_jupyter_notes/tree/master/naive_bayes_filter

import matplotlib.pyplot as plt
import csv
import string
import pandas as pd

setlists = pd.read_csv('/Users/josephdixon/Desktop/Data Projects/Setlist NB/cleaned_dead_setlists.csv')
setlists = setlists.drop(['Date'],axis=1)

#create list of years
year = 1965
years = []
while year < 1996:
    years.append(year)
    year += 1

#remove punctuation and create lists
setlists['Setlist'].str.replace('[','').str.replace(']','').str.replace('\'','').str.replace('\"','')
setlists['Setlist'] = setlists['Setlist'].str.split(':')

#split into train and test sets
train_data = setlists.sample(frac=0.8,random_state=1).reset_index(drop=True)
test_data = setlists.drop(train_data.index).reset_index(drop=True)
train_data = train_data.reset_index(drop=True)

#build frequency array and append to train data
song_array = list(set(train_data['Setlist'].sum()))
song_counts = pd.DataFrame([
    [row[1].count(song) for song in song_array]
    for _, row in train_data.iterrows()], columns=song_array)
train_data = pd.concat([train_data.reset_index(), song_counts], axis=1).iloc[:,1:]

#set up dictionaries with probabilities for functions to access
p_year = {}
n_year = {}
Nsongs = len(train_data.columns) - 2
alpha = 1

for year in years:
    p_year[year] = train_data['Year'].value_counts()[year] / train_data.shape[0]
    n_year[year] = train_data.loc[train_data['Year'] == year,'Setlist'].apply(len).sum()


#returns bayesian probability of a song being played in a given year
def prob_song_year(song,year):
    if song in train_data.columns:
        return (train_data.loc[train_data['Year'] == year, song].sum() + alpha) / (n_year[year] + alpha*Nsongs)
    else:
        return 1

#iterates through setlist and applies prob_song_year function to each song for each possible year
def classify(setlist):

    current_max = 0
    current_guess = None

    for year in years:
        p_year_given_setlist = p_year[year]
        for song in setlist:
            p_year_given_setlist *= prob_song_year(song,year)

        if p_year_given_setlist > current_max:
            current_max = p_year_given_setlist
            current_guess = year

    return current_guess

#apply model to test set and return accuracy
test_data['predicted'] = test_data['Setlist'].apply(classify)
correct = (test_data['predicted'] == test_data['Year']).sum() / test_data.shape[0] * 100
print(correct)
