import pytest
from codebot import linter, pylint_run_commands


@pytest.fixture
def pylinter():
    return linter.PyLinter(pylint_run_commands.PylintRC())


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


def test_parse_score_with_negative_score(pylinter):
    text = """    
************* Module tests.beginner_errors
C:  1, 0: Final newline missing (missing-final-newline)
C:  1, 0: Missing module docstring (missing-docstring)
W:  1, 0: Statement seems to have no effect (pointless-statement)
E:  1, 0: Undefined variable 'kdsjakfl' (undefined-variable)
E:  1, 9: Undefined variable 'j' (undefined-variable)

--------------------------------------
Your code has been rated at -120.00/10

"""
    assert pylinter._parse_score(text) == -120
