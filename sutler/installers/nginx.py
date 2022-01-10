import click
import os
from typing import Any
from ..application import Run
from .installer import Installer


class NginxInstaller(Installer):
    def _render_file(self, tp: str, fp: str, root: bool = False, **variables: Any) -> None:
        """
        :param str tp: Template path
        :param str fp: File Path
        :param Any variables: The variables for the template
        :return: None
        :rtype: None
        """
        tmp_dir = self.app.sys_path('tmp', 'sutler-templates')
        filename = os.path.basename(fp)

        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        tmp_file_path = os.path.join(tmp_dir, filename)
        template = self.app.jinja.get_template(tp)
        template.stream(variables).dump(tmp_file_path, 'utf-8')

        Run.command(f"mv {tmp_file_path} {fp}", root=root)
        if root:
            Run.command(f"chown root:root {fp}", root=True)

    def install(self, project: str, domain: str, php_version: str) -> None:
        Run.update()
        Run.install('nginx')
        Run.command('systemctl stop nginx', root=True)

        # make the directory for the project
        project_path = self.app.sys_path('var', 'www', project)
        Run.command(f"mkdir -p {project_path}", root=True)
        Run.command(f"mkdir -p {project_path}/public", root=True)
        Run.command(f"chown -r www-data:www-data {project_path}", root=True)

        # Build all the config paths
        etc_path = self.app.sys_path('etc', 'nginx')
        config_path = os.path.join(etc_path, 'nginx.conf')
        sites_available_path = os.path.join(etc_path, 'sites-available')
        sites_enabled_path = os.path.join(etc_path, 'sites-enabled')
        project_config_path = os.path.join(sites_available_path, project)

        # let's keep the old nginx config path
        if os.path.exists(config_path):
            Run.command(f'mv {config_path} {config_path}.old', root=True)

        # render the template files to their config paths
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
        Run.command('systemctl start nginx', root=True)

    def uninstall(self) -> None:
        Run.uninstall('nginx')
