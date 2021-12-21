import re


class Str:
    @staticmethod
    def camel(value: str) -> str:
        value = re.sub('([A-Z]+)', r' \1', value)
        value = re.sub(r"(_|-)+", " ", value).title().replace(" ", "")
        return ''.join([value[0].lower(), value[1:]])

    @staticmethod
    def snake(value: str) -> str:
        value = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', re.sub(r"(_|-)+", " ", value))).split()
        return '_'.join(value).lower()
