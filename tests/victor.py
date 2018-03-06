from .test_sweet import TestSweet
from .test import Test
from .preprocess import strip_punctuation, split_by_words, split_by_syllables, flatten_sonnets, reverse_sonnets, reverse_lines
from .utils import get_sequence_lengths, sample, enforce_sonnet

from numpy import concatenate, reshape
from hmmlearn.hmm import MultinomialHMM
import pyphen

def _fit(model, data):
    model.fit(reshape(concatenate(data), (-1, 1)), get_sequence_lengths(data))

def _run_syllables(model, token_to_elem):
    sequence, _ = model.sample(140)
    sequence = reshape(sequence, (14, 10))
    sequence = '\n'.join([''.join([token_to_elem[elem] for elem in line]) for line in sequence])
    return sequence

def _run_words(model, token_to_elem):
    syl = pyphen.Pyphen(lang='en')
    sonnet = ''
    state = None
    for _ in range(14):
        count = 0
        while count is not 10:
            if state is None:
                next_state = sample(model.startprob_)
            else:
                next_state = sample(model.transmat_[state])
            emission = sample(model.emissionprob_[next_state])
            word = token_to_elem[emission]
            syl_count = len(syl.inserted(word).split('-'))
            if count + syl_count > 10:
                continue
            else:
                count += syl_count
                state = next_state
                sonnet += (word + ' ')
        sonnet += '\n'
    return sonnet

def _run_rhymes(model, token_to_elem, rhyming_dictionary):
    elem_to_token = {v:k for k, v in token_to_elem.items()}
    syl = pyphen.Pyphen(lang='en')
    sonnet = ''
    state = None
    rhyming_struct = {}
    for line_no in range(13, -1, -1):
        count = 0
        while count is not 10:
            if state is None:
                p_state = model.startprob_
            else:
                p_state = model.transmat_[state]
            next_state = sample(p_state)
            p_emit = model.emissionprob_[next_state]
            if count is 0:
                rhyming_struct, word = enforce_sonnet(rhyming_struct, rhyming_dictionary, token_to_elem, elem_to_token, p_emit, line_no)
            else:
                emission = sample(p_emit)
                word = token_to_elem[emission]
            syl_count = len(syl.inserted(word).split('-'))
            if count + syl_count > 10:
                continue
            else:
                count += syl_count
                state = next_state
                sonnet = (word + ' ') + sonnet
        sonnet = '\n' + sonnet
    return sonnet

ts = TestSweet()

states = 25
n_iter = 100

model = MultinomialHMM(n_components=states, n_iter=n_iter, verbose=True)
fit = lambda data: _fit(model, data)
run = lambda token_to_elem, rhyming_dictionary: _run_syllables(model, token_to_elem)
pipeline = [strip_punctuation, split_by_words, split_by_syllables, flatten_sonnets]
idx = ts.add_pipeline(pipeline)
ts.add_test(Test(model, fit, run), idx)

model = MultinomialHMM(n_components=states, n_iter=n_iter, verbose=True)
fit = lambda data: _fit(model, data)
run = lambda token_to_elem, rhyming_dictionary: _run_words(model, token_to_elem)
pipeline = [strip_punctuation, split_by_words, flatten_sonnets]
idx = ts.add_pipeline(pipeline)
ts.add_test(Test(model, fit, run), idx)

model = MultinomialHMM(n_components=states, n_iter=n_iter, verbose=True)
fit = lambda data: _fit(model, data)
run = lambda token_to_elem, rhyming_dictionary: _run_rhymes(model, token_to_elem, rhyming_dictionary)
pipeline = [strip_punctuation, split_by_words, reverse_lines, reverse_sonnets, flatten_sonnets]
idx = ts.add_pipeline(pipeline)
ts.add_test(Test(model, fit, run), idx)
