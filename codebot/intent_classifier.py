import dialogflow
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import json
import os
import pandas as pd

class BaseIntentClassifier:

    def classify(self, text):
        raise NotImplementedError

class DialogFlowIntentClassifier(BaseIntentClassifier):

    def __init__(self, project_id, session_id=0, language_code='en'):
        self.language_code = language_code
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(project_id, session_id)


    def classify(self, text):
        """Returns the result of detect intent with texts as inputs.

        Using the same `session_id` between requests allows continuation
        of the conversaion."""

        if not text:
            return 'Confirmation'

        text_input = dialogflow.types.TextInput(
            text=text, language_code=self.language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = self.session_client.detect_intent(
            session=self.session, query_input=query_input)

        return response.query_result.intent.display_name


class BayesIntentClassifier(BaseIntentClassifier):
    """Kind of multinomial naive Bayes.

    Based on https://chatbotslife.com/text-classification-using-algorithms-e4d50dcba45."""

    def __init__(self, stemmer):
        self._intent_classes = pd.Series()
        self._class_to_token = pd.Series()
        self._token_counts = pd.Series()
        self._class_counts = pd.Series()
        self._stemmer = stemmer

    def fit(self, training_data):
        intent_word_data = pd.DataFrame(columns=['class', 'token'])
        for _, row in training_data.iterrows():
            for token in nltk.word_tokenize(row['sentence']):
                token = self._stemmer.stem(token)
                intent_word_data = intent_word_data.append({'class': row['class'], 'token': token},
                                        ignore_index=True)

        self._intent_classes = intent_word_data['class'].unique()
        self._class_to_token = intent_word_data.groupby(['class'])['token'].unique()
        self._token_counts = intent_word_data.groupby(['token'])['token'].count()
        self._class_counts = intent_word_data.groupby(['class']).size()

    def classify(self, text):

        high_class = ''
        high_score = 0
        for intent_class in self._intent_classes:

            score = self.calculate_class_score_commonality(text, intent_class)

            if score > high_score:
                high_class = intent_class
                high_score = score

        return high_class

    def calculate_class_score_commonality(self, text, intent_class):
        score = 0
        for token in nltk.word_tokenize(text):
            stemmed_token = self._stemmer.stem(token.lower())
            if stemmed_token in self._class_to_token.loc[intent_class]:
                # treat each word with relative weight, based on the number of total counts in the intent class.
                score += (1 / self._class_counts.loc[intent_class])

        return score

def bayesian_classifier_factory():
    intent_data = preprocess_dialogflow_intent_files(os.path.join(os.path.dirname(__file__), 'intents'))
    stemmer = LancasterStemmer()
    bayesian_intent_classifier = BayesIntentClassifier(stemmer)
    bayesian_intent_classifier.fit(intent_data)
    return bayesian_intent_classifier


def preprocess_dialogflow_intent_files(intent_dir):
    """Turns the JSON exported from DialogFlow intents into dataframes."""
    intent_data = pd.DataFrame(columns=['class', 'sentence'])
    for filename in os.listdir(intent_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(intent_dir, filename)
            intent_class, example_sentences = preprocess_dialogflow_intent_file(filepath)
            for example_sentence in example_sentences:
                intent_data = intent_data.append({'class': intent_class,
                                                  'sentence': example_sentence},
                                                 ignore_index=True)

    return intent_data



def preprocess_dialogflow_intent_file(intent_filepath):
    """Turns the JSON exported from DialogFlow intents into a class name and a list of examples."""
    with open(intent_filepath) as fp:
        intent_spec = json.load(fp)
    intent_class = intent_spec['name']
    example_sentences = []
    for example in intent_spec['userSays']:
        example_sentences.append(example['data'][0]['text'])

    return intent_class, example_sentences




























