import itertools
import numpy as np
from .test import Test
from .test_sweet import TestSweet
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.optimizers import RMSprop
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
    model.add(LSTM(units=64, input_shape=(40, 1), return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(units=64, input_shape=(40, 1)))
    # model.add(LSTM(units = 100, input_shape = (40, 1), return_sequences=True))
    # model.add(Dropout(0.2))
    # model.add(LSTM(units = 100))
    model.add(Dense(token_size + 1, activation='softmax'))
    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    model.fit(x, y, batch_size=128, epochs=64, verbose=1)
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")

def run(token_to_elem, rhyming_dictionary=None):
    seed = "shall i compare thee to a summer's day?\n"
    elem_to_token = {v:k for k, v in token_to_elem.items()}
    poem_char_indices = [elem_to_token[char] for char in seed]
    for line in range(9):
        next_char = 0
        while(token_to_elem[next_char] != "\n"):
            history = poem_char_indices[-40:]
            x = np.reshape(np.array(history), (1, 40, 1))
            next_char = sample(list(model.predict(x))[0])
            #print(token_to_elem[next_char])
            poem_char_indices.append(next_char)
    return "".join([token_to_elem[tok] for tok in poem_char_indices])

ts.add_test(Test(model,fit, run), idx)
