from chatterbot.logic import LogicAdapter
from codebot.codebot_templates import templates
from chatterbot.conversation import Statement
from enum import Enum, auto
from codebot.intent_classifier import bayesian_classifier_factory
from codebot.linter import PyLinter
from codebot.pylint_run_commands import PylintRC
from codebot.exceptions import NoMoreErrors, ScoreParsingError
from codebot.response_db import response_db
from codebot.utils import is_valid_python_file, find_python_file, make_confident_statement


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
        self._linter = PyLinter(run_commands=PylintRC())
        self._intent_classifier = bayesian_classifier_factory()

        self._status = Status.EXPECTS_FILE
        self._proficiency_level = ProficiencyLevels.BEGINNER
        self._n_errors_to_ignore = 0
        self._ids_to_ignore = set()
        self._response = ''

        self._filepath = None
        self._first_score = None
        self._score = None
        self._n_messages = None
        self._last_send_message = None
        self._intent = None

        super().__init__(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):

        self._intent = self._intent_classifier.classify(statement.text)
        if self._intent == 'Exit':
            return self._say_goodbye()

        if self._status == Status.EXPECTS_FILE:
            return self._store_file(statement)
        elif self._status == Status.DETERMINE_PROFICIENCY:
            return self._determine_proficiency()
        elif self._status == Status.CONFIRM_PROFICIENCY:
            self._response = self._confirm_proficiency()
            if isinstance(self._response, Statement):
                return self._response
            return self._suggest_improvement()
        elif self._status == Status.WANTS_TO_HELP:
            return self._suggest_improvement()
        elif self._status == Status.EXPECTS_DECISION:
            return self._process_decision()
        elif self._status == Status.WAIT_FOR_CORRECTION:
            return self._check_correction()
        elif self._status == Status.END_CONVERSATION:
            raise SystemExit

    def _say_goodbye(self):
        self._status = Status.END_CONVERSATION
        try:
            self._score = self._linter.score(self._filepath)
        except ScoreParsingError:
            self._score = 0
        response = make_confident_statement(response_db['goodbye'].format(
            self._first_score, self._score))
        return response

    def _respond_to_no_more_errors(self):
        response = self._say_goodbye()
        response.text = response_db['no_more_errors'] + response.text
        return response

    def _check_correction(self):
        try:
            messages = self._analyze_code()
            n_messages = len(messages)
            _, next_message = self._get_first_error_in_db(messages)
            correction_succeeded = (n_messages != self._n_messages
                                    and self._last_send_message != next_message)
            if correction_succeeded:
                self._status = Status.WANTS_TO_HELP
                response = make_confident_statement(response_db['correction_succeeded'])
            else:
                response = make_confident_statement(response_db['correction_failed'])

            return response
        except NoMoreErrors:
            return self._respond_to_no_more_errors()

    def _process_decision(self) -> Statement:

        if self._intent == 'No_correction_now' or self._intent == 'Rejection':
            self._status = Status.WANTS_TO_HELP
            self._ignore_now()
            response = make_confident_statement(response_db['ignore_now'])
            return response

        elif self._intent == 'No_correction_forever':
            self._status = Status.WANTS_TO_HELP
            try:
                self._ignore_forever()

                response = make_confident_statement(response_db['ignore_forever'])
                return response
            except NoMoreErrors:
                return self._respond_to_no_more_errors()

        elif self._intent in ('Confirmation', 'Correction'):
            self._status = Status.WAIT_FOR_CORRECTION
            response = make_confident_statement(response_db['ask_to_correct'])
            return response
        else:
            response = make_confident_statement(response_db['not_understood'])
            return response

    def _suggest_improvement(self):
        try:
            messages = self._analyze_code()
            self._n_messages = len(messages)

            response = self._get_response(messages)
            response = self._response + response
            self._response = ''

            self._status = Status.EXPECTS_DECISION
            response = make_confident_statement(response)
            return response

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
            self._filepath = find_python_file(statement.text)
            if not is_valid_python_file(self._filepath):
                raise ValueError
            self._status = Status.DETERMINE_PROFICIENCY
            response = make_confident_statement(response_db['file_found'])
            return response
        except (AttributeError, ValueError):
            response = make_confident_statement(response_db['no_file_found'])
            return response

    def _get_response(self, pylint_output):
        proficiency_templates, message = self._get_first_error_in_db(pylint_output)
        self._last_send_message = message
        template = proficiency_templates[self._proficiency_level.value]
        return template.render(message)

    def _get_first_error_in_db(self, pylint_output):
        for i, message in enumerate(pylint_output):
            proficiency_templates = self.templates.get(message['message-id'])
            if proficiency_templates is not None:
                if i < self._n_errors_to_ignore:
                    continue
                return proficiency_templates, message

        raise NoMoreErrors()

    def _determine_proficiency(self):
        try:
            score = self._linter.score(self._filepath)
            self._first_score = score
        except ScoreParsingError:
            self._first_score = 0
        if self._first_score < self._threshold:
            self._proficiency_level = ProficiencyLevels.BEGINNER
        else:
            self._proficiency_level = ProficiencyLevels.ADVANCED

        self._status = Status.CONFIRM_PROFICIENCY
        proficiency_str = 'beginner' if self._proficiency_level == ProficiencyLevels.BEGINNER else 'advanced'
        response = make_confident_statement(response_db['encountered_proficiency_level'].format(proficiency_str))
        return response

    def _confirm_proficiency(self) -> str:
        if self._intent == 'Confirmation':
            self._status = Status.WANTS_TO_HELP
            return ''

        elif self._intent == 'Rejection':
            self._flip_proficiency_level()
            proficiency_str = ' beginner' if self._proficiency_level == ProficiencyLevels.BEGINNER else 'n advanced'
            response = response_db['rejected_proficiency_level'].format(proficiency_str)
            self._status = Status.WANTS_TO_HELP

        else:
            response = make_confident_statement(response_db['no_decision'])

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
