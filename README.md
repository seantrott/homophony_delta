# Homophony Delta

This repository contains code and data for a forthcoming paper:

> Trott, S., Bergen, B. (2021). Languages are efficient, but for whom?

Specifically, for a given lexicon (contained in `data/raw`), the code can be used to:

- Identify the number of homophones for each unique wordform.  
- Compute the **phonotactic probability** of each wordform using a phonotactic model (see `src/preprocessor.py` and `src.generative_model.py`).  
- Calculate the **homophony delta**, i.e., the difference between a wordform's *actual* number of homophones and how many it should have on account of its phonotactics (see `analyses/delta.Rmd`).  

Please contact me (sttrott at ucsd dot edu) if you have any trouble accessing the data or using the code.

## Using the code

Data preprocessing and calculation of phonotactic probability can be done using the `main.py` file.

To preprocess each raw lexicon:

```
python main.py --mode=preprocess
```

Once these lexica have been preprocessed, you can calculate phonotactic surprisal using 1000-fold cross-validation:

```
python main.py --mode=surprisal
```

## Running the analysis

The analyses can all be run by knitting the [`delta.Rmd`](https://github.com/seantrott/homophony_delta/blob/main/analyses/delta.Rmd) file in `analyses`. (An already-knit `.html` file is also included.)

## Data

All the relevant datasets should be included in the `data` directory.

### Raw data

In `data/raw`, you will find directories for each language of interest, along with the raw lexicon file in `.csv` format.

These raw files must be preprocessed before performing any analyses with them.

### Processed data

Similarly, `data/processed` is separated by directories for each language. Within each directory (e.g., [`data/processed/english`](https://github.com/seantrott/homophony_delta/tree/main/data/processed/english)), you will find the following files (examples below given for english):

- `reals/english_with_mps_5phone_holdout.csv`: the processed dataset with n-phone phonotactic probabilities (in this case, with a 5-phone model), along with minimal pairs / neighborhood sizes calculated.  In this case, phonotactic probabilities are calculated using cross-validation.  
- `reals/english_with_mps_5phone.csv`: the processed dataset with n-phone phonotactic probabilities (in this case, with a 5-phone model), along with minimal pairs / neighborhood sizes calculated.  In this case, phonotactic probabilities are calculated not using cross-validation.  
- `reals/english_lemmas_processed_5phone.csv`: the full dataset including all unique lemmas (not just wordforms) and phonotactic probabilities of the corresponding wordform.  
- `english_with_lstm.csv`: the processed dataset along with phonotactic probabilities calculated using an LSTM.  

Of these, the key file for the primary analysis is the **holdout** file.

### Frequency data

The critical analyses for English/German/Dutch also depends on a file containing **frequency data** for each wordform in that language.

These files can be found in `data/frequency`, under the corresponding language directory.

## Supplementary analyses

Note that the `analyses` folder also contains two other `.Rmd` files for several supplementary analyses:

- `delta_lstm.Rmd`: a replication of the primary analysis, using an LSTM to calculate phonotactic probability instead of an n-phone model.  
- `information_bottleneck.Rmd`: an alternative analysis of the key question, using information-theoretic measures of lexicon complexity.  

### Supplementary analysis with LSTM

Additionally, one of our supplementary analyses involved adapting [this codebase](https://github.com/rycolab/homophony-as-renyi-entropy) (from Pimentel et al., 2021](https://arxiv.org/abs/2109.13766)) for our datasets, to calculate phonotactic probability using an LSTM instead of an n-phone model.

If you're like to run the LSTM code, you can run:

```
python src/process_dataset_for_lstm.py
```

By default, this will run the code for English; you can change the language by adjusting the `language` parameter in the `process_dataset_for_lstm.py` file.


