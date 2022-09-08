#################
safetypes package
#################
Python is a not typed language, and runs under the paradigm of *try and success or fails*.
This package allows you to have the capability of apply **typing** features in last versions of Python,
allowing to the programmer to have a transparent mechanism to grant that typing annotations are
satisfied in the execution time of their programs.

To use this package you only need to add an annotation before a function or method definition::

    @safetypes
    def my_func(test: str) -> int

With this simple line when you run your program the annotation checks:

#. The **test** argument satisfies the condition to be a **str**.
#. The **return value** satisfies the condition to be an **int**.

Also you can use the *Typing package* to have multiple types for the same argument or to extend
the detail of typing your code::

    from typing import Union
    @safetypes
    def my_func(test: Union[int, float]) -> Union[int, float]

With this definition, the annotation checks if **test** argument and **return value**
are one of two possible types: **int** and **float**. Note that not necessarily needs to be the
same type in both cases, due to the annotation could not correlate a direct causality
between arguments and return types.
