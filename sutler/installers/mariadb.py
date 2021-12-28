import click
import os
from ..application import Run
from .installer import Installer


class MariadbInstaller(Installer):
    def install(self) -> None:
        Run.install('mariadb-server', 'mariadb-client')

        # Setup Mariadb to support utf-8
        src_path = self.app.templates_path('mysql', 'utf8.conf')
        dst_path = os.path.join('/etc', 'mysql', 'conf.d', 'utf8.conf')
        Run.command(f'cp "{src_path}" "{dst_path}"', root=True)

        # Secure the install
        click.echo()
        Run.command('mysql_secure_installation', root=True)
        click.echo()

        if not click.confirm('Do you want to create a new database right now?', default=None):
            # We're done!
            return

        click.echo()
        db_root_password = click.prompt('What is you mariadb root password?')
        db_name = click.prompt("The name of the new db?")
        db_user = click.prompt("The name of the db's primary user?")
        db_user_password = click.prompt('Their intended password?')

        # TODO: create a new database

    def uninstall(self) -> None:
        Run.uninstall('mariadb-server', 'mariadb-client')

        utf8_conf_path = os.path.join('/etc', 'mysql', 'conf.d', 'utf8.conf')
        if os.path.exists(utf8_conf_path):
            Run.command(f'rm "{utf8_conf_path}"', root=True)
