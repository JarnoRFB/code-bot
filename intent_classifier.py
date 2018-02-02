import dialogflow
from credentials import credentials
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'code-bot-service-account.json'


class DialogFlowIntentClassifier:

    def __init__(self, project_id, session_id, language_code='en'):
        self.language_code = language_code
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(project_id, session_id)


    def classify(self, text):
        """Returns the result of detect intent with texts as inputs.

        Using the same `session_id` between requests allows continuation
        of the conversaion."""

        print('Session path: {}\n'.format(self.session))


        text_input = dialogflow.types.TextInput(
            text=text, language_code=self.language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = self.session_client.detect_intent(
            session=self.session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))

        return response.query_result.intent.display_name

intent_classifier = DialogFlowIntentClassifier(credentials['project_id'], session_id=1)
intent_classifier.classify('yes')