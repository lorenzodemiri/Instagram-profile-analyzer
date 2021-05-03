from transformers import pipeline
import emoji

class SentimentAnalysis():
    def __init__(self):
        self.nlp = pipeline("sentiment-analysis")
    
    def return_sentiment(self, string: str):
        string = emoji.demojize(string, delimiters=("", ""))
        result = self.nlp(string)[0]
        return result['label'], round(result['score'], 4)


if __name__ == '__main__':
    temp = SentimentAnalysis()
    string = "solo testo"
    string = emoji.demojize(string, delimiters=("", ""))
    print(string, " RESULT -->", temp.return_sentiment(string))
