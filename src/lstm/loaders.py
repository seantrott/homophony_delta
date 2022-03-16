"""Utility functions for data loading."""

from torch.utils.data import DataLoader

from lstm.util import constants
from lstm.h02_learn.dataset.types import TypeDataset



def generate_batch(batch):
    r"""
    Since the text entries have different lengths, a custom function
    generate_batch() is used to generate data batches and offsets,
    which are compatible with EmbeddingBag. The function is passed
    to 'collate_fn' in torch.utils.data.DataLoader. The input to
    'collate_fn' is a list of tensors with the size of batch_size,
    and the 'collate_fn' function packs them into a mini-batch.[len(entry[0][0]) for entry in batch]
    Pay attention here and make sure that 'collate_fn' is declared
    as a top level def. This ensures that the function is available
    in each worker.
    """
    tensor = batch[0][0]
    batch_size = len(batch)
    max_length = max([len(entry[0]) for entry in batch]) - 1  # Does not need to predict SOS

    x = tensor.new_zeros(batch_size, max_length)
    y = tensor.new_zeros(batch_size, max_length)

    for i, item in enumerate(batch):
        sentence = item[0]
        sent_len = len(sentence) - 1  # Does not need to predict SOS
        x[i, :sent_len] = sentence[:-1]
        y[i, :sent_len] = sentence[1:]

    x, y = x.to(device=constants.device), y.to(device=constants.device)
    return x, y


def get_data_loader(data, folds, batch_size, shuffle):
    fname = TypeDataset(data, folds)
    loader = DataLoader(fname, batch_size=batch_size, shuffle=shuffle,
                             collate_fn=generate_batch)
    return loader


def get_data_loaders(lexicon, word_info, batch_size, num_splits):
    ## First split up lexicon
    splits = lexicon.get_fold_splits(word_info, num_splits)
    ## Create data object with splits and alphabet
    data = [splits, lexicon.alphabet]
    ## Create folds
    folds = [list(range(num_splits - 1)), [num_splits - 1]]
    print(folds)
    ## Then use first (n-1) folds for trainloader
    trainloader = get_data_loader(
        data, folds[0], batch_size=batch_size, shuffle=True)
    ## Then use nth fold for devloader
    devloader = get_data_loader(
        data, folds[1], batch_size=batch_size, shuffle=False)


    return trainloader, devloader
