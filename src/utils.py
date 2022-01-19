"""Utility functions for preprocessing and analysis"""

import pandas as pd
import numpy as np 
import scipy.stats as ss

import statsmodels.formula.api as sm

import matplotlib.pyplot as plt

from tqdm import tqdm


### Utility function
def get_config_dict(config, language):

    n = dict(config.LANGUAGES_N)[language]
    return {'language': language,
            'phon_column': config.PHON_COLUMN[language],
            'word_column': config.WORD_COLUMN[language],
            'vowels': config.VOWEL_SETS[language],
            'match_on': config.MODEL_INFO['match_on'],
            'phonetic_remappings': config.PHONETIC_REMAPPINGS[language],
            'n': n, # Updated this
            'smoothing': config.MODEL_INFO['smoothing']}




### Utility function
def load_subtlex_for_proper_nouns(path = "data/frequency/mandarin/subtlex_mandarin.csv"):
    """Load SUBTLEX and identify orthographic representations which orthographic
    representations have proper nouns as a POS."""
    POS_TO_REMOVE = ['nr', 'ns', 'nt', 'nz']
    df_subtlex = pd.read_csv(path).dropna(subset=['WordForm', 'PoS'])
    print("{X} SUBTLEX entries".format(X = len(df_subtlex)))

    df_proper_nouns = df_subtlex[df_subtlex['PoS'].isin(POS_TO_REMOVE)]['WordForm'].values

    return df_proper_nouns

### Utility function
def count_syllables(word, language, vowels="IE{VQU@i#$u312456789cq0~"):
    """Counts number of vowels in word for rough estimate of number of syllables.

    For Japanese, increases count by 1 for every geminate. Placeless nasal codas ('N') included in 
    list of 'vowels' for ease."""
    counts = 0
    prev = ''
    for i in word:
        if i in vowels:
            counts += 1
        # Count geminates ('tt', 'kk') for additional mora.
        elif i == prev and language in ['japanese']:
            counts += 1
        prev = i
    return counts



