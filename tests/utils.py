import itertools
def split_line_by_syllable(line, pyphen):
    return itertools.chain(*[pyphen(word + ' ').split('-') for word in line])
