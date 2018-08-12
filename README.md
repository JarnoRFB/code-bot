![travis-ci](https://travis-ci.org/JarnoRFB/code-bot.svg?branch=master)

## Code-bot

The dialogue system Code-bot can be used to check Python code for violations of the
PEP8 coding standard as well as for errors in the code. The purpose of respecting
the PEP8 style guide is to make code more comprehensible to other programmers.

### Installation
We highly recommend you to use a virtual environment as provided by `conda`
or `pipenv`.

Inside your environment run

    $ cd codebot
    $ pip install -r requirements.txt


### Using Code-bot
To run Code-bot on the command line

    $ cd codebot
    $ PYTHONPATH=.. python codebot_cli.py

You are now able to chat with Code-bot on the command line!
Code-bot will ask you for a Python file that you would like to
be helped with and guide you through the process of improving it.

### Tests
To run the test suite

    $ cd tests
    $ pytest

