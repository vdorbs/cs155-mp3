import itertools

def append_space(syllable_list):
    syllable_list[-1] += ' '
    return syllable_list

def split_line_by_syllable(line, pyphen):
    return list(itertools.chain(*[append_space(pyphen(word).split('-')) for word in line]))

def create_token_dictionary(data):
    unique_elems = set()
    for sonnet in data:
        for line in sonnet:
            for elem in line:
                unique_elems.add(elem)
    return {elem:token for token, elem in enumerate(unique_elems)}

def get_sequence_lengths(data):
    return [len(line) for line in data]
