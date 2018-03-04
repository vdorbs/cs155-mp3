class Test:
    def __init__(self, model, fit=None, run=None):
        self.model = model
        self.fit = fit
        self.run = run

    def add_fit(self, fit):
        self.fit = fit

    def add_run(self, run):
        self.run = run
