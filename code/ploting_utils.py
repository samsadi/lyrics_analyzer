import plotly.tools as tls
tls.set_credentials_file(username=username, api_key=key)
credentials = tls.get_credentials_file()
import plotly.plotly as py
import pandas as pd
import numpy as np
from os import path
from plotly.graph_objs import *


def smoothing(x_vals, y_vals, frac=0.1):
    '''
    Use lowess smoothing to smoothen the values of input
    '''
    lowess = sm.nonparametric.lowess(y_vals, x_vals, frac = frac)
    y_smooth_vals = lowess[:, 1]
    x_smooth_vals = lowess[:, 0]
    return x_smooth_vals, y_smooth_vals


def topic_trend_plot(d, i):
	'''
    INPUT DataFrame, string
    OUTPUT plotly graph
    '''

    top_songs = top_songs.pd.read_csv(path.join(d, 'data/top_songs_per_topic.tsv'), sep='\t')

    topic = top_songs[top_songs['topic']==i]

    test = top_topic.join(df)
    topic_final = test[['artist', 'song', 'perc_top', 'topic', 'year', 'decade']]
    sorted_topic = topic_final.sort_values(['year'], ascending=[True])
    topic_grouped_year = sorted_topic.groupby('year').mean()

    x_i, y_i = smoothing(topic_grouped_year.index, topic_grouped_year['perc_top'])

    tracei = go.Scatter(
        x = x_i,
        y = y_i,
        fill='tonexty',
        mode='lines',
        name = 'Topic' + ' ' + i
    )
    return x_i, y_i, tracei


if __name__ == '__main__':

    d = path.dirname('/Users/Samaneh/Desktop/LyricsTrendAnalysis/')
    list = [0, 1, 2, 4, 5]

    xlist = []
    ylist = []
    tracelist = []

    for i in list:
        x_i , y_i, tracei = topic_trend_plot(d, i)
        xlist.append(x_i)
        ylist.append(y_i)
        tracelist.append(tracei)


    y_6 = ylist[6] #base

    y_5 += y_6
    trace5 = tracelist[5]
    trace5['y'] = y_5

    y_2 += y_5
    trace2 = tracelist[2]
    trace2['y'] = y_2

    y_1 += y_2
    trace1 = tracelist[1]
    trace1['y'] = y_1

    y_0 += y_1
    trace0 = tracelist[0]
    trace0['y'] = y_0

    data = [trace6,trace5,trace2,trace1,trace0]

    layout = go.Layout(
            title='Topic trends in song lyrics 1960-2010',
            titlefont=Font(
                family='Arial, sans-serif',
                size=24),
            xaxis = dict(title='Time'),
            yaxis = dict(title='Topic occurence index')
        )

    fig = Figure(data=data, layout=layout)
    py.iplot(fig, validate=False, filename = 'Topic Trends')
