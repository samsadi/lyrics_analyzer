import pandas as pd
import numpy as np
import re
from os import path
from stop_words import get_stop_words


def get_emotions_count(list_words, df, vocabulary):
    '''
    parameters:
    -----------
    list of words (typically 100 words long)
    df: from NRC emotions, of shape (word as index, emotions as column names)
    vocabulary: list of unique words for which we have emotions
                vocabulary = df[0].unique()
    '''
    # Initializing an array of 8 emotions + 2 sentiments (positive/negative).
    # Order:
    # anger, anticipation, disgust, fear, joy, negative,
    # positive, sadness, surprise, trust

    emotion_count = np.zeros(10)

    #counting the number of words in each emotion
    for word in list_words:
        if word in vocabulary:
            #looking up the word
            emotion_for_word = df.ix[ word ].values
            # Adding up the emotions
            emotion_count += emotion_for_word
    return emotion_count


def get_yearly_emotions(df_lyrics, df_emotions, vocabulary):

    # Calculate emotions per year:

    df_lyrics_year = df[['lyrics', 'year']]
    df_year_grouped = df_lyrics_year.groupby('year').sum()

    year_words = []
    for i in xrange(1960,2010):
        lyrics_year = df_year_grouped.ix[i]
        year_words.append(lyrics_year[i][0].split())

    emotions_count_yearly = np.zeros((50,10))

    for i in xrange(len(df_year_grouped)):
        emotions_count_yearly[i] = get_emotions_count(year_words, df_emotions, vocabulary)
    return emotions_count_yearly


if __name__ == '__main__':

    d = path.dirname('/Users/Samaneh/Desktop/LyricsTrendAnalysis/')
    df_lyrics = pd.read_csv(path.join(d, 'data/clean_lyrics.csv'), sep='\t', encoding='utf-8')
    all_lyrics = df_lyrics['lyrics']
    all_words = all_lyrics.str.split()

    emotions = pd.read_csv(path.join(d, 'data/NRC_emotions.txt'), sep='\t', header = None)
    df_emotions = emotions.pivot(0,1,2)
    vocabulary = df_emotions.index.unique()

    # Calculate total emotion count for all the lyrics:
    for i in xrange(len(all_words)):
        emotions_count += get_emotions_count(all_words[i], df_emotions, vocabulary)
    np.save("total_lyrics_emotions", emotions_count)

    # Calculate emotions per year:
    yearly_emotions = get_yearly_emotions(df_lyrics, df_emotions, vocabulary)
    np.save("yearly_emotions", yearly_emotions)
