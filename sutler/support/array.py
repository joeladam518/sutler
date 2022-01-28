from collections import OrderedDict
from typing import Union

ArrType = Union[list, tuple]


class Arr:
    @staticmethod
    def exclude(items: ArrType, exclude_: ArrType) -> ArrType:
        original_type = type(items)
        return original_type([item for item in items if item not in exclude_])

    @staticmethod
    def unique(items: ArrType) -> ArrType:
        original_type = type(items)
        return original_type(OrderedDict.fromkeys(items))
