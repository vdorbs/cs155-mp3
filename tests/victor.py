from .test_sweet import TestSweet
from .test import Test
from .preprocess import split_by_words, split_by_syllables, tokenize, flatten_sonnets
from .utils import get_sequence_lengths

from numpy import concatenate, reshape
from hmmlearn.hmm import MultinomialHMM

def _fit(model, data):
    model.fit(reshape(concatenate(data), (-1, 1)), get_sequence_lengths(data))

ts = TestSweet()
idx = ts.add_pipeline([split_by_words, split_by_syllables, tokenize, flatten_sonnets])
model = MultinomialHMM(n_components=10, n_iter=100, verbose=True)
fit = lambda data: _fit(model, data)
test = Test(model, fit)
ts.add_test(test, idx)
