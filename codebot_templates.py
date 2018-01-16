from template import make_templates


# Immver davor: In line x you violated a convention/you made an error.

templates = {
        'C0103': make_templates('In python, there are naming conventions for the different types that you should pay attention to. For example, constants should be all in capital letters and use underscores, e.g. MAX_OVERFLOW.', 'You violated the naming convention for the %s name. Please change it according to the conventions.', []),
        'C0111': make_templates('You should specify what a %s does. This so-called documentation string includes for example the command line syntax, environment variables and files. You use triple quotes to start and end the description. The doc strings allows to be inspected by the programmer at run time which is very convenient.', 'Remember to include docstrings to document what your code does. Using docstrings will save you time and troubleshooting.', [1]),
        'C0301': make_templates('The is too long. You should limit all lines to a maximum of 79 characters according to the Python conventions. The limits are chosen to avoid wrapping in editors with the window width set to 80. Wrapping disrupts the visual structure of the code and makes it more difficult to understand.', 'You exceeded the recommended line length of 79 characters. For flowing long blocks of text with fewer structural restrictions such as docstrings or comments, the line length should be limited to 72 characters.', [3]),
        'C0202': make_templates('There is a class methods should always have cls as first name.', 'Always use cls for the first argument to class methods. The cls name is used to easily differentiate class methods from instance methods. Always use self for the first argument to instance methods.', [2]),
        'E0213': make_templates('There is instance method here is an instance method. Instance methods should always have self as first name. Note that by not following the convention your code may be less readable to other Python programmers.', 'The first argument of an instance method has to be called self. This is nothing more than a convention: the name self has absolutely no special meaning to Python.', []),
        'E0601': make_templates('You accessed a local variable before you assigned it.', 'You accessed a local variable before its assignment.', [2]),
        'E0602': make_templates('You used a variable that is undefined. Remember that you just have to use the equal sign to assign a value to a variable.', 'There is an undefined variable in this line. Always assign a variable before accessing it.', [2]),
        'E0104': make_templates('You wrote a "return" that is outside of its function. You might have to change the indentation of the return statement.', 'There is a return statement outside of a function.', []),
        'E0107': make_templates('You have used an operator which does not exist in Python. Remember that for example the operators -- and ++ from C cannot be used in Python. Use += or -= instead!', 'You used a non-existent operator in this line, possibly a wrong pre- or post-increment or decrement operator.', [4]),'E1102': make_templates('You accessed a non-callable object.','You accessed a non-callable object', [0]),
        #'E1121': Too many positional arguments for function call
                 }
