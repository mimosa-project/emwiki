from abc import ABCMeta, abstractmethod


class FileTest(metaclass=ABCMeta):

    @abstractmethod
    def test_constractor(self):
        pass

    @abstractmethod
    def test_read(self):
        pass

    @abstractmethod
    def test_write(self):
        pass
