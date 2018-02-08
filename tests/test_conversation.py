import os

import codebot
from chatterbot import ChatBot
import pytest
from codebot.response_db import response_db
from codebot.adapters import Status


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
    print(lintadapter._first_score)
    assert 'advanced' in response.text
    assert lintadapter._status == Status.CONFIRM_PROFICIENCY


def test_exit(bot, lintadapter):
    lintadapter._status = Status.WANTS_TO_HELP # Could be any status.
    lintadapter._first_score = 0
    response = bot.get_response('i want to exit now')
    assert response.text == response_db['goodbye'].format(0, 0)
















