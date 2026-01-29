from dataclasses import dataclass, field
from typing import Optional

import pytest

from .dataclass_io import DataclassWithIO

# TODO:
#   Union
#   Optional

SAMPLE_DATA: dict[str, dict] = {
    "ExampleSimple": {
        "example_str": "example_str",
        "example_int": 1,
        "example_bool": True,
        "example_list": "example_list",
        "example_dict": "example_dict",
    },
    "ExampleSimpleField": {
        "example_str_field": "example_str",
        "example_int_field": None,
        "example_bool_field": True,
        "example_list_field": "example_list",
        "example_dict_field": "example_dict",
    },
    "ExampleSimpleUnion": {
        "example_union_str": "example_str",
        "example_union_int": 1,
        "example_union_bool": True,
        "example_union_list": "example_list",
        "example_union_dict": "example_dict",
        "example_optional_str": "example_str",
        "example_optional_int": 1,
        "example_optional_bool": True,
        "example_optional_list": "example_list",
        "example_optional_dict": "example_dict",
    },
    "ExampleNestedChild1": {
        "example_str": "example_str_1",
        "example_int": 1,
    },
    "ExampleNestedChild2": {
        "example_str": "example_str_2",
        "example_int": 2,
    },
    "ExampleNestedParent": {
        "example_nested_simple": {
            "example_str": "example_str_1",
            "example_int": 1,
        },
        "example_nested_union": {
            "example_str": "example_str_1",
            "example_int": 1,
        },
        "example_nested_optional": {
            "example_str": "example_str_1",
            "example_int": 1,
        },
        "example_list": [
            {
                "example_str": "example_str_1",
                "example_int": 1,
            },
            {
                "example_str": "example_str_2",
                "example_int": 2,
            },
        ],
    },
}


@dataclass
class ExampleSimple(DataclassWithIO):
    example_str: str
    example_int: int
    example_bool: bool
    example_list: list
    example_dict: dict


@dataclass
class ExampleSimpleField(DataclassWithIO):
    example_str_field: str = field(default="default_str")
    example_int_field: int = field(default=2)
    example_bool_field: bool = field(default=False)
    example_list_field: list = field(default_factory=list)
    example_dict_field: dict = field(default_factory=dict)


@dataclass
class ExampleSimpleUnion(DataclassWithIO):
    example_union_str: str | None = None
    example_union_int: int | None = None
    example_union_bool: bool | None = None
    example_union_list: list | None = None
    example_union_dict: dict | None = None
    example_optional_str: Optional[str] = None
    example_optional_int: Optional[int] = None
    example_optional_bool: Optional[bool] = None
    example_optional_list: Optional[list] = None
    example_optional_dict: Optional[dict] = None


@dataclass
class ExampleNestedChild(DataclassWithIO):
    example_str: str
    example_int: int


@dataclass
class ExampleNestedParent(DataclassWithIO):
    example_nested_simple: ExampleNestedChild
    example_nested_union: ExampleNestedChild | None
    example_nested_optional: Optional[ExampleNestedChild]
    example_list: list[ExampleNestedChild] = field(default_factory=list)


TESTS = [
    pytest.param(
        SAMPLE_DATA["ExampleSimple"],
        ExampleSimple,
        ExampleSimple(**SAMPLE_DATA["ExampleSimple"]),
        id="ExampleSimple",
    ),
    pytest.param(
        SAMPLE_DATA["ExampleSimpleField"],
        ExampleSimpleField,
        ExampleSimpleField(**SAMPLE_DATA["ExampleSimpleField"]),
        id="ExampleSimpleField",
    ),
    pytest.param(
        SAMPLE_DATA["ExampleSimpleUnion"],
        ExampleSimpleUnion,
        ExampleSimpleUnion(**SAMPLE_DATA["ExampleSimpleUnion"]),
        id="ExampleSimpleUnion",
    ),
    pytest.param(
        SAMPLE_DATA["ExampleNestedParent"],
        ExampleNestedParent,
        ExampleNestedParent(
            example_nested_simple=ExampleNestedChild(**SAMPLE_DATA["ExampleNestedChild1"]),
            example_nested_union=ExampleNestedChild(**SAMPLE_DATA["ExampleNestedChild1"]),
            example_nested_optional=ExampleNestedChild(**SAMPLE_DATA["ExampleNestedChild1"]),
            example_list=[
                ExampleNestedChild(**SAMPLE_DATA["ExampleNestedChild1"]),
                ExampleNestedChild(**SAMPLE_DATA["ExampleNestedChild2"]),
            ],
        ),
        id="ExampleNested",
    ),
]


@pytest.mark.parametrize(("data", "object_class", "expected"), TESTS)
def test_from_dict(data, object_class, expected):
    assert object_class.from_dict(data) == expected


@pytest.mark.parametrize(("expected", "object_class", "class_instance"), TESTS)
def test_to_dict(expected, object_class, class_instance):
    assert class_instance.to_dict() == expected
