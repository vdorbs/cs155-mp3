"""
Contains prepreprocessing functions for Shakespeare sonnets.

Can be used as building blocks in preprocessing pipelines.
"""
import pyphen

from .utils import *

def split_by_words(data):
    return [[[word for word in line.split(' ')] for line in sonnet] for sonnet in data]

def split_by_syllables(data):
    syl = pyphen.Pyphen(lang='en')
    return [[split_line_by_syllable(line, syl.inserted) for line in sonnet] for sonnet in data]

