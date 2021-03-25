"""Code to preprocess lexica and calculate surprisal."""


import argparse
import os
import pandas as pd

import src.config as config
from src.utils import get_config_dict
from src.preprocessor import Preprocessor


### 5-phone: English, Dutch, German
### 4-phone: Japanese, French, Mandarin


def preprocess_lexicon(language):
    """Preprocess lexicon."""
    config_dict = get_config_dict(config, language)
    preprocessor = Preprocessor(**config_dict)
    info_for_generation = preprocessor.preprocess_lexicon()
    return info_for_generation


def heldout_surprisal():
    """Calculate heldout surprisal"""
    for language, n in config.LANGUAGES_N:
        print("Calculating held-out surprisal for: {language}".format(language=language))

        ## Get config dict
        config_dict = get_config_dict(config, language)
        PHON_COLUMN = config_dict['phon_column']

        ## Load real lexicon
        LOAD_PATH = "data/processed/{lan1}/reals/{lan2}_with_mps_{n}phone.csv".format(lan1=language, lan2=language, n=n)
        SAVE_PATH = "data/processed/{lan1}/reals/{lan2}_with_mps_{n}phone_holdout.csv".format(lan1=language, lan2=language, n=n)
        df_lexicon = pd.read_csv(LOAD_PATH)
        print(len(df_lexicon))

        # Get heldout surprisal
        print("Calculating heldout surprisal...")
        NUM_FOLDS = 1000
        print("Number of folds: {x}".format(x = NUM_FOLDS))
        df_real_heldout = Preprocessor.calculate_heldout_surprisal(df_lexicon[PHON_COLUMN].values, n=n, 
            num_folds=NUM_FOLDS)
        df_real_heldout[PHON_COLUMN] = df_real_heldout['word']
        df_real_heldout = df_real_heldout[[PHON_COLUMN, 'heldout_log_prob', 'heldout_surprisal']]
        print(len(df_real_heldout))
        
        # Merge with real processed lexicon
        df_merged = pd.merge(df_lexicon, df_real_heldout, on=PHON_COLUMN)
        print(len(df_merged))

        print("Saving to: {path}".format(path=SAVE_PATH))
        df_merged.to_csv(SAVE_PATH)




def preprocess_pipeline():
    """Read in raw lexicon and create preprocessed version."""
    for language, n in config.LANGUAGES_N:
        print("Preprocessing lexica for: {language}".format(language=language))
        if not os.path.exists("data/processed/{lan}".format(lan=language)):
            print("Creating directory: data/processed/{lan}".format(lan=language))
            os.mkdir("data/processed/{lan}".format(lan=language))
        if not os.path.exists("data/processed/{lan}/reals".format(lan=language)):
            print("Creating directory: data/processed/{lan}/reals".format(lan=language))
            os.mkdir("data/processed/{lan}/reals".format(lan=language))
        config_dict = get_config_dict(config, language)
        ## Reset n according to language
        config_dict['n'] = n
        preprocessor = Preprocessor(**config_dict)
        info_for_generation = preprocessor.preprocess_lexicon()
        print("Now getting minimal pairs")
        preprocessor.get_minimal_pairs()



def main(mode):
    """Run specified mode."""
    mode_to_func = {
        'preprocess': preprocess_pipeline,
        'surprisal': heldout_surprisal
    }
    print(mode)
    func = mode_to_func[mode]
    func()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run analysis.')
    parser.add_argument('--mode', default='extract_reals', type=str,
                        help='Extract real parameters for each language')

    args = vars(parser.parse_args())

    main(**args)