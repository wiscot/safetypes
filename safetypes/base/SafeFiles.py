import functools
import inspect
import sys
import types
import typing

from safetypes.base.SafeFunctionTypes import SafeFunctionTypes


class SafeTypes:

    def __init__(self, wrapped,
                 only_debug: bool = True,
                 strict: bool = True,
                 args_alias: str = 'args',
                 kwargs_alias: str = 'kwargs'
                 ):

        assert callable(wrapped) or wrapped is None
        assert type(only_debug) is bool

        self._wrapped = wrapped
        self._only_debug = only_debug
        self._strict = strict
        self._args_alias = args_alias
        self._kwargs_alias = kwargs_alias

        signature = inspect.signature(wrapped)
        parameter_values = signature.parameters.values()
        self._parameter_names = tuple(
            parameter.name
            for parameter in parameter_values
            if parameter.name != self._args_alias and parameter.name != self._kwargs_alias
        )
        self._parameter_types = tuple(
            self._replace(parameter.annotation, parameter.empty, object)
            for parameter in parameter_values
            if parameter.name != self._args_alias and parameter.name != self._kwargs_alias
        )
        self._parameter_def = tuple(
            parameter.default is not parameter.empty
            for parameter in parameter_values
            if parameter.name != self._args_alias and parameter.name != self._kwargs_alias
        )
        self._return_type = self._replace(signature.return_annotation, signature.empty, object)

        if (wrapped.__qualname__ == wrapped.__name__) or ('.<locals>' in wrapped.__qualname__):
            self._module_name = wrapped.__module__
            self._class_obj = None
            self._class_name = None
            self._func_name = wrapped.__name__
            self._func_type = SafeFunctionTypes.FUNCTION
        else:
            self._module_name = wrapped.__module__
            self._class_obj = None
            p = wrapped.__qualname__.rfind('.')
            self._class_name = wrapped.__qualname__[:p]
            self._func_name = wrapped.__qualname__[p + 1:]
            self._func_type = SafeFunctionTypes.UNKNOWN

        @functools.wraps(wrapped)
        def hook_wrapper(*args, **kwargs):
            try:
                return self._ghost_wrapper(*args, **kwargs)
            except TypeError as te:
                traceback = te.__traceback__
                message = str(te)

            if traceback is not None:
                back_frame = traceback.tb_frame.f_back
                back_tb = types.TracebackType(tb_next=None, tb_frame=back_frame, tb_lasti=back_frame.f_lasti,
                                              tb_lineno=back_frame.f_lineno)
                raise TypeError(message).with_traceback(back_tb)

        self.wrapper = hook_wrapper

    @staticmethod
    def _replace(obj, old, new):
        return new if obj is old else obj

    @staticmethod
    def _get_full_name(argument):
        return '.'.join([argument.__module__, argument.__qualname__]) \
            if argument.__module__ != 'builtins' else argument.__qualname__

    @staticmethod
    def _get_types_list(class_type):
        return sorted([SafeTypes._get_full_name(x) for x in list(class_type.__args__) if x.__name__ != 'NoneType'])

    @staticmethod
    def _raise_error(argument, parameter_type, parameter_name):
        if type(parameter_type) in [typing.Type, typing._UnionGenericAlias]:
            valid_types = SafeTypes._get_types_list(parameter_type)

            if NoneType in parameter_type.__args__:
                raise TypeError(f'{parameter_name} should be of types '
                                f'{", ".join(valid_types)} '
                                f'or None, not '
                                f'{SafeTypes._get_full_name(type(argument))}')
            elif len(valid_types) > 1:
                raise TypeError(f'{parameter_name} should be of types '
                                f'{", ".join(valid_types)}, not '
                                f'{SafeTypes._get_full_name(type(argument))}')
            else:
                raise TypeError(f'{parameter_name} should be of type '
                                f'{valid_types[0]}, not '
                                f'{SafeTypes._get_full_name(type(argument))}')
        elif type(parameter_type) in [typing._GenericAlias]:
            valid_types = SafeTypes._get_types_list(parameter_type)
            raise TypeError(f'{parameter_name} should be of type '
                            f'{valid_types[0]}, not '
                            f'{SafeTypes._get_full_name(type(argument))}')
        else:
            raise TypeError(f'{parameter_name} should be of type '
                            f'{SafeTypes._get_full_name(parameter_type)}, not '
                            f'{SafeTypes._get_full_name(type(argument))}')

    def _introspect_wrapped_type(self):
        self._class_obj = getattr(sys.modules[self._module_name], self._class_name)
        ftype = self._class_obj.__dict__[self._func_name].__class__.__name__
        if ftype == 'staticmethod':
            self._func_type = SafeFunctionTypes.STATIC_METHOD
        elif ftype == 'classmethod':
            self._func_type = SafeFunctionTypes.CLASS_METHOD
        elif ftype == 'function':
            self._func_type = SafeFunctionTypes.INSTANCE_METHOD
        else:
            raise TypeError(f"Unknown Class Function Type {ftype}")

    @staticmethod
    def _evaluate(argument, parameter_type, parameter_name) -> bool:

        if type(parameter_type) is type:
            if type(argument) is type:
                if not issubclass(argument, parameter_type):
                    SafeTypes._raise_error(argument, parameter_type, parameter_name)
            elif not isinstance(argument, parameter_type):
                SafeTypes._raise_error(argument, parameter_type, parameter_name)

        elif type(parameter_type) in [typing._UnionGenericAlias, typing._GenericAlias, typing.Type]:
            if type(argument) is type:
                if not issubclass(argument, parameter_type.__args__):
                    SafeTypes._raise_error(argument, parameter_type, parameter_name)
            elif not isinstance(argument, parameter_type.__args__):
                SafeTypes._raise_error(argument, parameter_type, parameter_name)
        else:
            if not isinstance(argument, parameter_type):
                SafeTypes._raise_error(argument, parameter_type, parameter_name)

        return True

    def _ghost_wrapper(self, *arguments, **kwarguments):

        if self._func_type is SafeFunctionTypes.UNKNOWN:
            self._introspect_wrapped_type()

        if self._func_type == SafeFunctionTypes.INSTANCE_METHOD:
            if len(arguments) < 1 or (not isinstance(arguments[0], self._class_obj)):
                raise TypeError(f'For instance methods, the first parameter is required and must be '
                                f'an instance of the {".".join([self._module_name, self._class_name])} class '
                                f'or a class that inherits from it.')

        elif self._func_type == SafeFunctionTypes.CLASS_METHOD:
            if len(arguments) < 1 or (not type((arguments[0]) is type)) or (not issubclass(arguments[0], self._class_obj)):
                raise TypeError(f'For class methods, the first parameter is required and must be '
                                f'the class '
                                f'{".".join([self._module_name, self._class_name])} or a descendant class.')

        if self._strict and len(arguments) > len(self._parameter_names):
            raise TypeError(f'They are more unnamed arguments than expected.')

        used_args = []
        for argument, parameter_type, parameter_name in zip(
                arguments, self._parameter_types, self._parameter_names
        ):
            SafeTypes._evaluate(argument, parameter_type, parameter_name)
            used_args.append(parameter_name)

        for parameter_name, argument in dict(**kwarguments).items():
            if parameter_name in self._parameter_names:
                parameter_type = self._parameter_types[self._parameter_names.index(parameter_name)]
                SafeTypes._evaluate(argument, parameter_type, parameter_name)
                used_args.append(parameter_name)
            elif self._strict:
                raise TypeError(f"Unexpected parameter {parameter_name}.")

        unused_args = list(set(self._parameter_names) - set(used_args))
        if len(unused_args) > 0:
            for named in unused_args:
                if not self._parameter_def[self._parameter_names.index(named)]:
                    raise TypeError(f"Mandatory parameter {named} not found.")

        result = self._wrapped(*arguments, **kwarguments)
        SafeTypes._evaluate(result, self._return_type, 'return')

        return result
