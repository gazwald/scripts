#!/usr/bin/env python
from enum import Enum
from typing import Any


class Status(Enum):
    SUCCESS = 1
    FAILURE = 2


def _fetch_from_index(
    index: int, path: list[str], data: list | tuple
) -> tuple[Any, Status]:
    left: Any = data[index]

    if path:
        return traverse(path, left)

    return left, Status.SUCCESS


def _find_in_array(path: list[str], data: list | tuple) -> tuple[Any, Status]:
    key: str = path.pop(0)

    for element in data:
        left, right = traverse(key, element)
        if right == Status.SUCCESS:
            return left, right

    return None, Status.FAILURE


def _traverse_array(path: list[str], data: list | tuple) -> tuple[Any, Status]:
    def _key_is_integer(key: str) -> bool:
        return key.isnumeric() and len(data) >= int(key)

    def _key_is_wild(key: str) -> bool:
        return key == "*"

    if path:
        key: str = path.pop(0)

        if _key_is_integer(key):
            return _fetch_from_index(int(key), path, data)

        if _key_is_wild(key):
            return _find_in_array(path, data)

    return None, Status.FAILURE


def _traverse_map(path: list[str], data: dict) -> tuple[Any, Status]:
    key: str = path.pop(0)

    if key in data:
        left = data[key]
        if path:
            return traverse(path, left)

        return left, Status.SUCCESS

    return None, Status.FAILURE


def traverse(path: str | list[str], data: Any) -> tuple[Any, Status]:
    """
    Use if you want both the value and whether the path exists
    """
    if isinstance(path, str):
        path = path.split(".")

    if path:
        if isinstance(data, dict):
            return _traverse_map(path, data)
        if isinstance(data, (list, tuple)):
            return _traverse_array(path, data)

    return None, Status.FAILURE


def get_value(path: str, data: Any) -> Any:
    """
    Convienience method.
    Use if you don't care if the path exists and just want a value
    """
    left, _ = traverse(path, data)
    return left


def path_exists(path: str, data: Any) -> Status:
    """
    Convienience method.
    Use if you only want to know that the path exists but don't care about the value
    """
    _, right = traverse(path, data)
    return right
