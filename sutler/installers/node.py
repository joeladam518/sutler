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
        app = App()
        if version not in node_versions:
            click.ClickException('Invalid node version')

        if app.os_type() == 'debian':
            Run.command(f"curl -sL \"https://deb.nodesource.com/setup_{version}.x\" | sudo -E bash -")
            Run.command("apt-get install -y nodejs", root=True)
        else:
            Run.command("apt-get install -y node", root=True)

    @staticmethod
    def uninstall():
        app = App()
        os_type = app.os_type()

        name = 'nodejs' if os_type == 'debian' else 'node'
        Run.command("apt-get purge -y", name, root=True)
        Run.command("apt-get --purge autoremove -y", root=True)

        if os_type == 'debian':
            click.echo('# TODO: uninstall the apt-sources list')
