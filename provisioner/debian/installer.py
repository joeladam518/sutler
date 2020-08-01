from click import ClickException, echo
from .desktop import install as install_desktop
from .server import install as install_server


class Installer:
    def __init__(self, machine_type='server', os_type='debian'):
        self.machine_type = machine_type.lower()
        self.os_type = os_type.lower()

    def validate(self):
        if self.os_type not in ['debian', 'ubuntu', 'raspberry pi']:
            raise ClickException('Invalid os type.')

        if self.machine_type not in ['desktop', 'server', 'lemp', 'lamp', 'mqtt']:
            raise ClickException('Invalid machine type')

    def install(self):
        if self.machine_type == 'desktop':
            return install_desktop(self.os_type)
        elif self.machine_type == 'server':
            return install_server(self.os_type)
        else:
            return False
