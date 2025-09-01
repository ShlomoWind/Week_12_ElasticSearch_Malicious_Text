import pandas as pd

class CsvLoader:
    def __init__(self, path):
        self.path = path
        self.df = None

    def load(self):
        self.df = pd.read_csv(self.path)
        return self.df