import click
import os
from typing import Optional
from ..application import Run
from .installer import Installer


def allow_regular_users_to_access_root_mysql(password: Optional[str] = None) -> None:
    # Allows any user to access mariadb root.
    # https://mariadb.com/kb/en/authentication-plugin-unix-socket/
    execute(
        "UPDATE mysql.user SET plugin = 'mysql_native_password' WHERE User = 'root'; FLUSH PRIVILEGES;",
        password=password,
        username='root'
    )


def create_db(name: str) -> None:
    if not name or name == '*':
        click.ClickException('Failed to create db. Invalid name.')
    else:
        execute(f"CREATE DATABASE IF NOT EXISTS {name} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")


def create_user(username: str, password: str, db_name: str, host: str = 'localhost') -> None:
    if not username or username == 'root':
        click.ClickException('Failed to create user. Invalid username.')

    if not password:
        click.ClickException('Failed to create user. Invalid password.')

    if not host:
        click.ClickException('Failed to create user. Invalid host.')

    if not db_name or db_name == '*':
        click.ClickException('Failed to create user. Invalid db.')

    if user_doesnt_exist(username, host):
        execute(f"CREATE USER '{username}'@'{host}' IDENTIFIED BY '{password}';")
    else:
        update_user_password(username, password, host)
        execute(f"REVOKE ALL PRIVILEGES ON *.* FROM '{username}'@'{host}';")
        execute("FLUSH PRIVILEGES;")

    execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{username}'@'{host}';")
    execute("FLUSH PRIVILEGES;")


def disallow_regular_users_to_access_root_mysql(password: Optional[str] = None) -> None:
    # Resets root authentication back to unix_socket
    # https://mariadb.com/kb/en/authentication-plugin-unix-socket/
    execute(
        "UPDATE mysql.user SET plugin = 'unix_socket' WHERE User = 'root'; FLUSH PRIVILEGES;",
        password=password,
        username='root'
    )


def execute(query: str, password: Optional[str] = None, username: Optional[str] = 'root') -> None:
    if username and password:
        Run.command(f'mysql -u "{username}" -p "{password}" -e "{query}"', root=True)
    else:
        Run.command(f'mysql -e "{query}"', root=True)


def secure_installation() -> str:
    """
    Mirrors the mysql_secure_installation script from mariadb
    https://github.com/atcurtis/mariadb/blob/master/scripts/mysql_secure_installation.sh

    :return: The root password for mariadb
    :rtype: str
    """
    password = click.prompt(
        "Enter your desired root password for mariadb",
        type=str,
        hide_input=True,
        confirmation_prompt='Confirm the root password',
        show_default=False,
    )

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

    return password


def update_user_password(username: str, password: str, host: Optional[str] = None) -> None:
    query = f"UPDATE mysql.user SET Password = PASSWORD('{password}') WHERE User = '{username}'"
    query += f" AND Host = '{host}';" if host else ";"
    execute(query)


def user_doesnt_exist(user: str, host: Optional[str] = 'localhost') -> bool:
    return not user_exists(user, host)


def user_exists(user: str, host: Optional[str] = 'localhost') -> bool:
    query = f"SELECT COUNT(*) FROM mysql.user WHERE User = '{user}'"
    query += f" AND Host = '{host}';" if host else ";"
    result = Run.command(f'mysql -se "{query}"', root=True, capture_output=True)
    return int(result) > 0


class MariadbInstaller(Installer):
    # TODO: This only works for ubuntu
    def install(self, db: Optional[str] = None, user: Optional[str] = None) -> None:
        Run.install('mariadb-server', 'mariadb-client')
        click.echo()

        # Secure the mariadb installation
        # Run.command('mysql_secure_installation', root=True)
        secure_installation()

        # Setup Mariadb to support utf-8
        source = self.app.templates_path('mysql', 'utf8.conf')
        destination = os.path.join('/etc', 'mysql', 'conf.d', 'utf8.conf')
        Run.command(f'cp "{source}" "{destination}"', root=True)

        # Create a database if we have the required information
        if db and user:
            click.echo()
            user_password = click.prompt(
                f"Enter {user}'s password",
                type=str,
                hide_input=True,
                confirmation_prompt=f"Confirm {user}'s password",
                show_default=False,
                default=None
            )
            if user_password:
                create_db(name=db)
                create_user(username=user, password=user_password, db_name=db)

        click.echo()

    def uninstall(self) -> None:
        Run.uninstall('mariadb-server', 'mariadb-client')

        # TODO: Should I just remove the entire 'mysql' directory?
        config_path = os.path.join('/etc', 'mysql', 'conf.d', 'utf8.conf')
        if os.path.exists(config_path):
            Run.command(f'rm "{config_path}"', root=True)
