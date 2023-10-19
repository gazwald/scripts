from find_path import _fetch_from_index, Status
import pytest

data = [
    {"key1": "value1"},
    {"key2": "value2"},
    {"key3": "value3"},
    {"key4": "value4"},
]

@pytest.mark.parametrize(
    "index,path,data,expected",
    [
        pytest.param(
            1,
            [],
            data,
            ({"key2": "value2"}, Status.SUCCESS),
            id="SingleValue",
        ),
        pytest.param(
            2,
            ["key3"],
            data,
            ("value3", Status.SUCCESS),
            id="SingleValueWithPath",
        ),
        pytest.param(
            3,
            ["key5"],
            data,
            (None, Status.FAILURE),
            id="MissingValueWithPath",
        ),
    ],
)
def test_fetch_from_index(index: int, path: list[str], data: list | tuple, expected):
    result = _fetch_from_index(index, path, data)
    assert result == expected

