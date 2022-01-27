import click
import os
from typing import Any, Optional
from ..helpers import installed
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

        # Configure the server
        self._configure_nginx(domain, php_version, project)

        # Configure the firewall
        if self.app.os.id in ['ubuntu', 'debian']:
            self._configure_ufw()

    def _configure_nginx(self, domain: str, php_version: str, project: str) -> None:
        """
        Configure Nginx

        :param str domain: The domain for the nginx config
        :param str php_version: The php version to install
        :param str project: The project name. (For folder names an such...)
        :return: None
        :rtype: None
        """
        self.app.os.exec('systemctl stop nginx', root=True)

        # Build all the paths
        nginx_etc_path = self.app.sys_path('etc', 'nginx')
        nginx_config_path = os.path.join(nginx_etc_path, 'nginx.conf')
        sites_available_path = os.path.join(nginx_etc_path, 'sites-available')
        sites_enabled_path = os.path.join(nginx_etc_path, 'sites-enabled')
        project_nginx_path = os.path.join(sites_available_path, project)
        project_files_path = self.app.sys_path('var', 'www', project)

        # Make the project's directory on the server and throw a couple of test files on it.
        self.app.os.exec(f"mkdir -p {project_files_path}", root=True)
        self.app.os.exec(f"mkdir -p {project_files_path}/public", root=True)
        self._render_file(
            os.path.join('php', 'test.php.jinja2'),
            os.path.join(project_files_path, 'public', 'index.php'),
            root=True,
            project_name=project
        )
        self.app.os.cp(
            self.app.templates_path('php', 'info.php'),
            os.path.join(project_files_path, 'public', 'info.php'),
            root=True
        )
        self.app.os.exec(
            f"chown -R www-data:www-data {project_files_path}",
            root=True
        )

        # Keep the old nginx config
        if os.path.exists(nginx_config_path):
            self.app.os.exec(f'mv {nginx_config_path} {nginx_config_path}.old', root=True)

        # Render the template files to their config paths
        self._render_file(
            os.path.join('nginx', 'nginx.conf.jinja2'),
            nginx_config_path,
            root=True
        )
        self._render_file(
            os.path.join('nginx', 'sites-available', 'php-http.nginx.jinja2'),
            project_nginx_path,
            root=True,
            domain=domain,
            project_name=project,
            php_version=php_version,
            gzip_config=self.app.jinja.get_template('nginx/snippets/compression.conf.jinja2').render()
        )

        # Enable the nginx project site
        os.chdir(sites_enabled_path)
        self.app.os.exec(f"rm {sites_enabled_path}/*", root=True)
        self.app.os.exec(f"ln -s {project_nginx_path}", root=True)
        os.chdir(self.app.user.home)

        self.app.os.exec('systemctl start nginx', root=True)

    def _configure_ufw(self) -> None:
        """
        Configure the firewall

        :return: None
        :rtype: None
        """
        if not installed('ufw'):
            self.app.os.install('ufw')

        click.echo()
        self.app.os.exec("ufw allow ssh", root=True)
        self.app.os.exec("ufw allow 'Nginx HTTP'", root=True)
        self.app.os.exec("ufw allow 'Nginx HTTPS'", root=True)
        click.echo()
        click.echo('Checking ufw status:')
        self.app.os.exec("ufw status", root=True)
        click.echo()
        # TODO: maybe ask if we should enable the firewall?
        self.app.os.exec("ufw enable", root=True)
        click.echo()

    def _render_file(self, tp: str, fp: str, root: bool = False, **variables: Any) -> None:
        """
        Render a Template

        :param str tp: Template path
        :param str fp: File Path
        :param Any variables: The variables for the template
        :return: None
        :rtype: None
        """
        template = self.app.jinja.get_template(tp)
        stream = template.stream(variables)

        if not root:
            stream.dump(fp, 'utf-8')
        else:
            tmp_dir = self.app.sys_path('tmp', 'sutler-templates')

            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)

            tmp_fp = os.path.join(tmp_dir, os.path.basename(fp))
            stream.dump(tmp_fp, 'utf-8')

            self.app.os.mv(tmp_fp, fp, root=True)
            self.app.os.exec(f"chown root:root {fp}", root=True)
