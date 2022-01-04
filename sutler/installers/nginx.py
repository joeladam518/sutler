import click
from ..application import Run
from .installer import Installer


class NginxInstaller(Installer):
    def install(self) -> None:
        Run.update()
        Run.install('nginx')
        # Run.command("ufw allow 'Nginx HTTP'", root=True)
        # Run.command("ufw allow 'Nginx HTTPS'", root=True)

        click.echo()
        click.echo('Checking ufw status:')
        Run.command("ufw status", root=True)
        click.echo()

        Run.command('systemctl stop nginx', root=True)

    def uninstall(self) -> None:
        pass
