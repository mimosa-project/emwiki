from abc import ABCMeta, abstractmethod


class File(metaclass=ABCMeta):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass
