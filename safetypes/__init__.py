from typing import Callable

from safetypes.base.SafeFiles import SafeTypes


def safe_types(wrapped: Callable or None = None, only_debug: bool = True):
    """
    Decorator function to validate typing in function calls. Raises a TypeError exception if types does not match.
    :param wrapped: Wrapped object.
    :param only_debug: If true only check types when python runs in debug mode.
    :return: Returns the wrapper function if validation is successful.
    """
    def _decorator(func: Callable or None):
        safe = SafeTypes(func, only_debug=only_debug)
        return safe.wrapper

    return _decorator(wrapped) if callable(wrapped) else _decorator
