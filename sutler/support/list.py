from collections import OrderedDict


class List:
    @staticmethod
    def only(items: list, excluded: list) -> list:
        for exclude in excluded:
            try:
                items.remove(exclude)
            except ValueError:
                pass

        return items

    @staticmethod
    def unique(items: list) -> list:
        return list(OrderedDict.fromkeys(items))
