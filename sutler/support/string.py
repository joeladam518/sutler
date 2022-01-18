import re

ALLOWED_CHARS_PATTERN = re.compile(r'[^-a-z0-9]+')
DUPLICATE_DASH_PATTERN = re.compile(r'-{2,}')
NUMBERS_PATTERN = re.compile(r'(?<=\d),(?=\d)')
DEFAULT_SEPARATOR = '-'


class Str:
    @staticmethod
    def camel(value: str) -> str:
        value = re.sub('([A-Z]+)', r' \1', value)
        value = re.sub(r"(_|-)+", " ", value).title().replace(" ", "")
        return ''.join([value[0].lower(), value[1:]])

    @staticmethod
    def slug(text: str, separator: str = DEFAULT_SEPARATOR):
        # Convert all dashes/underscores into separator
        flip = '_' if separator == DEFAULT_SEPARATOR else DEFAULT_SEPARATOR
        text = re.sub(r'[\%s]' % flip, DEFAULT_SEPARATOR, text)

        # replace @ with at
        text = text.replace('@', f'{DEFAULT_SEPARATOR}at{DEFAULT_SEPARATOR}')

        # cleanup numbers
        text = NUMBERS_PATTERN.sub('', text)

        # lowercase
        text = text.lower()

        # replace all unwanted characters
        text = re.sub(ALLOWED_CHARS_PATTERN, DEFAULT_SEPARATOR, text)

        # remove redundant
        text = DUPLICATE_DASH_PATTERN.sub(DEFAULT_SEPARATOR, text).strip(DEFAULT_SEPARATOR)

        if separator != DEFAULT_SEPARATOR:
            text = text.replace(DEFAULT_SEPARATOR, separator)

        return text

    @staticmethod
    def snake(value: str) -> str:
        value = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', re.sub(r"(_|-)+", " ", value))).split()
        return '_'.join(value).lower()
