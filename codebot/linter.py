from pylint import epylint as lint
import re
import json
from .pylint_run_commands import PylintRC


class PyLinter:

    def __init__(self, rcfilepath='pylintrc'):
        self._run_commands = PylintRC(rcfilepath)
        self._rcfilepath = rcfilepath

    def lint(self, filepath) -> dict:
        output, _ = lint.py_run(
            command_options=f'{filepath} --score=y --rcfile={self._rcfilepath} --output-format=json',
            return_std=True)
        json_str = ''.join(output.read())
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return dict()

    def score(self, filepath) -> float:
        output, _ = lint.py_run(
            command_options=f'{filepath} --score=y --rcfile={self._rcfilepath} --output-format=parseable',
            return_std=True)
        output = output.read()
        return self._parse_score(output)

    def _parse_score(self, text_report):
        lines = text_report.split('\n')
        print('lines ', lines)
        match = re.search(r'(-?\d?\d\.\d\d)/10', lines[-3])
        return float(match.group(1))

    def ignore(self, symbol):
        self._run_commands.ignore(symbol)