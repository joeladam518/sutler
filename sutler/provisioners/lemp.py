import click
import os
from typing import Any, Optional
from ..application import Run
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
        """
        # Slug the domain id no project given
        if not project:
            project = Str.slug(domain)

        # Run the server provisioner first
        provisioner = ServerProvisioner(self.ctx)
        provisioner.run()

        click.echo()
        click.echo('Setting up your lemp server')
        click.echo()

        # Install the LEMP stack
        os.chdir(self.app.user.home)
        MariadbInstaller(self.ctx).install()
        NodeInstaller(self.ctx).install('16')
        PhpInstaller(self.ctx).install(php_version, env='server')
        ComposerInstaller(self.ctx).install()
        NginxInstaller(self.ctx).install()

        # Configure the server
        self._configure_nginx(project, domain, php_version)
        # self._configure_ufw()

    def _configure_nginx(self, domain: str, php_version: str, project: str) -> None:
        """
        Configure Nginx
        :param str domain: The domain for the nginx config
        :param str php_version: The php version to install
        :param str project: The project name. (For folder names an such...)
        :return:
        """
        # TODO: Which one is better to use?
        Run.command('systemctl stop nginx', root=True)
        # Run.command('service nginx stop', root=True)

        # Make the project's directory on the server and throw a couple of test files on it.
        project_path = self.app.sys_path('var', 'www', project)
        Run.command(f"mkdir -p {project_path}", root=True)
        Run.command(f"mkdir -p {project_path}/public", root=True)
        self._render_file(os.path.join('php', 'test.php.jinja2'), os.path.join(project_path, 'public', 'index.php'))
        self._copy_file(self.app.templates_path('php', 'info.php'), os.path.join(project_path, 'public', 'info.php'))
        Run.command(f"chown -R www-data:www-data {project_path}", root=True)

        # Build all the config paths
        etc_path = self.app.sys_path('etc', 'nginx')
        config_path = os.path.join(etc_path, 'nginx.conf')
        sites_available_path = os.path.join(etc_path, 'sites-available')
        sites_enabled_path = os.path.join(etc_path, 'sites-enabled')
        project_config_path = os.path.join(sites_available_path, project)

        # Keep the old nginx config
        if os.path.exists(config_path):
            Run.command(f'mv {config_path} {config_path}.old', root=True)

        # Render the template files to their config paths
        self._render_file(
            os.path.join('nginx', 'nginx.conf.jinja2'),
            config_path,
            root=True
        )
        self._render_file(
            os.path.join('nginx', 'sites-available', 'php-http.nginx.jinja2'),
            project_config_path,
            root=True,
            domain=domain,
            project_name=project,
            php_version=php_version,
            gzip_config=self.app.jinja.get_template('nginx/snippets/compression.conf.jinja2').render()
        )

        # Enable the nginx project site
        os.chdir(sites_enabled_path)
        Run.command(f"rm {sites_enabled_path}/*", root=True)
        Run.command(f"ln -s {project_config_path}", root=True)
        os.chdir(self.app.user.home)

        # TODO: Which one is better to use?
        Run.command('systemctl start nginx', root=True)
        # Run.command('service nginx start', root=True)

    def _configure_ufw(self) -> None:
        """
        Configure the firewall
        :return: None
        """
        click.echo()
        Run.command("ufw allow SSH", root=True)
        Run.command("ufw allow 'Nginx HTTP'", root=True)
        Run.command("ufw allow 'Nginx HTTPS'", root=True)
        click.echo()
        click.echo('Checking ufw status:')
        Run.command("ufw status", root=True)
        click.echo()

    def _copy_file(self, _from: str, _to: str, root: bool = False) -> None:
        """
        Copy a file
        :param str _from: From Path
        :param str _to: To Path
        :param bool root: Run as root
        :return: None
        """
        Run.command(f"cp {_from} {_to}", root=root)

    def _move_file(self, _from: str, _to: str, root: bool = False) -> None:
        """
        Move a file
        :param str _from: From Path
        :param str _to: To Path
        :param bool root: Run as root
        :return: None
        """
        Run.command(f"mv {_from} {_to}", root=root)

    def _render_file(self, tp: str, fp: str, root: bool = False, **variables: Any) -> None:
        """
        Render a Template
        :param str tp: Template path
        :param str fp: File Path
        :param Any variables: The variables for the template
        :return: None
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

            self._move_file(tmp_fp, fp, root=True)
            Run.command(f"chown root:root {fp}", root=True)
