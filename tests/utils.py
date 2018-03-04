import itertools

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

