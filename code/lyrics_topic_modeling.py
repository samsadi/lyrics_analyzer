import pandas as pd
import numpy as np
import re
from os import path
from stop_words import get_stop_words
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
from numpy.random import rand, RandomState
from numpy import array, matrix, linalg
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt


def get_top_values(lst, n, labels):
    '''
    OUTPUT list of top n labels
    '''
    return [labels[i] for i in np.argsort(lst)[-1:-n-1:-1]]


def get_song_info(song_index):
    '''
    OUTPUT lists of song information
    '''
    song_vocab = []
    total_song_words = []
    lyrics = clean_lyrics[song_index]
    total_song_words.append(lyrics.split())
    total_num_words = len(total_song_words)
    new_words = [word for word in total_song_words if word not in song_vocab]
    song_vocab.append(new_words)
    return total_song_words, song_vocab


# Tfidf Vectorizer for lyrics:
def tfidf(clean_lyrics, stop_word_list):
    '''
    Learn vocabulary and idf, return document-term matrix
    '''
    vectorizer = TfidfVectorizer(analyzer = 'word', stop_words = stop_word_list)
    document_term_mat = vectorizer.fit_transform(clean_lyrics)
    words = vectorizer.get_feature_names()
    vocab_size = len(words)
    return document_term_mat, words


def build_model(document_term_mat, n_topics):
    '''
    Use Non-negative Matrix Factorization to featurize the document-term matrix
    '''
    nmf = NMF(n_components = n_topics)
    W = nmf.fit_transform(document_term_mat)
    H = nmf.components_
    return W, H


def describe_nmf_results_H(H, n_top_words = 20):
    '''
    Output the top words in each topic
    '''
    for topic_num, topic in enumerate(H):
        print("Topic %d:" % topic_num)
        print(" ".join([words[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    return


def describe_nmf_results_W(W, n_top_topics = 10):
    '''
    Output the top topics in each document
    '''
    for doc_num, topic_row in enumerate(W[:10]): # print out the first 10 documents
        print("Document %d:" % doc_num)
        print topic_row.argsort()[::-1][:n_top_topics]
    return


def main_topic_per_doc(W):
    '''
    Output a list that holds the top topic in each document
    '''
    main_topic = []
    for doc_num, topic_row in enumerate(W):
        main_topic.append(topic_row.argsort()[::-1][0])
        #print("Song %d:" % doc_num, "Main Topic: %d" % topic_row.argsort()[::-1][0])
    return main_topic


def save_results(W, H, vocab_size, song_vocab, main_topic, song_id, document_term_mat, clean_lyrics):
    '''
    Save the output of the Tfidf and NMF results
    '''
    np.save('doc_topic', W)
    np.save('total_words', np.array(vocab_size))
    np.save('song_vocab', np.array(song_vocab))
    np.save('main_topic', main_topic)
    np.save('song_id', song_id)
    np.save('topic_word', H)
    np.save('document_term_mat', document_term_mat)
    np.save('clean_lyrics', clean_lyrics)

    song_list = df[['recording_id', 'year', 'genre_cluster', 'artist_name', 'track_name',                'lyrics_artist', 'lyrics_track', 'lyrics']]
    doc_topic = W
    doc_topic_df = pd.DataFrame(doc_topic)
    main_topic_df = pd.DataFrame(main_topic)
    main_topic_df.columns=['main_topic']

    song_list_topics = song_list.join(doc_topic_df)
    song_list_topics_mt = song_list_topics.join(main_topic_df)

    # Top songs per topic
    top_songs = pd.DataFrame()
    for i in range(0, n_topics):
        temp = song_list_topics[['artist_name','track_name', i]].sort([i], ascending=[0])
        temp.columns = ['artist', 'song', 'perc_top']
        temp['topic'] = i
        top_songs = pd.concat([top_songs, temp])
    top_songs.to_csv(path.join(d, 'data/top_songs_per_topic.tsv'), sep='\t')



if __name__ == '__main__':

    clean_lyrics = pd.read_csv(path.join(d, 'data/clean_lyrics.csv'), sep='\t', encoding='utf-8')
    stop_word_list = get_stop_words_list()

    document_term_mat, words = tfidf(clean_lyrics, stop_word_list)
    W, H = build_model(document_term_mat)

    describe_nmf_results_H(H)
    print("------------------------------")
    describe_nmf_results_W(W)

    # Total tf-idf score:
    total = np.sum(document_term_mat.toarray(), axis=0)
    print "top 20 by total tf-idf"
    print get_top_values(total, 20, words)

    main_topic = main_topic_per_doc(W)
    save_results(W, H, vocab_size, song_vocab, main_topic, song_id, document_term_mat, clean_lyrics)
