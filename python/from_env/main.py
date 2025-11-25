from __future__ import annotations

import os
from functools import cache
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from typing import Callable


def str_to_bool(data: str) -> bool:
    return data.casefold().lower() in ("yes", "true")


@cache
def from_env[T](env_string: str, default: T, return_type: Callable[..., T]) -> T:
    env_value: str | None = os.getenv(env_string, None)
    if env_value is None:
        return default

    if return_type == bool:
        return cast(T, str_to_bool(env_value))

    return return_type(env_value)
