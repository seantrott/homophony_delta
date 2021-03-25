"""Code to identify number of minimal pairs for each word in a lexicon."""

import os
import os.path as op
import pandas as pd 
import itertools
import math

import editdistance as ed

from collections import defaultdict
from tqdm import tqdm

import src.config as config
import src.utils as utils

import re


def generate_mp_regex(wordform):
    regex = "^("
    forms = []
    # mutations
    for index in range(len(wordform)):
        forms.append(wordform[:index] + '.' + wordform[index+1:])

    # insertions
    for index in range(len(wordform) + 1):
        forms.append(wordform[:index] + '.' + wordform[index:])

    # deletions
    for index in range(len(wordform)):
        forms.append(wordform[:index] + wordform[index+1:])
    regex += "|".join(forms)

    regex = regex.replace("$", "\$")
    regex += ")$"
    return regex

def find_minimal_pairs_lazy(wordforms):
    word_to_size = defaultdict(int)
    # unique_combos = math.factorial(len(wordforms)) / (math.factorial(2) * (math.factorial(len(wordforms)-2)))
    seen = set()
    for w1 in tqdm(wordforms):
        seen.add(w1)
        regex = re.compile(generate_mp_regex(w1))
        matches = [w for w in wordforms if w not in seen and regex.match(w)]
        for w2 in matches:
            word_to_size[w1] += 1
            word_to_size[w2] += 1
    return word_to_size





