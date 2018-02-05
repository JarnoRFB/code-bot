import dialogflow



class DialogFlowIntentClassifier:

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
