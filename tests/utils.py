import json
import itertools
from numpy import cumsum, where, zeros
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
    P = cumsum(p)
    r = rand() * max(P)
    return len(where(P < r)[0])

def load_rhymes(path='data/rhyming_dictionary.json'):
    with open(path, 'r') as fh:
        return json.loads(fh.read())

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

def condition_rhymable(rhyming_dictionary, elem_to_token, p):
    p_cond = zeros(p.shape)
    for rhymable in rhyming_dictionary.keys():
        token = elem_to_token[rhymable]
        p_cond[token] = p[token]
    return p_cond / sum(p_cond)

def condition_rhyme(rhyming_dictionary, elem_to_token, word, p):
    p_cond = zeros(p.shape)
    for rhyming in rhyming_dictionary[word]:
        token = elem_to_token[rhyming]
        p_cond[token] = p[token]
    return p_cond / sum(p_cond)

def enforce_rhyming(leaders, followers_to_leaders, rhyming_struct, rhyming_dictionary, token_to_elem, elem_to_token, p_emit, line_no):
    if line_no not in leaders:
        leader = followers_to_leaders[line_no]
        p = condition_rhyme(rhyming_dictionary, elem_to_token, rhyming_struct[leader], p_emit)
    else:
        p = condition_rhymable(rhyming_dictionary, elem_to_token, p_emit)
    emission = sample(p)
    word = token_to_elem[emission]
    if line_no in leaders:
        rhyming_struct[line_no] = word
    return rhyming_struct, word

def enforce_sonnet(rhyming_struct, rhyming_dictionary, token_to_elem, elem_to_token, p_emit, line_no):
    leaders = [2, 3, 6, 7, 10, 11, 13]
    followers = [0, 1, 4, 5, 8, 9, 12]
    followers_to_leaders = {follower:leader for follower, leader in zip(followers, leaders)}
    rhyming_struct, word = enforce_rhyming(leaders, followers_to_leaders, rhyming_struct, rhyming_dictionary, token_to_elem, elem_to_token, p_emit, line_no)
    return rhyming_struct, word

def enforce_limerick(rhyming_struct, rhyming_dictionary, token_to_elem, elem_to_token, p_emit, line_no):
    leaders = [3, 4]
    followers_to_leaders = { 0:4, 1:4, 2:3 }
    rhyming_struct, word = enforce_rhyming(leaders, followers_to_leaders, rhyming_struct, rhyming_dictionary, token_to_elem, elem_to_token, p_emit, line_no)
    return rhyming_struct, word
