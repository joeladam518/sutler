from collections import OrderedDict
from typing import Union

# ----------------------------------------------------------------------------------------------------------------------
# Public interface

ArrType = Union[list, tuple]


class Arr:
    @staticmethod
    def exclude(items: ArrType, _exclude: ArrType) -> ArrType:
        original_type = type(items)
        return original_type([item for item in items if item not in _exclude])

    @staticmethod
    def unique(items: ArrType) -> ArrType:
        original_type = type(items)
        return original_type(OrderedDict.fromkeys(items))
