"""
Built for fun, untested, do not use.
"""

import re
from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from pprint import pprint
from typing import TYPE_CHECKING, Callable, Final, Iterator, NamedTuple


class Position(Enum):
    minute = 0
    hour = 1
    day = 2
    month = 3
    weekday = 4


class ValueType(Enum):
    wild = auto()
    int = auto()
    list = auto()
    range = auto()


class Status(Enum):
    ok = 0
    error = 1


class Result(NamedTuple):
    status: Status
    value: int | tuple[int, ...] | None = None
    value_type: ValueType | None = None


class MinMax(NamedTuple):
    min: int
    max: int


ENUM_MONTHS: Final[dict[str, int]] = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}
ENUM_WEEKDAYS: Final[dict[str, int]] = {
    "sun": 0,
    "mon": 1,
    "tue": 2,
    "wed": 3,
    "thu": 4,
    "fri": 5,
    "sat": 6,
}

_limit_size: Callable[[int, int, int], bool] = lambda s, l, v: v >= s and v <= l
_limit_length: Callable[[int, int, tuple], bool] = lambda s, l, v: len(v) >= s and len(v) <= l

MIN_MAX: Final[dict[Position, MinMax]] = {
    Position(0): MinMax(0, 59),
    Position(1): MinMax(0, 23),
    Position(2): MinMax(1, 31),
    Position(3): MinMax(1, 12),
    Position(4): MinMax(0, 6),
}


def _inclusive_range(start: int, stop: int, step: int = 1) -> Iterator[int]:
    steps = (stop - start) // step

    yield start

    i = 0
    while i < steps:
        i += 1
        yield start + (step * i)


class TabValue(NamedTuple):
    value: int | tuple[int, ...] | None
    value_type: ValueType | None = None
    step: int | None = None
    status: Status = Status.ok
    source: str = ""

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, TabValue):
            return False

        return self.value == value.value

    def match(self, value: int) -> bool:
        if self.value is None:
            return True
        if isinstance(self.value, int):
            return value == self.value
        if isinstance(self.value, tuple):
            return value in self.value

        return False

    @classmethod
    def from_string(cls, position: Position, value: str) -> TabValue:
        if "/" in value:
            return cls._split_step(position, value)

        left = cls._split(position, value)

        return TabValue(
            value=left.value,
            value_type=left.value_type,
            step=None,
            status=left.status,
            source=value,
        )

    @classmethod
    def _split(cls, position: Position, value: str | None) -> Result:
        """
        None, '', '*' are wildcards, and in steps represent every nth value of that part
        """
        if value in (None, "", "*"):
            return Result(Status.ok, None, ValueType.wild)
        elif "," in value:
            return cls._split_sequence(value, ValueType.list)
        elif "-" in value:
            return cls._unpack_sequence(position, cls._split_sequence(value, ValueType.range))

        return cls._to_int(value)

    @classmethod
    def _split_step(cls, position: Position, value: str) -> TabValue:
        _left, _right = value.split("/")
        left, right = cls._split(position, _left), cls._to_int(_right)
        if left.status == Status.error or right.status == Status.error:
            status = Status.error
        else:
            status = Status.ok

        if TYPE_CHECKING:
            assert isinstance(right.value, int)

        left = cls._unpack_sequence(position, left, right.value)

        status = left.status if status == Status.ok else status.error

        return TabValue(
            value=left.value,
            value_type=left.value_type,
            step=right.value,
            status=status,
            source=value,
        )

    @staticmethod
    def _unpack_sequence(position: Position, left: Result, step: int = 1):
        if left.value is None:
            return Result(
                Status.ok,
                tuple(_inclusive_range(MIN_MAX[position].min, MIN_MAX[position].max, step)),
            )
        elif isinstance(left.value, int):
            return Result(
                Status.ok,
                tuple(
                    _inclusive_range(left.value, MIN_MAX[position].max, step),
                ),
            )
        elif isinstance(left.value, tuple) and len(left.value) == 2:
            return Result(
                Status.ok,
                tuple(_inclusive_range(*left.value, step)),
            )

        return Result(Status.error)

    @classmethod
    def _split_sequence(
        cls,
        value: str,
        value_type: ValueType,
    ) -> Result:
        match value_type:
            case ValueType.list:
                values = value.split(",")
            case ValueType.range:
                values = value.split("-")
            case _:
                return Result(Status.error)

        left: tuple[int, ...] = tuple(
            result.value
            for result in (cls._to_int(v) for v in values)
            if result.status == Status.ok and isinstance(result.value, int)
        )
        if len(left) == len(values):
            return Result(Status.ok, left, value_type)

        return Result(Status.error)

    @staticmethod
    def _to_int(value: str) -> Result:
        if value in ENUM_MONTHS.keys():
            return Result(Status.ok, ENUM_MONTHS[value], ValueType.int)
        if value in ENUM_WEEKDAYS.keys():
            return Result(Status.ok, ENUM_WEEKDAYS[value], ValueType.int)
        if not value.isnumeric():
            return Result(Status.error)

        return Result(Status.ok, int(value), ValueType.int)


