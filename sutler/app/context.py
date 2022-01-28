import click
from typing import Any


class Context:
    """ Object that acts like a dictionary """
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __getattr__(self, item):
        return None

    def __repr__(self):
        args = ['{}={}'.format(k, repr(v)) for k, v in vars(self).items()]
        return 'Context({})'.format(', '.join(args))

    def get(self, key: str, default: Any = None) -> Any:
        if not hasattr(self, key):
            return default

        attr = getattr(self, key, None)

        return default if callable(attr) else attr

    def print(self) -> None:
        items = vars(self).items()

        if len(items) == 0:
            click.secho("No context", fg='bright_white')
            return

        for key, value in items:
            if isinstance(value, dict):
                value = ', '.join(['{}={}'.format(k, repr(v)) for k, v in value.items()])
            elif isinstance(value, (list, tuple)):
                value = ', '.join(list(map(lambda val: str(val), value)))
            click.secho(f"{key}: ", nl=False, fg='bright_black')
            click.secho(f"{value}", fg='bright_white')

    def set(self, key: str, value: Any) -> None:
        setattr(self, key, value)
