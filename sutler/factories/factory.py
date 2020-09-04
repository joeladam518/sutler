from abc import ABC
import os
import sys
import platform
import sysconfig


class Factory(ABC):
    @staticmethod
    def get_platform():
        print("os.name                      ", os.name)
        print("sys.platform                 ", sys.platform)
        print("platform.system()            ", platform.system())
        print("sysconfig.get_platform()     ", sysconfig.get_platform())
        print("platform.machine()           ", platform.machine())
        print("platform.architecture()      ", platform.architecture())
