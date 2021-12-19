import click
from ..support import List, Run
from ..utils import confirm

php_versions = (
    '5.3',
    '5.4',
    '5.5',
    '5.6',
    '7.0',
    '7.1',
    '7.2',
    '7.3',
    '7.4',
    '8.0',
    '8.1',
)

php_extensions = {
    "common": [
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
        'zip',
    ],
    "desktop": [],
    "development": [
        'intl',
        'dev',
        'igbinary',
        'memcached',
        # 'pcov',  # code coverage
        'redis',
        'xdebug',
    ],
    "server": [
        'fpm',
        'gd',
        'igbinary',
        'memcached',
        # 'imap',  # work with IMAP protocol, as well as the NNTP, POP3 and local mailbox access methods.
        'intl',
        'redis',
    ],
}


def extensionize(extension: str, version: str = '') -> str:
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
    def install(version: str, env: str = 'desktop', additional: tuple = (), exclude: tuple = ()):
        if version not in php_versions:
            raise click.ClickException('Invalid php version')

        if env not in php_extensions:
            raise click.ClickException('Environment not supported')

        # Build the packages to be installed
        packages = [*php_extensions["common"], *php_extensions[env], *list(additional)]

        if float(version) < 8.0:
            packages.append('json')

        packages = List.unique(packages)
        packages = List.exclude(packages, list(exclude))
        packages = list(map(lambda ext: extensionize(ext, version), packages))
        packages = [f"php{version}", *packages]

        click.echo()
        click.secho("Extensions to be installed:", fg='cyan')
        print(*packages, sep='\n')

        click.echo()
        if confirm('Proceed with the install?', fg='cyan'):
            Run.command("apt update", root=True)
            Run.command("apt install -y", *packages, root=True)

        click.echo()

    @staticmethod
    def uninstall(version: str):
        packages = get_installed_packages(version)

        if len(packages) == 0:
            click.echo(f"No packages found for php{version}")
            return

        click.echo()
        click.secho('Packages to be uninstalled:', fg='cyan')
        print(*packages, sep='\n')

        click.echo()
        if confirm('Proceed with the uninstall?', fg='cyan'):
            Run.command("apt-get purge -y", *packages, root=True)
            Run.command("apt-get --purge autoremove -y", root=True)

        click.echo()
