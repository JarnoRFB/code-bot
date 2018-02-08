import os

import re
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from codebot.codebot_templates import templates

from enum import Enum, auto
from codebot.intent_classifier import DialogFlowIntentClassifier
from codebot.credentials import credentials
from codebot.linter import PyLinter
from codebot.exceptions import NoMoreErrors
from codebot.response_db import response_db

class ProficiencyLevels(Enum):
    BEGINNER = 0
    ADVANCED = 1


class Status(Enum):
    EXPECTS_FILE = auto()
    DETERMINE_PROFICIENCY = auto()
    CONFIRM_PROFICIENCY = auto()
    WANTS_TO_HELP = auto()
    EXPECTS_DECISION = auto()
    TREAT = auto()
    WAIT_FOR_CORRECTION = auto()
    IGNORE_NOW = auto()
    IGNORE_FOREVER = auto()
    END_CONVERSATION = auto()


class PylintAdapter(LogicAdapter):
    _threshold = 5

    templates = templates

    def __init__(self, **kwargs):
        self._ids_to_ignore = set()
        self._n_errors_to_ignore = 0
        self._filepath = None
        self._status = Status.EXPECTS_FILE
        self._proficiency_level = ProficiencyLevels.BEGINNER.value
        self._intent_classifier = DialogFlowIntentClassifier(credentials['project_id'])
        self._first_score = None
        self._score = None
        self._n_messages = None
        self._last_send_message_id = None
        self._linter = PyLinter()
        self._response = None

        super().__init__(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):

        intent = self._intent_classifier.classify(statement.text)
        if intent == 'Exit':
            return self._say_goodbye()

        if self._status == Status.EXPECTS_FILE:
            return self._store_file(statement)
        elif self._status == Status.DETERMINE_PROFICIENCY:
            return self._determine_proficiency(statement)
        elif self._status == Status.CONFIRM_PROFICIENCY:
            self._response = self._confirm_proficiency(statement)
            return self._suggest_improvement(statement)
        elif self._status == Status.WANTS_TO_HELP:
            return self._suggest_improvement(statement)
        elif self._status == Status.EXPECTS_DECISION:
            return self._process_decision(statement)
        elif self._status == Status.WAIT_FOR_CORRECTION:
            return self._check_correction(statement)
        elif self._status == Status.END_CONVERSATION:
            raise SystemExit

    def _say_goodbye(self):
        self._status = Status.END_CONVERSATION
        try:
            self._score = self._linter.score(self._filepath)
        except:
            self._score = 0
        response = Statement(response_db['goodbye'].format(
                self._first_score, self._score))
        response.confidence = 1
        return response

    def _respond_to_no_more_errors(self):
        response = self._say_goodbye()
        response.text = 'There are no more errors in your code. ' + response.text
        return response

    def _check_correction(self, statement):
        messages = self._analyze_code()
        n_messages = len(messages)
        _, next_message = self._get_first_error_in_db(messages)
        correction_succeded = (n_messages != self._n_messages
                               and self._last_send_message_id != next_message['message-id'])
        if correction_succeded:
            self._status = Status.WANTS_TO_HELP
            selected_statement = Statement('Great you did it!')
            selected_statement.confidence = 1
        else:
            selected_statement = Statement('The error is still there...')
            selected_statement.confidence = 1

        return selected_statement

    def _process_decision(self, statement):
        intent = self._intent_classifier.classify(statement.text)

        if intent == 'No_correction_now' or intent == 'Rejection':
            self._status = Status.WANTS_TO_HELP
            self._ignore_now()
            response = Statement("Ok I will ignore the error for now.")
            response.confidence = 1
            return response

        elif intent == 'No_correction_forever':
            self._status = Status.WANTS_TO_HELP
            self._ignore_forever()

            response = Statement("Ok I won't bother you with this type of errors again.")
            response.confidence = 1
            return response

        elif intent in ('Confirmation', 'Correction'):
            self._status = Status.WAIT_FOR_CORRECTION
            response = Statement('Tell me once you have corrected the issue.')
            response.confidence = 1
            return response
        else:
            response = Statement("Sorry I don't understand you. Can you say this in a different way?")
            response.confidence = 1
            return response

    def _suggest_improvement(self, statement):
        try:
            messages = self._analyze_code()
            print(messages)
            self._n_messages = len(messages)

            response = self._get_response(messages)
            if self._response is not None:
                response = f'{self._response} {response}'
                self._response = None
            self._status = Status.EXPECTS_DECISION
            selected_statement = Statement(response)
            selected_statement.confidence = 1
            return selected_statement

        except ValueError:
            return self._say_goodbye()
        except NoMoreErrors:
            return self._respond_to_no_more_errors()

    def _analyze_code(self):
        messages = self._linter.lint(self._filepath)
        if not messages:
            raise NoMoreErrors()
        return messages

    def _store_file(self, statement):
        try:
            self._filepath = self._find_python_file(statement.text)
            if not self._is_valid_file(self._filepath):
                raise ValueError
            self._status = Status.DETERMINE_PROFICIENCY
            response = Statement(response_db['file_found'])
            response.confidence = 1
            return response
        except (AttributeError, ValueError):
            response = Statement(response_db['no_file_found'])
            response.confidence = 1
            return response

    def _find_python_file(self, text):
        m = re.search(r'\s?([a-zA-Z0-9_\-]+?\.py)[\s\n]?', text)
        return m.group(1)

    def _get_response(self, pylint_output):
        proficiency_templates, message = self._get_first_error_in_db(pylint_output)
        self._last_send_message_id = message['message-id']
        template = proficiency_templates[self._proficiency_level.value]
        return template.render(message)

    def _get_first_error_in_db(self, pylint_output):
        for i, message in enumerate(pylint_output):
            if i < self._n_errors_to_ignore:
                continue
            if message['message-id'] in self._ids_to_ignore:
                continue
            proficiency_templates = self.templates.get(message['message-id'])
            if proficiency_templates is not None:
                return proficiency_templates, message

        raise NoMoreErrors()

    def _is_valid_file(self, filepath):
        return os.path.isfile(filepath) and (os.path.splitext(filepath)[1] == '.py')

    def _determine_proficiency(self, statement):
        try:
            score = self._linter.score(self._filepath)
            self._first_score = score
        except:
            self._first_score = 0
        if self._first_score < self._threshold:
            self._proficiency_level = ProficiencyLevels.BEGINNER
        else:
            self._proficiency_level = ProficiencyLevels.ADVANCED

        self._status = Status.CONFIRM_PROFICIENCY
        proficiency_str = 'beginner' if self._proficiency_level == ProficiencyLevels.BEGINNER else 'advanced'
        response = Statement(response_db['encountered_proficiency_level'].format(proficiency_str))
        response.confidence = 1
        return response

    def _confirm_proficiency(self, statement):
        intent = self._intent_classifier.classify(statement.text)
        if intent == 'Confirmation':
            self._status = Status.WANTS_TO_HELP
            return

        elif intent == 'Rejection':
            self._flip_proficiency_level()
            proficiency_str = ' beginner' if self._proficiency_level == ProficiencyLevels.BEGINNER else 'n advanced'
            response = Statement(
                'Ok I will treat you as a%s programmer instead. Should I analyze your code now?' % proficiency_str)
            self._status = Status.WANTS_TO_HELP

        else:
            response = Statement('Either reject or agree.')

        response.confidence = 1
        return response

    def _flip_proficiency_level(self):
        if self._proficiency_level == ProficiencyLevels.BEGINNER:
            self._proficiency_level = ProficiencyLevels.ADVANCED
        else:
            self._proficiency_level = ProficiencyLevels.BEGINNER

    def _ignore_now(self):
        self._n_errors_to_ignore += 1

    def _ignore_forever(self):
        pylint_output = self._analyze_code()
        _, message = self._get_first_error_in_db(pylint_output)
        self._linter.ignore(message['symbol'])
