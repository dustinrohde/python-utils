from functools import partial

from .merge import merge


def setdefault(value, default, cls=None, merge_lists=False, merge_sets=False,
               merge_dicts=False, depth=1):
    """Transform ``value`` by applying some rules with ``default``.

    The following rules are applied:
        1. If ``value`` is None, return ``default``.
        2. If ``default`` is None, return ``value``.
        3. If ``merge_dicts`` is True, merge mapping types.
        4. If ``merge_lists`` is True, merge mutable sequence types.
        5. If ``merge_sets`` is True, merge set types.

    Args:
        value: The value to be transformed.
        default: The default value.
        cls (type): Desired return type. If possible, the transformed value
            will be returned as an instance of ``cls``. If is omitted or None,
            the return type will be the same as ``value``.
        merge_lists (bool): If ``value`` is a mutable sequence, concatenate
            and return ``default`` + ``value``.
        merge_sets (bool): If ``value`` is a set type, return its union with
            ``default``.
        merge_dicts (bool): If ``value`` is a mapping type, return ``value``
            plus any items from ``default`` whose keys are not in ``value``.
        depth (int): If ``merge_dicts`` is enabled, this sets the max depth
            of nested mappings that will be merged. If -1, no limit will be
            enforced.

    Attributes:
        setdefault.merge_all (function): Run with all merge flags enabled.
        setdefault.merge_dicts (function): Run with `merge_dicts` enabled.
        setdefault.merge_lists (function): Run with `merge_lists` enabled.
        setdefault.merge_sets (function): Run with `merge_sets` enabled.
    """
    if value is None:
        if cls:
            return cls(default)
        return default
    if default is None:
        if cls:
            return cls(value)
        return value

    if not cls:
        cls = type(value)

    if merge_dicts:
        return _setdefault_dict(value, default, cls)
    if merge_lists:
        return _setdefault_list(value, default, cls)
    if merge_sets:
        return _setdefault_set(value, default, cls)
    return value


def _setdefault_dict(value, default, cls):
    if issubclass(cls, Mapping):
        return merge_mappings(None, default, value, _type=cls)
    return value


def _setdefault_set(value, default, cls):
    if issubclass(cls, Set):
        return value | default
    return value


def _setdefault_list(value, default, cls):
    if issubclass(cls, MutableSequence):
        return cls(*default, *value)
    return value


def _setdefault_all(value, default, cls=None):
    """Call ``setdefault`` but transform set types and mutable sequences.

    Additional transformations:
    """
    return setdefault(value, default, cls, merge_dicts=True, merge_sets=True,
                      merge_lists=True)


setdefault.merge_all = _setdefault_all
setdefault.merge_dicts = partial(setdefault, merge_dicts=True)
setdefault.merge_lists = partial(setdefault, merge_lists=True)
setdefault.merge_sets = partial(setdefault, merge_sets=True)