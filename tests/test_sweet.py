"""
test_sweet.py

A class for training models and preprocessing data
"""
from .utils import load_data, create_token_dictionary, apply_token_dictionary

class TestSweet:
    def __init__(self, path='data/shakespeare.txt'):
        self.data = load_data(path)
        self.pipelines = []
        self.processed_data = []
        self.token_to_elems = []
        self.tests = []

    def process_data(self):
        """
        Applies all data processing pipelines to the training data
        """
        processed_data = [self._apply_pipeline(p, self.data) for p in self.pipelines]
        token_dictionaries = [create_token_dictionary(data) for data in processed_data]
        self.processed_data = [apply_token_dictionary(token_dictionary, data) for data, token_dictionary in zip(processed_data, token_dictionaries)]
        self.token_to_elems = [{v: k for k, v in token_dictionary.items()} for token_dictionary in token_dictionaries]

    def _apply_pipeline(self, pipeline, data):
        """
        Applies the preproccing pipeline to data.

        Inputs:
        pipeline:       A list of data preprocessing functions
        data:           A raw, unprocessed dataset

        Outputs:
        data:           A processed dataset
        """
        for p in pipeline:
            data = p(data)
        return data

    def add_pipeline(self, pipeline):
        """
        Registers a new preprocessing pipeline.

        Inputs:
        pipeline:       A list of data preprocessing functions

        Outputs:
        idx:            The index of the preprocessing pipeline
        """
        idx = len(self.pipelines)
        self.pipelines.append(pipeline)
        return idx

    def add_test(self, test, idx):
        """
        Registers a new test to the test suite.

        Inputs:
        test:           The test to be run
        idx:            The index of the preprocessing pipeline which the
                        dataset should be processed with.
        """
        self.tests.append({'test': test, 'data': idx})

    def run_tests(self):
        """
        Runs all tests in the suite.
        """
        if self.processed_data == []:
            raise Exception('Data unprocessed')

        for test in self.tests:
            test['test'].fit(self.processed_data[test['data']])
            sequence = test['test'].run(self.token_to_elems[test['data']])
            print(sequence)
