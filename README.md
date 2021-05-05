# Homophony Delta

This repository contains code and data for a forthcoming paper:

> Trott, S., Bergen, B. (2021). Languages are efficient, but for whom?

Specifically, for a given lexicon (contained in `data/raw`), the code can be used to:

- Identify the number of homophones for each unique wordform.  
- Compute the **phonotactic probability** of each wordform using a phonotactic model (see `src/preprocessor.py` and `src.generative_model.py`).  
- Calculate the **homophony delta**, i.e., the difference between a wordform's *actual* number of homophones and how many it should have on account of its phonotactics (see `analyses/delta.Rmd`).  


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


