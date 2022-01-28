import click
import os
from typing import Optional
from ..configurators import MariadbConfigurator
from .installer import Installer


class MariadbInstaller(Installer):
    def install(self, db: Optional[str] = None, user: Optional[str] = None) -> None:
        self.app.os.install('mariadb-server', 'mariadb-client')
        click.echo()

        mariadb = MariadbConfigurator(self.app)

        # Secure the mariadb installation
        # self.app.systems.exec('mysql_secure_installation', root=True)
        mariadb.secure_installation()

        # Setup Mariadb to support utf-8
        source = self.app.templates_path('mysql', 'utf8.conf')
        destination = os.path.join(os.sep, 'etc', 'mysql', 'conf.d', '99-utf8.conf')
        self.app.os.cp(source, destination, root=True)

        # Create a database if we have the required information
        if db:
            if not user:
                click.echo()
                user = click.prompt(
                    f'Please provide a user for {db}',
                    type=str,
                    hide_input=False,
                    show_default=False,
                    default=None
                )
            click.echo()
            user_password = click.prompt(
                f"Enter {user}'s password",
                type=str,
                hide_input=True,
                confirmation_prompt=f"Confirm {user}'s password",
                show_default=False,
                default=None
            )
            mariadb.create_db(name=db)
            mariadb.create_user(username=user, password=user_password, db_name=db)

        click.echo()

    def uninstall(self) -> None:
        self.app.os.uninstall('mariadb-server', 'mariadb-client')

        # TODO: Should I just remove the entire 'mysql' directory?
        config_path = os.path.join(os.sep, 'etc', 'mysql', 'conf.d', '99-utf8.conf')

        if os.path.exists(config_path):
            self.app.os.rm(config_path, root=True)
