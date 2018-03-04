import itertools
from numpy import cumsum, floor
from numpy.random import rand

def append_space(syllable_list):
    """
    Input:
    syllable_list:      A list of syllables that make up a single word

    Output:
    syllable_list:      A list of syllables, with a space appended to the
                        last element
    """
    syllable_list[-1] += ' '
    return syllable_list

def split_line_by_syllable(line, pyphen):
    """
    Input:
    line:       A list of words
    pyphen:     A hyphenating function

    Outputs:
    line:       A list of syllables with a space appended at the end of each word
    """
    return list(itertools.chain(*[append_space(pyphen(word).split('-')) for word in line]))

def create_token_dictionary(data):
    unique_elems = set()
    for line in data:
        for elem in line:
            unique_elems.add(elem)
    return {elem:token for token, elem in enumerate(unique_elems)}

def apply_token_dictionary(token_dictionary, data):
    return [[token_dictionary[elem] for elem in line] for line in data]

def get_sequence_lengths(data):
    return [len(line) for line in data]

def sample(p):
    return floor(cumsum(p) - rand()).tolist().index(0)

def load_data(path):
    """
    Input:
    path:       Path to dataset in filesystem

    Output:
    sonnets:    A list of list of strings, where each string is a line in a sonnet
    """
    sonnets = []
    sonnet = None
    with open(path, 'r') as fid:
        lines = fid.readlines()
        for line in lines:
            line = line.strip()
            if line.isdigit():
                sonnet = []
            else:
                if line == '':
                    if sonnet is not None:
                        # Ignoring sonnets without 14 lines
                        if len(sonnet) is 14:
                            sonnets.append(sonnet)
                            sonnet = None
                else:
                    sonnet.append(line)
    if len(sonnet) is 14:
        sonnets.append(sonnet)
    return sonnets
