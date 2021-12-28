import os
import hashlib
import shutil
from subprocess import CalledProcessError
from urllib import request
from ..application import Run
from ..helpers import is_installed
from .installer import Installer


class ComposerInstaller(Installer):
    def install(self) -> None:
        if not is_installed('php'):
            self.ctx.fail('You must install php before you can install composer')

        home_dir = self.app.user.home
        composer_setup_path = os.path.join(home_dir, 'composer-setup.php')
        composer_path = os.path.join(home_dir, 'composer.phar')

        with request.urlopen('https://composer.github.io/installer.sig') as response:
            expected_signature = response.read().decode('utf-8')

        with request.urlopen('https://getcomposer.org/installer') as response:
            with open(composer_setup_path, 'wb') as setup_file:
                shutil.copyfileobj(response, setup_file)

        with open(composer_setup_path, 'r') as setup_file:
            actual_signature = hashlib.sha384(setup_file.read().encode())
            actual_signature = actual_signature.hexdigest()

        if actual_signature != expected_signature:
            self.ctx.fail("Failed to install php-composer. Hashes didnt match")

        try:
            Run.command(f'php {composer_setup_path}')
            Run.command(f'mv {composer_path} /usr/local/bin/composer', root=True)
        except CalledProcessError as ex:
            Run.command(f'rm {composer_setup_path}')
            raise ex
        else:
            Run.command(f'rm {composer_setup_path}')

    def uninstall(self) -> None:
        Run.command('rm /usr/local/bin/composer', root=True)
