#regular packages
import pandas as pd
import string
import numpy as np
import os

#nlp packages
import nltk
import contractions
#nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *


def __general_preprocess__(text_col):
    # lowe cases
    text_col = text_col.apply(lambda x: ' '.join([w.lower() for w in x.split()]))
    # expand contractions
    text_col = text_col.apply(lambda x: ' '.join([contractions.fix(word) for word in x.split()]))
    # remove numbers
    text_col = text_col.apply(lambda x: ' '.join(re.sub("[^a-zA-Z]+", " ", x).split()))

    return text_col

def __remove_plurals__(text):
    special_words = {"gis"}
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    processed_words = [word if word in special_words else lemmatizer.lemmatize(word) for word in words]
    return ' '.join(processed_words)
    # = [word if word in special_words else lemmatizer.lemmatize(word) for word in words]

    # return ' '.join(processed_words)


def __remove_stopwords__(text_col, stopwords):
    # remove stopwords
    text_col = text_col.apply(lambda x: ' '.join([w for w in x.split() if w not in stopwords]))
    return text_col


def __remove_punctuation__(text_col):
    special_chars = {'-'}
    punctuation = ''.join(c for c in string.punctuation if c not in special_chars)
    # Define the set of punctuation characters
    # punctuation = set(string.punctuation)
    # Remove punctuation except for special characters
    text_col = text_col.apply(lambda x: ''.join([i for i in x if i not in punctuation]))

    return text_col


def __get_word_freq__(data_col):
    word_freq = data_col.str.split(expand=True).stack().value_counts()
    #print(type(word_freq))
    return word_freq

def __decade_pre_process__(data, stopword):
    #print(data.head())
    data['Abstract Note'] = data['Abstract Note'].astype(str)
    data['abstract'] = __general_preprocess__(data['Abstract Note'])
    data['abstract'] = __remove_punctuation__(data['abstract'])
    data['abstract'] = data['abstract'].apply(lambda x: __remove_plurals__(x))
    data['abstract'] = __remove_stopwords__(data['abstract'], stopword)
    data_freq = __get_word_freq__(data['abstract'])
    return data_freq#[:30]