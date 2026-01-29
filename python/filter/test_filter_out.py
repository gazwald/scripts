import pytest

from .filter_out import FilterConfig, filter_map, filter_out, filter_seq

default_config = FilterConfig()


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param({}, None, id="empty-dict"),
        pytest.param({"hello": "world", "goodbye": None}, {"hello": "world"}, id="key-removed"),
    ],
)
def test_filter_map(data, expected):
    assert filter_map(data, default_config) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param(list(), None, id="list-empty"),
        pytest.param(tuple(), None, id="tuple-empty"),
        pytest.param(set(), None, id="set-empty"),
        pytest.param([None], None, id="list-none"),
        pytest.param((None,), None, id="tuple-none"),
        pytest.param({None}, None, id="set-none"),
        pytest.param(["hello", "world", None], ["hello", "world"], id="list"),
        pytest.param(("hello", "world", None), ("hello", "world"), id="tuple"),
        pytest.param({"hello", "world", None}, {"hello", "world"}, id="set"),
    ],
)
def test_filter_seq(data, expected):
    assert filter_seq(data, default_config) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param("hello", "hello", id="string"),
        pytest.param(b"hello", b"hello", id="bytes"),
        pytest.param(" ", None, id="string-empty"),
        pytest.param(b" ", None, id="bytes-empty"),
        pytest.param(None, None, id="none"),
        pytest.param(True, True, id="bool-true"),
        pytest.param(False, False, id="bool-false"),
        pytest.param(1, 1, id="int"),
        pytest.param(1.0, 1.0, id="float"),
        pytest.param(
            {
                "string": "hello",
                "empty_string": " ",
                "bytes": b"hello",
                "empty_bytes": b" ",
                "number": 1,
                "none": None,
                "bool": True,
            },
            {
                "string": "hello",
                "bytes": b"hello",
                "number": 1,
                "bool": True,
            },
            id="dict-simple",
        ),
        pytest.param(
            {
                "dict": {"hello": "world", "goodbye": None},
                "list": ["hello", "world", None],
                "set": {"hello", "world", None},
            },
            {
                "dict": {"hello": "world"},
                "list": ["hello", "world"],
                "set": {"hello", "world"},
            },
            id="dict-complex",
        ),
    ],
)
def test_filter_out(data, expected):
    assert filter_out(data) == expected
