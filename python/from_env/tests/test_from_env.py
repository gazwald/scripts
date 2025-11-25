import os
from unittest import mock

import pytest

from from_env import from_env


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(
        os.environ,
        {
            "EXAMPLE_STR": "pytest.localdomain",
            "EXAMPLE_INT": "27910",
            "EXAMPLE_BOOL_TRUE": "true",
            "EXAMPLE_BOOL_FALSE": "FALSE",
            "EXAMPLE_BOOL_YES": "YES",
            "EXAMPLE_BOOL_NOT_BOOL": "NOT_BOOL",
        },
    ):
        yield


@pytest.mark.parametrize(
    ("env_string", "default", "return_type", "expected"),
    [
        pytest.param("EXAMPLE_STR", "missing.localdomain", str, "pytest.localdomain"),
        pytest.param("EXAMPLE_STR_MISSING", "missing.localdomain", str, "missing.localdomain"),
        pytest.param("EXAMPLE_INT", 27910, int, 27910),
        pytest.param("EXAMPLE_INT_MISSING", 27910, int, 27910),
        pytest.param("EXAMPLE_BOOL_YES", True, bool, True),
        pytest.param("EXAMPLE_BOOL_TRUE", True, bool, True),
        pytest.param("EXAMPLE_BOOL_FALSE", False, bool, False),
        pytest.param("EXAMPLE_BOOL_NOT_BOOL", False, bool, False),
        pytest.param("EXAMPLE_BOOL_TRUE_MISSING", True, bool, True),
        pytest.param("EXAMPLE_BOOL_FALSE_MISSING", False, bool, False),
    ],
)
def test_from_env(env_string, default, return_type, expected):
    result = from_env(env_string, default, return_type)
    assert result == expected
    assert isinstance(result, return_type)
