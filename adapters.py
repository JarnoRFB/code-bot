import json
import os
import sys
from io import StringIO
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from codebot_templates import templates
from pylint import epylint as lint
import re
from enum import Enum, auto
from intent_classifier import DialogFlowIntentClassifier
from credentials import credentials


def run_pylint(filepath):
    output, _ = lint.py_run(command_options=f'{filepath} --score=y --rcfile=pylintrc --output-format=json',
                            return_std=True)
    return output.read()


def get_score(filepath):
    output, _ = lint.py_run(command_options=f'{filepath} --score=y --rcfile=pylintrc --output-format=parseable',
                            return_std=True)
    return float(parse_score(output.read()))


def parse_score(text_report):
    lines = text_report.split('\n')
    m = re.search(r'(-?\d\.\d\d)/10', lines[-3])
    return m.group(1)


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
    rcfilename = 'pylintrc'
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

        super().__init__(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):

        intent = self._intent_classifier.classify(statement.text)
        if intent == 'Exit':
            return self._exit()

        if self._status == Status.EXPECTS_FILE:
            return self.store_file(statement)
        elif self._status == Status.DETERMINE_PROFICIENCY:
            return self._determine_proficiency(statement)
        elif self._status == Status.CONFIRM_PROFICIENCY:
            return self._confirm_proficiency(statement)
        elif self._status == Status.WANTS_TO_HELP:
            return self.suggest_improvement(statement)
        elif self._status == Status.EXPECTS_DECISION:
            return self._process_decision(statement)
        elif self._status == Status.WAIT_FOR_CORRECTION:
            return self._check_correction(statement)
        elif self._status == Status.END_CONVERSATION:
            raise SystemExit

    def _exit(self):
        self._status = Status.END_CONVERSATION
        self._score = get_score(self._filepath)
        response = Statement(
            f'It was fun to code with you! You improved your score from {self._first_score} to {self._score} out of 10 possible points. See you later')
        response.confidence = 1
        return response

    def _check_correction(self, statement):
        pylint_output, score, n_messages = self._analyze_code()
        print(pylint_output)
        _, next_message = self._get_first_error_in_db(pylint_output)
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
            selected_statement = Statement("Ok I will ignore the error for now.")
            selected_statement.confidence = 1
            return selected_statement

        elif intent == 'No_correction_forever':
            self._status = Status.WANTS_TO_HELP
            self._ignore_forever()

            selected_statement = Statement("Ok I won't bother you with this type of errors again.")
            selected_statement.confidence = 1
            return selected_statement

        elif intent == 'Confirmation':
            self._status = Status.WAIT_FOR_CORRECTION
            selected_statement = Statement('Tell me once you have corrected the issue.')
            selected_statement.confidence = 1
            return selected_statement
        else:
            raise ValueError('No matched intent')

    def suggest_improvement(self, statement):
        pylint_output, score, n_messages = self._analyze_code()
        self._n_messages = n_messages
        try:
            response = self._get_response(pylint_output)

            self._status = Status.EXPECTS_DECISION
            selected_statement = Statement(response)
            selected_statement.confidence = 1
            return selected_statement
        except ValueError:
            return self._exit()

    def _analyze_code(self):
        pylint_output = self._run_pylint()
        n_messages = len(pylint_output)
        score = get_score(self._filepath)  # TODO is this neccessary
        return pylint_output, score, n_messages

    def store_file(self, statement):
        if self._is_valid_file(statement.text):
            self._filepath = statement.text
            self._status = Status.DETERMINE_PROFICIENCY
            selected_statement = Statement('Alright, should I look over your code now?')
            selected_statement.confidence = 1
            return selected_statement
        else:
            selected_statement = Statement('Sorry but that is no file.')
            selected_statement.confidence = 1
            return selected_statement

    def _run_pylint(self):
        if not os.path.isfile(self.rcfilename):
            self._create_rcfile()
        pylint_output = run_pylint(self._filepath)
        json_str = ''.join(pylint_output)
        return json.loads(json_str)

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

        raise ValueError('No more errors.')

    def _create_rcfile(self):
        with open(self.rcfilename, 'w') as rcfile:
            rcfile.write('')

    def _is_valid_file(self, filepath):
        return os.path.isfile(filepath) and (os.path.splitext(filepath)[1] == '.py')

    def _determine_proficiency(self, statement):
        score = get_score(self._filepath)
        self._first_score = score
        if score < self._threshold:
            self._proficiency_level = ProficiencyLevels.BEGINNER
        else:
            self._proficiency_level = ProficiencyLevels.ADVANCED

        self._status = Status.CONFIRM_PROFICIENCY
        proficiency_str = 'beginner' if self._proficiency_level == ProficiencyLevels.BEGINNER else 'advanced'
        selected_statement = Statement(
            'From looking at your code you seem to be %s at coding. Is that right?' % proficiency_str)
        selected_statement.confidence = 1
        return selected_statement

    def _confirm_proficiency(self, statement):
        intent = self._intent_classifier.classify(statement.text)
        if intent == 'Confirmation':
            response = Statement(
                'Ok should I analyze your code now?')
            self._status = Status.WANTS_TO_HELP

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
        pylint_output, _, _ = self._analyze_code()
        _, message = self._get_first_error_in_db(pylint_output)
        self._ids_to_ignore.add(message['message-id'])
