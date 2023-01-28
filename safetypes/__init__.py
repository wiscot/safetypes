from typing import Callable

from safetypes.base.SafeFiles import SafeTypes


def safe_types(
        wrapped: Callable or None = None,
        only_debug: bool = True,
        strict: bool = True,
        args_alias: str = 'args',
        kwargs_alias: str = 'kwargs'
):
    """
    Decorator function to validate typing in function calls. Raises a TypeError exception if types does not match.
    :param wrapped: Wrapped object.
    :param only_debug: If true only check types when python runs in debug mode.
    :param strict: If True only declared arguments are evaluated and other arguments raises an error. If false, then
    undeclared arguments are considered as variable and unknown arguments and all of them are accepted as is.
    :param args_alias: If strict is True then this is the alias for the *args argument.
    :param kwargs_alias: If strict is True then this is the alias for the *kwargs argument.
    :return: Returns the wrapper function if validation is successful.
    """
    def _decorator(func: Callable or None):
        safe = SafeTypes(func, only_debug=only_debug, strict=strict, args_alias=args_alias, kwargs_alias=kwargs_alias)
        return safe.wrapper

    return _decorator(wrapped) if callable(wrapped) else _decorator
