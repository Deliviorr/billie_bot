from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from translate import Translator

transloter_eng = Translator(to_lang="en")

def sentiment_analyse(tekst):
    vertaling = transloter_eng.translate(tekst)
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(vertaling)
    scores_compound = scores['compound']

    if scores_compound <= -0.5:
        return "Boos"
    elif -0.5 < scores_compound < 0:
        return "negatief"
    elif scores_compound == 0:
        return "neutraal"
    elif scores_compound > 0:
        return "positief"
    return "Niet bepaald"