class TestSweet:
    def __init__(self, path='data/shakespeare.txt'):
        self.data = self.load_data(path)
        self.pipelines = []
        self.processed_data = []
        self.tests = []

    def load_data(self, path):
        sonnets = []
        sonnet = None
        with open(path, 'r') as fid:
            lines = fid.readlines()
            for line in lines:
                line = line.strip()
                if line.isdigit():
                    sonnet = []
                else:
                    if line == '':
                        if sonnet is not None:
                            # Ignoring sonnets without 14 lines
                            if len(sonnet) is 14:
                                sonnets.append(sonnet)
                                sonnet = None
                    else:
                        sonnet.append(line)
        if len(sonnet) is 14:
            sonnets.append(sonnet)
        return sonnets

    def process_data(self):
        self.processed_data = [self.apply_pipeline(p, self.data) for p in self.pipelines]

    def apply_pipeline(self, pipeline, data):
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
        self.tests.append({'model': model, 'data': self.processed_data[idx]})

    def run_tests(self):
        for test in self.tests:
            pass
