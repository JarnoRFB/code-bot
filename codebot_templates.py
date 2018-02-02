from template import make_templates


# Immer davor: In line x, you..."

templates = {
        'C0103': make_templates('should pay attention to the naming conventions for the different types in python. For example, constants should be all in capital letters and use underscores, e.g. MAX_OVERFLOW.', 'violated the naming convention for the %s name. Please change it according to the conventions.', []),
        'C0111': make_templates('should specify what a %s does. This so-called documentation string includes for example the command line syntax, environment variables and files. You use triple quotes to start and end the description. The doc strings allows to be inspected by the programmer at run time which is very convenient.', 'should remember to include docstrings to document what your code does. Using docstrings will save you time and troubleshooting.', [1]),
        'C0301': make_templates('should limit the line length to a maximum of 79 characters according to the Python conventions. The limits are chosen to avoid wrapping in editors with the window width set to 80. Wrapping disrupts the visual structure of the code and makes it more difficult to understand.', 'exceeded the recommended line length of 79 characters. For flowing long blocks of text with fewer structural restrictions such as docstrings or comments, the line length should be limited to 72 characters.', [3]),
        'C0202': make_templates('should always have cls as first name in a class method', 'should always use cls for the first argument to class methods. The cls name is used to easily differentiate class methods from instance methods, which use self as the first argument to instance methods.', [2]),
        'E0213': make_templates('should always have self as first name. Note that by not following the convention your code may be less readable to other Python programmers.', 'should call fhe first argument of the instance method ''self''. This is nothing more than a convention: the name self has absolutely no special meaning to Python.', []),
        'E0601': make_templates('accessed a local variable before you assigned it.', 'You accessed a local variable before its assignment.', [2]),
        'E0602': make_templates('used the variable %s that is undefined. Remember that you just have to use the equal sign to assign a value to a variable.', 'used an undefined variable. Always assign a variable before accessing it.', [2]),
        'E0104': make_templates('wrote a "return" that is outside of its function. You might have to change the indentation of the return statement.', 'used a return statement outside of a function.', []),
        'E0107': make_templates('have used an operator which does not exist in Python. Remember that for example the operators -- and ++ cannot be used in Python. Use += or -= instead!', 'used a non-existent operator in this line, possibly a wrong pre- or post-increment or decrement operator.', [4]),
        'E1102': make_templates('accessed a non-callable object.','accessed a non-callable object', [0]),
        'E0211': make_templates('should use ''self'' as the first argument to instance methods and ''cls'' as first argument to class methods. The first argument of a method in Python must always be the object on which the method is invoked. .', 'forgot to define an argument for a method. Remember that the bound instance is always the first argument.', []),
                 }
