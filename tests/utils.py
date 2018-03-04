import itertools

def append_space(syllable_list):
    syllable_list[-1] += ' '
    return syllable_list

def split_line_by_syllable(line, pyphen):
    return list(itertools.chain(*[append_space(pyphen(word).split('-')) for word in line]))

