class Test:
    def __init__(self, model, fit=None):
        self.model = model
        self.fit = fit

    def add_fit(self, fit):
        self.fit = fit
