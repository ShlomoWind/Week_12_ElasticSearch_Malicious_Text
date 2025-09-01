import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

class Sentiment:
    def __init__(self,text):
        self.text = text
        try:
            self.analyzer = SentimentIntensityAnalyzer()
        except Exception:
            nltk.download('vader_lexicon', quiet=True)
            self.analyzer = SentimentIntensityAnalyzer()

    def sentiment_type(self):
        score = self.analyzer.polarity_scores(self.text)
        if score['compound'] >= 0.5:
            return 'positive'
        elif score['compound'] <= -0.5:
            return 'negative'
        else:
            return 'neutral'