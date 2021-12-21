import click
from ..application import App
from ..support import Run

node_versions = (
    '14',
    '15',
    '16',
    '17'
)


class NodeInstaller:
    @staticmethod
    def install(version: str):
        if version not in node_versions:
            click.ClickException('Invalid node version')

        app = App()
        if app.os_type() == 'debian':
            click.ClickException('Platform not supported.')

        Run.command(f"curl -sL \"https://deb.nodesource.com/setup_{version}.x\" | sudo -E bash -")
        Run.command("apt-get install -y nodejs", root=True)

    @staticmethod
    def uninstall():
        app = App()
        if app.os_type() != 'debian':
            click.ClickException('Operating system not supported.')

        Run.command("apt-get purge -y", 'nodejs', root=True)
        Run.command("apt-get --purge autoremove -y", root=True)
        # TODO: uninstall the apt-sources list
