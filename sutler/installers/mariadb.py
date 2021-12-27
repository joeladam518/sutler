import os
import shutil
from ..application import Run
from .installer import Installer


class MariadbInstaller(Installer):
    def install(self) -> None:
        Run.install('mariadb-server', 'mariadb-client')
        Run.command('mysql_secure_installation', root=True)

        # Setup Mariadb to support utf-8
        src_path = self.app.templates_path('mysql', 'utf8.conf')
        dst_path = os.path.join('/etc', 'mysql', 'conf.d', 'utf8.conf')
        Run.command(f'cp "{src_path}" "{dst_path}"', root=True)

    def uninstall(self) -> None:
        Run.uninstall('mariadb-server', 'mariadb-client')
