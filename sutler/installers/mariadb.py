import click
import os
from subprocess import CompletedProcess
from typing import Optional, TYPE_CHECKING, Union
from .installer import Installer
from ..support import Version

if TYPE_CHECKING:
    from ..app import App


class MariadbConfigurator:
    """
    NOTES:
        - >= version 10.4 mysql.user is a view and not a table. You have to use operations like
          "ALTER USER" and "SET Password" instead of modifying the table directly.
        - ubuntu uses the 'unix_socket' plugin for root out of the box, where debian uses 'mysql_native_password'
        - Eventually, we should migrate away from 'mysql_native_password to the 'auth_ed25519' plugin
          because it's more secure.
    """
    def __init__(self, app: 'App', password: Optional[str] = None, host: str = 'localhost'):
        self.app = app
        self.host = host
        self.user = 'root'
        self.password = password
        self.version = self.get_version()

    def allow_regular_users_to_access_root_mysql(self) -> None:
        # Allows any user to access mariadb root.
        # https://mariadb.com/kb/en/authentication-plugin-unix-socket/
        query1 = f"UPDATE mysql.user SET plugin = 'mysql_native_password' WHERE User = 'root' AND Host = '{self.host}';"
        query2 = f"ALTER USER 'root'@'{self.host}' IDENTIFIED VIA 'mysql_native_password';"
        self.execute(query1 if self.version < Version('10.4') else query2)
        self.execute("FLUSH PRIVILEGES;")

    def create_db(self, name: str) -> None:
        if not name or name == '*':
            click.ClickException('Failed to create db. Invalid name.')

        self.execute(f"CREATE DATABASE IF NOT EXISTS {name} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

    def create_user(self, username: str, password: str, db_name: str, host: str = 'localhost') -> None:
        if not username or username == 'root':
            click.ClickException('Failed to create user. Invalid username.')

        if not password:
            click.ClickException('Failed to create user. Invalid password.')

        if not host:
            click.ClickException('Failed to create user. Invalid host.')

        if not db_name or db_name == '*':
            click.ClickException('Failed to create user. Invalid db.')

        if self.user_doesnt_exist(username, host):
            self.execute(f"CREATE USER '{username}'@'{host}' IDENTIFIED BY '{password}';")
        else:
            self.update_user_password(username, password, host)
            self.execute(f"REVOKE ALL PRIVILEGES ON *.* FROM '{username}'@'{host}';")
            self.execute("FLUSH PRIVILEGES;")

        self.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{username}'@'{host}';")
        self.execute("FLUSH PRIVILEGES;")

    def disallow_regular_users_to_access_root_mysql(self) -> None:
        # Resets root authentication back to unix_socket
        # https://mariadb.com/kb/en/authentication-plugin-unix-socket/
        query1 = f"UPDATE mysql.user SET plugin = 'unix_socket' WHERE User = 'root' AND Host = '{self.host}';"
        query2 = f"ALTER USER 'root'@'{self.host}' IDENTIFIED VIA 'unix_socket';"
        self.execute(query1 if self.version < Version('10.4') else query2)
        self.execute("FLUSH PRIVILEGES;")

    def execute(self, query: str, root: bool = True, capture_output: bool = False) -> Union[CompletedProcess, str]:
        command = f'mysql'
        command += f' --user="{self.user}" --password="{self.password}"' if self.user and self.password else ''
        command += f' --silent' if capture_output else ''
        command += f' --execute="{query}"'
        return self.app.sys.exec(command, root=root, capture_output=capture_output)

    def get_version(self) -> Version:
        return Version(self.execute("SELECT VERSION();", capture_output=True))

    def secure_installation(self) -> str:
        """
        Mirrors the mysql_secure_installation script from mariadb
        https://github.com/atcurtis/mariadb/blob/master/scripts/mysql_secure_installation.sh

        :return: The root password for mariadb
        :rtype: str
        """
        self.password = click.prompt(
            "Enter your desired root password for mariadb",
            type=str,
            hide_input=True,
            confirmation_prompt='Confirm the root password',
            show_default=False,
        )

        # Set the root user's password. But REMEMBER mariadb will only let root login as mysql root...
        self.update_user_password('root', self.password)
        self.disallow_regular_users_to_access_root_mysql()
        # Remove anonymous users
        self.execute("DELETE FROM mysql.user WHERE User = '';")
        # Disallow remote root login
        self.execute("DELETE FROM mysql.user WHERE User = 'root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');")
        # Remove test database
        self.execute("DROP DATABASE IF EXISTS test;")
        self.execute("DELETE FROM mysql.db WHERE Db = 'test' OR Db = 'test\\_%'")
        # Reset privileges
        self.execute("FLUSH PRIVILEGES;")

        return self.password

    def update_user_password(self, username: str, password: str, host: str = 'localhost') -> None:
        query1 = f"UPDATE mysql.user SET Password = PASSWORD('{password}') WHERE User='{username}' AND Host='{host}';"
        query2 = f"SET PASSWORD FOR '{username}'@'{host}' = PASSWORD('{password}');"
        self.execute(query1 if self.version < Version('10.4') else query2)

    def user_doesnt_exist(self, user: str, host: Optional[str] = 'localhost') -> bool:
        return not self.user_exists(user, host)

    def user_exists(self, user: str, host: Optional[str] = 'localhost') -> bool:
        query = f"SELECT COUNT(*) FROM mysql.user WHERE User = '{user}'"
        query += f" AND Host = '{host}';" if host else ";"
        return int(self.execute(query, capture_output=True)) > 0


class MariadbInstaller(Installer):
    def install(self, db: Optional[str] = None, user: Optional[str] = None) -> None:
        self.app.sys.install('mariadb-server', 'mariadb-client')
        click.echo()

        mariadb = MariadbConfigurator(self.app)

        # Secure the mariadb installation
        # self.app.systems.exec('mysql_secure_installation', root=True)
        mariadb.secure_installation()

        # Setup Mariadb to support utf-8
        source = self.app.templates_path('mysql', 'utf8.conf')
        destination = os.path.join(os.sep, 'etc', 'mysql', 'conf.d', '99-utf8.conf')
        self.app.sys.exec(f'cp "{source}" "{destination}"', root=True)

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
        self.app.sys.uninstall('mariadb-server', 'mariadb-client')

        # TODO: Should I just remove the entire 'mysql' directory?
        config_path = os.path.join(os.sep, 'etc', 'mysql', 'conf.d', '99-utf8.conf')

        if os.path.exists(config_path):
            self.app.sys.rm(config_path, root=True)
