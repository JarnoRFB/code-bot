import os
from pylint import epylint as lint

class PylintRC:

    def __init__(self, filename):
        # Create RC file one level above due to some strange pylint behavior.
        self._filename = os.path.join('..', filename)
        self.create()

    @property
    def filepath(self):
        return self._filename

    def does_exist(self) -> bool:
        return os.path.isfile(self._filename)

    def create(self):
        with open(self._filename, 'w') as rcfile:
            rcfile.write(self._generate_rcfile())

    def _generate_rcfile(self):
        return """[MASTER]

# A comma-separated list of package or module names from where C extensions may
# be loaded. Extensions are loading into the active Python interpreter and may
# run arbitrary code
extension-pkg-whitelist=

# Add files or directories to the blacklist. They should be base names, not
# paths.
ignore=CVS

# Add files or directories matching the regex patterns to the blacklist. The
# regex matches against base names, not paths.
ignore-patterns=

# Python code to execute, usually for sys.path manipulation such as
# pygtk.require().
#init-hook=

# Use multiple processes to speed up Pylint.
jobs=1

# List of plugins (as comma separated values of python modules names) to load,
# usually to register additional checkers.
load-plugins=

# Pickle collected data for later comparisons.
persistent=yes

# Specify a configuration file.
#rcfile=

# When enabled, pylint would attempt to guess common misconfiguration and emit
# user-friendly hints instead of false-positive error messages
suggestion-mode=yes

# Allow loading of arbitrary C extensions. Extensions are imported into the
# active Python interpreter and may run arbitrary code.
unsafe-load-any-extension=no


[MESSAGES CONTROL]

# Only show warnings with the listed confidence levels. Leave empty to show
# all. Valid levels: HIGH, INFERENCE, INFERENCE_FAILURE, UNDEFINED
confidence=

# Disable the message, report, category or checker with the given id(s). You
# can either give multiple identifiers separated by comma (,) or put this
# option multiple times (only on the command line, not in the configuration
# file where it should appear only once).You can also use "--disable=all" to
# disable everything first and then reenable specific checks. For example, if
# you want to run only the similarities checker, you can use "--disable=all
# --enable=similarities". If you want to run only the classes checker, but have
# no Warning level messages displayed, use"--disable=all --enable=classes
# --disable=W"
disable=print-statement,
        parameter-unpacking,
        unpacking-in-except,
        old-raise-syntax,
        backtick,
        long-suffix,
        old-ne-operator,
        old-octal-literal,
        import-star-module-level,
        non-ascii-bytes-literal,
        raw-checker-failed,
        bad-inline-option,
        locally-disabled,
        locally-enabled,
        file-ignored,
        suppressed-message,
        useless-suppression,
        deprecated-pragma,
        apply-builtin,
        basestring-builtin,
        buffer-builtin,
        cmp-builtin,
        coerce-builtin,
        execfile-builtin,
        file-builtin,
        long-builtin,
        raw_input-builtin,
        reduce-builtin,
        standarderror-builtin,
        unicode-builtin,
        xrange-builtin,
        coerce-method,
        delslice-method,
        getslice-method,
        setslice-method,
        no-absolute-import,
        old-division,
        dict-iter-method,
        dict-view-method,
        next-method-called,
        metaclass-assignment,
        indexing-exception,
        raising-string,
        reload-builtin,
        oct-method,
        hex-method,
        nonzero-method,
        cmp-method,
        input-builtin,
        round-builtin,
        intern-builtin,
        unichr-builtin,
        map-builtin-not-iterating,
        zip-builtin-not-iterating,
        range-builtin-not-iterating,
        filter-builtin-not-iterating,
        using-cmp-argument,
        eq-without-hash,
        div-method,
        idiv-method,
        rdiv-method,
        exception-message-attribute,
        invalid-str-codec,
        sys-max-int,
        bad-python3-import,
        deprecated-string-function,
        deprecated-str-translate-call,
        deprecated-itertools-function,
        deprecated-types-field,
        next-method-defined,
        dict-items-not-iterating,
        dict-keys-not-iterating,
        dict-values-not-iterating

# Enable the message, report, category or checker with the given id(s). You can
# either give multiple identifier separated by comma (,) or put this option
# multiple time (only on the command line, not in the configuration file where
# it should appear only once). See also the "--disable" option for examples.
enable=c-extension-no-member


[REPORTS]

# Python expression which should return a note less than 10 (10 is the highest
# note). You have access to the variables errors warning, statement which
# respectively contain the number of errors / warnings messages and the total
# number of statements analyzed. This is used by the global evaluation report
# (RP0004).
evaluation=10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)

# Template used to display messages. This is a python new-style format string
# used to format the message information. See doc for all details
#msg-template=

# Set the output format. Available formats are text, parseable, colorized, json
# and msvs (visual studio).You can also give a reporter class, eg
# mypackage.mymodule.MyReporterClass.
output-format=text

# Tells whether to display a full report or only the messages
reports=no

# Activate the evaluation score.
score=yes


[REFACTORING]

# Maximum number of nested blocks for function / method body
max-nested-blocks=5

# Complete name of functions that never returns. When checking for
# inconsistent-return-statements if a never returning function is called then
# it will be considered as an explicit return statement and no message will be
# printed.
never-returning-functions=optparse.Values,sys.exit


[TYPECHECK]

# List of decorators that produce context managers, such as
# contextlib.contextmanager. Add to this list to register other decorators that
# produce valid context managers.
contextmanager-decorators=contextlib.contextmanager

# List of members which are set dynamically and missed by pylint inference
# system, and so shouldn't trigger E1101 when accessed. Python regular
# expressions are accepted.
generated-members=

# Tells whether missing members accessed in mixin class should be ignored. A
# mixin class is detected if its name ends with "mixin" (case insensitive).
ignore-mixin-members=yes

# This flag controls whether pylint should warn about no-member and similar
# checks whenever an opaque object is returned when inferring. The inference
# can return multiple potential results while evaluating a Python object, but
# some branches might not be evaluated, which results in partial inference. In
# that case, it might be useful to still emit no-member and other checks for
# the rest of the inferred objects.
ignore-on-opaque-inference=yes

# List of class names for which member attributes should not be checked (useful
# for classes with dynamically set attributes). This supports the use of
# qualified names.
ignored-classes=optparse.Values,thread._local,_thread._local

# List of module names for which member attributes should not be checked
# (useful for modules/projects where namespaces are manipulated during runtime
# and thus existing member attributes cannot be deduced by static analysis. It
# supports qualified module names, as well as Unix pattern matching.
ignored-modules=

# Show a hint with possible names when a member name was not found. The aspect
# of finding the hint is based on edit distance.
missing-member-hint=yes

# The minimum edit distance a name should have in order to be considered a
# similar match for a missing member name.
missing-member-hint-distance=1

# The total number of similar names that should be taken in consideration when
# showing a hint for a missing member.
missing-member-max-choices=1


[SPELLING]

# Limits count of emitted suggestions for spelling mistakes
max-spelling-suggestions=4

# Spelling dictionary name. Available dictionaries: none. To make it working
# install python-enchant package.
spelling-dict=

# List of comma separated words that should not be checked.
spelling-ignore-words=

# A path to a file that contains private dictionary; one word per line.
spelling-private-dict-file=

# Tells whether to store unknown words to indicated private dictionary in
# --spelling-private-dict-file option instead of raising a message.
spelling-store-unknown-words=no


[VARIABLES]

# List of additional names supposed to be defined in builtins. Remember that
# you should avoid to define new builtins when possible.
additional-builtins=

# Tells whether unused global variables should be treated as a violation.
allow-global-unused-variables=yes

# List of strings which can identify a callback function by name. A callback
# name must start or end with one of those strings.
callbacks=cb_,
          _cb

# A regular expression matching the name of dummy variables (i.e. expectedly
# not used).
dummy-variables-rgx=_+$|(_[a-zA-Z0-9_]*[a-zA-Z0-9]+?$)|dummy|^ignored_|^unused_

# Argument names that match this expression will be ignored. Default to name
# with leading underscore
ignored-argument-names=_.*|^ignored_|^unused_

# Tells whether we should check for unused import in __init__ files.
init-import=no

# List of qualified module names which can have objects that can redefine
# builtins.
redefining-builtins-modules=six.moves,past.builtins,future.builtins


[BASIC]

# Naming style matching correct argument names
argument-naming-style=snake_case

# Regular expression matching correct argument names. Overrides argument-
# naming-style
#argument-rgx=

# Naming style matching correct attribute names
attr-naming-style=snake_case

# Regular expression matching correct attribute names. Overrides attr-naming-
# style
#attr-rgx=

# Bad variable names which should always be refused, separated by a comma
bad-names=foo,
          bar,
          baz,
          toto,
          tutu,
          tata

# Naming style matching correct class attribute names
class-attribute-naming-style=any

# Regular expression matching correct class attribute names. Overrides class-
# attribute-naming-style
#class-attribute-rgx=

# Naming style matching correct class names
class-naming-style=PascalCase

# Regular expression matching correct class names. Overrides class-naming-style
#class-rgx=

# Naming style matching correct constant names
const-naming-style=UPPER_CASE

# Regular expression matching correct constant names. Overrides const-naming-
# style
#const-rgx=

# Minimum line length for functions/classes that require docstrings, shorter
# ones are exempt.
docstring-min-length=-1

# Naming style matching correct function names
function-naming-style=snake_case

# Regular expression matching correct function names. Overrides function-
# naming-style
#function-rgx=

# Good variable names which should always be accepted, separated by a comma
good-names=i,
           j,
           k,
           ex,
           Run,
           _

# Include a hint for the correct naming format with invalid-name
include-naming-hint=no

# Naming style matching correct inline iteration names
inlinevar-naming-style=any

# Regular expression matching correct inline iteration names. Overrides
# inlinevar-naming-style
#inlinevar-rgx=

# Naming style matching correct method names
method-naming-style=snake_case

# Regular expression matching correct method names. Overrides method-naming-
# style
#method-rgx=

# Naming style matching correct module names
module-naming-style=snake_case

# Regular expression matching correct module names. Overrides module-naming-
# style
#module-rgx=

# Colon-delimited sets of names that determine each other's naming style when
# the name regexes allow several styles.
name-group=

# Regular expression which should only match function or class names that do
# not require a docstring.
no-docstring-rgx=^_

# List of decorators that produce properties, such as abc.abstractproperty. Add
# to this list to register other decorators that produce valid properties.
property-classes=abc.abstractproperty

# Naming style matching correct variable names
variable-naming-style=snake_case

# Regular expression matching correct variable names. Overrides variable-
# naming-style
#variable-rgx=


[LOGGING]

# Logging modules to check that the string format arguments are in logging
# function parameter format
logging-modules=logging


[MISCELLANEOUS]

# List of note tags to take in consideration, separated by a comma.
notes=FIXME,
      XXX,
      TODO


[FORMAT]

# Expected format of line ending, e.g. empty (any line ending), LF or CRLF.
expected-line-ending-format=

# Regexp for a line that is allowed to be longer than the limit.
ignore-long-lines=^\s*(# )?<?https?://\S+>?$

# Number of spaces of indent required inside a hanging  or continued line.
indent-after-paren=4

# String used as indentation unit. This is usually "    " (4 spaces) or "\t" (1
# tab).
indent-string='    '

# Maximum number of characters on a single line.
max-line-length=100

# Maximum number of lines in a module
max-module-lines=1000

# List of optional constructs for which whitespace checking is disabled. `dict-
# separator` is used to allow tabulation in dicts, etc.: {1  : 1,\n222: 2}.
# `trailing-comma` allows a space between comma and closing bracket: (a, ).
# `empty-line` allows space-only lines.
no-space-check=trailing-comma,
               dict-separator

# Allow the body of a class to be on the same line as the declaration if body
# contains single statement.
single-line-class-stmt=no

# Allow the body of an if to be on the same line as the test if there is no
# else.
single-line-if-stmt=no


[SIMILARITIES]

# Ignore comments when computing similarities.
ignore-comments=yes

# Ignore docstrings when computing similarities.
ignore-docstrings=yes

# Ignore imports when computing similarities.
ignore-imports=no

# Minimum lines number of a similarity.
min-similarity-lines=4


[CLASSES]

# List of method names used to declare (i.e. assign) instance attributes.
defining-attr-methods=__init__,
                      __new__,
                      setUp

# List of member names, which should be excluded from the protected access
# warning.
exclude-protected=_asdict,
                  _fields,
                  _replace,
                  _source,
                  _make

# List of valid names for the first argument in a class method.
valid-classmethod-first-arg=cls

# List of valid names for the first argument in a metaclass class method.
valid-metaclass-classmethod-first-arg=mcs


[IMPORTS]

# Allow wildcard imports from modules that define __all__.
allow-wildcard-with-all=no

# Analyse import fallback blocks. This can be used to support both Python 2 and
# 3 compatible code, which means that the block might have code that exists
# only in one or another interpreter, leading to false positives when analysed.
analyse-fallback-blocks=no

# Deprecated modules which should not be used, separated by a comma
deprecated-modules=optparse,tkinter.tix

# Create a graph of external dependencies in the given file (report RP0402 must
# not be disabled)
ext-import-graph=

# Create a graph of every (i.e. internal and external) dependencies in the
# given file (report RP0402 must not be disabled)
import-graph=

# Create a graph of internal dependencies in the given file (report RP0402 must
# not be disabled)
int-import-graph=

# Force import order to recognize a module as part of the standard
# compatibility libraries.
known-standard-library=

# Force import order to recognize a module as part of a third party library.
known-third-party=enchant


[DESIGN]

# Maximum number of arguments for function / method
max-args=5

# Maximum number of attributes for a class (see R0902).
max-attributes=7

# Maximum number of boolean expressions in a if statement
max-bool-expr=5

# Maximum number of branch for function / method body
max-branches=12

# Maximum number of locals for function / method body
max-locals=15

# Maximum number of parents for a class (see R0901).
max-parents=7

# Maximum number of public methods for a class (see R0904).
max-public-methods=20

# Maximum number of return / yield for function / method body
max-returns=6

# Maximum number of statements in function / method body
max-statements=50

# Minimum number of public methods for a class (see R0903).
min-public-methods=2


[EXCEPTIONS]

# Exceptions that will emit a warning when being caught. Defaults to
# "Exception"
overgeneral-exceptions=Exception
"""

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
