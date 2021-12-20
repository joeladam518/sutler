from typing import Union, Tuple


def tuplize_float(value: float) -> tuple:
    return tuplize_str(str(value))


def tuplize_int(value: int) -> tuple:
    return tuplize_float(float(value))


def tuplize_str(value: str) -> tuple:
    try:
        if '.' in value:
            return tuple(map(lambda val: int(val), value.split('.')))
        else:
            return tuplize_int(int(value))
    except ValueError:
        raise ValueError(f'Can not convert "{value}" to a version.')


def versionize(version: Union[str, int, float, Tuple[int, int], Tuple[int, int, int]]) -> Tuple[int, int, int]:
    if isinstance(version, int):
        version = tuplize_int(version)
    elif isinstance(version, float):
        version = tuplize_float(version)
    elif isinstance(version, str):
        version = tuplize_str(version)

    if len(version) >= 3:
        return int(version[0]), int(version[1]), int(version[2])

    if len(version) == 2:
        return int(version[0]), int(version[1]), 0

    if len(version) == 1:
        return int(version[0]), 0, 0

    return 0, 0, 0


class Version:
    def __init__(self, a: Union[str, int, float, Tuple[int, int], Tuple[int, int, int]]):
        self.a = versionize(a)

    def compare(self, b: Union[str, int, float, Tuple[int, int], Tuple[int, int, int]]) -> int:
        b = versionize(b)

        if self.a == b:
            return 0

        return -1 if self.a < b else 1

    def eq(self, b: Union[str, int, float, Tuple[int, int], Tuple[int, int, int]]) -> bool:
        return self.a == versionize(b)

    def ne(self, b: Union[str, int, float, Tuple[int, int], Tuple[int, int, int]]) -> bool:
        return self.a != versionize(b)

    def lt(self, b: Union[str, int, float, Tuple[int, int], Tuple[int, int, int]]) -> bool:
        return self.a < versionize(b)

    def le(self, b: Union[str, int, float, Tuple[int, int], Tuple[int, int, int]]) -> bool:
        return self.a <= versionize(b)

    def gt(self, b: Union[str, int, float, Tuple[int, int], Tuple[int, int, int]]) -> bool:
        return self.a > versionize(b)

    def ge(self, b: Union[str, int, float, Tuple[int, int], Tuple[int, int, int]]) -> bool:
        return self.a >= versionize(b)

    def __eq__(self, other):
        if isinstance(other, Version):
            return self.a == other.a
        else:
            raise TypeError('Invalid type comparison.')

    def __ne__(self, other):
        if isinstance(other, Version):
            return self.a != other.a
        else:
            raise TypeError('Invalid type comparison.')

    def __lt__(self, other):
        if isinstance(other, Version):
            return self.a < other.a
        else:
            raise TypeError('Invalid type comparison.')

    def __le__(self, other):
        if isinstance(other, Version):
            return self.a <= other.a
        else:
            raise TypeError('Invalid type comparison.')

    def __gt__(self, other):
        if isinstance(other, Version):
            return self.a > other.a
        else:
            raise TypeError('Invalid type comparison.')

    def __ge__(self, other):
        if isinstance(other, Version):
            return self.a >= other.a
        else:
            raise TypeError('Invalid type comparison.')

    def __str__(self):
        return f"{self.a[0]}.{self.a[1]}.{self.a[2]}"

    def __repr__(self):
        return f"Version({self.a[0]}, {self.a[1]}, {self.a[2]})"
