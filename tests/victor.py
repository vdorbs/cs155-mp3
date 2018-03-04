from .test_sweet import TestSweet
from .test import Test
from .preprocess import split_by_words, split_by_syllables, flatten_sonnets
from .utils import get_sequence_lengths, sample

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

ts = TestSweet()

# model = MultinomialHMM(n_components=5, n_iter=10, verbose=True)
# fit = lambda data: _fit(model, data)
# run = lambda token_to_elem: _run_syllables(model, token_to_elem)
# pipeline = [split_by_words, split_by_syllables, flatten_sonnets]
# idx = ts.add_pipeline(pipeline)
# ts.add_test(Test(model, fit, run), idx)

model = MultinomialHMM(n_components=5, n_iter=10, verbose=True)
fit = lambda data: _fit(model, data)
run = lambda token_to_elem: _run_words(model, token_to_elem)
pipeline = [split_by_words, flatten_sonnets]
idx = ts.add_pipeline(pipeline)
ts.add_test(Test(model, fit, run), idx)
