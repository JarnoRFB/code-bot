import os

class PylintRC:

    def __init__(self, filename='pylintrc'):
        self._filename = filename
        self.create()

    @property
    def filepath(self):
        return self._filename

    def does_exist(self) -> bool:
        return os.path.isfile(self._filename)

    def create(self):
        if not self.does_exist():
            with open(self.filename, 'w') as rcfile:
                rcfile.write('')

    def ignore(self, symbol):
        wait_for_empty_line = False
        with open(self._filename, 'r') as fp:
            lines = fp.readlines()
        with open(self._filename, 'w') as fp:
            for i, line in enumerate(lines):
                if line.startswith('disable='):
                    wait_for_empty_line = True
                if wait_for_empty_line and line == '\n':
                    fp.write(' ' * 8 + symbol + ',\n')
                    wait_for_empty_line = False

                fp.write(line)
