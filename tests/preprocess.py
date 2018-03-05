"""
Contains prepreprocessing functions for Shakespeare sonnets.

Can be used as building blocks in preprocessing pipelines.
"""
import pyphen

from .utils import *

def strip_punctuation(data):
    """
    Input:
    data:       A list of lists of strings

    Output:
    data:       A list of lists of strings with punctuation stripped
    """
    return [[line.strip('.,;:-!?()') for line in sonnet] for sonnet in data]

def join_sonnets(data):
    """
    Input:
    data:       A list of lists of strings

    Output:
    data:       A list of strings
    """
    return ["".join(sonnet) for sonnet in data]
    
def group_characters(data):
    """
    Input:
    data:       A list of strings

    Output:
    data:       A list of of lists of lists of characters of length 41 (with the output in the last index)
    """
    return [[[chr for chr in sonnet[i:i+41]] for i in range(len(sonnet) - 40)] for sonnet in data]

def split_by_words(data):
    """
    Input:
    data:       A list of lists of strings

    Output:
    data:       A list of lists of lists of words
    """
    return [[[word for word in line.split(' ')] for line in sonnet] for sonnet in data]

def split_by_syllables(data):
    """
    Input:
    data:       A list of lists of lists of words

    Output:
    data:       A list of list of lists of syllables
    """
    syl = pyphen.Pyphen(lang='en')
    return [[split_line_by_syllable(line, syl.inserted) for line in sonnet] for sonnet in data]

def flatten_sonnets(data):
    return list(itertools.chain(*data))


