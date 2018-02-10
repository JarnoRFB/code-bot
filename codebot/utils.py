import os
import re
from chatterbot.conversation import Statement


def is_valid_python_file(filepath):
    return os.path.isfile(filepath) and (os.path.splitext(filepath)[1] == '.py')


def find_python_file(text):
    m = re.search(r'\s?([a-zA-Z0-9_\-]+?\.py)[\s\n]?', text)
    return m.group(1)

def make_confident_statement(text):
    statement = Statement(text)
    statement.confidence = 1
    return statement