from collections import OrderedDict


class List(object):
    @staticmethod
    def unique(items: list) -> list:
        return list(OrderedDict.fromkeys(items))

    @staticmethod
    def exclude(items: list, excluded: list) -> list:
        for exclude in excluded:
            try:
                items.remove(exclude)
            except ValueError:
                pass

        return items
