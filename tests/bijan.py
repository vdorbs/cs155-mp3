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
    join_sonnets,
    group_characters,
    flatten_sonnets
)

ts = TestSweet()
idx = ts.add_pipeline([
    join_sonnets,
    group_characters,
    flatten_sonnets
])

model = Sequential()

def fit(data):
    token_size = max(list(itertools.chain(*data)))
    x = [np.array(dataset[:-1]).reshape(-1, 1) for dataset in data]
    y = [np.array(dataset[-1]) for dataset in data]
    x = np.array(x)
    y = np.array(y)
    #print(x.shape)
    #print(y.shape)
    y = np_utils.to_categorical(y)
    model.add(LSTM(units = 60, input_shape = (40, 1), return_sequences = True))
    model.add(Dropout(.2))
    model.add(LSTM(60))
    model.add(Dense(token_size + 1, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    model.fit(x, y, batch_size = 128, epochs=30, verbose=1)

def run(token_to_elem, rhyming_dictionary=None):
    seed = "shall i compare thee to a summer's day?\n"
    elem_to_token = {v:k for k, v in token_to_elem.items()}
    poem_char_indices = [elem_to_token[char] for char in seed]
    temperatures = [1.5, 1.0, 0.75, 0.25]
    poem = "" #Poem will hold soltuions for multiple temperatures
    for temp in temperatures:
        for line in range(9):
            next_char = 0
            while(token_to_elem[next_char] != "\n"):
                history = poem_char_indices[-40:]
                x = np.reshape(np.array(history), (1, 40, 1))
                next_char = sample(list(model.predict(x))[0], temp)
                #print(token_to_elem[next_char])
                poem_char_indices.append(next_char)
                #print(chars)
                #print(token_to_elem[next_char])
        poem += "\n\n\nTemperature = {}\n\n\n".format(temp)
        poem += "".join([token_to_elem[tok] for tok in poem_char_indices])
    return poem
ts.add_test(Test(model,fit, run), idx)

