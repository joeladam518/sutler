from typing import Union, Tuple


def versionize(version: Union[str, int, float, Tuple[int, int], Tuple[int, int, int]]) -> Tuple[int, int, int]:
    if isinstance(version, int):
        version = versionize_int(version)
    elif isinstance(version, float):
        version = versionize_float(version)
    elif isinstance(version, str):
        version = versionize_str(version)

    if len(version) >= 3:
        return int(version[0]), int(version[1]), int(version[2])

    if len(version) == 2:
        return int(version[0]), int(version[1]), 0

    if len(version) == 1:
        return int(version[0]), 0, 0

    return 0, 0, 0


def versionize_float(value: float) -> tuple:
    return versionize_str(str(value))


def versionize_int(value: int) -> tuple:
    return versionize_float(float(value))


def versionize_str(value: str) -> tuple:
    error_message = f'Can not convert "{value}" to a version.'

    if '.' not in value:
        try:
            return versionize_int(int(value))
        except ValueError:
            raise ValueError(error_message)

    string_list = []
    for val in value.split('.'):
        try:
            if '-' in val:
                val_parts = val.split('-')
                string_list.append(int(val_parts[0]))
            else:
                string_list.append(int(val))
        except ValueError:
            raise ValueError(error_message)

    return tuple(string_list)


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
