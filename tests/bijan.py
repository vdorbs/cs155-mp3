import itertools
import numpy as np
from .test import Test
from .test_sweet import TestSweet
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
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
    print(x.shape)
    print(y.shape)
    y = np_utils.to_categorical(y)
    model.add(LSTM(units = 150, input_shape = (40, 1)))
    model.add(Dense(token_size + 1, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    model.fit(x, y, epochs=10, verbose=1)

def run(token_to_elem):
    return []

ts.add_test(Test(model,fit, run), idx)

