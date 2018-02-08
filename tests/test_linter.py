import pytest
from codebot import linter

@pytest.fixture
def pylinter():
    return linter.PyLinter()

def test_parse_score_with_10(pylinter):
    text = """    
--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

"""
    assert pylinter._parse_score(text) == 10

def test_parse_score_with_in_between(pylinter):
    text = """    
************* Module tests.advanced_errors
C:  4, 0: Missing function docstring (missing-docstring)

-------------------------------------------------------------------
Your code has been rated at 6.67/10 (previous run: 10.00/10, -3.33)

"""
    assert pylinter._parse_score(text) == 6.67