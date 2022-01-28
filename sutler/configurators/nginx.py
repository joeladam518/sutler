import os
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..app import App


class NginxConfigurator:
    def __init__(self, app: 'App'):
        self.app: 'App' = app

    def lemp(self, domain: str, project: str, php_version: str) -> None:
        """
        Configure nginx for php and http (not https)

        :param str domain: The domain for the nginx config
        :param str php_version: The php version to install
        :param str project: The project name. (For folder names an such...)
        :return: None
        :rtype: None
        """
        # Stop nginx
        self.app.os.exec('systemctl stop nginx', root=True)

        # Build all the paths
        nginx_etc_path = self.app.sys_path('etc', 'nginx')
        nginx_config_path = os.path.join(nginx_etc_path, 'nginx.conf')
        sites_available_path = os.path.join(nginx_etc_path, 'sites-available')
        sites_enabled_path = os.path.join(nginx_etc_path, 'sites-enabled')
        project_nginx_path = os.path.join(sites_available_path, project)
        project_files_path = self.app.sys_path('var', 'www', project)

        # Make the project's directory on the server and throw a couple of test files on it.
        self.app.os.exec(f'mkdir -p {project_files_path}', root=True)
        self.app.os.exec(f'mkdir -p {project_files_path}/public', root=True)
        self.app.render(
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
        if os.path.exists(nginx_config_path) and not os.path.exists(f'{nginx_config_path}.old'):
            self.app.os.mv(nginx_config_path, f'{nginx_config_path}.old', root=True)

        # Render the template files to their config paths
        self.app.render(
            os.path.join('nginx', 'nginx.conf.jinja2'),
            nginx_config_path,
            root=True
        )
        self.app.render(
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

        # Start nginx
        self.app.os.exec('systemctl start nginx', root=True)
