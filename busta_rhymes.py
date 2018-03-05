#!/usr/bin/env python3

from tests.utils import load_data
import json

def lw(word):
    return word.rsplit(' ', 1)[1].strip('"\'.,;:-!?()').lower()

def busta_rhymes(path='data/shakespeare.txt'):
    data = load_data(path)
    rhymes = {}
    pairs = []
    rhyme_sets = []
    for sonnet in data:
        pairs.extend([(lw(sonnet[i]), lw(sonnet[i+2]))for i in range(0, 9, 4)])
        pairs.append((lw(sonnet[-2]), lw(sonnet[-1])))
    while pairs != []:
        rhyme_set = set(pairs.pop())
        for i, pair in enumerate(pairs):
            if not rhyme_set.isdisjoint(set(pair)):
                rhyme_set |= set(pair)
                pairs.pop(i)
        rhyme_sets.append(rhyme_set)
    for rhyme_set in rhyme_sets:
        for word in rhyme_set:
            s = rhyme_set.copy()
            s.discard(word)
            rhymes[word] = list(s)
    with open('data/rhyming_dictionary.json', 'w') as fh:
        fh.write(json.dumps(rhymes))


if __name__ == '__main__':
    busta_rhymes()
