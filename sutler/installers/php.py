import click
from ..application import Run
from ..helpers import confirm
from .installer import Installer
from os.path import exists
from ..support import List, OS, Version

php_extensions = {
    'common': (
        'bcmath',
        'cli',
        'common',
        'curl',
        'mbstring',
        'mysql',
        'opcache',
        'pgsql',
        'readline',
        'sqlite3',
        'xml',
        'zip'
    ),
    'desktop': (),
    'development': (
        'intl',
        'dev',
        'igbinary',
        'memcached',
        # 'pcov',  # code coverage
        'redis',
        'xdebug'
    ),
    'server': (
        'fpm',
        'gd',
        'igbinary',
        'memcached',
        # 'imap',  # work with IMAP protocol, as well as the NNTP, POP3 and local mailbox access methods.
        'intl',
        'redis',
    ),
}

php_versions = {
    'install': ('7.4', '8.0', '8.1'),
    'uninstall': ('5.3', '5.4', '5.5', '5.6', '7.0', '7.1', '7.2', '7.3', '7.4', '8.0', '8.1'),
}


def extensionize(extension: str, version: str) -> str:
    return f"php{version}-{extension}"


def get_installed_packages(version: str) -> list:
    cmd = "dpkg -l | grep php%s | sed 's/^ii\s*//' | sed 's/\s\{3,\}.*$//' | tr '\n' ' '"
    packages = Run.command(cmd % version, capture_output=True)
    packages = packages.strip().split(' ')

    return list(filter(lambda package: bool(package), packages))


class PhpInstaller(Installer):
    def install(self, version: str, env: str = 'desktop', append: tuple = (), exclude: tuple = ()) -> None:
        if version not in php_versions['install']:
            self.ctx.fail('Invalid php version')
            return

        if env not in php_extensions:
            self.ctx.fail('Environment not supported')
            return

        # combine the extensions to be installed
        extensions = [*php_extensions['common'], *php_extensions[env], *append]

        if Version(version) < Version('8.0'):
            extensions.append('json')

        # filter out extensions
        extensions = List.unique(extensions)
        extensions = List.only(extensions, list(exclude))

        # build the extension strings and add them to the packages list
        packages = [f"php{version}", *list(map(lambda ext: extensionize(ext, version), extensions))]

        click.echo()
        click.secho("Packages to be installed:", fg='cyan')
        print(*packages, sep='\n')

        click.echo()
        if confirm('Proceed?', fg='cyan'):
            if not self._php_sources_are_installed():
                self._install_php_sources()
            Run.install(*packages)
        else:
            click.secho('Exiting...')

        click.echo()

    def uninstall(self, version: str) -> None:
        if version not in php_versions['uninstall']:
            self.ctx.fail('Invalid php version')
            return

        packages = get_installed_packages(version)

        if len(packages) == 0:
            click.echo(f"No packages found for php{version}")
            return

        click.echo()
        click.secho('Packages to be uninstalled:', fg='cyan')
        print(*packages, sep='\n')

        click.echo()
        if confirm('Proceed?', fg='cyan'):
            Run.uninstall(*packages)
        else:
            click.secho('Exiting...')

        click.echo()

    def _install_php_sources(self) -> None:
        if self.app.context.os in ['debian', 'raspbian']:
            Run.install('apt-transport-https', 'ca-certificates', 'software-properties-common', 'lsb-release', 'gnupg2')
            Run.command('wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg', root=True)
            source = 'deb https://packages.sury.org/php/ $(lsb_release -sc) main'
            file_path = '/etc/apt/sources.list.d/sury-php.list'
            Run.command(f'echo "{source}" | sudo tee {file_path}')
        elif self.app.context.os == 'ubuntu':
            Run.install('software-properties-common')
            Run.command('add-apt-repository ppa:ondrej/php -y', root=True)

    def _php_sources_are_installed(self) -> bool:
        # NOTE: 'cmd' will only work for debian based machines
        cmd = "find /etc/apt/ -name *.list | xargs cat | grep ^[[:space:]]*deb | grep '%s' | grep 'php'"
        if self.app.context.os in ['debian', 'raspbian']:
            if exists('/etc/apt/sources.list.d/sury-php.list'):
                return True
            proc = Run.command(cmd % 'sury', check=False, supress_output=True)
            return proc.returncode == 0

        if self.app.context.os == 'ubuntu':
            if exists(f"/etc/apt/sources.list.d/ondrej-ubuntu-php-{OS.get_release_value('VERSION_CODENAME')}.list"):
                return True
            proc = Run.command(cmd % 'ondrej', check=False, supress_output=True)
            return proc.returncode == 0

        return False
