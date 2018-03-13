from .test_sweet import TestSweet
from .test import Test
from .preprocess import strip_punctuation, split_by_words, split_by_syllables, flatten_sonnets, reverse_sonnets, reverse_lines
from .utils import get_sequence_lengths, sample, enforce_sonnet, enforce_limerick

from numpy import concatenate, reshape
from .HMM_helper import (
    text_to_wordcloud,
    states_to_wordclouds,
    parse_observations,
    sample_sentence,
    visualize_sparsities,
    animate_emission
)
from hmmlearn.hmm import MultinomialHMM
import pyphen

def _fit(model, data):
    model.fit(reshape(concatenate(data), (-1, 1)), get_sequence_lengths(data))
    visualize_sparsities(model, O_max_cols=50)

def _run_syllables(model, token_to_elem):
    sequence, _ = model.sample(140)
    sequence = reshape(sequence, (14, 10))
    sequence = '\n'.join([''.join([token_to_elem[elem] for elem in line]) for line in sequence])
    return sequence

def _run_words(model, token_to_elem):
    print("VISUALIZING SPARSITIES")
    #visualize_sparsities(model, O_max_cols=50)
    print("WORDCLOUDS")
    wordclouds = states_to_wordclouds(model, token_to_elem, max_words=50)
    
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

def _run_limerick(model, token_to_elem, rhyming_dictionary):
    elem_to_token = {v:k for k, v in token_to_elem.items()}
    syl = pyphen.Pyphen(lang='en')
    limerick = ''
    state = None
    rhyming_struct = {}
    syllables = [9, 9, 5, 5, 9]
    for line_no in range(len(syllables)-1, -1, -1):
        max_syl = syllables[line_no]
        count = 0
        while count != syllables[line_no]:
            if state is None:
                p_state = model.startprob_
            else:
                p_state = model.transmat_[state]
            next_state = sample(p_state)
            p_emit = model.emissionprob_[next_state]
            if count is 0:
                rhyming_struct, word = enforce_limerick(rhyming_struct, rhyming_dictionary, token_to_elem, elem_to_token, p_emit, line_no)
            else:
                emission = sample(p_emit)
                word = token_to_elem[emission]
            syl_count = len(syl.inserted(word).split('-'))
            if count + syl_count > max_syl:
                continue
            else:
                count += syl_count
                state = next_state
                limerick = (word + ' ') + limerick
        limerick = '\n' + limerick
    return limerick

ts = TestSweet()

states = 25
n_iter = 100


#model1 = MultinomialHMM(n_components=states, n_iter=n_iter, verbose=True)
#fit1 = lambda data: _fit(model1, data)
#run1 = lambda token_to_elem, rhyming_dictionary: _run_syllables(model1, token_to_elem)
#pipeline1 = [strip_punctuation, split_by_words, split_by_syllables, flatten_sonnets]
#idx1 = ts.add_pipeline(pipeline1)
#ts.add_test(Test(model1, fit1, run1), idx1)

model2 = MultinomialHMM(n_components=states, n_iter=n_iter, verbose=True)
fit2 = lambda data: _fit(model2, data)
run2 = lambda token_to_elem, rhyming_dictionary: _run_words(model2, token_to_elem)
pipeline2 = [strip_punctuation, split_by_words, flatten_sonnets]
idx2 = ts.add_pipeline(pipeline2)
ts.add_test(Test(model2, fit2, run2), idx2)

#model3 = MultinomialHMM(n_components=states, n_iter=n_iter, verbose=True)
#fit3 = lambda data: _fit(model3, data)
#run3 = lambda token_to_elem, rhyming_dictionary: _run_rhymes(model3, token_to_elem, rhyming_dictionary)
#pipeline3 = [strip_punctuation, split_by_words, reverse_lines, reverse_sonnets, flatten_sonnets]
#idx3 = ts.add_pipeline(pipeline3)
#ts.add_test(Test(model3, fit3, run3), idx3)

#model4 = MultinomialHMM(n_components=states, n_iter=n_iter, verbose=True)
#fit4 = lambda data: _fit(model4, data)
#run4 = lambda token_to_elem, rhyming_dictionary: _run_limerick(model4, token_to_elem, rhyming_dictionary)
#pipeline4 = [strip_punctuation, split_by_words, reverse_lines, reverse_sonnets, flatten_sonnets]
#idx4 = ts.add_pipeline(pipeline4)
#ts.add_test(Test(model4, fit4, run4), idx4)
