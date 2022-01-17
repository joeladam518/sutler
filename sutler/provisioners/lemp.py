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
        :param str domain:        The domain of your site
        :param str php_version:   The php version you would like to install
        :param Optional project:  Project name. This will be the folder we put all of you project files in. If None,
                                  We'll just slug your domain.
        :return:
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

        os.chdir(self.app.user.home)

        installer = MariadbInstaller(self.ctx)
        installer.install()

        installer = NodeInstaller(self.ctx)
        installer.install('16')

        installer = PhpInstaller(self.ctx)
        installer.install(php_version, env='server')

        installer = ComposerInstaller(self.ctx)
        installer.install()

        installer = NginxInstaller(self.ctx)
        installer.install()

        # Configure Nginx
        self._configure_nginx(project, domain, php_version)

        # Configure ufw
        # Run.command("ufw allow 'Nginx HTTP'", root=True)
        # Run.command("ufw allow 'Nginx HTTPS'", root=True)
        # click.echo()
        # click.echo('Checking ufw status:')
        # Run.command("ufw status", root=True)
        # click.echo()

    def _configure_nginx(self, domain: str, php_version: str, project: str):
        # TODO: Which one is better to use?
        # Run.command('service nginx stop', root=True)
        Run.command('systemctl stop nginx', root=True)

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

        # Let's keep the old nginx config path
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

        # enable the nginx project site
        os.chdir(sites_enabled_path)
        Run.command(f"rm {sites_enabled_path}/*", root=True)
        Run.command(f"ln -s {project_config_path}", root=True)
        # TODO: Which one is better to use?
        # Run.command('service nginx start', root=True)
        Run.command('systemctl start nginx', root=True)

    def _copy_file(self, from_path: str, to_path: str, root: bool = False) -> None:
        Run.command(f"cp {from_path} {to_path}", root=root)

    def _render_file(self, tp: str, fp: str, root: bool = False, **variables: Any) -> None:
        """
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

            Run.command(f"mv {tmp_fp} {fp}", root=True)
            Run.command(f"chown root:root {fp}", root=True)
