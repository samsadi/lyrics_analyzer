import pandas as pd
import numpy as np
import re
import string
from os import path
import unidecode

def get_data(d):
    '''
    OUTPUT a dataframe including all the data
    '''

    df_scraped = pd.DataFrame.from_csv(path.join(d, 'data/scraped_lyrics.tsv'), sep='\t', index_col=False)

    # the main data without the lyrics and the genre: shape = (17094, 269)
    df_main = pd.read_csv(path.join(d, 'data/EvolutionMusicUSA_MainData.csv'))

    # the data including genre: shape = (17094, 141)
    df_genre = pd.read_table(path.join(d, 'data/EvolutionMusicUSA_TagData.tsv'))

    # take the song year and genre cluster from the main data and add to the sraped data:
    df_scraped['year'] = df_main['year']
    df_scraped['fiveyear'] = df_main['fiveyear']
    df_scraped['decade'] = df_main['decade']
    df_scraped['genre_cluster'] = df_main['cluster']

    df_merge = pd.merge(df_scraped, df_genre, how='inner', on=['recording_id', 'recording_id'])

    # keep only the songs that have lyrics:
    df_lyrics_exist = df_merge[df_merge['lyrics']!='Lyrics Not found']

    # final dataframe to be used:
    final_data = df_lyrics_exist
    final_data = final_data.reset_index(drop=True)
    df = final_data.copy()
    final_data.to_csv(path.join(d, 'data/final_data.csv'), sep='\t', encoding='utf-8')
    return

if __name__ == '__main__':

    d = path.dirname('/Users/Samaneh/Desktop/LyricsTrendAnalysis/')
    get_data(d)
