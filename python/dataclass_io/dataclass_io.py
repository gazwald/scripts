from __future__ import annotations

import json
from dataclasses import Field, asdict, dataclass, fields, is_dataclass
from pathlib import Path
from types import GenericAlias
from typing import Any, Callable, ClassVar, Self, Union, get_args

__all__ = ["DataclassWithIO"]


@dataclass(
    init=False,
    repr=False,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=False,
    match_args=False,
    kw_only=False,
    slots=False,
    weakref_slot=False,
)
class DataclassWithIO:
    """
    Why not use Pydantic? Why not, indeed...
    Exceptions? Probably.
    Unhandled edge cases? Certainly.
    """

    _filter_function: ClassVar[Callable[[dict], dict]] | None = None

    @staticmethod
    def _from_dict_sub(field: Field, data: Any) -> Any | None:
        """
        Problems? Travel to the __future__.
        """

        def peel_the_onion(var) -> type | None:
            for utype in get_args(var):
                if you_are_my_type(utype):
                    return utype

        def you_are_my_type(var) -> bool:
            return is_dataclass(var) and hasattr(var, "from_dict")

        def you_are_a_list(args: tuple) -> bool:
            return (
                len(args) == 1
                and field_type is not None
                and field_type.__name__.startswith("list")
                and you_are_my_type(args[0])
            )

        def you_are_a_dict(args: tuple) -> bool:
            return (
                len(args) == 2
                and field_type is not None
                and field_type.__name__.startswith("dict")
                and you_are_my_type(args[1])
            )

        if not isinstance(data, (dict, list)):
            return data

        if isinstance(field.type, str):
            field_type = eval(field.type)  # YOLO
        elif isinstance(field.type, (type, GenericAlias)):
            field_type = field.type
        elif isinstance(field.type, Union):
            field_type = peel_the_onion(field.type)
        else:
            return data

        if isinstance(field_type, GenericAlias):
            args = get_args(field_type)
            if isinstance(data, list) and you_are_a_list(args):
                chosen_one = args[0]
                return [chosen_one.from_dict(element) for element in data]
            elif isinstance(data, dict) and you_are_a_dict(args):
                chosen_one = args[1]
                return {key: chosen_one.from_dict(value) for key, value in data.items()}
        elif field_type and you_are_my_type(field_type) and isinstance(data, dict):
            return field_type.from_dict(data)

        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self | None:
        return cls(
            **{
                field.name: cls._from_dict_sub(field, data[field.name])
                for field in fields(cls)
                if field.name in data.keys()
            }
        )

    def to_dict(self) -> dict:
        if self._filter_function:
            return self._filter_function(asdict(self))

        return asdict(self)

    @classmethod
    def from_path(cls, path: Path) -> Self | None:
        if not path.is_file() or not path.name.endswith("json"):
            return None

        try:
            data = json.loads(path.read_bytes())
        except:
            return None

        return cls.from_dict(data)

    def to_path(self, path: Path, overwrite: bool = True) -> None:
        if path.is_file() and overwrite is False:
            return None

        try:
            with open(path, "w") as handle:
                json.dump(self.to_dict(), handle)
        except:
            pass
