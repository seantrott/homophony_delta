"""Code to process data for LSTM, fit LSTM, and calculate surprisal for each wordform.

Note that to run this code, you must already have run the preprocessor––this code works with the already-processed lexica.
"""

import config
from utils import get_config_dict
from lstm.data.alphabet import Alphabet
from lstm.data.lexicon import Lexicon

from lstm.h02_learn.train_info import TrainInfo
from lstm.h02_learn.model import LstmLM
from lstm.util import constants
from lstm.loaders import generate_batch, get_data_loaders
from lstm.eval_model import eval_per_word

import random
import pandas as pd
import torch

from tqdm import tqdm


############################ Code for creating Lexicon object ####################
def create_lexicon(language='english'):
    """Create Alphabet, lexicon, and dictionary of wordform entries."""    

    ## First, read in processed lexicon dataframe.
    config_dict = get_config_dict(config, language=language)
    n = config_dict['n'] ## Just for accessing the saved file
    PROCESSED_PATH = "data/processed/{lan1}/reals/{lan2}_with_mps_{n}phone_holdout.csv".format(lan1=language, lan2=language, n=n)
    print(PROCESSED_PATH)
    df_processed = pd.read_csv(PROCESSED_PATH)

    ## Then construct alphabet.
    alphabet = Alphabet()
    PHON = config_dict['phon_column']
    WORD = config_dict['word_column']

    # Then create lexicon and dictionary.
    print("Creating lexicon object...")
    lexicon = Lexicon(df_processed, alphabet, PHON=PHON, WORD=WORD)
    word_info = lexicon.process_data()

    return alphabet, lexicon, word_info, df_processed

### Main
random.seed(42)

#### Parameters
batch_size = 32
language = 'english' ### Change this parameter to determine which language to run it for
num_splits = 10

## Config dict
config_dict = get_config_dict(config, language=language)
PHON = config_dict['phon_column']
WORD = config_dict['word_column']

## Create objects
alphabet, lexicon, word_info, df_processed = create_lexicon(language=language)

trainloader, devloader = get_data_loaders(
    lexicon, word_info, batch_size, num_splits)

############################ Code for creating dataloader




########################### Code for training model
embedding_size = 64
hidden_size = 256
nlayers = 2
dropout = .33

print("Creating model object...")
model = LstmLM(
	        lexicon.alphabet, embedding_size, hidden_size,
	        nlayers=nlayers, dropout=dropout) \
	        .to(device=constants.device)

## Create train info
eval_batches = 20
wait_epochs = 5
wait_iterations = eval_batches * wait_epochs
train_info = TrainInfo(wait_iterations, eval_batches)


## Fit model
print("Fitting model")
model.fit(trainloader, devloader, train_info)
## TODO: Save model?
## model.save(model_path)

## TODO: Print out final loss for model?

## Once model is done, get surprisal of wordforms (both in train/dev sets)
print("Evaluating wordforms")
df_train = eval_per_word(trainloader, model, alphabet)
## TODO: Use different model to get dev?
df_dev = eval_per_word(devloader, model, alphabet)

## Merge together
df_all = pd.concat([df_train, df_dev])
df_all[PHON] = df_all['words']

### Then merge with original dataframe
df_merged = pd.merge(df_processed, df_all, on = PHON)
# df_merged['surprisal_lstm'] = df_merged['losses']
df_merged['logprob_lstm'] = df_merged['surprisal_lstm'].apply(lambda x: -x)

## SAVE_PATH
SAVE_PATH = "data/processed/{lan1}/reals/{lan2}_with_lstm.csv".format(lan1=language, lan2=language)
df_merged.to_csv(SAVE_PATH)


