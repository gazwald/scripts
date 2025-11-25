import pytest

from main import _loop_detect


@pytest.mark.parametrize(
    ("data", "window_min", "expected"),
    [
        pytest.param([1, 2, 3, 4, 5], 1, None, id="NonSeqWin1"),
        pytest.param([1, 2, 3, 4, 5], 2, None, id="NonSeqWin2"),
        pytest.param([1, 2, 3, 4, 5], 3, None, id="NonSeqWin3"),
        pytest.param([1, 2, 3, 4, 5], 4, None, id="NonSeqWin4"),
        pytest.param([1, 2, 3, 4, 5], 5, None, id="NonSeqWin5"),
        pytest.param([1, 2, 1, 2], 2, 2, id="2SeqWin2"),
        pytest.param([1, 2, 1, 2], 3, None, id="2SeqWin3"),
        pytest.param([1, 2, 1, 2], 4, None, id="2SeqWin4"),
        pytest.param([1, 2, 3, 1, 2, 3], 2, 3, id="3SeqWin2"),
        pytest.param([1, 2, 3, 1, 2, 3], 3, 3, id="3SeqWin3"),
        pytest.param([1, 2, 3, 1, 2, 3], 4, None, id="3SeqWin4"),
        pytest.param([1, 2, 3, 4, 1, 2, 3, 4], 2, 4, id="4SeqWin2"),
        pytest.param([1, 2, 3, 4, 1, 2, 3, 4], 3, 4, id="4SeqWin3"),
        pytest.param([1, 2, 3, 4, 1, 2, 3, 4], 4, 4, id="4SeqWin4"),
        pytest.param([1, 2, 3, 4, 5, 1, 2, 3, 4, 5], 2, 5, id="5SeqWin2"),
        pytest.param([1, 2, 3, 4, 5, 1, 2, 3, 4, 5], 3, 5, id="5SeqWin3"),
        pytest.param([1, 2, 3, 4, 5, 1, 2, 3, 4, 5], 4, 5, id="5SeqWin4"),
        pytest.param([1, 2, 3, 4, 5, 1, 2, 3, 4, 5], 5, 5, id="5SeqWin5"),
        pytest.param([1, 2, 3, 4, 5, 1, 2, 3, 4, 5], 6, None, id="5SeqWin6"),
    ],
)
def test_loop_detect(data: list[int], window_min: int, expected: int | None):
    assert _loop_detect(data, window_min) == expected
