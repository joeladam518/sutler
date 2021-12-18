import subprocess
from ..utils import get_os


class NodeInstaller(object):
    @staticmethod
    def install(version):
        os_type = get_os()
        if os_type in ['debian', 'raspbian', 'ubuntu']:
            subprocess.run(f"curl -sL \"https://deb.nodesource.com/setup_{version}.x\" | sudo -E bash -")
            subprocess.run("sudo apt-get install -y nodejs")
        else:
            subprocess.run("sudo apt-get install -y node")
