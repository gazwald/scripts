def _loop_detect(data: list, window_min: int = 3) -> int | None:
    if window_min <= 1:
        return None

    length: int = len(data)
    length_half: int = length // 2

    if length <= 1:
        return None

    if length % 2 == 0 and length_half >= window_min:
        left = data[:length_half]
        right = data[length_half:]
        if left == right:
            return length_half

    while window_min <= (length_half - 1):
        start = window_min * -1
        tail = data[start:]
        part = data[start * 2 : start]
        if part == tail:
            return window_min
        window_min += 1

    return None
