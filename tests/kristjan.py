from .test_sweet import TestSweet
from .preprocess import (
        split_by_words,
        split_by_syllables
)

ts = TestSweet()
ts.add_pipeline([
    split_by_words,
    split_by_syllables
])
