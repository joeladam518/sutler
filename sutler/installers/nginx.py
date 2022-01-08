import click
import os
from ..application import Run
from .installer import Installer


class NginxInstaller(Installer):
    def install(self) -> None:
        Run.update()
        Run.install('nginx')

        # Run.command("ufw allow 'Nginx HTTP'", root=True)
        # Run.command("ufw allow 'Nginx HTTPS'", root=True)
        # click.echo()
        # click.echo('Checking ufw status:')
        # Run.command("ufw status", root=True)
        # click.echo()

        Run.command('systemctl stop nginx', root=True)

        nginx_conf_path = os.path.join(os.sep, 'etc', 'nginx', 'nginx.conf')
        if os.path.exists(nginx_conf_path):
            Run.command(f'mv {nginx_conf_path} {nginx_conf_path}.old', root=True)
        self.app.render_file(
            os.path.join('nginx', 'nginx.conf.jinja2'),
            nginx_conf_path
        )

    def uninstall(self) -> None:
        Run.uninstall('nginx')
