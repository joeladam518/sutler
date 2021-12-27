import os
from ..application import Run
from .installer import Installer


def create_db(name: str, user_name: str, user_password: str) -> None:
    pass


class MariadbInstaller(Installer):
    def install(self) -> None:
        Run.install('mariadb-server', 'mariadb-client')

        # Secure the install
        Run.command('mysql_secure_installation', root=True)

        # Setup Mariadb to support utf-8
        src_path = self.app.templates_path('mysql', 'utf8.conf')
        dst_path = os.path.join('/etc', 'mysql', 'conf.d', 'utf8.conf')
        Run.command(f'cp "{src_path}" "{dst_path}"', root=True)

        # TODO: create a new database

    def uninstall(self) -> None:
        Run.uninstall('mariadb-server', 'mariadb-client')
