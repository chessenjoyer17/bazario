from collections.abc import Iterable
from typing import get_args, get_origin

ORIG_BASES = "__orig_bases__"


def extract_orig_bases(cls: type) -> Iterable:
    return getattr(cls, ORIG_BASES, ())


def extract_base_generic_type(cls: type) -> type | None:
    orig_bases = extract_orig_bases(cls)

    for orig_base in orig_bases:
        if get_origin(orig_base) is not None:
            return orig_base

    return None


def matches_generic_type(
    hint: type,
    base_generic: type,
    expected_arg: type,
) -> bool:
    """
    Checks whether the type `hint` is a generalized type
    derived from `base_generic` and whether it contains
    `expected_arg` as a type argument.
    """

    if get_origin(hint) is not base_generic:
        return False

    args = get_args(hint)

    return expected_arg in args
