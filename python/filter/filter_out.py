from __future__ import annotations

from typing import AbstractSet, Mapping, NamedTuple, Sequence, overload

__all__ = [
    "FilterConfig",
    "filter_map",
    "filter_seq",
    "filter_out",
]


class FilterConfig(NamedTuple):
    allow_empty_string: bool = False
    allow_empty_map: bool = False
    allow_empty_seq: bool = False


def filter_map(data: Mapping, config: FilterConfig) -> Mapping | None:
    new_map = {}
    for key, original_value in data.items():
        if original_value is None:
            continue

        checked_value = filter_out(original_value, config)

        if checked_value is None:
            continue

        new_map[key] = checked_value

    if len(new_map.keys()) == 0 and not config.allow_empty_map:
        return None

    return new_map


@overload
def filter_seq(data: Sequence, config) -> Sequence | None: ...
@overload
def filter_seq(data: AbstractSet, config) -> AbstractSet | None: ...


def filter_seq(data, config: FilterConfig):
    new_list = []
    for original_value in data:
        if original_value is None:
            continue

        checked_value = filter_out(original_value, config)

        if checked_value is None:
            continue

        new_list.append(checked_value)

    if len(new_list) == 0 and not config.allow_empty_seq:
        return None

    return type(data)(new_list)


@overload
def filter_out(data: None, config: FilterConfig | None = None) -> None: ...
@overload
def filter_out(data: str | bytes, config: FilterConfig | None = None) -> str | bytes | None: ...
@overload
def filter_out(data: int | float, config: FilterConfig | None = None) -> int | float: ...
@overload
def filter_out(data: Mapping, config: FilterConfig | None = None) -> Mapping | None: ...
@overload
def filter_out(data: Sequence, config: FilterConfig | None = None) -> Sequence | None: ...
@overload
def filter_out(data: AbstractSet, config: FilterConfig | None = None) -> AbstractSet | None: ...


def filter_out(data, config: FilterConfig | None = None):
    """
    Filter out unwanted values
    """
    if data is None or isinstance(data, (int, float)):
        return data

    if config is None:
        config = FilterConfig()

    if isinstance(data, (str, bytes)):
        if not data.strip() and not config.allow_empty_string:
            return None

        return data

    if isinstance(data, Mapping):
        return filter_map(data, config)

    if isinstance(data, (Sequence, AbstractSet)):
        return filter_seq(data, config)
