# safetypes package
Python is a non typed language, and runs under the paradigm of *first try and then it success or fails*.
This package allows you to have the capability of apply **typing** features in last versions of Python,
allowing to the developer to have a transparent mechanism to grant that typing annotations are
satisfied in the execution time of their programs.

To use this package you only need to add an annotation before a function or method definition:
```python
@safe_types
def my_func(test: str) -> int:
    ...
```
With this simple line when you run your program the annotation checks:

1. The **test** argument satisfies the condition to be a **str**.
2. The **return value** satisfies the condition to be an **int**.

Also, you can use the *Typing package* to have multiple types for the same argument or to extend
the detail of typing your code::
```python
from typing import Union

@safe_types
def my_func(test: Union[int, float]) -> Union[int, float]:
    ...
```
With this definition, the annotation checks if **test** argument and **return value**
are one of two possible types: **int** and **float**. Note that not necessarily needs to be the
same type in both cases, due to the annotation could not correlate a direct causality
between arguments and return types.

If you have optional arguments, like this one:
```python
@safe_types
def my_func(test: str = 'empty') -> None:
    ...

my_func()
```
Then the **test** argument is ignored if it is not used when you call the function.

If you want to accept unknown arguments using ***args** or ****kwargs** then you can use the non-strict
validation as follows:
```python
@safe_types(strict=False)
def my_func(test: str, *args, **kwargs) -> None:
    ...

my_func('yeah!', 'more... yeah!!', yeah='Not enough!!!')
```
In this case, the argument **test** will be checked but other parameters passed as additional and unknown
arguments will be ignored and not checked.