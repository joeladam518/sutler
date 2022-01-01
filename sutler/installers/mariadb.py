import click
import os
from typing import Optional
from ..application import Run
from .installer import Installer


def allow_regular_users_to_access_root_mysql(password: Optional[str] = None) -> None:
    """
    Allows any user to access mariadb root.
    https://mariadb.com/kb/en/authentication-plugin-unix-socket/
    """
    execute(
        "UPDATE mysql.user SET plugin = 'mysql_native_password' WHERE User = 'root'; FLUSH PRIVILEGES;",
        password=password
    )


def create_db(name: str, username: str, password: str) -> None:
    if not name or name == '*':
        click.ClickException('Failed to create db. Invalid data.')
    execute(f"CREATE DATABASE IF NOT EXISTS {name} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    create_user(db=name, username=username, password=password)


def create_user(db: str, username: str, password: str, host: str = 'localhost') -> None:
    if not username or username == 'root' or not password or not db or db == '*':
        click.ClickException('Failed to create user. Invalid data.')
    if user_exists(username, host):
        update_user_password(username, password)
    else:
        execute(f"CREATE USER '{username}'@'{host}' IDENTIFIED BY '{password}';")
    execute(f"GRANT ALL PRIVILEGES ON {db}.* TO '{username}'@'{host}';")
    execute("FLUSH PRIVILEGES;")


def disallow_regular_users_to_access_root_mysql(password: Optional[str] = None) -> None:
    """
    Resets root authentication back to unix_socket
    https://mariadb.com/kb/en/authentication-plugin-unix-socket/
    """
    execute(
        "UPDATE mysql.user SET plugin = 'unix_socket' WHERE User = 'root'; FLUSH PRIVILEGES;",
        password=password
    )


def execute(statement: str, username: str = 'root', password: Optional[str] = None) -> None:
    if password is not None:
        Run.command(f'mysql -u "{username}" -p "{password}" -e "{statement}"', root=True)
    else:
        Run.command(f'mysql -e "{statement}"', root=True)


def secure_installation(password: str) -> None:
    # Mirrors: https://github.com/atcurtis/mariadb/blob/master/scripts/mysql_secure_installation.sh
    # Set the root user's password. But REMEMBER mariadb will only let root login as mysql root...
    update_user_password('root', password)
    # Remove anonymous users
    execute("DELETE FROM mysql.user WHERE User = '';")
    # Disallow remote root login
    execute("DELETE FROM mysql.user WHERE User = 'root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');")
    # Remove test database
    execute("DROP DATABASE IF EXISTS test;")
    execute("DELETE FROM mysql.db WHERE Db = 'test' OR Db = 'test\\_%'")
    # Reset privileges
    execute("FLUSH PRIVILEGES;")


def update_user_password(username: str, password: str) -> None:
    execute(f"UPDATE mysql.user SET Password = PASSWORD('{password}') WHERE User = '{username}';")


def user_exists(user: str, host: str = 'localhost') -> bool:
    statement = f"SELECT COUNT(*) FROM mysql.user WHERE User = '{user}' AND Host = '{host}';"
    output = Run.command(f'mysql -se "{statement}"', root=True, capture_output=True)
    return int(output) > 0


class MariadbInstaller(Installer):
    def install(self) -> None:
        Run.install('mariadb-server', 'mariadb-client')

        # Setup Mariadb to support utf-8
        src_path = self.app.templates_path('mysql', 'utf8.conf')
        dst_path = os.path.join('/etc', 'mysql', 'conf.d', 'utf8.conf')
        Run.command(f'cp "{src_path}" "{dst_path}"', root=True)
        click.echo()

        # Get the root password
        root_password = click.prompt(
            "Enter your desired root password for mariadb",
            type=str,
            hide_input=True,
            confirmation_prompt=True,
            show_default=False,
        )
        # Secure the mariadb installation
        # Run.command('mysql_secure_installation', root=True)
        secure_installation(root_password)
        click.echo()

        if not click.confirm('Would you like to create a database now?', default=None):
            # We're done!
            click.echo()
            return

        # Gather the necessary data
        # TODO: could we get this from a build.yml file?
        db_name = click.prompt(
            "Enter the database's name",
            type=str,
            hide_input=False,
            show_default=False,
        )
        db_user = click.prompt(
            "Enter a username for the database",
            type=str,
            hide_input=False,
            show_default=False,
        )
        db_user_password = click.prompt(
            f"Enter {db_user}'s password",
            type=str,
            hide_input=True,
            confirmation_prompt=True,
            show_default=False,
        )
        create_db(name=db_name, username=db_user, password=db_user_password)
        click.echo()

    def uninstall(self) -> None:
        Run.uninstall('mariadb-server', 'mariadb-client')

        config_path = os.path.join('/etc', 'mysql', 'conf.d', 'utf8.conf')
        if os.path.exists(config_path):
            Run.command(f'rm "{config_path}"', root=True)
