from abc import ABC, abstractmethod


class Provisioner(ABC):
    @abstractmethod
    def run(self):
        pass
