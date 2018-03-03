import os

import codebot
from chatterbot import ChatBot
import pytest
from codebot.response_db import response_db
from codebot.adapters import Status, ProficiencyLevels


@pytest.fixture
def bot():
    testbot = ChatBot(
        'TestCodeBot',
        logic_adapters=[
            'codebot.adapters.PylintAdapter'
        ],
    )
    return testbot


@pytest.fixture
def lintadapter(bot):
    return bot.logic.get_adapters()[0]


def test_file_found(bot, lintadapter):
    bot_input = bot.get_response('errors.py')
    assert bot_input == response_db['file_found']
    assert lintadapter._status == Status.DETERMINE_PROFICIENCY


def test_no_file_found(bot, lintadapter):
    bot_input = bot.get_response('nonexitant.py')
    assert bot_input == response_db['no_file_found']
    assert lintadapter._status == Status.EXPECTS_FILE


def test_encountered_beginner(bot, lintadapter):
    lintadapter._status = Status.DETERMINE_PROFICIENCY
    response = bot.get_response('yes')
    assert 'beginner' in response.text
    assert lintadapter._status == Status.CONFIRM_PROFICIENCY


def test_encountered_advanced(bot, lintadapter):
    lintadapter._status = Status.DETERMINE_PROFICIENCY
    lintadapter._filepath = os.path.join(os.path.dirname(__file__), 'advanced_errors.py')
    response = bot.get_response('yes')
    assert 'advanced' in response.text
    assert lintadapter._status == Status.CONFIRM_PROFICIENCY


def test_rejected_proficiency(bot, lintadapter):
    lintadapter._status = Status.CONFIRM_PROFICIENCY
    lintadapter._proficiency_level = ProficiencyLevels.BEGINNER
    lintadapter._filepath = os.path.join(os.path.dirname(__file__), 'two_errors.py')

    response = bot.get_response('No that is wrong')
    assert response.text.startswith(response_db['rejected_proficiency_level'].format('n advanced'))
    assert lintadapter._proficiency_level == ProficiencyLevels.ADVANCED


@pytest.mark.xfail(reason='weak classifier detects wrong intent')
def test_no_decision(bot, lintadapter):
    lintadapter._status = Status.CONFIRM_PROFICIENCY
    response = bot.get_response("I can't decide")
    assert response.text == response_db['no_decision']
    assert lintadapter._status == Status.CONFIRM_PROFICIENCY


def test_exit(bot, lintadapter):
    lintadapter._status = Status.WANTS_TO_HELP  # Could be any status.
    lintadapter._first_score = 0
    response = bot.get_response('i want to exit now')
    assert response.text == response_db['goodbye'].format(0, 0)
    assert lintadapter._status == Status.END_CONVERSATION


def test_exit_with_no_more_errors(bot, lintadapter):
    lintadapter._status = Status.WANTS_TO_HELP
    lintadapter._filepath = os.path.join(os.path.dirname(__file__), 'advanced_errors.py')

    lintadapter._first_score = 0
    response = bot.get_response('yes')
    assert response.text.startswith(response_db['no_more_errors'])
    assert lintadapter._status == Status.END_CONVERSATION


def test_correction_succeeded(bot, lintadapter):
    lintadapter._status = Status.WANTS_TO_HELP
    lintadapter._filepath = os.path.join(os.path.dirname(__file__), 'two_errors.py')
    bot.get_response('go on')
    bot.get_response('yes i want to correct it')
    lintadapter._filepath = os.path.join(os.path.dirname(__file__), 'one_error.py')
    response = bot.get_response('i did it')
    assert response.text == response_db['correction_succeeded']
    assert lintadapter._status == Status.WANTS_TO_HELP


def test_correction_failed(bot, lintadapter):
    lintadapter._status = Status.WANTS_TO_HELP
    lintadapter._filepath = os.path.join(os.path.dirname(__file__), 'two_errors.py')
    bot.get_response('go on')
    bot.get_response('yes i want to correct it')
    response = bot.get_response('i did it')
    assert response.text == response_db['correction_failed']
    assert lintadapter._status == Status.WAIT_FOR_CORRECTION


@pytest.mark.xfail(reason='weak classifier detects wrong intent')
def test_ignore_now_response(bot, lintadapter):
    lintadapter._status = Status.WANTS_TO_HELP
    lintadapter._filepath = os.path.join(os.path.dirname(__file__), 'two_errors.py')
    response_before_ignore = bot.get_response('go on')
    response = bot.get_response('i want to ignore the error for now')
    assert response.text == response_db['ignore_now']
    assert lintadapter._status == Status.WANTS_TO_HELP
    response_after_ignore = bot.get_response('go on')
    assert response_before_ignore.text.startswith('In line')
    assert response_after_ignore.text.startswith('In line')
    assert response_before_ignore.text != response_after_ignore.text


def test_ignore_forever(bot, lintadapter):
    lintadapter._status = Status.WANTS_TO_HELP
    lintadapter._filepath = os.path.join(os.path.dirname(__file__), 'two_errors.py')
    response_before_ignore = bot.get_response('go on')
    response = bot.get_response("i dont care about this type of errors")
    assert response.text == response_db['ignore_forever']
    assert lintadapter._status == Status.WANTS_TO_HELP
    response_after_ignore = bot.get_response('go on')
    assert response_before_ignore.text.startswith('In line')
    assert response_after_ignore.text.startswith(response_db['no_more_errors'])
    assert lintadapter._status == Status.END_CONVERSATION


def test_not_understood(bot, lintadapter):
    lintadapter._status = Status.EXPECTS_DECISION
    response = bot.get_response('jadsk"(§"asjfdj)#@zonk')
    assert response.text == response_db['not_understood']
    assert lintadapter._status == Status.EXPECTS_DECISION
