import click
from ..application import App
from ..installers import PhpInstaller, NodeInstaller, RedisInstaller
from ..support import Run


@click.group()
def install():
    pass


@click.command()
def dotfiles():
    click.echo("Installing dotfiles!")


@click.command()
@click.pass_context
def fzf(ctx):
    app = ctx.find_root().obj.get('app', App())
    Run.script(f"{app.context.get_path('scripts')}/install-fzf")


@click.command()
def mariadb():
    click.echo("Installing mariadb!")


@click.command()
@click.pass_context
@click.argument('version', type=str, required=True)
def nodejs(ctx, version):
    installer = NodeInstaller(ctx)
    installer.install(version)


@click.command()
@click.pass_context
@click.argument('version', type=str, required=True)
@click.option('-e', '--env', 'environment', type=str, default='desktop',
              help='The environment on witch to install php on.')
@click.option('-a', '--additional', 'additional', type=str, multiple=True, default=(),
              help="Any additional extension you might want to install")
@click.option('-x', '--exclude', 'exclude', type=str, multiple=True, default=(),
              help="Extension you want to exclude from installing")
def php(ctx, version, environment, additional, exclude):
    installer = PhpInstaller(ctx)
    installer.install(version, environment, additional, exclude)


@click.command()
@click.pass_context
def php_composer(ctx):
    installer = PhpInstaller(ctx)
    installer.install_composer()


@click.command()
@click.pass_context
def redis(ctx):
    installer = RedisInstaller(ctx)
    installer.install()


install.add_command(dotfiles)
install.add_command(fzf)
install.add_command(mariadb)
install.add_command(nodejs)
install.add_command(php)
install.add_command(php_composer)
install.add_command(redis)
