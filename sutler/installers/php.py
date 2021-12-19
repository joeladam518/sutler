import click
from typing import Optional, Union
from ..support import List, Run
from ..utils import confirm, tuple_version

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


def get_installed_packages(version) -> list:
    php_packages = Run.command(
        "dpkg -l | grep php%s | sed 's/\s\{3,\}.*$//' | sed 's/^ii  //' | tr '\n' ' '" % version,
        capture_output=True
    )
    php_packages = php_packages.strip()
    php_packages = php_packages.split(' ')

    return list(filter(lambda package: bool(package), php_packages))


class PhpInstaller:
    @staticmethod
    def extensions(key: Optional[str] = None) -> Union[dict, tuple, None]:
        if key is None:
            return php_extensions
        else:
            return php_extensions.get(key)

    @staticmethod
    def versions(key: Optional[str] = None) -> Union[dict, tuple, None]:
        if key is None:
            return php_versions
        else:
            return php_versions.get(key)

    @staticmethod
    def install(version: str, env: str = 'desktop', append: tuple = (), exclude: tuple = ()) -> None:
        if version not in php_versions['install']:
            raise click.ClickException('Invalid php version')

        if env not in php_extensions:
            raise click.ClickException('Environment not supported')

        # combine the extensions to be installed
        extensions = [*php_extensions['common'], *php_extensions[env], *append]

        if tuple_version(version) < (8, 0):
            extensions.append('json')

        # filter out extensions
        extensions = List.unique(extensions)
        extensions = List.exclude(extensions, list(exclude))

        # build the extension strings and add them to the packages list
        packages = [f"php{version}", *list(map(lambda ext: extensionize(ext, version), extensions))]

        click.echo()
        click.secho("Packages to be installed:", fg='cyan')
        print(*packages, sep='\n')

        click.echo()
        if confirm('Proceed?', fg='cyan'):
            Run.command("apt update", root=True)
            Run.command("apt install -y", *packages, root=True)
        else:
            click.secho('Exiting...')

        click.echo()

    @staticmethod
    def uninstall(version: str) -> None:
        if version not in php_versions['uninstall']:
            raise click.ClickException('Invalid php version')

        packages = get_installed_packages(version)

        if len(packages) == 0:
            click.echo(f"No packages found for php{version}")
            return

        click.echo()
        click.secho('Packages to be uninstalled:', fg='cyan')
        print(*packages, sep='\n')

        click.echo()
        if confirm('Proceed?', fg='cyan'):
            Run.command("apt-get purge -y", *packages, root=True)
            Run.command("apt-get --purge autoremove -y", root=True)
        else:
            click.secho('Exiting...')

        click.echo()
