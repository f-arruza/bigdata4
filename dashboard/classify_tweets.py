from pymongo import MongoClient
import os
import re
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


class Classification():

    # vocabulary in spanish
    filename_vocabulary = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       'classification_models/tweets.vocabulary')
    vocabulary = pickle.load(open(filename_vocabulary, 'rb'))

    # vocabulary in english
    filename_vocabulary_english = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       'classification_models/tweets_english.vocabulary')
    vocabulary_english = pickle.load(open(filename_vocabulary_english, 'rb'))

    # polarity's model in spanish
    filename_model_polarities = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             'classification_models/naive_bayes_polarities.model')
    model_polarities = pickle.load(open(filename_model_polarities, 'rb'))

    # polarity's model in english
    filename_model_polarities_english = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             'classification_models/naive_bayes_polarities_english.model')
    model_polarities_english = pickle.load(open(filename_model_polarities_english, 'rb'))

    # create count vectorizer
    count_vectorizer = CountVectorizer(analyzer = "word", tokenizer = None,
                                       preprocessor = None, stop_words = None,
                                       max_features = 2000, vocabulary = vocabulary)

    # create count vectorizer in english
    count_vectorizer_english = CountVectorizer(analyzer = "word", tokenizer = None,
                                               preprocessor = None, stop_words = None,
                                               max_features = 2000, vocabulary = vocabulary_english)

    def __init__(self):
        pass

    def get_preprocess_text(self, stopwords, text):
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"@\S+", "", text)
        words = re.sub(r"[^A-Za-záéíóúÁÉÍÓÚñ]", " ", text).lower().split()
        text = [w for w in words if not w in stopwords]
        return " ".join(text)

    def generate_training_dataset(self, tweets_classified):
        # load nltk data
        nltk.download('stopwords')
        # get spanish stopwords
        spanish_stopwords = set(stopwords.words('spanish'))

        tweet_texts = []
        tweet_topics = []
        tweet_polarities = []

        for tweet in tweets_classified:
            tweet_texts.append(self.get_preprocess_text(spanish_stopwords, tweet['text']))
            tweet_topics.append(tweet['topic_id'])
            tweet_polarities.append(tweet['polarity_id'])
        return [tweet_texts, tweet_topics, tweet_polarities]

    def generate_dataset(self, tweets):
        # load nltk data
        nltk.download('stopwords')
        # get spanish stopwords
        spanish_stopwords = set(stopwords.words('spanish'))

        tweet_texts = []

        for tweet in tweets:
            tweet_texts.append(self.get_preprocess_text(spanish_stopwords, tweet['payload']))
        return [tweet_texts]

    def generate_dataset_by_lang(self, tweets, lang):
        # load nltk data
        nltk.download('stopwords')
        # get spanish stopwords
        if lang == 'es':
            lang_stopwords = set(stopwords.words('spanish'))
        else:
            lang_stopwords = set(stopwords.words('english'))

        tweet_texts = []

        for tweet in tweets:
            tweet_texts.append(self.get_preprocess_text(lang_stopwords, tweet['payload']))
        return [tweet_texts]

    def generate_dataset_replies(self, replies):
        # load nltk data
        nltk.download('stopwords')
        # get spanish stopwords
        spanish_stopwords = set(stopwords.words('spanish'))

        reply_texts = []

        for reply in replies:
            reply_texts.append(self.get_preprocess_text(spanish_stopwords, reply['reply_text']))
        return [reply_texts]

    def generate_dataset_replies_original(self, replies):
        # load nltk data
        nltk.download('stopwords')
        # get spanish stopwords
        spanish_stopwords = set(stopwords.words('spanish'))

        reply_texts = []

        for reply in replies:
            reply_texts.append(self.get_preprocess_text(spanish_stopwords, reply['original_text']))
        return [reply_texts]

    def generate_dataset_single_text(self, lang, text):
        # load nltk data
        nltk.download('stopwords')
        # get stopwords
        g_stopwords = set(stopwords.words(lang))
        tweet_texts = []
        tweet_texts.append(self.get_preprocess_text(g_stopwords, text))
        return [tweet_texts]

    def classify_by_topic(self, dataset):
        # create training dataset vectorizer
        dataset_vectorizer = self.count_vectorizer.transform(dataset[0]).toarray()
        return self.model_topics.predict(dataset_vectorizer)

    def classify_by_polarity(self, dataset):
        # create training dataset vectorizer
        dataset_vectorizer = self.count_vectorizer.transform(dataset[0]).toarray()
        return self.model_polarities.predict(dataset_vectorizer)

    def classify_by_polarity_english(self, dataset):
        # create training dataset vectorizer
        dataset_vectorizer = self.count_vectorizer_english.transform(dataset[0]).toarray()
        return self.model_polarities_english.predict(dataset_vectorizer)

    def get_topic(self, key):
        topic = 'Sin clasificar'
        if key == 0:
            topic = 'otro'
        elif key == 1:
            topic = 'proceso de paz'
        elif key == 2:
            topic = 'electoral'
        elif key == 3:
            topic = 'corrupción'
        return topic

    def get_polarity(self, key):
        polarity = 'Sin clasificar'
        if key == 1:
            polarity = 'negativo'
        elif key == 2:
            polarity = 'casi negativo'
        elif key == 3:
            polarity = 'neutro'
        elif key == 4:
            polarity = 'casi positivo'
        elif key == 5:
            polarity = 'positivo'
        return polarity

    def get_polarity_by_lang(self, key, lang):
        polarity_id = 4
        polarity = 'Otro'

        if lang == 'es':
            if key == 1 or key == 2:
                polarity_id = 1
                polarity = 'Negativo'
            elif key == 3:
                polarity_id = 3
                polarity = 'Neutro'
            elif key == 4 or key == 5:
                polarity_id = 2
                polarity = 'Positivo'
        elif lang == 'en':
            if key == 1:
                polarity_id = 1
                polarity = 'Negativo'
            elif key == 2:
                polarity_id = 2
                polarity = 'Positivo'
            elif key == 3:
                polarity_id = 3
                polarity = 'Neutro'
        return [polarity_id, polarity]
