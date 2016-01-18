import pandas as pd
import numpy as np
import re
import string
from nltk.stem.snowball import SnowballStemmer
snowball = SnowballStemmer('english')


def get_clean_lyrics(lyrics):
    '''
    get rid of all the unnecessary tags, symbols, line breaks, etc.
    returns a numpy array with the cleaned lyrics.

    '''
    #lower case
    clean = all_lyrics.str.lower()

    #reference to verse and chorus
    clean = clean.str.replace('chorus:','')
    clean = clean.str.replace('verse:','')

    #new line breaks
    clean = clean.str.replace('\n', ' ')
    clean = clean.str.replace('\r', ' ')

    #untranslated symbols
    clean = clean.str.replace('amp', ' ')
    clean = clean.str.replace('quot', ' ')

    #stuff like repeat 5x
    clean = clean.str.replace(r'[\d]x','')

    #verse and chorus references
    clean = clean.str.replace(r'verse [\d]','')

    #keep words whitespace and '
    clean = clean.str.replace(r'[^\w\s\']','')

    clean = clean.str.replace(r'[\d]','')

    return clean


def get_stop_words_list():
    '''
    Prepare a list of (stop)words to be removed from the cleaned lyrics.

    '''

    #use english, french, and spanish stop words
    stop_words_eng = get_stop_words('english')
    stop_words_fr = get_stop_words('french')
    stop_words_sp = get_stop_words('spanish')

    stop_words = stop_words_eng + stop_words_fr + stop_words_sp

    #compile a list of words that can be considered noise
    noise_words = [
        "a","an", "an'", "about","above","ain't","ain", "aint", "all","along","also","although",
        "am","an","any","are","aren't", "away", "as","at","ay", "back", "be","because",
        "'cause","cause", "bit", "been","but","by","can", "can't", "cant","cannot","could",
        "couldn't","come","comes","cause", "chorus", "did","didn't","do", "don", "does",
        "doesn't","don't", "dont", "don'", "em'","else", "e.g.","either","etc","etc.",
        "even","ever","every", "for","from", "further","get","gets","give", "gives",
        "going", "goin'", "goes", "go","gonna", "gotta", "got","had","hardly","has",
        "hasn't","having","he", "hence","her","here","hereby","herein", "hereof","hereon",
        "hereto","herewith","him", "his","how","however","i","i'll", "ill",
        "im'","im", "i.e.","if","into","it","it's","its","just", "know", "ic", "lyricchecksum",
        "lyricid", "like","let", "make", "me","more","most", "mr","my","near","nor","now","of",
        "ok","on", "one","onto","other","our","out","over","put", "really", "re", "said",
        "same", "say", "see", "she","should","shouldn't","since","so","some","such","take",
        "than","that","thats", "that's", "the","their","them","then","there","thereby",
        "therefore","therefrom","therein", "tell", "thereof","thereon","thereto","therewith",
        "these","they","this","those","through", "thing","try", "thus","to","too","under",
        "until","till'", "unto","upon","us","very","viz", "want", "was", "wasn't", "wanna",
        "whatcha", "way", "we","went","were","what","when", "where","whereby","wherein",
        "whether","which","while", "will", "well", "wit", "who","whom",
        "whose","why","with","without","would","x", "you","your","you're", "youre", "y'all",
        "verse", "repeat", "chorus", "oh","ohh","ooh", "ah", "ahh", "yeah","yes", "u", "mmm",
        "uh", "hey", "la", "na", "yo", "ya", "yeh", "woah","whoa", "huh", "woah", "yea",
        "doo", "de", "nah", "da", "ha", "ba", "wo", "wow", "woo", "ooo", "dee", "dum",
        "hmm", "ve", "ll", "t", "muhahahahahahaha"
    ]

    remove_words = stop_words + noise_words
    remove_words = sorted(remove_words)

    return remove_words


if __name__ == '__main__':

    d = path.dirname('/Users/Samaneh/Desktop/LyricsAnalyzer/')
    df = pd.DataFrame.from_csv(path.join(d, 'data/final_data.csv'), sep='\t')
    song_list = df[['recording_id', 'year', 'genre_cluster', 'artist_name', 'track_name', 'lyrics_artist', 'lyrics_track', 'lyrics']]
    genres = np.array(song_list['genre_cluster'])

    all_lyrics = df['lyrics']
    clean_lyrics = get_clean_lyrics(all_lyrics)

    df_clean_lyrics = pd.DataFrame(get_clean_lyrics(all_lyrics))
    df_clean_lyrics.to_csv(path.join(d, 'data/clean_lyrics.csv'), sep='\t', encoding='utf-8')
