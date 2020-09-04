import click
from .factory import Factory
from ..provisioners import DesktopProvisioner, ServerProvisioner, LempProvisioner
from ..utils import get_os


class SetupFactory(Factory):
    provisioners = {
        "debian": {
            'desktop': DesktopProvisioner,
            'server': ServerProvisioner,
            'lemp': LempProvisioner
        },
    }

    def __init__(self, type_):
        self.machine_type = type_
        self.os_type = get_os()

    def get_provisioner(self):
        os_type = self.os_type

        if os_type in ['debian', 'raspbian', 'ubuntu']:
            os_type = 'debian'

        machine_provisioners = self.provisioners.get(os_type, None)

        if machine_provisioners is None:
            raise click.ClickException(f"I could not find any provisioners for the '{self.os_type}' operating system.")

        provisioner = machine_provisioners.get(self.machine_type, None)

        if provisioner is None:
            raise click.ClickException(f"There is no provisioner for a {self.os_type} {self.machine_type} machine.")

        return provisioner()
