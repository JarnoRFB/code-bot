![travis-ci](https://travis-ci.org/JarnoRFB/code-bot.svg?branch=master)

## Code-bot

The dialogue system Code-bot can be used to check Python code for violations of the
PEP8 coding standard 1 as well as for errors in the code. The purpose of respecting
the PEP8 style guide is to make code more comprehensible to other programmers.

### Installing dependencies
We highly recommend you to use a virtual environment as provided by `conda`
or `virtualenv`.

Inside your environment run

    $ cd codebot
    $ pip install -r requirements.txt


### To run Code-bot on the command line

    $ cd codebot
    $ PYTHONPATH=.. python codebot_cli.py

### Tests
To run the test suite

    $ cd tests
    $ pytest

