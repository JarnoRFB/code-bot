import pytest
from codebot.utils import *

def test_is_valid_python_file_should_return_true():
    filepath = 'advanced_errors.py'
    assert is_valid_python_file(filepath)

def test_is_valid_python_file_should_return_false():
    filepath = 'nonexistant.py'
    assert not is_valid_python_file(filepath)

def test_find_python_file():
    text = 'my file is advanced_errors.py. That is what I called it'
    assert find_python_file(text) == 'advanced_errors.py'

def test_find_python_file_should_raise():
    text = 'my file is advanced_errors.cpp. That is what I called it'
    with pytest.raises(AttributeError):
        find_python_file(text)

def test_make_confident_statement():
    text = 'hello world'
    statement = make_confident_statement(text)
    assert statement.text == text
    assert statement.confidence == 1