class Tab(NamedTuple):
    minute: TabValue
    hour: TabValue
    day: TabValue
    month: TabValue
    weekday: TabValue

    @classmethod
    def from_string(cls, value: str) -> Tab:
        value = value.strip().casefold()
        if value in ENUM_ATS:
            return ENUM_ATS[value]
        values = tuple(
            TabValue.from_string(Position(pos), part)
            for pos, part in enumerate(filter(lambda x: x != "", re.split(r"\s+", value)))
        )
        return Tab(*values)

    @property
    def status(self) -> Status:
        if any(
            status == Status.error
            for status in (
                self.minute.status,
                self.hour.status,
                self.day.status,
                self.month.status,
                self.weekday.status,
            )
        ):
            return Status.error

        return Status.ok

    def match(self, now: datetime | None = None, tz: timezone = timezone.utc) -> bool:
        if now is None:
            now = datetime.now(tz)

        return all(
            (
                self.month.match(now.month),
                self.weekday.match(now.isoweekday()),
                self.day.match(now.day),
                self.hour.match(now.hour),
                self.minute.match(now.minute),
            )
        )

    def next(self, now: datetime | None = None, tz: timezone = timezone.utc) -> bool:
        if now is None:
            now = datetime.now(tz)

        return self.match(now + timedelta(minutes=1))


ENUM_ATS: Final[dict[str, Tab]] = {
    "@yearly": Tab(
        minute=TabValue(value=0),
        hour=TabValue(value=0),
        day=TabValue(value=1),
        month=TabValue(value=1),
        weekday=TabValue(value=None),
    ),
    "@montly": Tab(
        minute=TabValue(value=0),
        hour=TabValue(value=0),
        day=TabValue(value=1),
        month=TabValue(value=None),
        weekday=TabValue(value=None),
    ),
    "@weekly": Tab(
        minute=TabValue(value=0),
        hour=TabValue(value=0),
        day=TabValue(value=None),
        month=TabValue(value=None),
        weekday=TabValue(value=0),
    ),
    "@daily": Tab(
        minute=TabValue(value=0),
        hour=TabValue(value=0),
        day=TabValue(value=None),
        month=TabValue(value=None),
        weekday=TabValue(value=None),
    ),
    "@hourly": Tab(
        minute=TabValue(value=0),
        hour=TabValue(value=None),
        day=TabValue(value=None),
        month=TabValue(value=None),
        weekday=TabValue(value=None),
    ),
}


def print_enums():
    for clean, raw in (
        ("@yearly", "0 0 1 1 *"),
        ("@montly", "0 0 1 * *"),
        ("@weekly", "0 0 * * 0"),
        ("@daily", "0 0 * * *"),
        ("@hourly", "0 * * * *"),
    ):
        print(clean)
        print(Tab.from_string(raw) == ENUM_ATS[clean])


def print_str(datum: str, now: datetime):
    t = Tab.from_string(datum)
    print(datum)
    pprint(t._asdict(), width=40)
    print("Run now: ", t.match(now))
    print("Run next: ", t.next(now))


def main():
    now = datetime.now(tz=timezone.utc)

    for datum in (
        "5 4 * *  *",
        "0,2,3 9-11 3/4 JAN  WED",
        f"* {now.hour} * JUN {now.isoweekday()}",
        f"{now.minute} {now.hour} * JUN {now.isoweekday()}",
        f"{now.minute + 1} {now.hour} * JUN {now.isoweekday()}",
    ):
        print_str(datum, now)


if __name__ == "__main__":
    main()
