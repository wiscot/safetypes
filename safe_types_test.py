from typing import Type

from safetypes import safe_types


@safe_types(only_debug=True)
def empty_function_without_typing():
    pass


@safe_types
def function_returning_value_without_typing():
    return 49.0


@safe_types
def function_returning_typed_value() -> float:
    return 49.0


@safe_types
def function_returning_invalid_typed_value() -> float:
    return 'dummy'


@safe_types
def function_with_one_parameter_without_typing(x):
    pass


@safe_types
def function_with_one_typed_parameter(x: float):
    pass


@safe_types
def function_with_one_typing_parameter(x: Type[str]):
    pass


class ClassMethodsTest:

    @safe_types
    def __init__(self):
        pass

    @staticmethod
    @safe_types
    def empty_static_method():
        pass

    @staticmethod
    @safe_types
    def one_typed_parameter_static_method(x: str):
        pass

    @safe_types
    def empty_instance_method(self):
        pass

    @classmethod
    @safe_types
    def empty_class_method(cls):
        pass


class ChildClassMethodsTest(ClassMethodsTest):
    pass


if __name__ == '__main__':
    empty_function_without_typing()
    function_returning_value_without_typing()
    function_returning_typed_value()
    try:
        function_returning_invalid_typed_value()
    except TypeError as te:
        print(te)
    function_with_one_parameter_without_typing(30)
    function_with_one_parameter_without_typing('dummy')
    function_with_one_parameter_without_typing(129.0)
    function_with_one_typed_parameter(48.45)
    try:
        function_with_one_typed_parameter('dummy')
    except TypeError as te:
        print(te)
    try:
        function_with_one_typed_parameter(85)
    except TypeError as te:
        print(te)
    function_with_one_typing_parameter('dummy')
    try:
        function_with_one_typing_parameter(91)
    except TypeError as te:
        print(te)

    cls = ClassMethodsTest()
    ClassMethodsTest.empty_static_method()
    cls.empty_static_method()
    try:
        cls.empty_static_method('dummy')
    except TypeError as te:
        print(te)

    ClassMethodsTest.one_typed_parameter_static_method('dummy')
    cls.one_typed_parameter_static_method('dummy')
    ClassMethodsTest.empty_instance_method(cls)
    cls.empty_instance_method()
    try:
        ClassMethodsTest.empty_instance_method()
    except TypeError as te:
        print(te)
    try:
        ClassMethodsTest.empty_instance_method(187)
    except TypeError as te:
        print(te)
    ClassMethodsTest.empty_instance_method(187)
    ClassMethodsTest.empty_class_method()

    ChildClassMethodsTest.empty_class_method()
