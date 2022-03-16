"""Simple class for representing lexicon dataset."""

import numpy as np
import pandas as pd

from lstm.data.alphabet import Alphabet


class Lexicon(object):

    def __init__(self, df, alphabet, PHON, WORD):
        self.PHON = PHON
        self.WORD = WORD
        self.df = df
        self.alphabet = alphabet
        self.max_words = None

        self.word_info = {}

    @staticmethod
    def get_fold_splits(data, n_folds):
        keys = sorted(list(data.keys()))
        np.random.shuffle(keys)
        splits = np.array_split(keys, n_folds)
        splits = [{key: data[key] for key in fold} for fold in splits]
        return splits

    def process_data(self):
        
        for _, row in self.df.iterrows():
            self.process_row(row)

        return self.word_info

    def process_row(self, row):
        wordform = row[self.PHON]
        self.alphabet.add_word(wordform)

        self.word_info[wordform] = {
                'idx': self.alphabet.word2idx(wordform),
                'word': row[self.WORD],
                'wordform': wordform
            }

    @staticmethod
    def get_word(row):
        return row.phones, list(row.phones)