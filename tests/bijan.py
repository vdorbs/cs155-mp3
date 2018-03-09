import itertools
import numpy as np
from .test import Test
from .test_sweet import TestSweet
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from .utils import sample
from .preprocess import (
    strip_punctuation,
    split_by_words,
    split_by_syllables,
    join_sonnet_syllables,
    group_syl,
    flatten_sonnets,
    to_lowercase
)

ts = TestSweet()
filt = [
    to_lowercase,
    strip_punctuation,
    split_by_words,
    split_by_syllables,
    join_sonnet_syllables,
    group_syl,
    flatten_sonnets
]
seed = [["shall i compare thee to a summers's day?"]]
for f in filt:
    seed = f(seed)
seed = seed[0][:-1]

idx = ts.add_pipeline(filt)

model = Sequential()

def fit(data):
    token_size = max(list(itertools.chain(*data)))
    x = [np.array(dataset[:-1]).reshape(-1, 1) for dataset in data]
    y = [np.array(dataset[-1]) for dataset in data]
    x = np.array(x)
    y = np.array(y)
    print(x.shape)
    print(y.shape)
    y = np_utils.to_categorical(y)
    model.add(LSTM(units = 50, input_shape = (8, 1), return_sequences=True))
    model.add(Dropout(.2))
    model.add(LSTM(50))
    model.add(Dense(token_size + 1, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    model.fit(x, y, epochs=10, verbose=1)

def run(token_to_elem, rhyming_dictionary=None):
    elem_to_token = {v:k for k, v in token_to_elem.items()}
    print(seed)
    poem_char_indices = [elem_to_token[char] for char in seed]
    for line in range(9):
        next_char = 0
        while(token_to_elem[next_char] != "\n"):
            history = poem_char_indices[-8:]
            x = np.reshape(np.array(history), (1, 8, 1))
            next_char = sample(list(model.predict(x))[0])
            #print(token_to_elem[next_char])
            poem_char_indices.append(next_char)
    return "".join([token_to_elem[tok] for tok in poem_char_indices])

ts.add_test(Test(model,fit, run), idx)

