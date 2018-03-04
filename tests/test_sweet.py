"""
test_sweet.py

A class for training models and preprocessing data
"""
from .utils import load_data

class TestSweet:
    def __init__(self, path='data/shakespeare.txt'):
        self.data = load_data(path)
        self.pipelines = []
        self.processed_data = []
        self.tests = []

    def process_data(self):
        """
        Applies all data processing pipelines to the training data
        """
        self.processed_data = [self._apply_pipeline(p, self.data) for p in self.pipelines]
        print(self.processed_data)

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

    def add_model(self, model, idx):
        """
        Registers a new model to the test suite.

        Inputs:
        model:          The model to be traines
        idx:            The index of the preprocessing pipeline which the
                        dataset should be processed with.
        """
        self.tests.append({'model': model, 'data': self.processed_data[idx]})

    def run_tests(self):
        """
        Runs all tests in the suite.
        """
        for test in self.tests:
            pass
