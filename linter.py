from pylint import epylint as lint
import re
import json
from pylintrc import PylintRC


class PyLinter:

    def __init__(self, rcfilepath='pylintrc'):
        self._run_commands = PylintRC(rcfilepath)

    def lint(self, filepath) -> dict:
        output, _ = lint.py_run(
            command_options=f'{filepath} --score=y --rcfile={self._run_commands.filepath} --output-format=json',
            return_std=True)
        json_str = ''.join(output.read())
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return dict()

    def score(self, filepath) -> float:
        output, _ = lint.py_run(
            command_options=f'{filepath} --score=y --rcfile={self._run_commands.filepath} --output-format=parseable',
            return_std=True)
        return self._parse_score(output.read())

    def _parse_score(self, text_report):
        lines = text_report.split('\n')
        match = re.search(r'(-?\d\.\d\d)/10', lines[-3])
        return float(match.group(1))

    def ignore(self, symbol):
        self._run_commands.ignore(symbol)