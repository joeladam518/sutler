import click
from ..installers import NodeInstaller, PhpInstaller, RedisInstaller


@click.group()
def uninstall():
    pass


@click.command()
@click.pass_context
def nodejs(ctx):
    installer = NodeInstaller(ctx)
    installer.uninstall()


@click.command()
@click.pass_context
@click.argument('version', type=str, required=True)
def php(ctx, version):
    installer = PhpInstaller(ctx)
    installer.uninstall(version)


@click.command()
@click.pass_context
def redis(ctx):
    installer = RedisInstaller(ctx)
    installer.uninstall()


uninstall.add_command(nodejs)
uninstall.add_command(php)
uninstall.add_command(redis)
