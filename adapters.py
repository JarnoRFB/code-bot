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

class WritableObject(object):
    """Dummy output stream for pylint"""

    def __init__(self):
        self._content = []

    def write(self, txt):

        self._content.append(txt)

    def read(self):
        return self._content


class NullIO(StringIO):
    def write(self, txt):
        pass


# def silent(fn):
#     """Decorator to silence functions."""
#     def silent_fn(*args, **kwargs):
#         saved_stderr = sys.stderr
#         saved_stdout = sys.stdout
#         sys.stderr = NullIO()
#         sys.stdout = NullIO()
#         result = fn(*args, **kwargs)
#         sys.stderr = saved_stderr
#         sys.stdout = saved_stdout
#         return result
#
#     return silent_fn
#
#
# run_pylint = silent(lint.Run)

def run_pylint(filepath):
    output, _ = lint.py_run(command_options=f'{filepath} --score=y --rcfile=pylintrc --output-format=json',
                           return_std=True)
    return output.read()

def get_score(filepath):
    output, _ = lint.py_run(command_options=f'{filepath} --score=y --rcfile=pylintrc --output-format=parseable',
                            return_std=True)
    return parse_score(output.read())

def parse_score(text_report):
    lines = text_report.split('\n')
    m = re.search(r'(-?\d\.\d\d)\/10', lines[-3])
    return m.group(1)

def docstring_parser(x):
    return (x.split()[1], )

class ProficiencyLevels(Enum):
    BEGINNER = 0
    ADVANCED = 1

class Status(Enum):
    EXPECTS_FILE = auto()
    DETERMINE_PROFICIENCY = auto()
    WANTS_TO_HELP = auto()
    EXPECTS_DECISION = auto()
    TREAT = auto()
    WAIT_FOR_CORRECTION = auto()
    IGNORE_NOW = auto()
    IGNORE_FOREVER = auto()

class PylintAdapter(LogicAdapter):
    rcfilename = 'pylintrc'

    templates = templates

    def __init__(self, **kwargs):
        self._filepath = None
        self._status = Status.EXPECTS_FILE
        self._proficiency_level = ProficiencyLevels.BEGINNER.value

        self._score = None
        self._n_messages = None
        self._last_send_message_id = None

        super().__init__(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):

        if self._status == Status.EXPECTS_FILE:
            return self.store_file(statement)
        elif self._status == Status.DETERMINE_PROFICIENCY:
            return self._determine_proficiency(statement)
        elif self._status == Status.WANTS_TO_HELP:
            return self.suggest_improvement(statement)
        elif self._status == Status.EXPECTS_DECISION:
            return self._process_decision(statement)
        elif self._status == Status.WAIT_FOR_CORRECTION:
            return self._check_correction(statement)

    def _check_correction(self, statement):
        pylint_output, score, n_messages = self._analyze_code()
        _, next_message = self._get_first_error_in_db(pylint_output)
        correction_succeded = (n_messages < self._n_messages
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
        if 'ignore' in statement.text:
            self._status = Status.IGNORE_NOW
        else:
            self._status = Status.WAIT_FOR_CORRECTION
            selected_statement = Statement('Tell me once you have corrected the issue.')
            selected_statement.confidence = 1
            return selected_statement

    def suggest_improvement(self, statement):
        pylint_output, score, n_messages = self._analyze_code()
        self._n_messages = n_messages
        self._score = score
        print(pylint_output)
        response = self._get_response(pylint_output)

        self._status = Status.EXPECTS_DECISION
        selected_statement = Statement(response)
        selected_statement.confidence = 1
        return selected_statement

    def _analyze_code(self):
        pylint_output = self._run_pylint()
        n_messages = len(pylint_output)
        score = get_score(self._filepath)
        return pylint_output, score, n_messages

    def store_file(self, statement):
        if self._is_valid_file(statement.text):
            self._filepath = statement.text
            self._status = Status.WANTS_TO_HELP
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
        template = proficiency_templates[self._proficiency_level]
        return template.render(message)

    def _get_first_error_in_db(self, pylint_output):
        for message in pylint_output:
            proficiency_templates = self.templates.get(message['message-id'])
            if proficiency_templates is not None:
                return proficiency_templates, message
        raise ValueError('no more errors')

    def _create_rcfile(self):
        with open(self.rcfilename, 'w') as rcfile:
            rcfile.write('')


    def _is_valid_file(self, filepath):
        return os.path.isfile(filepath) and (os.path.splitext(filepath)[1] == '.py')

    def _determine_proficiency(self, statement):
        score = get_score(self._filepath)
        if score < self._threshold:
            self._proficiency_level = ProficiencyLevels.BEGINNER
        else:
            self._proficiency_level = ProficiencyLevels.ADVANCED