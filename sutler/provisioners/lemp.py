import click
import os
from typing import Optional
from ..configurators import NginxConfigurator, UfwConfigurator
from ..installers import ComposerInstaller, MariadbInstaller, NginxInstaller
from ..installers import NodeInstaller, PhpInstaller
from .provisioner import Provisioner
from .server import ServerProvisioner
from ..support import Str


class LempProvisioner(Provisioner):
    def run(self, domain: str, php_version: str, project: Optional[str] = None) -> None:
        """
        Provision your lemp server

        :param str domain:             The domain of your site
        :param str php_version:        The php version you would like to install
        :param Optional[str] project:  Project name. This will be the folder we put all of you project files in.
                                       If None, we'll just slug the domain
        :return: None
        :rtype
        """
        # Run the base server provisioner first
        ServerProvisioner(self.ctx).run()

        click.echo()
        click.echo('Setting up your lemp server')
        click.echo()

        os.chdir(self.app.user.home)

        # Slug the domain id no project given
        if not project:
            project = Str.slug(domain)

        # Install the LEMP stack
        MariadbInstaller(self.ctx).install()
        NodeInstaller(self.ctx).install('16')
        PhpInstaller(self.ctx).install(php_version, env='server')
        ComposerInstaller(self.ctx).install()
        NginxInstaller(self.ctx).install()

        # Configure nginx
        NginxConfigurator(self.app).lemp(domain, project, php_version)

        # Configure the firewall
        if self.app.os.id in ['ubuntu', 'debian']:
            UfwConfigurator(self.app).http()
