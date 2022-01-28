import click
from typing import TYPE_CHECKING
from ..support import installed

if TYPE_CHECKING:
    from ..app import App


class UfwConfigurator:
    def __init__(self, app: 'App'):
        self.app: 'App' = app

    def http(self):
        if not installed('ufw'):
            self.app.os.install('ufw')

        self.app.os.exec("ufw allow ssh", root=True)
        self.app.os.exec("ufw allow 'Nginx HTTP'", root=True)

        click.echo()
        if click.confirm('Enable the firewall?', default=False):
            self.app.os.exec("ufw enable", root=True)
