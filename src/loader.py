import pandas as pd

class CsvLoader:
    def __init__(self, path):
        self.path = path
        self.df = None

    def load(self):
        self.df = pd.read_csv(self.path)
        if 'TweetID' in self.df.columns:
            self.df['TweetID'] = self.df['TweetID'].apply(lambda x: str(int(x)) if pd.notna(x) else None)
        if 'CreateDate' in self.df.columns:
            self.df['CreateDate'] = pd.to_datetime(self.df['CreateDate'], errors='coerce')
            self.df['CreateDate'] = self.df['CreateDate'].dt.strftime("%Y-%m-%dT%H:%M:%S")
            self.df['CreateDate'] = self.df['CreateDate'].where(self.df['CreateDate'].notna(), None)
        return self.df