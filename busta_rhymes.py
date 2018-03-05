#!/usr/bin/env python3

from tests.utils import load_data

def lw(word):
    return word.rsplit(' ', 1)[1].strip('.,;:-!?()')

def busta_rhymes(path='data/shakespeare.txt'):
    data = load_data(path)
    rhymes = {}
    pairs = []
    for sonnet in data:
        pairs.extend([(lw(sonnet[i]), lw(sonnet[i+2]))for i in range(0, 9, 4)])
        pairs.append((lw(sonnet[-2]), lw(sonnet[-1])))
    pairs.extend([(s, f) for f, s in pairs])

if __name__ == '__main__':
    busta_rhymes()
