from .test_sweet import TestSweet
from .test import Test
from .preprocess import split_by_words, split_by_syllables, flatten_sonnets
from .utils import get_sequence_lengths

from numpy import concatenate, reshape
from hmmlearn.hmm import MultinomialHMM

def _fit(model, data):
    model.fit(reshape(concatenate(data), (-1, 1)), get_sequence_lengths(data))

def _run(model, token_to_elem):
    sequence, _ = model.sample(140)
    sequence = reshape(sequence, (14, 10))
    sequence = '\n'.join([''.join([token_to_elem[elem] for elem in line]) for line in sequence])
    return sequence

ts = TestSweet()
idx = ts.add_pipeline([split_by_words, split_by_syllables, flatten_sonnets])
model = MultinomialHMM(n_components=5, n_iter=10, verbose=True)
fit = lambda data: _fit(model, data)
run = lambda token_to_elem: _run(model, token_to_elem)
test = Test(model, fit, run)
ts.add_test(test, idx)
